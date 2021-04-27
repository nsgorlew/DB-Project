#!/usr/bin/env python
# coding: utf-8

# In[1]:


import psycopg2
import config
from configparser import ConfigParser
import pandas as pd
import csv


# In[6]:


conn = psycopg2.connect(database='library', user='postgres', password='postgres')


# In[7]:


cur = conn.cursor()
cur.execute('SELECT version()')


# In[8]:


version = cur.fetchone()[0]


# In[9]:


print(version)


# In[2]:


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


# def connect():
#     """ Connect to the PostgreSQL database server """
#     conn = None
#     try:
#         # read connection parameters
#         params = config()
# 
#         # connect to the PostgreSQL server
#         print('Connecting to the PostgreSQL database...')
#         conn = psycopg2.connect(**params)
# 		
#         # create a cursor
#         cur = conn.cursor()
#         
# 	# execute a statement
#         print('PostgreSQL database version:')
#         cur.execute('SELECT version()')
#         cur.execute('SELECT current_database()')
# 
#         # display the PostgreSQL database server version
#         db_version = cur.fetchone()
#         print(db_version)
#        
#         # close the communication with the PostgreSQL
#         cur.close()
#     except (Exception, psycopg2.DatabaseError) as error:
#         print(error)
#     finally:
#         if conn is not None:
#             conn.close()
#             print('Database connection closed.')
# 
# # test code to verify the communication with the database
# connect()

# In[25]:


def create_initial_tables():
    
    """ create tables in the PostgreSQL database"""
    commands = (
          """
          CREATE TABLE READER(
                RID INTEGER NOT NULL,
                RTYPE VARCHAR(75),
                RNAME VARCHAR(75),
                RADDRESS VARCHAR(75),
                PHONE_NO INTEGER,
                PRIMARY KEY (RID)
                )
          """,
          """
          CREATE TABLE BRANCH (
                BID SERIAL NOT NULL,
                LNAME VARCHAR(75),
                LOCATION VARCHAR(75),
                PRIMARY KEY (BID)
                )
         """,
         """
          CREATE TABLE RESERVATION (
                RES_NO SERIAL NOT NULL,
                DTIME DATE,
                PRIMARY KEY (RES_NO)
                )
         """,
         """
          CREATE TABLE BORROWING (
                BOR_NO SERIAL NOT NULL,
                BDTIME DATE,
                RDTIME DATE,
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


# In[26]:


create_initial_tables()


# In[27]:


def create_all_tables():
    
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
            FOREIGN KEY (DOCID)
                REFERENCES DOCUMENT (DOCID)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE RESERVES (
            RID SERIAL NOT NULL,
            RESERVATION_NO SERIAL,
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


# In[28]:


create_all_tables()

