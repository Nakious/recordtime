from tkinter import *
from tkinter import ttk
import logging
from views.appadmin import WindowsAppAdmin
from config.bbdd import Database

class WindowsApp(): 
    
    def __init__(self):
        
        self.database = Database()
        self.database.main();
        #self.windowAdmin = WindowsAppAdmin()
        
        self.app=Tk()
        self.app.title("For WMcNeill")
        #photo = PhotoImage(file = "Any image file")
        #self.app.iconphoto(False, photo)
        self.app.geometry("600x200")
        self.app.grid
        self.app.columnconfigure(0,weight=1)
        self.app.columnconfigure(1,weight=1)
        self.app.columnconfigure(2,weight=1)
        self.app.rowconfigure(0, weight=1)
        self.app.rowconfigure(1, weight=1)
        self.app.rowconfigure(2, weight=1)
        self.app.resizable(0,0)
        
        self.window()
            
        self.app.mainloop()

    def window(self):
        
        set_client=self.database.getClient()
        list_client = [r for r, in set_client]
        self.cbClient = ttk.Combobox(self.app, values=list_client,width=15)
        self.cbClient.set('Select a client') 
        self.cbClient.grid(row=0,column=0,padx=10,pady=30)
        self.cbClient.bind("<<ComboboxSelected>>", self.selection_client)
        
        self.windowAdmin = WindowsAppAdmin()
        self.btn = Button(self.app, text = 'ADMIN', command=self.windowAdmin.window)
        self.btn.grid(row=2,column=2,padx=5)  
        
    def selection_client(self, event):
        client = self.cbClient.get()
        set_task=self.database.getTaskClient(client)
        list_task = [r for r, in set_task]
        self.cbTask = ttk.Combobox(self.app, values=list_task,width=15)
        self.cbTask.set('Select a task') 
        self.cbTask.grid(row=0,column=1,padx=10,pady=50)
        #self.cbTask.set(selection) 

            


        

        


