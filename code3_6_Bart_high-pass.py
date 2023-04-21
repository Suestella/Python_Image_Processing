import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog


class ImageProcessing:
    def __init__(self):
        self.image = None
        self.gray_image = None
        self.fft_image = None
        self.magnitude_spectrum = None
        self.filtered_image = None

    def open_image(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(filetypes=[('Image Files', '*.png;*.jpg;*.jpeg')])
        if file_path:
            self.image = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), cv2.IMREAD_COLOR)

    def apply_high_pass_filter(self):
        if self.image is not None:
            # Convert image to grayscale
            self.gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            # Apply Fourier Transform
            self.fft_image = np.fft.fft2(self.gray_image)
            # Shift zero-frequency component to center
            self.fft_image = np.fft.fftshift(self.fft_image)
            # Compute magnitude spectrum
            self.magnitude_spectrum = 20 * np.log(np.abs(self.fft_image))
            # Create high-pass filter mask using Butterworth filter
            rows, cols = self.gray_image.shape
            crow, ccol = rows // 2, cols // 2
            n = 2  # Order of Butterworth filter
            d_0 = 30  # Cut-off frequency
            # Create distance matrix
            u, v = np.meshgrid(np.arange(cols) - ccol, np.arange(rows) - crow)
            d_uv = np.sqrt(u ** 2 + v ** 2)
            # Create filter mask
            h = 1 / (1 + (d_0 / d_uv) ** (2 * n))
            # Apply filter
            self.filtered_image = self.fft_image * h
            # Shift zero-frequency component back to top-left
            self.filtered_image = np.fft.ifftshift(self.filtered_image)
            # Inverse Fourier Transform
            self.filtered_image = np.fft.ifft2(self.filtered_image)
            # Convert back to uint8
            self.filtered_image = np.abs(self.filtered_image).astype(np.uint8)

    def show_images(self):
        if self.image is not None:
            cv2.imshow('Original Image', self.image)
        if self.filtered_image is not None:
            cv2.imshow('Bart_high-pass Filtered Image', self.filtered_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == '__main__':
    image_processing = ImageProcessing()
    image_processing.open_image()
    image_processing.apply_high_pass_filter()
    image_processing.show_images()
