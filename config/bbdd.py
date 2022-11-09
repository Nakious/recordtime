import os
import sqlite3
from config.log import logger


class Database:
    
    def __init__(self):
        self.db_filename = './config/bbdd.db'
    
    def main(self):

        db_is_new = not os.path.exists(self.db_filename)
        self.conexionbd = sqlite3.connect(self.db_filename)

        if db_is_new:
            print('Need to create schema')
            logger.info('Need to create schema')
            cursorbd = self.conexionbd.cursor()
            cursorbd.execute("CREATE TABLE TASKS (ID_TASK INTEGER, NAME_TASK VARCHAR(100), DESCRIPTION VARCHAR(100), DEFAULT_TASK INTEGER, ID_CLIENT INTEGER, HIDE INTEGER, ARCHIVE INTEGER)")
            cursorbd.execute("CREATE TABLE CLIENTS (ID_CLIENT INTEGER, NAME_CLIENT VARCHAR(50), DESCRIPTION VARCHAR(100), HIDE INTEGER, ARCHIVE INTEGER)")
            cursorbd.execute("CREATE TABLE TIMES (TIME_INI VARCHAR(50), TIME_END VARCHAR(50), DESCRIPTION VARCHAR(100), ID_TASK INTEGER, ID_CLIENT INTEGER)")
            cursorbd.execute("INSERT INTO TASKS VALUES (1, 'task A', 'TASK ERROR 1', 0 , 1,  0 , 0 )")
            cursorbd.execute("INSERT INTO TASKS VALUES (2, 'task B', 'TASK ERROR 2', 0 , 2,  0 , 0 )")
            cursorbd.execute("INSERT INTO TASKS VALUES (3, 'task C', 'TASK ERROR 3', 0 , 3,  0 , 0 )")
            cursorbd.execute("INSERT INTO TASKS VALUES (4, 'task D', 'TASK ERROR 4', 0 , 4,  0 , 0 )")
            cursorbd.execute("INSERT INTO TASKS VALUES (5, 'Default Mail', 'Send mail', 1, 0, 0 , 0 )")
            cursorbd.execute("INSERT INTO TASKS VALUES (6, 'Default Call', 'Video call', 1, 0, 0 , 0 )")
            cursorbd.execute("INSERT INTO TASKS VALUES (6, 'Default Phone', 'Phone call', 1 , 0, 0 , 0 )")
            cursorbd.execute("INSERT INTO CLIENTS VALUES (1, 'Client A', 'Client A description', 0 , 0 )")
            cursorbd.execute("INSERT INTO CLIENTS VALUES (2, 'Client B', 'Client B description', 0 , 0 )")
            cursorbd.execute("INSERT INTO CLIENTS VALUES (3, 'Client C', 'Client C description', 0 , 0 )")
            cursorbd.execute("INSERT INTO CLIENTS VALUES (4, 'Client D', 'Client D description', 0 , 0 )")
        else:
            print('Database exists.')
            logger.info('Database exists.')
            
        self.conexionbd.commit()
        #self.conexionbd.close()
  
    def getClients(self, config):
        try:
            queryClient="SELECT NAME_CLIENT AS client FROM CLIENTS WHERE HIDE = 0 and ARCHIVE = 0"
            if config==1:
                queryClient="SELECT NAME_CLIENT FROM CLIENTS"
            set_client=self.conexionbd.execute(queryClient)
            return set_client
        except sqlite3.Error as error:
            logger.info(error)
    
    def deleteClients(self, client):#PROBAR
        try:
            queryClient="UPDATE CLIENTS SET ARCHIVE = 1 WHERE CLIENTS.NAME_CLIENT = ?"
            set_client=self.conexionbd.execute(queryClient,[client])
            return set_client
        except sqlite3.Error as error:
            logger.info(error)
                   
    def getTask(self, client):
        try:
            queryTask = "SELECT TASKS.NAME_TASK || '-' || TASKS.DESCRIPTION AS task FROM TASKS \
                WHERE TASKS.HIDE = 0 and TASKS.ARCHIVE = 0 and TASKS.DEFAULT_TASK = 1"
            if client!=None:
                queryTaskClient = " UNION  \
                SELECT TASKS.NAME_TASK || '-' || TASKS.DESCRIPTION AS task FROM TASKS  \
                inner join CLIENTS on CLIENTS.ID_CLIENT=TASKS.ID_CLIENT \
                WHERE TASKS.HIDE = 0 and TASKS.ARCHIVE = 0 and CLIENTS.NAME_CLIENT = ?" 
                queryTask = queryTask + queryTaskClient
                set_task=self.conexionbd.execute(queryTask,[client]);
            else:
                set_task=self.conexionbd.execute(queryTask)
            return set_task
        except sqlite3.Error as error:
            logger.info(error)  

if __name__ == "__main__":
    app = Database()
    Database.main()

