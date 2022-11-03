from config.log import logger
from views.app import WindowsApp

class MainAPP:
    def main(self):
        logger.info('Started')
        self.windowApp = WindowsApp()
        logger.info('Finished')

if __name__ == '__main__':
    mainApp = MainAPP()
    mainApp.main()
    
