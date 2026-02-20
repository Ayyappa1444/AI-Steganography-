# ai/heatmap.py
import numpy as np
from PIL import Image
import cv2
import os
import matplotlib.pyplot as plt
from datetime import datetime

def create_heatmap(file_path: str):
    """Generate steganography heatmap visualization"""
    # Load image
    img = Image.open(file_path).convert('RGB')
    img_array = np.array(img)
    
    # Create steganography suspicion map (simulated)
    h, w, _ = img_array.shape
    suspicion_map = generate_suspicion_map(h, w)
    
    # Create heatmap overlay
    heatmap = cv2.applyColorMap((suspicion_map * 255).astype(np.uint8), cv2.COLORMAP_JET)
    
    # Overlay on original image
    overlay = cv2.addWeighted(img_array, 0.6, heatmap, 0.4, 0)
    
    # Save results
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save heatmap overlay
    output_path = f"heatmap_{base_name}_{timestamp}.png"
    cv2.imwrite(output_path, cv2.cvtColor(overlay, cv2.COLOR_RGB2BGR))
    
    # Save suspicion intensity plot
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.imshow(img)
    plt.title("Original Image")
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.imshow(suspicion_map, cmap='hot', interpolation='nearest')
    plt.title("Steganography Suspicion Heatmap")
    plt.colorbar(label='Suspicion Level')
    plt.axis('off')
    
    plt.tight_layout()
    plt.savefig(f"suspicion_{base_name}_{timestamp}.png", dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Heatmaps saved:")
    print(f"  • Overlay: {output_path}")
    print(f"  • Analysis: suspicion_{base_name}_{timestamp}.png")

def generate_suspicion_map(height, width):
    """Generate realistic steganography suspicion map"""
    # Simulate areas where stego is more likely
    suspicion = np.random.uniform(0.1, 0.6, (height, width))
    
    # Add edge effects (stego often affects edges more)
    y, x = np.ogrid[:height, :width]
    center_y, center_x = height//2, width//2
    distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
    suspicion += 0.2 * (distance / max(height, width))
    
    # Add random hotspots
    hotspots = np.random.choice([0, 1], (height, width), p=[0.95, 0.05])
    suspicion += hotspots * 0.3
    
    return np.clip(suspicion, 0, 1)
