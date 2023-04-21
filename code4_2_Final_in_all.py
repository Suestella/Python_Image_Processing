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
        self.filtered_image_mean_filter = None
        self.filtered_image_median_filter = None
        self.filtered_image_adaptive_median_filter = None

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
        if self.filtered_image_mean_filter is not None:
            cv2.imshow('mean_filter Image', self.filtered_image_mean_filter)
        if self.filtered_image_median_filter is not None:
            cv2.imshow('median_filter Image', self.filtered_image_median_filter)
        if self.filtered_image_adaptive_median_filter is not None:
            cv2.imshow('adaptive_median_filter Image', self.filtered_image_adaptive_median_filter)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def add_gaussian_noise(self, mean=0, std=10):
        if self.image is not None:
            h, w, c = self.image.shape
            noise = np.random.normal(mean, std, (h, w, c))
            self.noisy_image = np.clip(self.image + noise, 0, 255).astype(np.uint8)

    def add_salt_and_pepper_noise(self, prob=0.01):
        if self.image is not None:
            h, w, c = self.image.shape
            noisy_image = np.copy(self.image)
            # 生成随机数矩阵，决定哪些像素添加椒盐噪声
            random_matrix = np.random.rand(h, w)
            # 设置随机数矩阵中小于prob/2的像素为0，小于prob的像素为255
            noisy_image[random_matrix <= prob / 2] = 0
            noisy_image[np.logical_and(random_matrix > prob / 2, random_matrix <= prob)] = 255
            self.noisy_image = noisy_image.astype(np.uint8)

    def apply_mean_filter(self, kernel_size):
        if self.image is not None:
            kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size * kernel_size)
            self.filtered_image_mean_filter = cv2.filter2D(self.image, -1, kernel)

    def apply_median_filter(self, kernel_size):
        if self.image is not None:
            self.filtered_image_median_filter = cv2.medianBlur(self.image, kernel_size)

    def apply_adaptive_median_filter(self, kernel_size):
        if self.image is not None:
            self.gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            rows, cols = self.gray_image.shape
            max_kernel_size = min(rows, cols)
            for i in range(rows):
                for j in range(cols):
                    k = 1
                    while k <= max_kernel_size:
                        half_k = k // 2
                        min_row = max(i - half_k, 0)
                        max_row = min(i + half_k, rows - 1)
                        min_col = max(j - half_k, 0)
                        max_col = min(j + half_k, cols - 1)
                        window = self.gray_image[min_row:max_row + 1, min_col:max_col + 1]
                        median = np.median(window)
                        std_dev = np.std(window)
                        if std_dev <= 30:
                            break
                        k += 2
                        if k > max_kernel_size:
                            self.gray_image[i, j] = median
                            break
                    else:
                        self.gray_image[i, j] = median

            self.filtered_image_adaptive_median_filter = cv2.cvtColor(self.gray_image, cv2.COLOR_GRAY2BGR)


img_proc = ImageProcessing()
img_proc.open_image()  # 选择一张图像
img_proc.add_gaussian_noise()  # 添加高斯噪声，默认均值为0，标准差为10
img_proc.add_salt_and_pepper_noise()  # 添加椒盐噪声，默认概率为0.01
img_proc.apply_mean_filter(3)  # 应用 3x3 的均值滤波器
img_proc.apply_median_filter(3) # 应用 3x3 的中值滤波器
img_proc.apply_adaptive_median_filter(3) # 应用自适应中值滤波器
img_proc.show_images()

