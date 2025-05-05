import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import sys
import importlib.util

class MenuScreen:
    def __init__(self, master, go_back_callback):
        self.master = master
        self.go_back_callback = go_back_callback
        self.master.title("DSA World - Menu")
        self.master.geometry("800x800")
        self.master.resizable(False, False)

        # Load background
        bg_path = os.path.join("assets", "background", "menu_bg.png")
        bg_image = Image.open(bg_path).resize((800, 800), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        self.canvas = tk.Canvas(self.master, width=800, height=800)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        self.create_buttons()

    def create_buttons(self):
        button_font = ("Pixel", 20, "bold")

        # Create all menu option buttons
        self.stack_button = tk.Button(
            self.master, 
            text="Stack", 
            font=button_font, 
            bg="#FFD93D", 
            fg="black", 
            command=lambda: self.select_option("Stack")
        )
        
        self.queue_button = tk.Button(
            self.master, 
            text="Queue", 
            font=button_font, 
            bg="#6BCB77", 
            fg="black", 
            command=lambda: self.select_option("Queue")
        )
        
        self.circular_queue_button = tk.Button(
            self.master, 
            text="Circular Queue", 
            font=button_font, 
            bg="#4D96FF", 
            fg="black", 
            command=lambda: self.select_option("Circular Queue")
        )
        
        self.linked_list_button = tk.Button(
            self.master, 
            text="Linked List", 
            font=button_font, 
            bg="#FF6B6B", 
            fg="black", 
            command=lambda: self.select_option("Linked List")
        )
        
        self.hanoi_button = tk.Button(
            self.master, 
            text="Hanoi Tower", 
            font=button_font, 
            bg="#9D4EDD", 
            fg="black", 
            command=lambda: self.select_option("Hanoi Tower")
        )
        
        self.back_button = tk.Button(
            self.master, 
            text="Back", 
            font=button_font, 
            bg="#333333", 
            fg="white", 
            command=self.go_to_home
        )

        # Position all buttons vertically centered
        center_x = 400
        start_y = 320
        
        self.canvas.create_window(center_x, start_y, window=self.stack_button, width=200, height=50)
        self.canvas.create_window(center_x, start_y + 80, window=self.queue_button, width=200, height=50)
        self.canvas.create_window(center_x, start_y + 160, window=self.circular_queue_button, width=200, height=50)
        self.canvas.create_window(center_x, start_y + 240, window=self.linked_list_button, width=200, height=50)
        self.canvas.create_window(center_x, start_y + 320, window=self.hanoi_button, width=200, height=50)
        # self.canvas.create_window(center_x, start_y + 400, window=self.back_button, width=200, height=50)

    def select_option(self, option):
        messagebox.showinfo("Selected", f"You selected: {option}")
        # Here you would typically launch the selected visualization
        # Example:
        # if option == "Stack":
        #     import stack_visualizer
        #     stack_visualizer.run()

    def go_to_home(self):
        """Navigate back to home screen (home.py)"""
        self.canvas.destroy()
        
        try:
            # Find home.py in the same directory
            home_dir = os.path.dirname(os.path.abspath(__file__))
            home_path = os.path.join(home_dir, "home.py")
            
            if os.path.exists(home_path):
                # Dynamically import home module
                spec = importlib.util.spec_from_file_location("home", home_path)
                home_module = importlib.util.module_from_spec(spec)
                sys.modules["home"] = home_module
                spec.loader.exec_module(home_module)
                
                # Create new home screen
                self.master.destroy()  # Close current window
                root = tk.Tk()
                home_module.HomeScreen(root)
                root.mainloop()
            else:
                raise FileNotFoundError("home.py not found")
        except Exception as e:
            print(f"Error loading home screen: {e}")
            # Fallback to original callback
            self.go_back_callback(self.master)


if __name__ == "__main__":
    root = tk.Tk()
    
    def dummy_callback(master):
        print("Default callback: Closing window")
        master.destroy()
    
    menu = MenuScreen(root, dummy_callback)
    root.mainloop()