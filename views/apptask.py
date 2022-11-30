from tkinter import *
from tkinter import ttk
from config.bbdd import Database
from config.log import logger
from tkinter import messagebox


class WindowsAppTask:
    
    def __init__(self):
        self.database = Database()
        self.database.main();

        
    def window(self):

        self.apptask=Tk()
      
        self.apptask.title("Tasks")
        screen_width = self.apptask.winfo_screenwidth()
        screen_height = self.apptask.winfo_screenheight()
        width = 600
        height = 300
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.apptask.geometry('%dx%d' % (width, height))
        self.apptask.columnconfigure(0,weight=1)
        self.apptask.columnconfigure(1,weight=1)
        self.apptask.columnconfigure(2,weight=1)
        self.apptask.columnconfigure(3,weight=1)
        self.apptask.rowconfigure(0, weight=1)
        self.apptask.rowconfigure(1, weight=1)
        self.apptask.rowconfigure(2, weight=1)
        self.apptask.rowconfigure(3, weight=1)

        self.listtask = Listbox(self.apptask)
        self.listtask.pack(side=LEFT)
        
        scrollbary = Scrollbar(self.listtask, orient=VERTICAL)
        scrollbarx = Scrollbar(self.listtask, orient=HORIZONTAL)
        
        self.tree = ttk.Treeview(self.listtask, columns=( "task"), selectmode="extended", height=300, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        scrollbary.config(command=self.tree.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.config(command=self.tree.xview)
        scrollbarx.pack(side=BOTTOM, fill=X)
        self.tree.heading('task', text="TASKS", anchor=W)
        self.tree.column('#0', stretch=NO, minwidth=0, width=0)
        self.tree.column('#1', stretch=NO, minwidth=0, width=200)
        self.tree.pack(side=BOTTOM)
        fetch=self.database.getTasks(task=None, config=1)
        for data in fetch:
            self.tree.insert('', 'end', values=data)
            self.tree.bind("<Double-1>", self.OnDoubleClick)

        
        self.labelName = Label( self.apptask, text = "Name :")
        self.labelName.pack()
        self.labelName.place(x=250,y=30)
        self.entryName = Entry(self.apptask)
        self.entryName.pack(side=LEFT)
        self.entryName.place(x=350,y=30)
        
        self.labelDescripcion = Label( self.apptask, text = "Description :")
        self.labelDescripcion.pack()
        self.labelDescripcion.place(x=250,y=60)
        self.entryDescription = Entry(self.apptask)
        self.entryDescription.pack()
        self.entryDescription.place(x=350,y=60)

        self.labelDefault = Label( self.apptask, text = "Default  ")
        self.labelDefault.pack()
        self.labelDefault.place(x=250,y=90)
        self.varRadioDefault = IntVar()
        self.radioDefault = Checkbutton(self.apptask, variable=self.varRadioDefault)
        self.radioDefault.pack()
        self.radioDefault.place(x=350,y=90)
        
        self.labelHide = Label( self.apptask, text = "Hide :")
        self.labelHide.pack()
        self.labelHide.place(x=250,y=120)
        self.varRadioHide = IntVar()
        self.radioHide = Checkbutton(self.apptask, variable=self.varRadioHide)
        self.radioHide.pack()
        self.radioHide.place(x=350,y=120)
        
        self.labeClient = Label( self.apptask, text = "Client :")
        self.labeClient.pack()
        self.labeClient.place(x=250,y=150)
        set_client=self.database.getClients(client=None, config=2)
        list_client = [r for r, in set_client]
        self.cbClient = ttk.Combobox(self.apptask, values=list_client,width=20)
        self.cbClient.pack()
        self.cbClient.place(x=350,y=150)
        
        self.btnedit = Button(self.apptask, text = 'EDIT TASK', command=self.editField, state=DISABLED)
        self.btnedit.pack()
        self.btnedit.place(x=250,y=180)
        
        self.btnsave = Button(self.apptask, text = 'SAVE TASK', command=self.updatetask, state=DISABLED)
        self.btnsave.pack()
        self.btnsave.place(x=350,y=180)
        
        self.btndelete = Button(self.apptask, text = 'DELETE TASK', command=self.deletetask, state=DISABLED, bg='#C80000', fg='white')
        self.btndelete.pack()
        self.btndelete.place(x=250,y=230)
        
        self.btncreate = Button(self.apptask, text = 'CREATE NEW TASK', command=self.createtask, bg='blue', fg='white')
        self.btncreate.pack()
        self.btncreate.place(x=350,y=230)
        
        self.btnadd = Button(self.apptask, text = 'ADD TASK', command=self.addtask, bg='blue', fg='white')

        self.apptask.mainloop()


    def OnDoubleClick(self, event):
        self.cleanFields()
        item = self.tree.selection()
        for i in item:
            task = self.database.getTasks(self.tree.item(i, "values")[0],config=None)
            for data in task:
                self.entryName.insert(0, data[1])
                self.entryName.configure(state=DISABLED)
                self.entryDescription.insert(0,data[2])
                self.entryDescription.configure(state=DISABLED)
                if data[3]==0:
                    self.radioDefault.deselect()
                else:
                    self.radioDefault.select()
                if data[4]==0:
                    self.radioHide.deselect()
                else:
                    self.radioHide.select()
                self.radioDefault.configure(state=DISABLED)
                self.radioHide.configure(state=DISABLED)
                client = self.database.getClients(data[6], config=3)
                for dataclient in client:
                    self.cbClient.set(dataclient[0])
                self.cbClient.configure(state=DISABLED)
        self.btnedit.configure(state=NORMAL)
        self.btndelete.configure(state=NORMAL)
        self.btnadd.pack()
        self.btnadd.place(x=350,y=230)
        self.btncreate.pack_forget()
        self.btncreate.destroy()



    def deletetask(self):
        item = self.tree.selection()
        for i in item:
            self.database.deleteTask(self.tree.item(i, "values")[0])
        self.refresh()
  
    def updatetask(self):
        newNametask = self.entryName.get()
        newDescriptiontask = self.entryDescription.get()
        newDefaulttask =  self.varRadioDefault.get()
        newHidetask =  self.varRadioHide.get()
        client = self.database.getClients(self.cbClient.get(), config=2)
        for data in client:
            NewClientTask=data[0]
        item = self.tree.selection()
        for i in item:
            print("ID task:",self.tree.item(i, "values")[1])
            idtask = self.tree.item(i, "values")[1]
        print(idtask,newNametask,newDescriptiontask,newHidetask)
        self.database.updateTask(idtask,newNametask,newDescriptiontask,newHidetask,newDefaulttask,NewClientTask)
        self.refresh()
        
    def cleanFields(self):
        self.entryName.configure(state=NORMAL)
        self.entryName.delete(0, END)
        self.entryDescription.configure(state=NORMAL)
        self.entryDescription.delete(0, END)
        self.radioHide.configure(state=NORMAL)
        self.radioDefault.configure(state=NORMAL)
        self.cbClient.set('Select a client') 
        self.cbClient.configure(state=NORMAL)

    def editField(self):
        self.btnsave.configure(state=NORMAL)
        self.entryName.configure(state=NORMAL)
        self.entryDescription.configure(state=NORMAL)
        self.radioHide.configure(state=NORMAL)
        self.radioDefault.configure(state=NORMAL)
        self.cbClient.configure(state=NORMAL)
        self.btnedit.configure(state=DISABLED)
    
    def createtask(self):
        newNametask = self.entryName.get()
        newDescriptiontask = self.entryDescription.get()
        newHidetask =  self.varRadioHide.get()
        newDefaulttask=  self.varRadioDefault.get()
        client = self.database.getClients(self.cbClient.get(), config=2)
        print(client)
        for dataclient in client:
            newClientTask = self.cbClient.set(dataclient[0])
        self.database.createTask(newNametask,newDescriptiontask,newHidetask,newDefaulttask,newClientTask)
        self.refresh()
    
    def addtask(self):
        self.entryName.configure(state=NORMAL)
        self.entryName.delete(0, END)
        self.entryDescription.configure(state=NORMAL)
        self.entryDescription.delete(0, END)
        self.radioHide.configure(state=NORMAL)
        self.radioDefault.configure(state=NORMAL)
        self.radioHide.deselect()
        self.radioDefault.deselect()
        self.btncreate = Button(self.apptask, text = 'CREATE NEW TASK', command=self.createtask, bg='blue', fg='white')
        self.btncreate.pack()
        self.btncreate.place(x=350,y=230)
        self.btnadd.pack_forget()
        self.btnadd.destroy()
        self.btnedit.configure(state=DISABLED)
        self.btndelete.configure(state=DISABLED)
        self.btnsave.configure(state=DISABLED)

    def refresh(self):
        self.apptask.destroy()
        self.__init__()
        self.window()
    


        




        
