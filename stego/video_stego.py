# stego/video_stego.py
import os
import base64
import numpy as np
from PIL import Image
from cryptography.fernet import Fernet
import hashlib
import shutil
from pathlib import Path

def generate_key_from_password(password: str) -> bytes:
    """Convert password to Fernet key"""
    key = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(key)

def hide_message_in_video(video_path: str, message: str, key: str, output_path: str):
    """
    Hide encrypted message in first 100 frames of video using image steganography
    REAL IMPLEMENTATION - Processes actual video frames
    """
    import cv2  # OpenCV for video processing
    
    # Generate encryption key
    fernet_key = generate_key_from_password(key)
    cipher = Fernet(fernet_key)
    
    # Encrypt message
    encrypted = cipher.encrypt(message.encode())
    data = base64.b64encode(encrypted).decode() + "|||VIDEO_END|||"
    binary_data = ''.join(format(ord(c), '08b') for c in data)
    
    # Open video
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    frame_count = 0
    data_index = 0
    
    print(f"Processing {total_frames} frames, embedding {len(binary_data)} bits...")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        frame_count += 1
        
        # Convert frame to PIL Image for steganography
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(frame_rgb)
        
        # Embed data in first 100 frames only
        if frame_count <= 100 and data_index < len(binary_data):
            pixels = list(pil_image.getdata())
            
            new_pixels = []
            for i, (r, g, b) in enumerate(pixels):
                if data_index < len(binary_data):
                    r = (r & 0xFE) | int(binary_data[data_index])
                    data_index += 1
                if data_index < len(binary_data):
                    g = (g & 0xFE) | int(binary_data[data_index])
                    data_index += 1
                if data_index < len(binary_data):
                    b = (b & 0xFE) | int(binary_data[data_index])
                    data_index += 1
                new_pixels.append((r, g, b))
                
                # Check if data fully embedded
                if data_index >= len(binary_data):
                    break
            
            # Rebuild frame
            stego_frame = Image.new('RGB', pil_image.size)
            stego_frame.putdata(new_pixels[:len(pixels)])
            frame = cv2.cvtColor(np.array(stego_frame), cv2.COLOR_RGB2BGR)
        
        out.write(frame)
        
        # Progress
        if frame_count % 30 == 0:
            print(f"Processed {frame_count}/{total_frames} frames...")
    
    cap.release()
    out.release()
    print(f"Video steganography complete: {output_path}")
    
    if data_index < len(binary_data):
        raise ValueError("Video too short! Message not fully embedded.")

def extract_message_from_video(video_path: str, key: str) -> str:
    """Extract message from video frames"""
    import cv2
    import numpy as np
    
    fernet_key = generate_key_from_password(key)
    cipher = Fernet(fernet_key)
    
    cap = cv2.VideoCapture(video_path)
    
    binary_data = ""
    frame_count = 0
    
    print("Extracting from first 100 frames...")
    
    while cap.isOpened() and frame_count < 100:
        ret, frame = cap.read()
        if not ret:
            break
            
        frame_count += 1
        
        # Convert to PIL for pixel access
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(frame_rgb)
        pixels = list(pil_image.getdata())
        
        # Extract LSB from each pixel
        for r, g, b in pixels[:1000]:  # Limit per frame
            binary_data += str(r & 1) + str(g & 1) + str(b & 1)
            
            # Convert 8 bits to char and check for end marker
            if len(binary_data) % 8 == 0:
                chunk = binary_data[-8:]
                char = chr(int(chunk, 2))
                if "|||VIDEO_END|||" in char * (len(binary_data) // 8 % 12):
                    break
        
        print(f"Frame {frame_count}: {len(binary_data)//8} chars extracted...")
    
    cap.release()
    
    # Convert binary to text
    chars = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    data = ''.join(chr(int(c, 2)) for c in chars if len(c) == 8)
    
    if "|||VIDEO_END|||" in data:
        encrypted_b64 = data.split("|||VIDEO_END|||")[0]
        encrypted = base64.b64decode(encrypted_b64)
        decrypted = cipher.decrypt(encrypted).decode()
        return decrypted
    else:
        raise ValueError("No message found or wrong key!")
