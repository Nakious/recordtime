import tkinter as tk

class RootApp(tk.Tk):
    # def __init__(self) -> None:
    #     super().__init__()
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Time Recording")
        self.resizable(False, False)
        self.attributes('-topmost', 1)
        # self.iconphoto(False, tk.PhotoImage(file="path/file.png")) 
       
    def on_closing(self):
        if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
            #mainApplication.save_time()
            self.destroy()