import tkinter as tk
from tkinter import ttk
from config.bbdd import Database
from config.log import logger
from tkinter import messagebox
import config.helpers as trh


class WindowsAppClient:
    
    def __init__(self, update_window_status):
        self.update_window_status = update_window_status
        
        self.database = Database()
        self.database.main();
        
        self.top = tk.Toplevel()
        self.frame = tk.Frame(self.top)
        self.top.title("Clients")
        self.top.attributes('-topmost', 1)
        #self.parent = parent
        self.top.protocol("WM_DELETE_WINDOW", self.closeWindow)
        self.initVar()
        self.initUI()
        self.refresh()
    
    def initVar(self):
        self.currentTreeSelection = ""
            
    def initUI(self):
        # Setup frame using a blueprint layout
        trh.tkinterLayout1(self=self)
        
        # Tree setup
        # Create the scrollbars
        scrollbary = tk.Scrollbar(self.frame_left_1)
        scrollbary.pack(side="right", fill="y")
        scrollbarx = tk.Scrollbar(self.frame_left_1, orient='horizontal')
        scrollbarx.pack(side="bottom", fill="x")

        # Create the tree widget and assign scrollbars
        self.tree = ttk.Treeview(self.frame_left_1, show='headings', yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        self.tree.bind('<<TreeviewSelect>>', self.select)

        # Set the scrollbar commands
        scrollbary.config(command=self.tree.yview)
        scrollbarx.config(command=self.tree.xview)
        
        # Define tree colums
        self.tree['columns'] = ("CLIENT")

        # Setup tree columns
        self.tree.column("#0", width=0, stretch="no")
        self.tree.column("CLIENT", anchor="w", width=140)
        
        self.tree.heading('#0', text="Label")
        self.tree.heading('CLIENT', text="CLIENT", anchor="w")
        
        self.tree.tag_configure('oddrow', background="white")
        self.tree.tag_configure('evenrow', background="lightblue")

        # Create widgets
        self.labelName = tk.Label(self.frame_right_1, text = "Client Name :")
        self.entryName = tk.Entry(self.frame_right_2)
        self.labelDescripcion = tk.Label(self.frame_right_1, text = "Client Description :")
        self.entryDescription = tk.Entry(self.frame_right_2)
        self.labelHide = tk.Label( self.frame_right_1, text = "Hide Client :")
        self.varRadioHide = tk.IntVar()
        self.radioHide = tk.Checkbutton(self.frame_right_2, variable=self.varRadioHide)
        
        self.btnclear = tk.Button(self.frame_right_3, text = 'CLEAR', command=self.refresh)
        self.btncreate = tk.Button(self.frame_right_3, text = 'CREATE CLIENT', command=self.create)
        self.btnsave = tk.Button(self.frame_right_3, text = 'UPDATE CLIENT', command=self.update)
        self.btndelete = tk.Button(self.frame_right_3, text = 'DELETE CLIENT', command=self.delete, bg='#C80000', fg='white')

        # Pack widgets
        self.tree.pack(**self.widget_options)
        
        self.labelName.pack(**self.widget_options)
        self.entryName.pack(**self.widget_options)
        self.labelDescripcion.pack(**self.widget_options)
        self.entryDescription.pack(**self.widget_options)
        self.labelHide.pack(**self.widget_options)
        self.radioHide.pack(**self.widget_options)
        
        self.btnclear.pack(**self.widget_options)
        self.btncreate.pack(**self.widget_options)
        self.btnsave.pack(**self.widget_options)
        self.btndelete.pack(**self.widget_options)
            

    def select(self, event):
        self.cleanFields()
        
        select = self.tree.selection()
        
        if self.deselectCheck():
            self.tree.selection_remove(select)
            return
        else:
            self.currentTreeSelection = select
            self.updateFormInfo(select)

    def deselectCheck(self):
        if self.currentTreeSelection == self.tree.selection(): return True
        
    def create(self):
        data = self.getFormInfo()
        
        if not self.createChecks(data["name"]):
            self.database.createClient(data["name"],data["description"],data["hide_status"])
            self.refresh()
            
    def update(self):
        data = self.getFormInfo()
        
        if not self.checkItemExists(data["name"]):
            messagebox.showerror("Error", "The client does not exist.")
            return
        else:
            self.database.updateClient(data["id"],data["name"],data["description"],data["hide_status"])
            self.refresh()

    def delete(self):
        item = self.tree.selection()
        for i in item:
            self.database.deleteClient(self.tree.item(i, "values")[0])
        self.refresh()
        
    def closeWindow(self):
        self.update_window_status()
        self.top.destroy()


    def refresh(self):
        self.updateTree()
        self.cleanFields()
    
    def cleanFields(self):
        self.entryName.delete(0, tk.END)
        self.entryDescription.delete(0, tk.END)
    
    def updateTree(self):
        self.tree.delete(*self.tree.get_children())
        
        fetch=self.database.getClients(config=1)
        
        self.count = 0
        for data in fetch:
            if self.count % 2 == 0:
                self.tree.insert('', 'end', values=data, tags=("evenrow", ))
            else:
                self.tree.insert('', 'end', values=data, tags=("oddrow", ))
            self.count += 1
    
    def getFormInfo(self):
        if self.tree.selection != "":
            id = self.getID(select=self.tree.selection())
        else:
            id = None
            
        dict = {"id" : id,
                "name" : self.entryName.get(),
                "description" : self.entryDescription.get(),
                "hide_status" : self.varRadioHide.get()}
        return dict
    
    def updateFormInfo(self, select):
        for i in select:
            fetch = self.database.getClient(self.tree.item(i, "values")[0])
            for data in fetch:
                self.entryName.insert(0, data[1])
                self.entryDescription.insert(0,data[2])
                if data[3]==0:
                    self.radioHide.deselect()
                else:
                    self.radioHide.select()
    
    def createChecks(self, item):
        if self.checkBlankName(item): 
            messagebox.showerror("Error", "The name cannot be blank.")
            return True
        if self.checkItemExists(item): 
            messagebox.showerror("Error", "The name already exists.")
            return True

    def checkBlankName(self, items):
        if items == "":
            return True
        
    def checkItemExists(self, item):
        fetch=self.database.getClients(config=1)
        
        for data in fetch:
            if item == data[0]:
                return True
        else: 
            return False
            
    def getID(self, select):
        for i in select:
            return self.tree.item(i, "values")[1]
        
        