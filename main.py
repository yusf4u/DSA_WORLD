import tkinter as tk
from screens.home import HomeScreen
import pygame
import os

if __name__ == '__main__':
    # مسار الموسيقى
    music_path = os.path.join("assets", "music", "The Icy Cave.mp3")

    # تهيئة pygame وتشغيل الموسيقى
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1)  # تشغيل الموسيقى بشكل متكرر (loop)

    # إعداد نافذة Tkinter
    root = tk.Tk()
    root.title("DSA World")
    root.geometry("800x800")
    root.resizable(False, False)

    app = HomeScreen(root)
    root.mainloop()

    # إيقاف الموسيقى عند إغلاق التطبيق
    pygame.mixer.music.stop()
