import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from screens.menu import MenuScreen  # استيراد شاشة المينيو

class HomeScreen:
    def __init__(self, master):
        self.master = master
        self.master.title("DSA World")
        self.master.geometry("800x800")
        self.master.resizable(False, False)

        # تحميل الخلفية
        bg_path = os.path.join("assets", "background", "home_bg.png")
        bg_image = Image.open(bg_path).resize((800, 800), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        self.canvas = tk.Canvas(self.master, width=800, height=800)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        self.create_buttons()

    def create_buttons(self):
        button_font = ("Pixel", 20, "bold")

        # إنشاء الأزرار
        self.start_button = tk.Button(self.master, text="Start", font=button_font, bg="#FFD93D", fg="black", command=self.start_game)
        self.about_button = tk.Button(self.master, text="About", font=button_font, bg="#6BCB77", fg="black", command=self.show_about)
        self.exit_button = tk.Button(self.master, text="Exit", font=button_font, bg="#FF6B6B", fg="black", command=self.master.quit)

        # تحديد الإحداثيات لتمركز الأزرار في منتصف الشاشة
        center_x = 400  # منتصف العرض (800 / 2)
        start_y = 360   # نبدأ من هذا الموضع وننزل تدريجياً

        self.canvas.create_window(center_x, start_y, window=self.start_button, width=200, height=50)
        self.canvas.create_window(center_x, start_y + 80, window=self.about_button, width=200, height=50)
        self.canvas.create_window(center_x, start_y + 160, window=self.exit_button, width=200, height=50)

    def start_game(self):
        self.canvas.destroy()
        self.start_button.destroy()
        self.about_button.destroy()
        self.exit_button.destroy()
        MenuScreen(self.master, self.__init__)  # يعيد تحميل home عند الرجوع

    def show_about(self):
        messagebox.showinfo("About", "DSA World\nCreated by [Your Name]\nAn interactive way to learn Data Structures")
