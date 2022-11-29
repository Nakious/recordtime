from config.log import logger
from tkinter import Tk
from views.approot import RootApp
from views.app import WindowsApp

def main():
    logger.info('Started')
    root = RootApp()
    windowApp = WindowsApp(parent=root)
    root.protocol("WM_DELETE_WINDOW", root.on_closing)
    root.mainloop()
    logger.info('Finished')

if __name__ == '__main__':
    main()
    
