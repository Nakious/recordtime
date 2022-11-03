from tkinter import *
import logging
from config.bbdd import Database

class WindowsAppAdmin:
    
    def __init__(self):
        self.database = Database()
        
    def window(self):
        
        appadmin=Tk()
        appadmin.geometry("750x250")
        appadmin.title("Admin")
        appadmin.columnconfigure(1, weight=3)
        appadmin.rowconfigure(1, weight=3)
        appadmin.resizable(0,0)
        Label(appadmin, text="Hey, Howdy?", font=('Helvetica 17 bold')).pack(pady=30)
        

        appadmin.mainloop()



        
