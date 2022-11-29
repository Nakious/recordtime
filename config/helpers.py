import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def tkinterLayout1(self):
        # Setup base frame
        self.frame.pack()

        ### Style ###
        # Setup style
        style = ttk.Style()

        # Set style to default
        style.theme_use("default")

        # Altenrative style code to enhance or over-write the default
        # style.configure("Treeview",
        #         background="#D3D3D3",
        #         foreground="black",
        #         rowheight=25,
        #         fieldbackground="#D3D3D3")

        # Sets the selected item colour
        style.map("Treeview", background=[('selected', 'blue')])

        ### Frames ###
        # Define packing options
        self.frame_pack_options = {'borderwidth' : 2, 'relief' : 'sunken', 'padx': 5, 'pady': 5}
        self.widget_options = {'padx': 2, 'pady': 2}

        # Create frame(s)
        self.left_frame = tk.Frame(self.frame, **self.frame_pack_options, background="grey")
        self.left_frame.pack(fill="both", side="left")
        self.right_frame = tk.Frame(self.frame, **self.frame_pack_options, background="grey")
        self.right_frame.pack(fill="both", side="right")

        self.frame_left_1 = tk.Frame(self.left_frame, **self.frame_pack_options)
        self.frame_right_1 = tk.Frame(self.right_frame, **self.frame_pack_options)
        self.frame_right_2 = tk.Frame(self.right_frame, **self.frame_pack_options)
        self.frame_right_3 = tk.Frame(self.right_frame, **self.frame_pack_options)
        self.frame_left_1.pack(side="left", fill="both", expand=True)
        self.frame_right_1.pack(side="left", fill="both", expand=True)
        self.frame_right_2.pack(side="left", fill="both", expand=True)
        self.frame_right_3.pack(side="left", fill="both", expand=True)