import psycopg2
import config
from configparser import ConfigParser
import pandas as pd
import csv

# from configparser import ConfigParser
def config(filename='database.ini', section='postgresql'):
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


# Connect DB


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()
        
	# execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
        cur.execute('SELECT current_database()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
       
        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

# test code to verify the communication with the database
connect()


#Creating Tables
#First create tables for publisher, person and admin, and then create the rest of the tables.

def create_initial_tables():
    
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE PUBLISHER (
            PUBLISHERID SERIAL NOT NULL,
            PUBNAME VARCHAR(255),
            ADDRESS VARCHAR(255),
            PRIMARY KEY (PUBLISHERID)
        )
        """,
        """
        CREATE TABLE PERSON (
            PID SERIAL NOT NULL,
            PNAME VARCHAR(75),
            PRIMARY KEY (PID)
        )
        """,
        """
        CREATE TABLE ADMIN (
            USERNAME VARCHAR(10) NOT NULL,
            PASSWORD VARCHAR(10),
            PRIMARY KEY (USERNAME, PASSWORD)
        )
        """,
        """
        CREATE TABLE READER (
            RID SERIAL NOT NULL,
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
        """
    )
    
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
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

def create_all_tables():
    
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE DOCUMENT (
            DOCID SERIAL NOT NULL,
            TITLE VARCHAR(255),
            PDATE DATE,
            PUBLISHERID INTEGER,
            PRIMARY KEY (DOCID),
            FOREIGN KEY (PUBLISHERID)
                REFERENCES PUBLISHER (PUBLISHERID)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE BOOK (
            DOCID INTEGER NOT NULL,
            ISBN VARCHAR(255),
            PRIMARY KEY (DOCID),
            FOREIGN KEY (DOCID)
                REFERENCES DOCUMENT (DOCID)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE JOURNAL_VOLUME (
            DOCID INTEGER NOT NULL,
            VOLUME_NO INTEGER CHECK (VOLUME_NO >= 0),
            EDITOR INTEGER,
            PRIMARY KEY (DOCID),
            FOREIGN KEY (DOCID)
                REFERENCES DOCUMENT (DOCID)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (EDITOR)
                REFERENCES PERSON (PID)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE JOURNAL_ISSUE (
            DOCID INTEGER NOT NULL,
            ISSUE_NO INTEGER NOT NULL CHECK (ISSUE_NO > 0 AND ISSUE_NO <= 10),
            SCOPE VARCHAR(75),
            PRIMARY KEY (DOCID, ISSUE_NO),
            FOREIGN KEY (DOCID)
                REFERENCES JOURNAL_VOLUME (DOCID)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE PROCEEDINGS (
            DOCID INTEGER NOT NULL,
            CDATE DATE,
            CLOCATION VARCHAR(75),
            CEDITOR VARCHAR(75),
            PRIMARY KEY (DOCID),
            FOREIGN KEY (DOCID)
                REFERENCES DOCUMENT (DOCID)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE AUTHORS (
            PID INTEGER NOT NULL,
            DOCID INTEGER NOT NULL,
            PRIMARY KEY (PID, DOCID),
            FOREIGN KEY (DOCID)
                REFERENCES BOOK (DOCID)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (PID)
                REFERENCES PERSON (PID)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE GEDITS (
                DOCID INTEGER NOT NULL,
                ISSUE_NO INTEGER NOT NULL,
                PID INTEGER NOT NULL,
                PRIMARY KEY (DOCID, ISSUE_NO, PID),
                FOREIGN KEY (PID)
                    REFERENCES PERSON (PID)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (DOCID, ISSUE_NO)
                    REFERENCES JOURNAL_ISSUE (DOCID, ISSUE_NO)
                    ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE CHAIRS (
            DOCID INTEGER NOT NULL,
            PID INTEGER NOT NULL,
            PRIMARY KEY (PID, DOCID),
            FOREIGN KEY (DOCID)
                REFERENCES PROCEEDINGS (DOCID)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (PID)
                REFERENCES PERSON (PID)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE COPY (
            DOCID INTEGER NOT NULL,
            COPYNO INTEGER NOT NULL,
            BID INTEGER NOT NULL,
            POSITION VARCHAR(255),
            PRIMARY KEY (DOCID, COPYNO, BID),
            FOREIGN KEY (DOCID)
                REFERENCES DOCUMENT (DOCID)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (BID)
                REFERENCES BRANCH (BID)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE RESERVES (
            RID INTEGER NOT NULL,
            RESERVATION_NO INTEGER NOT NULL,
            DOCID INTEGER NOT NULL,
            COPYNO INTEGER NOT NULL,
            BID INTEGER NOT NULL,
            PRIMARY KEY (RESERVATION_NO, DOCID, COPYNO, BID),
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
            BOR_NO INTEGER NOT NULL,
            DOCID INTEGER NOT NULL,
            COPYNO INTEGER NOT NULL,
            BID INTEGER NOT NULL,
            RID INTEGER NOT NULL,
            PRIMARY KEY (BOR_NO, DOCID, COPYNO, BID),
            FOREIGN KEY (DOCID, COPYNO, BID)
                REFERENCES COPY (DOCID, COPYNO, BID)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (RID)
                REFERENCES READER (RID)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """        
    )
    
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
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
create_all_tables()

# Data is populated using populate function(). For tables where the date information must be read from the csv files, separate functions are implemented (and IO is done using pandas).

def populate(csv_file, sql_insert):
    conn = None
    try:
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
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

def populate_documents():
    
    file = r'csv_files/Document.csv'
    sql_insert = """INSERT INTO DOCUMENT (TITLE, PDATE, PUBLISHERID)
                VALUES(%s, %s, %s)"""

    conn = None
    try:
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        cursor = conn.cursor()
        df = pd.read_csv(file, parse_dates=['PDATE'])
        for index, row in df.iterrows():
            cursor.execute(sql_insert, (row['TITLE'], row['PDATE'], row['PUBLISHERID']))
            conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            cursor.close()
            conn.close()
            print("Table populated. Connection closed.")


def populate_confproc():
    
    file = r'csv_files/confprocee.csv'
    sql_insert = """INSERT INTO PROCEEDINGS (DOCID, CDATE, CLOCATION, CEDITOR)
                VALUES(%s, %s, %s, %s)"""

    conn = None
    try:
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        cursor = conn.cursor()
        df = pd.read_csv(file, parse_dates=['CDATE'])
        for index, row in df.iterrows():
            cursor.execute(sql_insert, (row['DOCID'], row['CDATE'], row['CLOCATION'], row['CEDITOR']))
            conn.commit()


    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            cursor.close()
            conn.close()
            print("Table populated. Connection closed.")


populate('csv_files/Publisher.csv', """INSERT INTO PUBLISHER (PUBNAME, ADDRESS) VALUES(%s, %s)""")
populate_documents()
populate('csv_files/Person.csv', """INSERT INTO PERSON (PNAME) VALUES(%s)""")
populate('csv_files/book.csv', """INSERT INTO BOOK (DOCID, ISBN) VALUES(%s, %s)""")
populate('csv_files/JVolume.csv', 
         """INSERT INTO JOURNAL_VOLUME (DOCID, VOLUME_NO, EDITOR) VALUES(%s, %s, %s)""")
populate_confproc()
populate('csv_files/JIssue.csv', 
         """INSERT INTO JOURNAL_ISSUE (DOCID, ISSUE_NO, SCOPE) VALUES(%s, %s, %s)""")
populate('csv_files/Authors.csv', """INSERT INTO AUTHORS (PID, DOCID) VALUES(%s, %s)""")
populate('csv_files/Gedits.csv', """INSERT INTO GEDITS (DOCID, ISSUE_NO, PID) VALUES(%s, %s, %s)""")
populate('csv_files/Chairs.csv', """INSERT INTO CHAIRS (PID, DOCID) VALUES(%s, %s)""")

populate('csv_files/Branch.csv', 
         """INSERT INTO BRANCH (LNAME, LOCATION) VALUES(%s, %s)""")
populate('csv_files/Reader.csv', 
         """INSERT INTO READER (RTYPE, RNAME, RADDRESS, PHONE_NO) VALUES(%s, %s, %s, %s)""")
populate('csv_files/Borrowing.csv', 
         """INSERT INTO BORROWING (BDTIME, RDTIME) VALUES(%s, %s)""")
populate('csv_files/Reservation.csv', 
         """INSERT INTO RESERVATION (DTIME) VALUES(%s)""")
populate('csv_files/Copy.csv', 
         """INSERT INTO COPY (DOCID, COPYNO, BID, POSITION) VALUES(%s, %s, %s, %s)""")
populate('csv_files/Reserves.csv', 
         """INSERT INTO RESERVES (RID, RESERVATION_NO, DOCID, COPYNO, BID) VALUES(%s, %s, %s, %s, %s)""")
populate('csv_files/Borrows.csv', 
         """INSERT INTO BORROWS (BOR_NO, DOCID, COPYNO, BID, RID) VALUES(%s, %s, %s, %s, %s)""")
