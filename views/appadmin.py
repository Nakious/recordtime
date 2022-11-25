from tkinter import *
from config.bbdd import Database
from views.appclient import WindowsAppClient
from views.apptask import WindowsAppTask

class WindowsAppAdmin:
    
    def __init__(self):
        self.database = Database()

        
    def window(self):
        
        self.appadmin=Tk()
        self.appadmin.geometry("750x250")
        self.appadmin.title("Admin")
        self.appadmin.columnconfigure(1, weight=3)
        self.appadmin.rowconfigure(1, weight=3)
        self.appadmin.resizable(0,0)
        
        self.windowClient = WindowsAppClient()
        
        self.btn = Button(self.appadmin, text = 'Clients', command=self.windowClient.window)
        self.btn.grid(row=0,column=0,padx=50,pady=50)  
        
        self.windowTask = WindowsAppTask()
        
        self.btn = Button(self.appadmin, text = 'Tasks', command=self.windowTask.window)
        self.btn.grid(row=0,column=1,padx=50,pady=50)  
        
        self.appadmin.mainloop()




        
