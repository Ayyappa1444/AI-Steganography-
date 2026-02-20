import cv2
import numpy as np
import matplotlib.pyplot as plt

def psnr_mse(original, stego):
    orig = cv2.imread(original)
    steg = cv2.imread(stego)

    mse = np.mean((orig - steg) ** 2)
    psnr = 10 * np.log10((255**2) / mse) if mse != 0 else 100

    plt.bar(["MSE","PSNR"], [mse, psnr])
    plt.title("Stego Quality Metrics")
    plt.show()

    return psnr, mse
