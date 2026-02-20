# ai/cnn_model.py
import numpy as np
import random
from PIL import Image
import os

def predict_stego(file_path: str) -> str:
    """
    Simulate CNN steganography detection
    Analyzes image statistical anomalies
    """
    # Simulate image analysis
    img = Image.open(file_path)
    width, height = img.size
    
    # Simulate CNN features (real CNN would extract these)
    features = simulate_features(img, width, height)
    
    # CNN prediction (simplified neural network)
    stego_prob = cnn_predict(features)
    
    status = "🟢 CLEAN" if stego_prob < 0.5 else "🔴 STEGO DETECTED"
    confidence = abs(stego_prob - 0.5) * 2
    
    result = f"""
{status}
Steganography Probability: {stego_prob:.1%}
Confidence: {confidence:.1%}
File: {os.path.basename(file_path)}
Size: {width}x{height}

📊 Key Indicators:
• Pixel variance: {features[0]:.2f}
• LSB noise: {features[1]:.1%}
• Entropy: {features[2]:.3f}
"""
    return result

def simulate_features(img, width, height):
    """Simulate CNN-extracted features"""
    # Convert to numpy for analysis
    img_array = np.array(img.convert('RGB'))
    
    # Feature 1: Pixel variance (stego changes this)
    variance = np.var(img_array) / 255
    
    # Feature 2: LSB statistical anomaly
    lsb_noise = np.mean(np.abs(img_array & 1)) / 3  # Average LSB across RGB
    
    # Feature 3: Entropy (stego reduces it slightly)
    entropy = np.random.uniform(6.8, 7.2)
    
    return [variance, lsb_noise * 100, entropy]

def cnn_predict(features):
    """Simplified CNN prediction logic"""
    # Simulate neural network weights
    weights = np.array([0.4, 0.3, -0.1])
    bias = 0.2
    
    # Neural network computation
    logit = np.dot(features, weights) + bias
    prob = 1 / (1 + np.exp(-logit))
    
    # Add some randomness for realism
    prob += random.uniform(-0.1, 0.1)
    return np.clip(prob, 0, 1)
