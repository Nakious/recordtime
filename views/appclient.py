from tkinter import *
from config.bbdd import Database

class WindowsAppClient:
    
    def __init__(self):
        self.database = Database()

        
    def window(self):
        
        self.appadmin=Tk()
        self.appadmin.geometry("750x250")
        self.appadmin.title("Client")
        self.appadmin.columnconfigure(1, weight=3)
        self.appadmin.rowconfigure(1, weight=3)
        self.appadmin.resizable(0,0)
        
        self.appadmin.mainloop()


        




        
