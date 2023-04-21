import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog


class ImageProcessing:
    def __init__(self):
        self.image = None
        self.gray_image = None
        self.noisy_image = None
        self.fft_image = None
        self.magnitude_spectrum = None
        self.filtered_image = None

    def open_image(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(filetypes=[('Image Files', '*.png;*.jpg;*.jpeg')])
        if file_path:
            self.image = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), cv2.IMREAD_COLOR)

    def show_images(self):
        if self.image is not None:
            cv2.imshow('Original Image', self.image)
        if self.noisy_image is not None:
            cv2.imshow('Noisy Image', self.noisy_image)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def add_gaussian_noise(self, mean=0, std=10):
        if self.image is not None:
            h, w, c = self.image.shape
            noise = np.random.normal(mean, std, (h, w, c))
            self.noisy_image = np.clip(self.image + noise, 0, 255).astype(np.uint8)
img_proc = ImageProcessing()
img_proc.open_image()  # 选择一张图像
img_proc.add_gaussian_noise()  # 添加高斯噪声，默认均值为0，标准差为10
img_proc.show_images()  # 显示原始图像和带有高斯噪声的图像
