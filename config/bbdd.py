import os
import sqlite3
from config.log import logger


class Database:
    
    def __init__(self):
        self.db_filename = './config/bbdd.db'
        self.conexionbd = sqlite3.connect(self.db_filename)
    
    def main(self):

        db_is_new = not os.path.exists(self.db_filename)
        cursorbd = self.conexionbd.cursor()

        if db_is_new:
            print('Need to create schema')
            logger.info('Need to create schema')
            cursorbd.execute("CREATE TABLE TASK (ID_TASK INTEGER, NAME_TASK VARCHAR(100), DESCRIPTION VARCHAR(100), ID_CLIENT VARCHAR(50), HIDE INTEGER, ARCHIVE INTEGER)")
            cursorbd.execute("CREATE TABLE CLIENT (ID_CLIENT INTEGER, NAME_CLIENT VARCHAR(50), DESCRIPTION VARCHAR(100),  HIDE INTEGER, ARCHIVE INTEGER)")
            cursorbd.execute("CREATE TABLE TIME (TIME_INI VARCHAR(50), TIME_END VARCHAR(50), DESCRIPTION VARCHAR(100), ID_TASK INTEGER)")
            cursorbd.execute("INSERT INTO TASK VALUES (1, 'task 1', 'ERROR INFORME 1', 1 , 0 , 0 )")
            cursorbd.execute("INSERT INTO TASK VALUES (2, 'task 2', 'ERROR INFORME 2', 2 , 0 , 0 )")
            cursorbd.execute("INSERT INTO TASK VALUES (3, 'task 3', 'ERROR INFORME 3', 3 , 0 , 0 )")
            cursorbd.execute("INSERT INTO TASK VALUES (7, 'task 4', 'ERROR INFORME 4', 4 , 0 , 0 )")
            cursorbd.execute("INSERT INTO CLIENT VALUES (1, 'SAMCA', null , 0 , 0 )")
            cursorbd.execute("INSERT INTO CLIENT VALUES (2, 'DOUGLAS', null, 0 , 0 )")
            cursorbd.execute("INSERT INTO CLIENT VALUES (3, 'COCHES.ES', null, 0 , 0 )")
            cursorbd.execute("INSERT INTO CLIENT VALUES (4, 'SGS', null, 0 , 0 )")
        else:
            print('Database exists.')
            logger.info('Database exists.')
            
        self.conexionbd.commit()
        #self.conexionbd.close()
  
    def getClient(self):
        try:
            queryClient="SELECT NAME_CLIENT AS client FROM CLIENT WHERE HIDE = 0 and ARCHIVE = 0"
            set_client=self.conexionbd.execute(queryClient);
            return set_client
        except sqlite3.Error as error:
            logger.info(error)
            
    def getTaskClient(self, client):
        try:
            queryTask = "SELECT TASK.NAME_TASK || '-' || TASK.DESCRIPTION AS task FROM TASK  \
            inner join CLIENT on CLIENT.ID_CLIENT=TASK.ID_CLIENT \
            WHERE TASK.HIDE = 0 and TASK.ARCHIVE = 0 and CLIENT.NAME_CLIENT = ?"
            set_task=self.conexionbd.execute(queryTask,[client]);
            return set_task
        except sqlite3.Error as error:
            logger.info(error)
        

if __name__ == "__main__":
    app = Database()
    Database.main()

