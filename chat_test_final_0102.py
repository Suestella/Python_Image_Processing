import tkinter as tk

from tkinter import filedialog, ttk
from PIL import Image, ImageTk, ImageOps, ImageFilter, ImageMath
import math
import subprocess

class ImageProcessor:
    def __init__(self, master):
        self.master = master
        master.title("图像处理软件")
        master.geometry("800x600")



        self.x_value = tk.IntVar()
        self.y_value = tk.IntVar()

        self.log_gray = False
        # 添加指数变量的初始化
        self.expo_value = tk.DoubleVar(value=1.0)  # 初始化指数变量为1.0

        self.stretch_min = tk.DoubleVar()
        self.stretch_max = tk.DoubleVar()

        # 初始化线性拉伸变量
        self.stretch_min.set(0)
        self.stretch_max.set(255)



        self.img_path = None
        self.img_original = None
        self.img_current = None
        self.img_tk = None
        self.img_label = tk.Label(master)
        self.img_label.pack()

        self.scale_value = tk.DoubleVar()
        self.rotate_value = tk.DoubleVar()

        self.create_menu()
        self.create_toolbar()



    def create_menu(self):
        menubar = tk.Menu(self.master)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="打开图像", command=self.open_image)
        filemenu.add_command(label="退出", command=self.master.quit)
        menubar.add_cascade(label="文件", menu=filemenu)


        self.master.config(menu=menubar)



    def create_toolbar(self):
        toolbar = tk.Frame(self.master)

        # 添加按钮以调用另一个程序
        other_program_button = tk.Button(toolbar, text="锐化", command=self.run_other_program)
        other_program_button.pack(side=tk.LEFT, padx=2)

        # 对数灰度变换
        log_gray_button = tk.Button(toolbar, text="对数灰度变换", command=self.log_gray_image)
        log_gray_button.pack(side=tk.LEFT, padx=2)

        # 添加指数变换按钮
        expo_button = tk.Button(toolbar, text="指数变换", command=self.expo_gray_image)
        expo_button.pack(side=tk.LEFT, padx=2)

        # 线性拉伸按钮
        stretch_button = tk.Button(toolbar, text="线性拉伸", command=self.stretch_image)
        stretch_button.pack(side=tk.LEFT, padx=2)

        # 添加均衡化按钮
        equalize_button = tk.Button(toolbar, text="均衡化", command=self.equalize_gray_image)
        equalize_button.pack(side=tk.LEFT, padx=2)

        # 添加输入框和按钮
        smooth_label = tk.Label(toolbar, text="平滑：")
        smooth_label.pack(side=tk.LEFT, padx=2)

        smooth_entry = tk.Entry(toolbar, width=5)
        smooth_entry.pack(side=tk.LEFT, padx=2)

        smooth_button = tk.Button(toolbar, text="平滑处理", command=lambda: self.smooth_image(int(smooth_entry.get())))
        smooth_button.pack(side=tk.LEFT, padx=2)


        # 线性拉伸最小值输入框
        stretch_min_label = tk.Label(toolbar, text="最小值")
        stretch_min_label.pack(side=tk.LEFT, padx=2)
        stretch_min_entry = tk.Entry(toolbar, width=5, textvariable=self.stretch_min)
        stretch_min_entry.pack(side=tk.LEFT, padx=2)

        # 线性拉伸最大值输入框
        stretch_max_label = tk.Label(toolbar, text="最大值")
        stretch_max_label.pack(side=tk.LEFT, padx=2)
        stretch_max_entry = tk.Entry(toolbar, width=5, textvariable=self.stretch_max)
        stretch_max_entry.pack(side=tk.LEFT, padx=2)


        # 缩放
        scale_label = tk.Label(toolbar, text="缩放：")
        scale_label.pack(side=tk.LEFT, padx=2)

        scale_slider = tk.Scale(toolbar, from_=0.1, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, length=200,
                                variable=self.scale_value, command=self.scale_image)
        scale_slider.pack(side=tk.LEFT, padx=2)

        # 旋转
        rotate_label = tk.Label(toolbar, text="旋转：")
        rotate_label.pack(side=tk.LEFT, padx=2)

        rotate_slider = tk.Scale(toolbar, from_=-180.0, to=180.0, resolution=1.0, orient=tk.HORIZONTAL, length=200,
                                 variable=self.rotate_value, command=self.rotate_image)
        rotate_slider.pack(side=tk.LEFT, padx=2)

        # 镜像
        mirror_button = tk.Button(toolbar, text="镜像", command=self.mirror_image)
        mirror_button.pack(side=tk.LEFT, padx=2)

        # 上下左右平移
        move_frame = tk.Frame(toolbar)
        move_frame.pack(side=tk.LEFT, padx=2)

        move_label = tk.Label(move_frame, text="平移：")
        move_label.pack(side=tk.LEFT, padx=2)

        x_label = tk.Label(move_frame, text="X：")
        x_label.pack(side=tk.LEFT, padx=2)

        x_entry = tk.Entry(move_frame, width=5, textvariable=self.x_value)
        x_entry.pack(side=tk.LEFT, padx=2)

        y_label = tk.Label(move_frame, text="Y：")
        y_label.pack(side=tk.LEFT, padx=2)

        y_entry = tk.Entry(move_frame, width=5, textvariable=self.y_value)
        y_entry.pack(side=tk.LEFT, padx=2)

        move_button = tk.Button(move_frame, text="移动", command=self.move_image)
        move_button.pack(side=tk.LEFT, padx=2)

        # 恢复原图
        reset_button = tk.Button(toolbar, text="恢复", command=self.reset_image)
        reset_button.pack(side=tk.LEFT, padx=2)

        toolbar.pack(side=tk.TOP, fill=tk.X)

    def log_gray_image(self):
        if self.img_original:
            self.log_gray = not self.log_gray
            if self.log_gray:
                # 转换为灰度图像
                self.img_current = self.img_original.copy().convert("L")
                # 对数灰度变换
                self.img_current = self.img_current.point(lambda x: 255 * (math.log(x + 1) / math.log(256)))
            else:
                self.img_current = self.img_original.copy()
            self.update_image()

    # 添加指数变换函数
    def expo_gray_image(self):
        if self.img_original:
            # 转换为灰度图像
            self.img_current = self.img_original.copy().convert("L")
            # 获取指数变量
            expo = self.expo_value.get()
            # 指数灰度变换
            self.img_current = self.img_current.point(lambda x: 255 * pow(x / 255, expo))
            self.update_image()
    def stretch_image(self):
        if self.img_original:
            # 获取最小值和最大值
            stretch_min = self.stretch_min.get()
            stretch_max = self.stretch_max.get()

            # 转换为灰度图像
            self.img_current = self.img_original.copy().convert("L")

            # 线性拉伸变换
            img_min, img_max = self.img_current.getextrema()
            if img_max > img_min:
                k = (stretch_max - stretch_min) / (img_max - img_min)
                b = stretch_min - k * img_min
                self.img_current = self.img_current.point(lambda x: int(k * x + b))

            self.update_image()

    def equalize_gray_image(self):
        if self.img_path is not None:
            self.img_current = self.img_original.copy().convert("L")
            self.img_current = ImageOps.equalize(self.img_current)
            self.img_tk = ImageTk.PhotoImage(self.img_current)
            self.img_label.config(image=self.img_tk)

    def smooth_image(self, smooth_value):
        if self.img_path is None:
            return
        if self.img_original is None:
            self.img_original = Image.open(self.img_path).convert("L")

        self.img_current = self.img_original.copy()

        # 平滑处理
        self.img_current = self.img_current.filter(ImageFilter.SMOOTH_MORE)

        # 更新图像
        self.update_image()

        self.log_gray = False
        self.stretch_min.set(0)
        self.stretch_max.set(255)

        # 更新线性拉伸变量
        self.stretch_min.set(self.img_current.getextrema()[0])
        self.stretch_max.set(self.img_current.getextrema()[1])


    def move_image(self):
        if self.img_original:
            x = self.x_value.get()
            y = self.y_value.get()
            self.img_current = self.img_original.copy().transform(self.img_original.size, Image.AFFINE,
                                                                  (1, 0, x, 0, 1, y))
            self.update_image()

    def reset_image(self):
        if self.img_original:
            self.img_current = self.img_original.copy()

            self.update_image()
            self.scale_value.set(1.0)
            self.rotate_value.set(0.0)

    def open_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.img_path = file_path
            self.img_original = Image.open(file_path)

            self.img_current = self.img_original.copy()
            self.update_image()

    def update_image(self):
        if self.img_current:
            self.img_tk = ImageTk.PhotoImage(self.img_current)
            self.img_label.config(image=self.img_tk)

    def scale_image(self, value):
        if self.img_original:
            scale_factor = float(value)
            self.img_current = self.img_original.copy().resize((int(scale_factor * self.img_original.width), int(scale_factor * self.img_original.height)))
            self.update_image()

    def rotate_image(self, value):
        if self.img_original:
            rotate_angle = float(value)
            self.img_current = self.img_original.copy().rotate(rotate_angle)
            self.update_image()

    def mirror_image(self):
        if self.img_original:
            self.img_current = self.img_original.copy().transpose(method=Image.FLIP_LEFT_RIGHT)
            self.update_image()

    def run_other_program(self):
        # 在同一目录下的other_program.py程序
        subprocess.run(["python", "Robert_Sobel.py"])



root = tk.Tk()
app = ImageProcessor(root)
root.mainloop()
