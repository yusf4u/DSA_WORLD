### main.py
import tkinter as tk
from screens.home import HomeScreen

if __name__ == '__main__':
    root = tk.Tk()
    app = HomeScreen(root)
    root.mainloop()


### home.py
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
