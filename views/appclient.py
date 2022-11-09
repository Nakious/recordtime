from tkinter import *
from tkinter import ttk
from config.bbdd import Database
from config.log import logger


class WindowsAppClient:
    
    def __init__(self):
        self.database = Database()
        self.database.main();

        
    def window(self):
        
        self.appclient=Tk()

      
        self.appclient.title("Clients")
        screen_width = self.appclient.winfo_screenwidth()
        screen_height = self.appclient.winfo_screenheight()
        width = 500
        height = 300
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.appclient.geometry('%dx%d' % (width, height))
        self.appclient.columnconfigure(0,weight=1)
        self.appclient.columnconfigure(1,weight=1)
        self.appclient.columnconfigure(2,weight=1)
        self.appclient.columnconfigure(3,weight=1)
        self.appclient.rowconfigure(0, weight=1)
        self.appclient.rowconfigure(1, weight=1)
        self.appclient.rowconfigure(2, weight=1)
        self.appclient.rowconfigure(3, weight=1)
        #self.appclient.resizable(0,0)

        self.listclient = Listbox(self.appclient)
        self.listclient.pack(side=LEFT)
        
        scrollbary = Scrollbar(self.listclient, orient=VERTICAL)
        scrollbarx = Scrollbar(self.listclient, orient=HORIZONTAL)
        
        self.tree = ttk.Treeview(self.listclient, columns=( "CLIENT"), selectmode="extended", height=300, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        scrollbary.config(command=self.tree.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.config(command=self.tree.xview)
        scrollbarx.pack(side=BOTTOM, fill=X)
        self.tree.heading('CLIENT', text="CLIENT", anchor=W)
        self.tree.column('#0', stretch=NO, minwidth=0, width=0)
        self.tree.column('#1', stretch=NO, minwidth=0, width=200)
        self.tree.pack(side=BOTTOM)
        fetch=self.database.getClients(config=1)
        for data in fetch:
            self.tree.insert('', 'end', values=(data))
            self.tree.bind("<Double-1>", self.OnDoubleClick)

        
        self.labelName = Label( self.appclient, text = "Client Name :")
        self.labelName.pack()
        self.labelName.place(x=250,y=30)
        self.b = Entry(self.appclient)
        self.b.insert(0, "")
        self.b.pack(side=LEFT)
        self.b.place(x=350,y=30)
        
        self.labelDescripcion = Label( self.appclient, text = "Client Description :")
        self.labelDescripcion.pack()
        self.labelDescripcion.place(x=250,y=60)
        self.c = Entry(self.appclient)
        self.c.insert(0, "")
        self.c.pack()
        self.c.place(x=360,y=60)

        self.labelHide = Label( self.appclient, text = "Hide Client :")
        self.labelHide.pack()
        self.labelHide.place(x=250,y=90)
        self.radioHide = Checkbutton(self.appclient)
        self.radioHide.pack()
        self.radioHide.place(x=350,y=90)
        
        self.btn = Button(self.appclient, text = 'DELETE CLIENT', command=self.deleteClient)
        self.btn.pack()
        self.btn.place(x=300,y=120)

        self.appclient.mainloop()


    def OnDoubleClick(self, event):
        item = self.tree.selection()
        for i in item:
            print("you clicked on", self.tree.item(i, "values")[0])
            
    def deleteClient(self):
        item = self.tree.selection()
        for i in item:
            print("you clicked on", self.tree.item(i, "values")[0])
            self.database.deleteClients(self.tree.item(i, "values")[0])
    
    
    


        




        
