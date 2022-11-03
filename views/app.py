from tkinter import *
import logging
from views.appadmin import WindowsAppAdmin
from config.bbdd import Database

class WindowsApp(): 
    
    def __init__(self):
        
        self.database = Database()
        self.database.main();
        self.windowAdmin = WindowsAppAdmin()
        
        self.app=Tk()
        self.app.title("For WMcNeill")
        self.app.geometry("500x200")
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
        
        #list_client = ['Select a client']
        set_client=self.database.getClient()
        list_client = [r for r, in set_client]
        optionsClient = StringVar(self.app)
        optionsClient.set('Select a client')
        omClient=OptionMenu(self.app,  optionsClient, *list_client)
        omClient.grid(row=0,column=0,padx=5)
        

        self.btn = Button(self.app, text = 'ADMIN', command=self.windowAdmin.window)
        self.btn.grid(row=2,column=2,padx=5)  
        
        #self.database.conexionbd.close()
        
        set_task=self.database.getTaskClient()
        list_task = [r for r, in set_task]
        optionsTask = StringVar(self.app)
        optionsTask.set('Select a task')
        omTask=OptionMenu(self.app, optionsTask, *list_task)
        omTask.grid(row=0,column=1,padx=5,pady=5)
        

        

        


