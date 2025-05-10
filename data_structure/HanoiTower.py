import tkinter as tk
from tkinter import messagebox, StringVar, IntVar
import time
import pygame
import os

class TowerOfHanoiApp:
    def __init__(self, master, go_back_callback):
        self.master = master
        self.go_back_callback = go_back_callback
        
        # Initialize sound system
        pygame.mixer.init()
        self.error_sound = pygame.mixer.Sound(os.path.join("assets", "music", "error.mp3"))
        self.win_sound = pygame.mixer.Sound(os.path.join("assets", "music", "win.mp3"))
        self.move_sound = pygame.mixer.Sound(os.path.join("assets", "music", "push_button.mp3"))
        self.menu_sound = pygame.mixer.Sound(os.path.join("assets", "music", "menu_button.mp3"))
        
        self.master.title("Tower of Hanoi Visualizer")
        self.master.geometry("900x700")
        self.master.configure(bg="#121212")
        
        # Game state variables
        self.selected_disk = None
        self.selected_tower = None
        self.animation_in_progress = False
        
        self.create_widgets()

    def create_widgets(self):
        # Header with title
        header_frame = tk.Frame(self.master, bg="#121212")
        header_frame.pack(fill="x", pady=10)

        title_label = tk.Label(header_frame, text="TOWER OF HANOI VISUALIZER", 
                            font=("Arial", 24, "bold"), fg="#00ffff", bg="#121212")
        title_label.pack(pady=10)

        # Main content frame
        content_frame = tk.Frame(self.master, bg="#121212", highlightbackground="#00ffff", 
                              highlightthickness=2, padx=10, pady=10)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Canvas for visualization
        self.canvas_height = 400
        self.canvas_width = 800
        self.canvas = tk.Canvas(content_frame, width=self.canvas_width, height=self.canvas_height, 
                             bg="#001428", highlightthickness=0)
        self.canvas.pack(pady=10)
        
        # Bind click events to the canvas for interactive play
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        # Control frame
        control_frame = tk.Frame(content_frame, bg="#121212")
        control_frame.pack(fill="x", pady=10)

        # Number of disks selector
        disk_frame = tk.Frame(control_frame, bg="#121212")
        disk_frame.pack(side="left", padx=20)

        tk.Label(disk_frame, text="Number of Disks:", font=("Arial", 12), 
                fg="white", bg="#121212").pack(side="left")

        self.disk_var = IntVar(value=3)
        disk_options = [3, 4, 5, 6, 7]
        disk_menu = tk.OptionMenu(disk_frame, self.disk_var, *disk_options, command=self.reset)
        disk_menu.config(bg="#003366", fg="white", width=5)
        disk_menu.pack(side="left", padx=10)

        # Speed control
        speed_frame = tk.Frame(control_frame, bg="#121212")
        speed_frame.pack(side="left", padx=20)

        tk.Label(speed_frame, text="Animation Speed:", font=("Arial", 12), 
                fg="white", bg="#121212").pack(side="left")

        self.speed_var = StringVar(value="Medium")
        speed_options = ["Slow", "Medium", "Fast"]
        speed_menu = tk.OptionMenu(speed_frame, self.speed_var, *speed_options)
        speed_menu.config(bg="#003366", fg="white", width=8)
        speed_menu.pack(side="left", padx=10)

        # Buttons frame
        button_frame = tk.Frame(content_frame, bg="#121212")
        button_frame.pack(pady=15)

        self.reset_button = tk.Button(button_frame, text="RESET", bg="#003366", fg="#00ffff",
                                  font=("Arial", 12, "bold"), width=10, command=self.reset)
        self.reset_button.pack(side="left", padx=10)

        self.solve_button = tk.Button(button_frame, text="SOLVE", bg="#003366", fg="#00ffff",
                                  font=("Arial", 12, "bold"), width=10, command=self.solve)
        self.solve_button.pack(side="left", padx=10)

        self.step_button = tk.Button(button_frame, text="STEP", bg="#003366", fg="#00ffff",
                                 font=("Arial", 12, "bold"), width=10, command=self.step)
        self.step_button.pack(side="left", padx=10)

        # Split the lower part into two columns
        lower_frame = tk.Frame(content_frame, bg="#121212")
        lower_frame.pack(fill="x", expand=True)

        # Code display frame with highlighted pseudocode (left column)
        code_frame = tk.Frame(lower_frame, bg="#001428", highlightbackground="#00ffff", 
                           highlightthickness=1, padx=10, pady=10)
        code_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

        code_title = tk.Label(code_frame, text="Recursive Algorithm", font=("Arial", 12, "bold"), 
                           fg="#00ffff", bg="#001428")
        code_title.pack(anchor="w")

        # Pseudocode with syntax highlighting
        self.code_lines = [
            "function hanoi(n, source, auxiliary, target):",
            "    if n == 1:",
            "        move disk 1 from source to target",
            "    else:",
            "        hanoi(n-1, source, target, auxiliary)",
            "        move disk n from source to target",
            "        hanoi(n-1, auxiliary, source, target)"
        ]

        self.code_labels = []
        for line in self.code_lines:
            label = tk.Label(code_frame, text=line, font=("Consolas", 12), 
                         fg="white", bg="#001428", anchor="w")
            label.pack(fill="x", anchor="w")
            self.code_labels.append(label)

        # Instructions (right column)
        instruction_frame = tk.Frame(lower_frame, bg="#001428", highlightbackground="#00ffff", 
                                  highlightthickness=1, padx=10, pady=10)
        instruction_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))

        instruction_title = tk.Label(instruction_frame, text="How to Use", font=("Arial", 12, "bold"), 
                                 fg="#00ffff", bg="#001428")
        instruction_title.pack(anchor="w")

        instructions = tk.Label(instruction_frame, 
                            text="• Select the number of disks using the dropdown\n"
                                 "• Click SOLVE to run the animation automatically\n"
                                 "• Click STEP to execute one move at a time\n"
                                 "• Click RESET to restart with current disk count\n"
                                 "• Click on towers to play manually\n\n"
                                 "The goal is to move all disks from the leftmost peg\n"
                                 "to the rightmost peg, following these rules:\n"
                                 "1. Move only one disk at a time\n"
                                 "2. A larger disk cannot be placed on a smaller disk",
                            font=("Arial", 11), fg="white", bg="#001428", justify="left")
        instructions.pack(anchor="w", padx=10, fill="x")

        # Add back button
        self.back_button = tk.Button(
            self.master,
            text="← Back to Menu",
            font=("Consolas", 12, "bold"),
            bg="#333333",
            fg="white",
            command=lambda: [self.menu_sound.play(), self.go_back()]
        )
        self.back_button.place(x=10, y=10)

        # Initialize variables for animation
        self.disks = []
        self.moves = []
        self.current_move = 0
        self.towers = [[], [], []]  # Represents the three pegs
        self.tower_x = [self.canvas_width/4, self.canvas_width/2, 3*self.canvas_width/4]

        # Initial setup
        self.reset()

    def go_back(self):
        # Clear the current screen
        for widget in self.master.winfo_children():
            widget.destroy()
        # Call the go back callback
        self.go_back_callback(self.master)

    def reset(self, *args):
        """Reset the towers and create new disks"""
        self.canvas.delete("all")
        self.disks = []
        self.moves = []
        self.current_move = 0
        self.animation_in_progress = False
        self.selected_disk = None
        self.selected_tower = None
        self.towers = [[], [], []]

        # Draw towers (pegs)
        base_y = self.canvas_height - 50
        peg_height = 200

        # Draw base
        self.canvas.create_rectangle(100, base_y, self.canvas_width-100, base_y+20, 
                                fill="#8B4513", outline="")

        # Draw pegs
        for x in self.tower_x:
            self.canvas.create_rectangle(x-5, base_y-peg_height, x+5, base_y, 
                                    fill="#8B4513", outline="")

        # Create disks on the first peg
        num_disks = self.disk_var.get()
        max_width = 150
        min_width = 50
        width_step = (max_width - min_width) / (num_disks - 1) if num_disks > 1 else 0
        height = 20

        disk_colors = ["#FF0000", "#FFA500", "#FFFF00", "#00FF00", "#0000FF", "#4B0082", "#8B00FF"]

        for i in range(1, num_disks + 1):
            width = min_width + (i - 1) * width_step if num_disks > 1 else max_width
            disk = {
                "width": width,
                "height": height,
                "color": disk_colors[(i-1) % len(disk_colors)]
            }
            self.disks.append(disk)
            self.towers[0].insert(0, i)  # Insert at beginning to maintain order

        self.draw_towers()

        # Reset code highlighting
        for label in self.code_labels:
            label.config(fg="white")

        # Generate solution moves but don't animate yet
        self.generate_moves(num_disks, 0, 2, 1)

        # Enable buttons
        self.solve_button.config(state="normal")
        self.step_button.config(state="normal")

        # Reset move counter
        self.canvas.delete("move_text")
        self.canvas.create_text(
            self.canvas_width/2, 
            30, 
            text=f"Total Moves Required: {len(self.moves)}",
            fill="#00ffff",
            font=("Arial", 12),
            tags="move_text"
        )

    def draw_towers(self):
        """Draw all disks on their current towers"""
        self.canvas.delete("disk")
        base_y = self.canvas_height - 50

        for tower_idx, tower in enumerate(self.towers):
            for disk_idx, disk_num in enumerate(tower):
                disk = self.disks[disk_num-1]
                x = self.tower_x[tower_idx]
                y = base_y - (disk_idx + 1) * disk["height"]

                self.canvas.create_rectangle(
                    x - disk["width"]/2, 
                    y,
                    x + disk["width"]/2, 
                    y + disk["height"],
                    fill=disk["color"], 
                    outline="black",
                    tags="disk"
                )

                # Add disk number text
                self.canvas.create_text(
                    x, 
                    y + disk["height"]/2,
                    text=str(disk_num),
                    fill="white",
                    font=("Arial", 10, "bold"),
                    tags="disk"
                )

    def generate_moves(self, n, source, target, auxiliary):
        """Generate the sequence of moves using the Tower of Hanoi algorithm"""
        if n == 1:
            self.moves.append((source, target))
            return
        self.generate_moves(n-1, source, auxiliary, target)
        self.moves.append((source, target))
        self.generate_moves(n-1, auxiliary, target, source)

    def highlight_code(self, line_idx):
        """Highlight a specific line of pseudocode"""
        # Reset all lines to white
        for label in self.code_labels:
            label.config(fg="white")

        # Highlight the specified line
        if 0 <= line_idx < len(self.code_labels):
            self.code_labels[line_idx].config(fg="#00ffff")

    def animate_disk_move(self, disk_num, source, target, callback):
        """Animate the disk moving from source to target peg"""
        disk = self.disks[disk_num-1]
        base_y = self.canvas_height - 50
        lift_height = 100  # How high to lift the disk before moving sideways

        # Get current position of the disk
        source_x = self.tower_x[source]
        source_y = base_y - len(self.towers[source]) * disk["height"]

        # Create a temporary disk for animation (we'll move this one)
        disk_id = self.canvas.create_rectangle(
            source_x - disk["width"]/2, 
            source_y,
            source_x + disk["width"]/2, 
            source_y + disk["height"],
            fill=disk["color"], 
            outline="black",
            tags="moving_disk"
        )
        text_id = self.canvas.create_text(
            source_x, 
            source_y + disk["height"]/2,
            text=str(disk_num),
            fill="white",
            font=("Arial", 10, "bold"),
            tags="moving_disk"
        )

        # Animation steps
        steps = 20
        step_delay = 20  # ms between steps

        # Calculate movement paths
        # 1. Lift up
        lift_dy = (source_y - lift_height) / steps

        # 2. Move sideways
        target_x = self.tower_x[target]
        dx = (target_x - source_x) / steps

        # 3. Lower down
        target_stack_height = len(self.towers[target])
        final_y = base_y - (target_stack_height + 1) * disk["height"]
        lower_dy = (final_y - (source_y - lift_height)) / steps

        def lift():
            nonlocal source_y
            if steps_left[0] > 0:
                self.canvas.move(disk_id, 0, -lift_dy)
                self.canvas.move(text_id, 0, -lift_dy)
                source_y -= lift_dy
                steps_left[0] -= 1
                self.master.after(step_delay, lift)
            else:
                steps_left[0] = steps
                move_sideways()

        def move_sideways():
            if steps_left[0] > 0:
                self.canvas.move(disk_id, dx, 0)
                self.canvas.move(text_id, dx, 0)
                steps_left[0] -= 1
                self.master.after(step_delay, move_sideways)
            else:
                steps_left[0] = steps
                lower()

        def lower():
            if steps_left[0] > 0:
                self.canvas.move(disk_id, 0, lower_dy)
                self.canvas.move(text_id, 0, lower_dy)
                steps_left[0] -= 1
                self.master.after(step_delay, lower)
            else:
                self.canvas.delete("moving_disk")
                callback()

        steps_left = [steps]
        lift()

    def step(self):
        """Execute one move of the solution with animation"""
        if self.animation_in_progress or self.current_move >= len(self.moves):
            return

        self.animation_in_progress = True
        source, target = self.moves[self.current_move]

        # Determine which code line to highlight based on the move
        if len(self.towers[source]) == 1:  # Moving the last disk
            self.highlight_code(2)  # Highlight "move disk 1 from source to target"
        else:
            self.highlight_code(5)  # Highlight "move disk n from source to target"

        # Move disk from source to target
        if self.towers[source]:
            disk_num = self.towers[source][-1]  # Get the top disk

            def move_completed():
                # Actually move the disk in our data structure
                self.towers[source].pop()
                self.towers[target].append(disk_num)

                # Update move counter and display
                self.current_move += 1

                # Show move info
                move_text = f"Move {self.current_move}/{len(self.moves)}: Disk {disk_num} from Peg {source+1} to Peg {target+1}"
                self.canvas.delete("move_text")
                self.canvas.create_text(
                    self.canvas_width/2, 
                    30, 
                    text=move_text,
                    fill="#00ffff",
                    font=("Arial", 12),
                    tags="move_text"
                )

                # Redraw towers to ensure everything is clean
                self.draw_towers()

                self.animation_in_progress = False

                # Check if puzzle is solved
                if len(self.towers[2]) == self.disk_var.get():
                    self.win_sound.play()
                    messagebox.showinfo("Success", f"Puzzle solved in {len(self.moves)} moves!")

            # Start the animation
            self.animate_disk_move(disk_num, source, target, move_completed)
        else:
            self.animation_in_progress = False

    def solve(self):
        """Automatically solve the Tower of Hanoi puzzle with animation"""
        self.animation_in_progress = True
        self.solve_button.config(state="disabled")
        self.step_button.config(state="disabled")

        # Set animation speed
        speed = self.speed_var.get()
        if speed == "Slow":
            delay = 1500  # Longer delay for slow speed
        elif speed == "Medium":
            delay = 800   # Medium delay
        else:  # Fast
            delay = 400   # Shorter delay for fast speed

        def execute_next_move():
            if self.current_move < len(self.moves):
                self.step()
                # Adjust the delay based on when the animation completes
                self.master.after(delay, execute_next_move)
            else:
                self.animation_in_progress = False
                self.solve_button.config(state="normal")
                self.step_button.config(state="normal")

        execute_next_move()

    def on_canvas_click(self, event):
        """Handle clicks on the canvas for interactive play"""
        if self.animation_in_progress:
            return
            
        # Check which tower was clicked
        tower_clicked = None
        for i, x in enumerate(self.tower_x):
            if x - 50 < event.x < x + 50:
                tower_clicked = i
                break
                
        if tower_clicked is None:
            return
            
        if self.selected_disk is None:
            # Select a disk to move
            if self.towers[tower_clicked]:
                self.selected_disk = self.towers[tower_clicked][-1]
                self.selected_tower = tower_clicked
                self.highlight_tower(tower_clicked, True)
        else:
            # Try to move the selected disk
            if self.is_valid_move(tower_clicked):
                self.move_disk(self.selected_tower, tower_clicked)
                self.move_sound.play()
            else:
                self.error_sound.play()
                
            # Reset selection
            self.highlight_tower(self.selected_tower, False)
            self.selected_disk = None
            self.selected_tower = None

    def highlight_tower(self, tower_idx, highlight):
        """Highlight a tower to show selection"""
        tag = f"tower_{tower_idx}"
        self.canvas.delete(tag)
        
        if highlight:
            base_y = self.canvas_height - 50
            peg_height = 200
            x = self.tower_x[tower_idx]
            
            self.canvas.create_rectangle(
                x-7, base_y-peg_height, x+7, base_y,
                fill="#00ffff", outline="", tags=tag
            )

    def is_valid_move(self, target_tower):
        """Check if moving to target tower is valid"""
        if not self.towers[target_tower]:
            return True
            
        top_disk_target = self.towers[target_tower][-1]
        return self.selected_disk < top_disk_target

    def move_disk(self, source, target):
        """Move disk from source to target tower"""
        disk_num = self.towers[source].pop()
        
        def move_completed():
            self.towers[target].append(disk_num)
            self.draw_towers()
            
            # Check for win condition
            if len(self.towers[2]) == self.disk_var.get():
                self.win_sound.play()
                messagebox.showinfo("Congratulations!", "You solved the puzzle!")
                self.reset()
                
        self.animate_disk_move(disk_num, source, target, move_completed)