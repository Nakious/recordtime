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
            cursorbd.execute("CREATE TABLE TASKS (ID_TASK INTEGER PRIMARY KEY, NAME VARCHAR(100), DESCRIPTION VARCHAR(100), DEFAULT_TASK INTEGER, ID_CLIENT INTEGER, HIDE INTEGER, ARCHIVE INTEGER)")
            cursorbd.execute("CREATE TABLE CLIENTS (ID_CLIENT INTEGER PRIMARY KEY, NAME VARCHAR(50), DESCRIPTION VARCHAR(100), HIDE INTEGER, ARCHIVE INTEGER)")
            cursorbd.execute("CREATE TABLE TIMES (TIME_INI VARCHAR(50), TIME_END VARCHAR(50), DESCRIPTION VARCHAR(100), ID_TASK INTEGER, ID_CLIENT INTEGER)")
            cursorbd.execute("INSERT INTO TASKS VALUES (1, 'task A', 'TASK ERROR 1', 0 , 1,  0 , 0 )")
            cursorbd.execute("INSERT INTO TASKS VALUES (2, 'task B', 'TASK ERROR 2', 0 , 2,  0 , 0 )")
            cursorbd.execute("INSERT INTO TASKS VALUES (3, 'task C', 'TASK ERROR 3', 0 , 3,  0 , 0 )")
            cursorbd.execute("INSERT INTO TASKS VALUES (4, 'task D', 'TASK ERROR 4', 0 , 4,  0 , 0 )")
            cursorbd.execute("INSERT INTO TASKS VALUES (5, 'Default Mail', 'Send mail', 1, 0, 0 , 0 )")
            cursorbd.execute("INSERT INTO TASKS VALUES (6, 'Default Call', 'Video call', 1, 0, 0 , 0 )")
            cursorbd.execute("INSERT INTO TASKS VALUES (7, 'Default Phone', 'Phone call', 1 , 0, 0 , 0 )")
            cursorbd.execute("INSERT INTO CLIENTS VALUES (1, 'Client A', 'Client A description', 1 , 0 )")
            cursorbd.execute("INSERT INTO CLIENTS VALUES (2, 'Client B', 'Client B description', 0 , 0 )")
            cursorbd.execute("INSERT INTO CLIENTS VALUES (3, 'Client C', 'Client C description', 0 , 0 )")
            cursorbd.execute("INSERT INTO CLIENTS VALUES (4, 'Client D', 'Client D description', 0 , 0 )")
        else:
            print('Database exists.')
            logger.info('Database exists.')
            
        self.conexionbd.commit()
        #self.conexionbd.close()
    
    def getClients(self, config=None, client=None):
        try:
            query="SELECT NAME AS client FROM CLIENTS WHERE HIDE = 0 and ARCHIVE = 0 ORDER BY NAME"
            if config==1:
                query="SELECT NAME,ID_CLIENT FROM CLIENTS WHERE ARCHIVE = 0 ORDER BY NAME"
            data=self.conexionbd.execute(query)
            if config==2 and client!=None:
                query="SELECT * FROM CLIENTS WHERE NAME = ? AND ARCHIVE = 0 ORDER BY NAME"
                data=self.conexionbd.execute(query,[client])
            if config==3 and client!=None:
                query="SELECT NAME FROM CLIENTS WHERE ID_CLIENT = ? AND ARCHIVE = 0 ORDER BY NAME"
                data=self.conexionbd.execute(query,[client])
            return data
        except sqlite3.Error as error:
            logger.info(error)

    def getClient(self, client):
        try:
            query="SELECT * FROM CLIENTS WHERE NAME = ? AND ARCHIVE = 0"
            data=self.conexionbd.execute(query,[client])
            return data
        except sqlite3.Error as error:
            logger.info(error)
            
    def updateClient(self, idCLient, NameClient, DescriptionClient, HideClient):
        try:
            query="UPDATE CLIENTS SET NAME = ?, DESCRIPTION = ?, HIDE = ?  WHERE CLIENTS.ID_CLIENT = ?"
            self.conexionbd.execute(query,[NameClient,DescriptionClient,HideClient,idCLient])
            self.conexionbd.commit()
        except sqlite3.Error as error:
            logger.info(error)
    
    def createClient(self, NameClient, DescriptionClient, HideClient):
        try:
            query="INSERT INTO CLIENTS (NAME, DESCRIPTION, HIDE, ARCHIVE)  VALUES (?,?,?,0)"
            self.conexionbd.execute(query,[NameClient,DescriptionClient,HideClient])
            self.conexionbd.commit()
        except sqlite3.Error as error:
            logger.info(error)
    
    def deleteClient(self, client):#PROBAR
        try:
            query="UPDATE CLIENTS SET ARCHIVE = 1 WHERE CLIENTS.NAME = ?"
            data=self.conexionbd.execute(query,[client])
            self.conexionbd.commit()
            return data
        except sqlite3.Error as error:
            logger.info(error)
                   
            
    def getTasks(self, config=None, task=None):
        try:
            query="SELECT NAME AS client FROM CLIENTS WHERE HIDE = 0 and ARCHIVE = 0 ORDER BY NAME"
            if config==1 and task==None:
                query="SELECT NAME,ID_TASK FROM TASKS WHERE ARCHIVE = 0"
                data=self.conexionbd.execute(query)
            else:#PROBAR
                query="SELECT * FROM TASKS WHERE NAME = ? AND ARCHIVE = 0"
                data=self.conexionbd.execute(query,[task])
            return data
        except sqlite3.Error as error:
            logger.info(error)
            
    def getTask(self, task=None):
        try:
            query="SELECT * FROM TASKS ORDER BY NAME"
            data=self.conexionbd.execute(query)
            return data
        except sqlite3.Error as error:
            logger.info(error)
        # try:
        #     query = "SELECT TASKS.NAME || '-' || TASKS.DESCRIPTION AS task FROM TASKS \
        #         WHERE TASKS.HIDE = 0 and TASKS.ARCHIVE = 0 and TASKS.DEFAULT_TASK = 1"
        #     if client!=None:
        #         queryTaskClient = " UNION  \
        #         SELECT TASKS.NAME || '-' || TASKS.DESCRIPTION AS task FROM TASKS  \
        #         inner join CLIENTS on CLIENTS.ID_CLIENT=TASKS.ID_CLIENT \
        #         WHERE TASKS.HIDE = 0 and TASKS.ARCHIVE = 0 and CLIENTS.NAME = ?" 
        #         query = query + queryTaskClient
        #         data=self.conexionbd.execute(query,[client]);
        #     else:
        #         data=self.conexionbd.execute(query)
        #     return data
        # except sqlite3.Error as error:
        #     logger.info(error)  
            
    def deleteTask(self, task):
        try:
            query="UPDATE TASKS SET ARCHIVE = 1 WHERE NAME = ?"
            data=self.conexionbd.execute(query,[task])
            self.conexionbd.commit()
            return data
        except sqlite3.Error as error:
            logger.info(error)
            
    def updateTask(self, idTask, NameTask, DescriptionTask, HideTask, DefaultTask,NewClientTask):#PROBAR
        try:
            queryClient="UPDATE TASKS SET NAME = ?, DESCRIPTION = ?, HIDE = ?, DEFAULT_TASK = ?, ID_CLIENT = ?  WHERE TASKS.ID_TASK = ?"
            self.conexionbd.execute(queryClient,[NameTask,DescriptionTask,HideTask,DefaultTask,NewClientTask,idTask])
            self.conexionbd.commit()
        except sqlite3.Error as error:
            logger.info(error)
            
    def createTask(self, NameTask, DescriptionTask, HideTask, DefaultTask):#PROBAR
        try:
            queryClient="INSERT INTO TASKS (NAME, DESCRIPTION, HIDE, DEFAULT, ARCHIVE)  VALUES (?,?,?,?,0)"
            self.conexionbd.execute(queryClient,[NameTask, DescriptionTask, HideTask, DefaultTask])
            self.conexionbd.commit()
        except sqlite3.Error as error:
            logger.info(error)

if __name__ == "__main__":
    app = Database()
    Database.main()