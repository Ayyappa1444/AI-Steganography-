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
    Hide encrypted message in first 100 frames of video using LSB steganography
    """
    import cv2
    
    # Generate encryption key
    fernet_key = generate_key_from_password(key)
    cipher = Fernet(fernet_key)
    
    # Encrypt message
    encrypted = cipher.encrypt(message.encode())
    data = base64.b64encode(encrypted).decode() + "|||VIDEO_END|||"
    
    # Convert string to binary - properly handle each character's bytes
    binary_data = ''
    for char in data:
        binary_data += format(ord(char), '08b')
    
    # Open video
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Video writer (lossless preferred)
    ext = Path(output_path).suffix.lower()
    if ext == ".avi":
        fourcc = cv2.VideoWriter_fourcc(*'FFV1')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        if not out.isOpened():
            fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    else:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    if not out.isOpened():
        cap.release()
        raise ValueError("Failed to create output video. Try saving as .avi (lossless).")
    
    frame_count = 0
    data_index = 0
    
    print(f"Processing {total_frames} frames, embedding {len(binary_data)} bits...")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        frame_count += 1
        
        # Embed data in first 100 frames only
        if frame_count <= 100 and data_index < len(binary_data):
            # Work directly with numpy array (BGR format from OpenCV)
            pixels = frame.astype(np.uint8)
            
            # Flatten and embed
            flat_pixels = pixels.flatten()
            
            # Embed bits into LSB of each color channel
            max_bits = len(flat_pixels)
            bits_to_embed = min(len(binary_data) - data_index, max_bits)
            
            for i in range(bits_to_embed):
                # Clear LSB and set new bit
                flat_pixels[i] = (flat_pixels[i] & 0xFE) | int(binary_data[data_index + i])
            
            data_index += bits_to_embed
            
            # Reshape back and convert to BGR
            stego_frame = flat_pixels.reshape(pixels.shape)
            frame = stego_frame.astype(np.uint8)
        
        out.write(frame)
        
        # Progress
        if frame_count % 30 == 0:
            print(f"Processed {frame_count}/{total_frames} frames...")
        
        # Stop if all data embedded
        if data_index >= len(binary_data):
            # Write remaining frames without modification
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                frame_count += 1
                out.write(frame)
            break
    
    cap.release()
    out.release()
    print(f"Video steganography complete: {output_path}")
    
    if data_index < len(binary_data):
        raise ValueError("Video too short! Message not fully embedded.")

def extract_message_from_video(video_path: str, key: str) -> str:
    """Extract message from video frames"""
    import cv2
    
    fernet_key = generate_key_from_password(key)
    cipher = Fernet(fernet_key)
    
    cap = cv2.VideoCapture(video_path)
    
    marker = "|||VIDEO_END|||"
    bit_buffer = ""
    char_buffer = []
    frame_count = 0
    
    print("Extracting from first 100 frames...")
    
    while cap.isOpened() and frame_count < 100:
        ret, frame = cap.read()
        if not ret:
            break
            
        frame_count += 1
        
        # Extract LSB from each pixel
        flat_pixels = frame.flatten()
        
        for val in flat_pixels:
            bit_buffer += str(val & 1)
            
            # Process complete bytes
            while len(bit_buffer) >= 8:
                byte = bit_buffer[:8]
                bit_buffer = bit_buffer[8:]
                try:
                    char = chr(int(byte, 2))
                    char_buffer.append(char)
                except:
                    char_buffer.append('?')
                
                # Check for marker
                if len(char_buffer) >= len(marker):
                    if ''.join(char_buffer[-len(marker):]) == marker:
                        cap.release()
                        data = ''.join(char_buffer)
                        encrypted_b64 = data.split(marker)[0]
                        try:
                            encrypted = base64.b64decode(encrypted_b64)
                            decrypted = cipher.decrypt(encrypted).decode()
                            return decrypted
                        except Exception as e:
                            raise ValueError(f"Decryption failed: {e}")
        
        print(f"Frame {frame_count}: {len(char_buffer)} chars extracted...")
    
    cap.release()
    
    # Try to debug - show what we got
    if char_buffer:
        print(f"Extracted {len(char_buffer)} chars, marker not found")
        print(f"First 100 chars: {''.join(char_buffer[:100])}")
    
    raise ValueError("No message found or wrong key!")

# Aliases for compatibility with UI modules
def hide_video_message(video_path: str, message: str, key: str, output_path: str):
    """Alias for hide_message_in_video"""
    return hide_message_in_video(video_path, message, key, output_path)

def extract_video_message(video_path: str, key: str) -> str:
    """Alias for extract_message_from_video"""
    return extract_message_from_video(video_path, key)
