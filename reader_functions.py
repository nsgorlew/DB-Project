import psycopg2

def check_card_number(conn,reader_num):
    try:
        cur = conn.cursor()
        cur.execute("SELECT RID FROM READER WHERE RID=%s",(reader_num))
        row = cur.fetchone()
        if row is not None:
            reader_found = True
        else:
            print("That card number does not exist. ")
            reader_found = False
        cur.close()
        return reader_found
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
        

def get_reader_reserve_list(conn,reader_id):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM RESERVES WHERE RID=%s ORDER BY DOCID" %(reader_id))
        print("(Reader ID,Reservation #,Document ID, Copy #, Book ID)")
        while True:
            row = cur.fetchone()
            if row == None:
                break
            print(str(row)+" Status:Reserved")
        cur.close()      
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)

def get_document_list(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM DOCUMENT ORDER BY DOCID")
        while True:
            row = cur.fetchone()
            if row == None:
                break
            print(row)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
