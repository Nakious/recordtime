from tkinter import *
from tkinter import ttk
from config.bbdd import Database
from config.log import logger
from tkinter import messagebox


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
        self.tree.heading('CLIENT', text="CLIENTS", anchor=W)
        self.tree.column('#0', stretch=NO, minwidth=0, width=0)
        self.tree.column('#1', stretch=NO, minwidth=0, width=200)
        self.tree.pack(side=BOTTOM)
        fetch=self.database.getClients(config=1,client=None)
        for data in fetch:
            self.tree.insert('', 'end', values=data)
            self.tree.bind("<Double-1>", self.OnDoubleClick)

        
        self.labelName = Label( self.appclient, text = "Name :")
        self.labelName.pack()
        self.labelName.place(x=230,y=30)
        self.entryName = Entry(self.appclient)
        self.entryName.pack(side=LEFT)
        self.entryName.place(x=310,y=30)
        
        self.labelDescripcion = Label( self.appclient, text = "Description :")
        self.labelDescripcion.pack()
        self.labelDescripcion.place(x=230,y=60)
        self.entryDescription = Entry(self.appclient )
        self.entryDescription.pack()
        self.entryDescription.place(x=330,y=60)

        self.labelHide = Label( self.appclient, text = "Hide :")
        self.labelHide.pack()
        self.labelHide.place(x=230,y=90)
        self.varRadioHide = IntVar()
        self.radioHide = Checkbutton(self.appclient, variable=self.varRadioHide)
        self.radioHide.pack()
        self.radioHide.place(x=330,y=90)
        
        self.btnedit = Button(self.appclient, text = 'EDIT CLIENT', command=self.editField, state=DISABLED)
        self.btnedit.pack()
        self.btnedit.place(x=250,y=150)
        
        self.btnsave = Button(self.appclient, text = 'SAVE CLIENT', command=self.updateClient, state=DISABLED)
        self.btnsave.pack()
        self.btnsave.place(x=350,y=150)
        
        self.btndelete = Button(self.appclient, text = 'DELETE CLIENT', command=self.deleteClient, state=DISABLED, bg='#C80000', fg='white')
        self.btndelete.pack()
        self.btndelete.place(x=250,y=200)
        
        self.btncreate = Button(self.appclient, text = 'CREATE NEW CLIENT', command=self.createClient, bg='blue', fg='white')
        self.btncreate.pack()
        self.btncreate.place(x=350,y=200)
        
        self.btnadd = Button(self.appclient, text = 'ADD NEW CLIENT', command=self.addClient, bg='blue', fg='white')

        
        self.appclient.mainloop()


    def OnDoubleClick(self, event):     
        self.cleanFields()
        item = self.tree.selection()
        for i in item:
            client = self.database.getClients(self.tree.item(i, "values")[0], config=2)
            for data in client:
                self.entryName.insert(0, data[1])
                self.entryName.configure(state=DISABLED)
                self.entryDescription.insert(0,data[2])
                self.entryDescription.configure(state=DISABLED)
                if data[3]==0:
                    self.radioHide.deselect()
                else:
                    self.radioHide.select()
                self.radioHide.configure(state=DISABLED)
        self.btnedit.configure(state=NORMAL)
        self.btndelete.configure(state=NORMAL)
        self.btnadd.pack()
        self.btnadd.place(x=350,y=200)
        self.btncreate.pack_forget()
        self.btncreate.destroy()


    def deleteClient(self):
        item = self.tree.selection()
        for i in item:
            self.database.deleteClient(self.tree.item(i, "values")[0])
        self.refresh()
  
    def updateClient(self):
        newNameClient = self.entryName.get()
        newDescriptionClient = self.entryDescription.get()
        newHideClient =  self.varRadioHide.get()#NOT WORKING
        item = self.tree.selection()
        for i in item:
            print("ID CLIENTE:",self.tree.item(i, "values")[1])
            idCLient = self.tree.item(i, "values")[1]
        print(idCLient,newNameClient,newDescriptionClient,newHideClient)
        self.database.updateClient(idCLient,newNameClient,newDescriptionClient,newHideClient)
        self.refresh()
        
    def cleanFields(self):
        self.entryName.configure(state=NORMAL)
        self.entryName.delete(0, END)
        self.entryDescription.configure(state=NORMAL)
        self.entryDescription.delete(0, END)
        self.radioHide.configure(state=NORMAL)
    
    def editField(self):
        self.btnsave.configure(state=NORMAL)
        self.entryName.configure(state=NORMAL)
        self.entryDescription.configure(state=NORMAL)
        self.radioHide.configure(state=NORMAL)
        self.btnedit.configure(state=DISABLED)
    
    def createClient(self):
        newNameClient = self.entryName.get()
        newDescriptionClient = self.entryDescription.get()
        newHideClient = self.varRadioHide.get()
        answer = messagebox.askokcancel(title='Confirmation', message='Are you sure to create a client '+newNameClient+' ?', icon="info")
        if answer:
            self.database.createClient(newNameClient,newDescriptionClient,newHideClient)
            self.refresh()
    
    def addClient(self):
        self.entryName.configure(state=NORMAL)
        self.entryName.delete(0, END)
        self.entryDescription.configure(state=NORMAL)
        self.entryDescription.delete(0, END)
        self.radioHide.configure(state=NORMAL)
        self.radioHide.deselect()
        self.btncreate = Button(self.appclient, text = 'CREATE NEW CLIENT', command=self.createClient, bg='blue', fg='white')
        self.btncreate.pack()
        self.btncreate.place(x=350,y=200)
        self.btnadd.pack_forget()
        self.btnadd.destroy()
        self.btnedit.configure(state=DISABLED)
        self.btndelete.configure(state=DISABLED)
        self.btnsave.configure(state=DISABLED)
        
    def refresh(self):
        self.appclient.destroy()
        self.__init__()
        self.window()
    


        




        
