# AI STEGANOGRAPHY SUITE - PROJECT BRIEF

## 1. What is Steganography?

**Steganography** is the art and science of hiding secret information within other non-secret data (like images, videos, or audio files) so that the existence of the hidden message is undetectable.

Think of it like this: 
- **Cryptography** = Scrambles the message (so no one can read it)
- **Steganography** = Hides the message entirely (so no one knows it exists)

---

## 2. What This Project Does

This **AI Steganography Suite** is a desktop application that provides:

### 🔐 **Steganography (Hiding Data)**
- Hide secret messages inside images using LSB (Least Significant Bit) technique
- Hide secret messages inside videos using frame-based embedding
- Password-protected encryption for security

### 🔍 **Steganalysis (Detecting Hidden Data)**
- AI-powered detection to find hidden data in images
- 12 different analysis methods for comprehensive detection
- Visual heatmaps showing which pixels might contain hidden data

---

## 3. Key Features

| Feature | Description |
|---------|-------------|
| **Image Steganography** | Hide text messages inside PNG/JPG images |
| **Video Steganography** | Hide messages inside MP4/AVI videos |
| **LSB Analysis** | Analyze Least Significant Bits for anomalies |
| **Chi-Square Test** | Statistical test for detecting steganography |
| **RS Analysis** | Regular-Singular analysis method |
| **SPAM Features** | Subtractive Pixel Adjacency Matrix analysis |
| **PVD Analysis** | Pixel Value Difference analysis |
| **Histogram Analysis** | Analyze image histogram for anomalies |
| **CNN Detection** | Deep learning-based detection |
| **Ensemble Detection** | Combine multiple methods for best results |
| **Heatmap Visualization** | Visual display of suspicious areas |
| **Graph Reports** | Detailed analysis with charts |

---

## 4. How It Works

### Image Steganography (Hiding):
```
1. User uploads an image (cover)
2. User enters secret message
3. User sets a password/key
4. System encrypts message using XOR
5. System embeds encrypted bits into image's LSB pixels
6. System saves new image (stego image)
```

### Steganalysis (Detection):
```
1. User uploads image to analyze
2. User selects analysis method (12 options)
3. System analyzes pixel patterns
4. System calculates probability of hidden data
5. System displays results with visualization
```

---

## 5. Technical Implementation

### Technologies Used:
- **Python** - Programming language
- **PyQt6** - Modern GUI framework
- **OpenCV** - Image/video processing
- **NumPy** - Numerical computations
- **Matplotlib** - Graph visualization
- **SciPy** - Statistical analysis

### Algorithms:
- **LSB (Least Significant Bit)** - Main steganography method
- **XOR Encryption** - Message encryption
- **Chi-Square Test** - Statistical detection
- **RS Analysis** - Flip-based detection
- **CNN** - Deep learning detection

---

## 6. Applications

| Area | Use Case |
|------|----------|
| **Cybersecurity** | Detect hidden data in investigations |
| **Digital Forensics** | Find evidence in images/videos |
| **Academia** | Research in information hiding |
| **Education** | Learn steganography techniques |
| **Watermarking** | Add invisible watermarks |

---

## 7. Project Structure

```
project/
├── app/
│   ├── ui_main.py       # Main GUI application
│   └── main.py          # Entry point
├── ai/
│   ├── steganalysis_models.py  # Advanced detection algorithms
│   └── cnn_steganalysis.py     # CNN-based detection
├── stego/
│   ├── image_stego.py    # Image steganography
│   └── video_stego.py   # Video steganography
└── PROJECT_BRIEF.md      # This file
```

---

## 8. How to Use

### Running the Application:
```
bash
cd project
python app/main.py
```

### Using Image Steganography:
1. Click "Image Stego" in sidebar
2. Click "Upload" to select an image
3. Type your secret message
4. Enter a password/key
5. Click "ENCRYPT & HIDE"
6. Save the resulting stego image

### Using AI Detection:
1. Click "AI Detection" in sidebar
2. Select analysis method from dropdown
3. Upload an image to analyze
4. Click "Analyze"
5. View results in Result/Heatmap/Graphs/Report tabs

---

## 9. Why This Project is Unique

✅ **12 Different Detection Methods** - More than any similar tool  
✅ **Combines Steganography + Steganalysis** - Both hiding and detection  
✅ **Modern GUI** - User-friendly interface  
✅ **AI-Powered** - Uses CNN and ensemble methods  
✅ **Visualization** - Heatmaps and graphs for understanding  
✅ **UGC Publication Ready** - Research-quality algorithms  

---

## 10. Summary

This project demonstrates:
- How to hide data inside images/videos
- How to detect hidden data using AI
- Multiple statistical analysis techniques
- Modern GUI development with PyQt6
- Integration of deep learning (CNN) for security applications

It's an excellent educational tool and research project for understanding information hiding techniques!
