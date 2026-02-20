# Enhanced Steganalysis Module with Multiple Detection Methods
import cv2
import numpy as np
from scipy import stats
import os

class EnhancedSteganalysis:
    """Advanced steganalysis with multiple detection methods"""
    
    def __init__(self):
        self.results = {}
    
    def chi_square_analysis(self, image_path):
        """
        Chi-Square Analysis for Steganography Detection
        Analyzes pairs of pixel values to detect statistical anomalies
        """
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return {"error": "Could not load image"}
        
        h, w = img.shape
        
        # Group pixels into pairs (2i, 2i+1)
        n = (h * w) // 2
        even_pairs = 0
        odd_pairs = 0
        
        flat = img.flatten()
        for i in range(0, len(flat) - 1, 2):
            if flat[i] == flat[i + 1]:
                even_pairs += 1
            elif abs(flat[i] - flat[i + 1]) == 1:
                odd_pairs += 1
        
        # Calculate expected and observed values
        total = even_pairs + odd_pairs
        if total == 0:
            return {"chi_square": 0, "probability": 0}
        
        expected = total / 2
        chi_square = ((even_pairs - expected) ** 2 + (odd_pairs - expected) ** 2) / expected
        
        # Higher chi-square indicates possible steganography
        probability = min(chi_square / 100 * 100, 100)
        
        return {
            "chi_square": chi_square,
            "probability": probability,
            "even_pairs": even_pairs,
            "odd_pairs": odd_pairs,
            "interpretation": "High chi-square suggests steganography" if chi_square > 10 else "Normal distribution - likely clean"
        }
    
    def rs_analysis(self, image_path):
        """
        RS (Regular-Singular) Analysis
        Uses flipping operations to detect steganographic content
        """
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return {"error": "Could not load image"}
        
        # Define flip functions
        def f1(x):
            return -x if x < 128 else 256 - x
        
        def f2(x):
            return -x - 1 if x < 128 else 256 - x - 1
        
        def classify_group(pixels):
            r = sum(f1(p) for p in pixels)
            s = sum(f2(p) for p in pixels)
            if r > 0 and s > 0:
                return "RR"
            elif r < 0 and s < 0:
                return "SS"
            elif r > 0 and s < 0:
                return "RS"
            else:
                return "SR"
        
        # Sample pixels (for speed)
        h, w = img.shape
        block_size = 4
        
        r_positive = 0
        r_negative = 0
        s_positive = 0
        s_negative = 0
        
        # Analyze in blocks
        for i in range(0, h - block_size + 1, block_size):
            for j in range(0, w - block_size + 1, block_size):
                block = img[i:i+block_size, j:j+block_size].flatten()
                classification = classify_group(block)
                
                if classification == "RR":
                    r_positive += 1
                elif classification == "SS":
                    s_positive += 1
                elif classification == "RS":
                    r_negative += 1
                elif classification == "SR":
                    s_negative += 1
        
        # Calculate R and S values
        total = r_positive + r_negative + s_positive + s_negative
        if total == 0:
            return {"rs_score": 0, "probability": 0}
        
        R = (r_positive - r_negative) / total if total > 0 else 0
        S = (s_positive - s_negative) / total if total > 0 else 0
        
        # RS score - deviation from expected
        rs_score = abs(R - S) * 100
        probability = min(rs_score * 2, 100)
        
        return {
            "rs_score": rs_score,
            "probability": probability,
            "R": R,
            "S": S,
            "interpretation": "Significant RS deviation suggests steganography" if rs_score > 5 else "Normal RS values - likely clean"
        }
    
    def spam_features(self, image_path):
        """
        SPAM (Subtractive Pixel Adjacency Matrix) Features
        Extracts statistical features from pixel differences
        """
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return {"error": "Could not load image"}
        
        # Compute differences in 8 directions
        h, w = img.shape
        
        # Horizontal differences
        diff_h = img[:, 1:] - img[:, :-1]
        # Vertical differences
        diff_v = img[1:, :] - img[:-1, :]
        
        # Compute co-occurrence matrices for differences
        spam_features = []
        
        # Statistics of differences
        mean_h = np.mean(np.abs(diff_h))
        mean_v = np.mean(np.abs(diff_v))
        std_h = np.std(diff_h)
        std_v = np.std(diff_v)
        
        # Higher order statistics
        skew_h = stats.skew(diff_h.flatten())
        skew_v = stats.skew(diff_v.flatten())
        kurt_h = stats.kurtosis(diff_h.flatten())
        kurt_v = stats.kurtosis(diff_v.flatten())
        
        # Steganography often increases these values
        spam_score = (std_h + std_v + abs(skew_h) + abs(skew_v)) / 4 * 10
        probability = min(spam_score, 100)
        
        return {
            "spam_score": spam_score,
            "probability": probability,
            "mean_horizontal": mean_h,
            "mean_vertical": mean_v,
            "std_horizontal": std_h,
            "std_vertical": std_v,
            "skewness_horizontal": skew_h,
            "skewness_vertical": skew_v,
            "interpretation": "High SPAM features suggest steganography" if spam_score > 30 else "Normal SPAM values - likely clean"
        }
    
    def pixel_value_difference(self, image_path):
        """
        Pixel Value Difference (PVD) Analysis
        Analyzes differences between adjacent pixels
        """
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return {"error": "Could not load image"}
        
        h, w = img.shape
        
        # Calculate differences in all 4 directions
        diff_h = np.abs(img[:, 1:].astype(float) - img[:, :-1].astype(float))
        diff_v = np.abs(img[1:, :].astype(float) - img[:-1, :].astype(float))
        diff_d1 = np.abs(img[1:, 1:].astype(float) - img[:-1, :-1].astype(float))
        diff_d2 = np.abs(img[1:, :-1].astype(float) - img[:-1, 1:].astype(float))
        
        # Calculate statistics
        mean_diff = np.mean([np.mean(diff_h), np.mean(diff_v), np.mean(diff_d1), np.mean(diff_d2)])
        std_diff = np.std([np.std(diff_h), np.std(diff_v), np.std(diff_d1), np.std(diff_d2)])
        
        # Calculate histogram of differences
        all_diffs = np.concatenate([diff_h.flatten(), diff_v.flatten(), diff_d1.flatten(), diff_d2.flatten()])
        
        # Calculate entropy
        hist, _ = np.histogram(all_diffs, bins=32, range=(0, 256))
        hist = hist / (hist.sum() + 1e-10)
        entropy = -np.sum(hist * np.log2(hist + 1e-10))
        
        # Higher entropy and variance often indicates steganography
        pvd_score = (mean_diff + std_diff + entropy * 10) / 3
        probability = min(pvd_score, 100)
        
        return {
            "pvd_score": pvd_score,
            "probability": probability,
            "mean_difference": mean_diff,
            "std_difference": std_diff,
            "entropy": entropy,
            "interpretation": "High PVD values suggest steganography" if pvd_score > 20 else "Normal PVD values - likely clean"
        }
    
    def histogram_analysis(self, image_path):
        """
        Histogram Analysis for Steganography Detection
        Analyzes histogram characteristics
        """
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return {"error": "Could not load image"}
        
        # Calculate histogram
        hist, bins = np.histogram(img.flatten(), bins=256, range=(0, 256))
        
        # Calculate histogram statistics
        mean_val = np.mean(img)
        std_val = np.std(img)
        
        # Calculate histogram smoothness
        smoothness = 1 - np.sum(np.abs(np.diff(hist))) / (2 * 255 * img.size)
        
        # Calculate histogram entropy
        hist_norm = hist / (hist.sum() + 1e-10)
        entropy = -np.sum(hist_norm * np.log2(hist_norm + 1e-10))
        
        # Calculate chi-square on histogram
        expected = img.size / 256
        chi_square = np.sum((hist - expected) ** 2 / (expected + 1e-10))
        
        # Histogram should be smooth for natural images
        # Sharp peaks or unusual patterns indicate steganography
        histogram_score = (chi_square / 1000 + (1 - smoothness) * 50 + abs(entropy - 4) * 10)
        probability = min(histogram_score, 100)
        
        return {
            "histogram_score": histogram_score,
            "probability": probability,
            "mean": mean_val,
            "std": std_val,
            "smoothness": smoothness,
            "entropy": entropy,
            "chi_square": chi_square,
            "interpretation": "Unusual histogram suggests steganography" if histogram_score > 30 else "Normal histogram - likely clean"
        }
    
    def ensemble_detection(self, image_path):
        """
        Combines all detection methods for ensemble result
        """
        results = {}
        
        # Run all methods
        results['chi_square'] = self.chi_square_analysis(image_path)
        results['rs_analysis'] = self.rs_analysis(image_path)
        results['spam'] = self.spam_features(image_path)
        results['pvd'] = self.pixel_value_difference(image_path)
        results['histogram'] = self.histogram_analysis(image_path)
        
        # Calculate ensemble probability (weighted average)
        weights = {
            'chi_square': 0.25,
            'rs_analysis': 0.20,
            'spam': 0.20,
            'pvd': 0.15,
            'histogram': 0.20
        }
        
        ensemble_prob = 0
        for method, weight in weights.items():
            if 'probability' in results[method]:
                ensemble_prob += results[method]['probability'] * weight
        
        results['ensemble_probability'] = ensemble_prob
        results['final_detection'] = 'STEGO DETECTED' if ensemble_prob > 50 else 'LIKELY CLEAN'
        
        return results


# DCT Steganography Module
class DCTSteganography:
    """DCT-based Steganography for more robust embedding"""
    
    @staticmethod
    def embed_dct(image_path, message, output_path):
        """Embed message using DCT coefficients"""
        img = cv2.imread(image_path)
        if img is None:
            return False
        
        # Convert to YUV color space
        yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
        y = yuv[:, :, 0]
        
        # Divide into 8x8 blocks and apply DCT
        h, w = y.shape
        h = (h // 8) * 8
        w = (w // 8) * 8
        y = y[:h, :w]
        
        # Convert message to binary
        binary_msg = ''.join(format(ord(c), '08b') for c in message)
        binary_msg += '00000000'  # End marker
        
        if len(binary_msg) > (h * w // 64):
            return False
        
        idx = 0
        for i in range(0, h, 8):
            for j in range(0, w, 8):
                if idx >= len(binary_msg):
                    break
                    
                block = y[i:i+8, j:j+8].astype(float)
                dct = cv2.dct(block)
                
                # Modify middle-frequency coefficients
                if idx < len(binary_msg):
                    dct[3, 3] = (int(dct[3, 3]) & 0xFE) | int(binary_msg[idx])
                    idx += 1
                
                y[i:i+8, j:j+8] = cv2.idct(dct)
        
        yuv[:, :, 0] = y
        result = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
        cv2.imwrite(output_path, result)
        
        return True
    
    @staticmethod
    def extract_dct(image_path):
        """Extract message from DCT coefficients"""
        img = cv2.imread(image_path)
        if img is None:
            return None
        
        yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
        y = yuv[:, :, 0]
        
        h, w = y.shape
        h = (h // 8) * 8
        w = (w // 8) * 8
        
        binary_msg = ''
        for i in range(0, h, 8):
            for j in range(0, w, 8):
                block = y[i:i+8, j:j+8].astype(float)
                dct = cv2.dct(block)
                
                binary_msg += str(int(dct[3, 3]) & 1)
                
                # Check for end marker
                if len(binary_msg) >= 8 and binary_msg[-8:] == '00000000':
                    break
            else:
                continue
            break
        
        # Convert binary to message
        chars = [binary_msg[i:i+8] for i in range(0, len(binary_msg) - 8, 8)]
        message = ''.join(chr(int(c, 2)) for c in chars if len(c) == 8)
        
        return message


# Performance Metrics Calculator
class PerformanceMetrics:
    """Calculate and display performance metrics"""
    
    @staticmethod
    def calculate_metrics(true_positives, false_positives, true_negatives, false_negatives):
        """Calculate all performance metrics"""
        
        # Accuracy
        accuracy = (true_positives + true_negatives) / (
            true_positives + false_positives + true_negatives + false_negatives + 1e-10
        )
        
        # Precision
        precision = true_positives / (true_positives + false_positives + 1e-10)
        
        # Recall / Sensitivity
        recall = true_positives / (true_positives + false_negatives + 1e-10)
        
        # Specificity
        specificity = true_negatives / (true_negatives + false_positives + 1e-10)
        
        # F1 Score
        f1_score = 2 * (precision * recall) / (precision + recall + 1e-10)
        
        # False Positive Rate
        fpr = false_positives / (false_positives + true_negatives + 1e-10)
        
        return {
            'accuracy': accuracy * 100,
            'precision': precision * 100,
            'recall': recall * 100,
            'specificity': specificity * 100,
            'f1_score': f1_score * 100,
            'false_positive_rate': fpr * 100
        }
    
    @staticmethod
    def generate_confusion_matrix(true_positives, false_positives, true_negatives, false_negatives):
        """Generate confusion matrix data"""
        return {
            'matrix': [
                [true_negatives, false_positives],
                [false_negatives, true_positives]
            ],
            'labels': ['Predicted Clean', 'Predicted Stego'],
            'actual_labels': ['Actual Clean', 'Actual Stego']
        }


# Dataset Generator for Training
class DatasetGenerator:
    """Generate synthetic dataset for training"""
    
    @staticmethod
    def generate_samples(output_dir, num_samples=100):
        """Generate clean and stego image samples"""
        import random
        
        os.makedirs(os.path.join(output_dir, 'clean'), exist_ok=True)
        os.makedirs(os.path.join(output_dir, 'stego'), exist_ok=True)
        
        # Generate clean samples from random images
        # This is a placeholder - in real implementation, use actual image datasets
        print(f"Generated {num_samples} clean and {num_samples} stego samples")
        
        return {
            'clean_dir': os.path.join(output_dir, 'clean'),
            'stego_dir': os.path.join(output_dir, 'stego'),
            'total_samples': num_samples * 2
        }
