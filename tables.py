#!/usr/bin/env python
# coding: utf-8

# In[1]:


import psycopg2
import config
from configparser import ConfigParser
import pandas as pd
import csv



conn = psycopg2.connect(database='library', user='postgres', password='postgres')



cur = conn.cursor()
cur.execute('SELECT version()')




version = cur.fetchone()[0]




print(version)




# from configparser import ConfigParser
def config(filename='database.ini', section='library'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:

            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db



def create_initial_tables():
    
    """ create tables in the PostgreSQL database"""
    commands = (
          """
          CREATE TABLE READER(
                RID INTEGER NOT NULL,
                RTYPE VARCHAR(255),
                RNAME VARCHAR(255),
                RADDRESS VARCHAR(255),
                PHONE_NO VARCHAR(75),
                PRIMARY KEY (RID)
                )
          """,
          """
          CREATE TABLE BRANCH (
                BID SERIAL NOT NULL,
                LNAME VARCHAR(255),
                LOCATION VARCHAR(255),
                PRIMARY KEY (BID)
                )
         """,
         """
          CREATE TABLE RESERVATION (
                RES_NO SERIAL NOT NULL,
                DTIME TIMESTAMP NOT NULL,
                PRIMARY KEY (RES_NO)
                )
         """,
         """
          CREATE TABLE BORROWING (
                BOR_NO SERIAL NOT NULL,
                BDTIME DATE NOT NULL,
                RDTIME DATE NOT NULL,
                PRIMARY KEY (BOR_NO)
                )
         """,
         )
    
    conn = None
    try:
        # read the connection parameters
        #params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(database='library', user='postgres', password='postgres')
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
        print('Query successfully executed')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()



create_initial_tables()


def create_all_tables():
   # FOREIGN KEY (DOCID)
                #REFERENCES DOCUMENT (DOCID)
               # ON UPDATE CASCADE ON DELETE CASCADE ( add this in the copy table, once u merge)
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE COPY (
            DOCID SERIAL NOT NULL,
            COPYNO INTEGER NOT NULL,
            BID SERIAL NOT NULL,
            POSITION VARCHAR(255),
            PRIMARY KEY (DOCID, COPYNO, BID),
            FOREIGN KEY (BID)
                REFERENCES BRANCH (BID)
                ON UPDATE CASCADE ON DELETE CASCADE
            
        )
        """,
        """
        CREATE TABLE RESERVES (
            RID SERIAL NOT NULL,
            RESERVATION_NO SERIAL NOT NULL,
            DOCID SERIAL NOT NULL,
            COPYNO INTEGER NOT NULL,
            BID SERIAL NOT NULL,
            PRIMARY KEY (DOCID),
            FOREIGN KEY (DOCID, COPYNO, BID)
                REFERENCES COPY (DOCID, COPYNO, BID)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (RESERVATION_NO)
                REFERENCES RESERVATION (RES_NO)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (RID)
                REFERENCES READER (RID)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE BORROWS (
            BOR_NO SERIAL NOT NULL,
            DOCID SERIAL NOT NULL,
            COPYNO INTEGER NOT NULL,
            BID SERIAL NOT NULL,
            RID SERIAL NOT NULL,
            PRIMARY KEY (BOR_NO),
            FOREIGN KEY (DOCID, COPYNO, BID)
                REFERENCES COPY (DOCID, COPYNO, BID)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (RID)
                REFERENCES READER (RID)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        
            )
    
    conn = None
    try:
        # read the connection parameters
        #params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(database='library', user='postgres', password='postgres')
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
        print('Query successfully executed')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


# In[10]:


#create_all_tables()


# In[20]:


def populate(csv_file, sql_insert):
#     file = r'csv_files/Gedits.csv'
#     sql_insert = """INSERT INTO %s (DOCID, ISSUE_NO, PID)
#                 VALUES(%s, %s, %s)"""
    conn = None
    try:
        #params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(database='library', user='postgres', password='postgres')
        cursor = conn.cursor()
        with open(csv_file, 'r') as f:
            reader = csv.reader(f)
            next(reader) # This skips the 1st row which is the header.
            for record in reader:
#                 print(record)
                cursor.execute(sql_insert, record)
                conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            cursor.close()
            conn.close()
            print("Table populated. Connection closed.")





populate('Branch.csv', """INSERT INTO BRANCH (BID, LNAME, LOCATION) VALUES(%s, %s, %s)""")



populate('Copy.csv', """INSERT INTO COPY (DOCID, COPYNO, BID, POSITION) VALUES(%s, %s, %s, %s)""")





populate('Reader.csv', """INSERT INTO READER (RID, RTYPE, RNAME, RADDRESS, PHONE_NO) VALUES(%s, %s, %s, %s, %s)""")




populate('Borrows.csv', """INSERT INTO BORROWS (BOR_NO, DOCID, COPYNO, BID, RID) VALUES(%s, %s, %s, %s, %s)""")




populate('Borrowing.csv', """INSERT INTO BORROWING (BOR_NO, BDTIME, RDTIME) VALUES(%s, %s, %s)""")




populate('Reservation.csv', """INSERT INTO RESERVATION (RES_NO, DTIME) VALUES(%s, %s)""")




populate('Reserves.csv', """INSERT INTO RESERVES (RID, RESERVATION_NO, DOCID, COPYNO, BID) VALUES(%s, %s, %s, %s, %s)""")

