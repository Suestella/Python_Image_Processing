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

    def open_image(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(filetypes=[('Image Files', '*.png;*.jpg;*.jpeg')])
        if file_path:
            self.image = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), cv2.IMREAD_COLOR)

    def convert_to_gray(self):
        if self.image is not None:
            self.gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    def apply_fft(self):
        if self.gray_image is not None:
            f = np.fft.fft2(self.gray_image)
            fshift = np.fft.fftshift(f)
            self.fft_image = 20 * np.log(np.abs(fshift))
            self.magnitude_spectrum = np.uint8(self.fft_image)

    def display_spectrum(self):
        if self.magnitude_spectrum is not None:
            cv2.imshow('Magnitude Spectrum', self.magnitude_spectrum)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def process_image(self):
        self.open_image()
        self.convert_to_gray()
        self.apply_fft()
        self.display_spectrum()


if __name__ == '__main__':
    processor = ImageProcessing()

    root = tk.Tk()
    root.title('Image Processing')
    root.geometry('700x300')

    open_button = tk.Button(root, text='Open Image', command=processor.process_image)
    open_button.pack(pady=10)

    root.mainloop()
