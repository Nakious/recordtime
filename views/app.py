import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import logging
from views.appclient import WindowsAppClient
from views.apptask import WindowsAppTask
from config.bbdd import Database
import config.helpers as helper

class WindowsApp:
    def __init__(self, parent):
        
        self.database = Database()
        self.database.main();
        
        self.parent = parent
        self.initVar()
        self.initUI()
        print(self.parent)
        
    def initVar(self):
        #Variables
        self.hours = 0
        self.minutes = 0
        self.seconds = 0
        self.running = False
        self.current_client = None
        self.current_task = None
        self.update_time = None
        self.clients = [r for r, in self.database.getClients()]
        self.tasks = [row[1] for row in self.database.getTask()]
        
        self.tmt = 0
        
        # Windows and status
        self.clients_window = None
        self.clients_window_status = 0
        self.tasks_window = None
        self.tasks_window_status = 0

    def initUI(self):               
        # Create a 'file' menu item.
        self.my_menu = tk.Menu(self.parent)
        self.parent.config(menu=self.my_menu)
        self.file_menu = tk.Menu(self.my_menu, tearoff=0)
        self.my_menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Refresh", command=None)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="About", command=None)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=None)
        
        # Create an 'edit' menu item.
        self.edit_menu = tk.Menu(self.my_menu, tearoff=0)
        self.my_menu.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Clients", command=self.open_clients_window)
        self.edit_menu.add_command(label="Tasks", command=self.open_tasks_window)
        self.edit_menu.add_command(label="Note Types", command=None)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Settings", command=None)
        
        # Create an 'task filter' menu item.
        self.task_filter_menu = tk.Menu(self.my_menu, tearoff=0)
        self.my_menu.add_cascade(label="Task Filters", menu=self.task_filter_menu)
        self.task_filter_menu.add_command(label="Apply Filters", command=None)
        self.task_filter_menu.add_command(label="Remove Filters", command=None)
        self.task_filter_menu.add_separator()
        self.task_filter_menu.add_command(label="Edit Filters", command=None)
        
        # Create an 'backup' menu item.
        self.backup_menu = tk.Menu(self.my_menu, tearoff=0)
        self.my_menu.add_cascade(label="Backup", menu=self.backup_menu)
        self.backup_menu.add_command(label="Take Backup", command=None)
        self.backup_menu.add_command(label="Restore Backup", command=None)

        # Create and setup frames.
        self.frame1 = tk.Frame(self.parent, relief="raised", borderwidth=1)
        self.frame1.pack()
        
        self.frame2 = tk.Frame(self.parent, relief="raised", borderwidth=1)
        self.frame2.pack()
        
        self.frame3 = tk.Frame(self.parent, relief="raised", borderwidth=1)
        self.frame3.pack()
        
        self.frame4 = tk.Frame(self.parent, relief="raised", borderwidth=1)
        self.frame4.pack()
        
        self.frame_buttons = tk.Frame(self.parent, relief="raised", borderwidth=1)
        self.frame_buttons.pack()
        
        # Create the widgets for the frame
        # Client
        self.current_lbl = tk.Label(self.frame1, text="Select a Client", width=13, font=("arial",11))
        self.client_combo = ttk.Combobox(self.frame1, value=self.clients)
        #self.client_combo.bind("<<ComboboxSelected>>", self.client_select)
        
        # Task
        self.tasks_lbl= tk.Label(self.frame2, text="Select a Task", width=13, font=("arial",11))
        self.task_combo = ttk.Combobox(self.frame2, value=self.tasks)
        #self.task_combo.bind("<<ComboboxSelected>>", self.task_select)
        
        # Stopwatch
        self.stopwatch_lbl = tk.Label(self.frame4, text='00:00:00', font=('Arial', 11))
        self.stopwatch_state_lbl = tk.Label(self.frame4, text="IDLE", font=('Arial', 11))
        
        # Additional time
        self.tasks_tmt_lbl = tk.Label(self.frame3, text=f"Task Min_Time: {self.tmt}", font=("arial",9))
        self.default_mt_lbl = tk.Label(self.frame3, text="Default Min_Time: ", font=("arial",9))
        
        # Buttons
        self.start_button = tk.Button(self.frame_buttons, text='Start', height=1, width=5, font=('Arial', 11), command=None)
        self.save_button = tk.Button(self.frame_buttons, text='Save', height=1, width=5, font=('Arial', 11), command=None)
        self.add_notes_button = tk.Button(self.frame_buttons, text='Notes', height=1, width=5, font=('Arial', 11), command=None)
        self.cancel_button = tk.Button(self.frame_buttons, text='Cancel', height=1, width=5, font=('Arial', 11), command=None)
        
        # Layout the widgets in the frame
        # Client
        self.current_lbl.pack(side="left")
        self.client_combo.pack(side="left")
        
        # Task
        self.tasks_lbl.pack(side="left")
        self.task_combo.pack(side="left")
        
        # Default time
        self.tasks_tmt_lbl.pack(side="right")
        self.default_mt_lbl.pack(side="right")
                
        # Stopwatch
        self.stopwatch_lbl.pack(side="left")
        self.stopwatch_state_lbl.pack(side="left")
        
        # Buttons
        self.start_button.pack(side="left", padx=5)
        self.save_button.pack(side="left", padx=5)
        self.add_notes_button.pack(side="left", padx=5)
        self.cancel_button.pack(side="left", padx=5)


    def open_clients_window(self):
        
        def update_clients_window_status():
            self.clients_window_status = 0
            
        if self.clients_window_status == 0:
            self.clients_window_status = 1
            self.clients_window = WindowsAppClient(update_window_status=update_clients_window_status)
            
    def open_tasks_window(self):
        
        def update_tasks_window_status():
            self.tasks_window_status = 0
            
        if self.tasks_window_status == 0:
            self.tasks_window_status = 1
            self.tasks_window = WindowsAppTask(update_window_status=update_tasks_window_status)
    
    #     set_client=self.database.getClients(config=None)
    #     list_client = [r for r, in set_client]
    #     self.cbClient = ttk.Combobox(self.app, values=list_client,width=20)
    #     self.cbClient.set('Select a client') 

    #     self.cbClient.bind("<<ComboboxSelected>>", self.selection_client)
    #     set_task=self.database.getTask(client=None)
    #     list_task = [r for r, in set_task]
    #     self.cbTask = ttk.Combobox(self.app, values=list_task,width=20)
    #     self.cbTask.set('Select a task') 
        
   
    # def selection_client(self, event):
    #     client = self.cbClient.get()
    #     set_task=self.database.getTask(client)
    #     list_task = [r for r, in set_task]
    #     self.cbTask = ttk.Combobox(self.app, values=list_task,width=20)
    #     self.cbTask.set('Select a task') 
    #     self.cbTask.grid(row=0,column=1)
    #     #self.cbTask.set(selection) 

