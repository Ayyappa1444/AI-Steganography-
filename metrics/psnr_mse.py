import cv2
import numpy as np
import math

def calculate_psnr(img1, img2):
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return 100, 0
    psnr = 20 * math.log10(255.0 / math.sqrt(mse))
    return psnr, mse
