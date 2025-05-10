import tkinter as tk
from screens.home import HomeScreen
import pygame
import os

if __name__ == '__main__':

    root = tk.Tk()
    root.title("DSA World")
    root.geometry("800x800")
    root.resizable(False, False)

    app = HomeScreen(root)
    root.mainloop()
