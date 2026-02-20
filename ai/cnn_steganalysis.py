# CNN-based Steganalysis Model
# Using a proper Convolutional Neural Network for detecting steganographic content

import numpy as np
import cv2
import os
from typing import Tuple, List

class SteganalysisCNN:
    """
    Convolutional Neural Network for Steganalysis
    Based on Yedroudj-Net architecture (efficient for steganalysis)
    """
    
    def __init__(self):
        self.model = None
        self.is_trained = False
        self.classes = ['Clean', 'Stego']
        
    def create_model(self):
        """
        Create a CNN model for steganalysis
        Architecture: Yedroudj-Net inspired (efficient for steganalysis)
        """
        try:
            import tensorflow as tf
            from tensorflow.keras import layers, models
            
            # Build the model
            model = models.Sequential([
                # Block 1: Initial feature extraction
                layers.Conv2D(32, (5, 5), padding='same', input_shape=(256, 256, 1)),
                layers.BatchNormalization(),
                layers.ReLU(),
                
                # Block 2: Spatial rich model features
                layers.Conv2D(32, (5, 5), padding='same'),
                layers.BatchNormalization(),
                layers.ReLU(),
                layers.MaxPooling2D((2, 2)),
                layers.Dropout(0.25),
                
                # Block 3
                layers.Conv2D(64, (3, 3), padding='same'),
                layers.BatchNormalization(),
                layers.ReLU(),
                layers.Dropout(0.25),
                
                # Block 4
                layers.Conv2D(64, (3, 3), padding='same'),
                layers.BatchNormalization(),
                layers.ReLU(),
                layers.MaxPooling2D((2, 2)),
                layers.Dropout(0.25),
                
                # Block 5
                layers.Conv2D(128, (3, 3), padding='same'),
                layers.BatchNormalization(),
                layers.ReLU(),
                layers.Dropout(0.25),
                
                # Block 6
                layers.Conv2D(128, (3, 3), padding='same'),
                layers.BatchNormalization(),
                layers.ReLU(),
                layers.MaxPooling2D((2, 2)),
                layers.Dropout(0.25),
                
                # Classification head
                layers.Flatten(),
                layers.Dense(256),
                layers.ReLU(),
                layers.Dropout(0.5),
                layers.Dense(1, activation='sigmoid')
            ])
            
            # Compile model
            model.compile(
                optimizer='adam',
                loss='binary_crossentropy',
                metrics=['accuracy', 'AUC']
            )
            
            self.model = model
            return model
            
        except ImportError:
            print("TensorFlow not installed. Using statistical model instead.")
            return None
    
    def preprocess_image(self, image_path: str, target_size: Tuple[int, int] = (256, 256)) -> np.ndarray:
        """Preprocess image for CNN"""
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return None
        
        # Resize to target size
        img = cv2.resize(img, target_size)
        
        # Normalize to [0, 1]
        img = img.astype(np.float32) / 255.0
        
        # Add channel dimension
        img = np.expand_dims(img, axis=(0, -1))
        
        return img
    
    def extract_features(self, image_path: str) -> np.ndarray:
        """Extract handcrafted features for steganalysis"""
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return None
        
        features = []
        
        # 1. LSB features
        lsb = img & 1
        lsb_features = [
            np.mean(lsb),
            np.std(lsb),
            np.sum(lsb == 0) / lsb.size,
            np.sum(lsb == 1) / lsb.size
        ]
        features.extend(lsb_features)
        
        # 2. Statistical features
        stats_features = [
            np.mean(img) / 255.0,
            np.std(img) / 255.0,
            np.min(img) / 255.0,
            np.max(img) / 255.0,
            np.median(img) / 255.0
        ]
        features.extend(stats_features)
        
        # 3. Gradient features
        sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
        gradient_magnitude = np.sqrt(sobelx**2 + sobely**2)
        
        gradient_features = [
            np.mean(gradient_magnitude) / 255.0,
            np.std(gradient_magnitude) / 255.0,
            np.max(gradient_magnitude) / 255.0
        ]
        features.extend(gradient_features)
        
        # 4. Co-occurrence matrix features
        # (simplified - just use a few statistics)
        cooc_mean = np.mean(img[:, 1:] == img[:, :-1])
        features.append(cooc_mean)
        
        # 5. FFT features (magnitude statistics)
        f = np.fft.fft2(img)
        fshift = np.fft.fftshift(f)
        magnitude = np.abs(fshift)
        
        fft_features = [
            np.mean(magnitude) / 255.0,
            np.std(magnitude) / 255.0,
            np.max(magnitude) / 255.0
        ]
        features.extend(fft_features)
        
        return np.array(features, dtype=np.float32)
    
    def predict(self, image_path: str) -> dict:
        """Predict if image contains steganographic content"""
        if self.model is None:
            self.create_model()
        
        # Try CNN prediction first
        if self.model is not None and self.is_trained:
            try:
                img = self.preprocess_image(image_path)
                if img is not None:
                    prediction = self.model.predict(img, verbose=0)[0][0]
                    
                    return {
                        'method': 'CNN',
                        'probability': float(prediction * 100),
                        'prediction': 'Stego' if prediction > 0.5 else 'Clean',
                        'confidence': float(max(prediction, 1 - prediction) * 100)
                    }
            except:
                pass
        
        # Fall back to feature-based prediction
        features = self.extract_features(image_path)
        if features is None:
            return {'error': 'Could not process image'}
        
        # Simple rule-based prediction using features
        # This is a simplified version - real model would be trained
        lsb_1_ratio = features[3]  # Ratio of LSB 1s
        
        # If LSB distribution is significantly different from 50%, suspicious
        deviation = abs(lsb_1_ratio - 0.5)
        
        if deviation > 0.1:
            probability = 50 + deviation * 200
        else:
            probability = 50 - deviation * 100
        
        probability = max(0, min(100, probability))
        
        return {
            'method': 'Feature-based',
            'probability': float(probability),
            'prediction': 'Stego' if probability > 50 else 'Clean',
            'confidence': float(abs(probability - 50) * 2)
        }
    
    def train(self, train_data: List[Tuple[str, int]], epochs: int = 10):
        """
        Train the CNN model
        train_data: List of (image_path, label) tuples where label is 0 for clean, 1 for stego
        """
        if self.model is None:
            self.create_model()
        
        if self.model is None:
            print("Cannot train - TensorFlow not available")
            return False
        
        # Prepare training data
        X = []
        y = []
        
        for path, label in train_data:
            img = self.preprocess_image(path)
            if img is not None:
                X.append(img)
                y.append(label)
        
        if len(X) == 0:
            print("No valid training samples")
            return False
        
        X = np.vstack(X)
        y = np.array(y)
        
        # Train the model
        history = self.model.fit(
            X, y,
            epochs=epochs,
            validation_split=0.2,
            batch_size=16,
            verbose=1
        )
        
        self.is_trained = True
        return history
    
    def save_model(self, path: str):
        """Save trained model"""
        if self.model is not None:
            self.model.save(path)
            print(f"Model saved to {path}")
    
    def load_model(self, path: str):
        """Load trained model"""
        try:
            import tensorflow as tf
            self.model = tf.keras.models.load_model(path)
            self.is_trained = True
            print(f"Model loaded from {path}")
        except Exception as e:
            print(f"Could not load model: {e}")


class EnsembleDetector:
    """Ensemble of multiple steganalysis methods"""
    
    def __init__(self):
        self.cnn = SteganalysisCNN()
        self.cnn.create_model()
    
    def detect(self, image_path: str) -> dict:
        """Run ensemble detection"""
        from ai.steganalysis_models import EnhancedSteganalysis
        
        # Get CNN prediction
        cnn_result = self.cnn.predict(image_path)
        
        # Get statistical analysis
        stats = EnhancedSteganalysis()
        ensemble_result = stats.ensemble_detection(image_path)
        
        # Combine results
        probabilities = []
        
        if 'probability' in cnn_result:
            probabilities.append(cnn_result['probability'])
        
        if 'ensemble_probability' in ensemble_result:
            probabilities.append(ensemble_result['ensemble_probability'])
        
        if 'chi_square' in ensemble_result:
            probabilities.append(ensemble_result['chi_square'].get('probability', 50))
        
        if 'spam' in ensemble_result:
            probabilities.append(ensemble_result['spam'].get('probability', 50))
        
        if 'rs_analysis' in ensemble_result:
            probabilities.append(ensemble_result['rs_analysis'].get('probability', 50))
        
        # Calculate weighted ensemble
        if probabilities:
            avg_probability = np.mean(probabilities)
            
            return {
                'ensemble_probability': float(avg_probability),
                'prediction': 'Stego Detected' if avg_probability > 50 else 'Likely Clean',
                'confidence': float(abs(avg_probability - 50) * 2),
                'methods_used': len(probabilities),
                'individual_results': {
                    'cnn': cnn_result,
                    'statistical': ensemble_result
                }
            }
        
        return {'error': 'Detection failed'}
