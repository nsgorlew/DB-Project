import psycopg2

def check_card_number(conn,card_num):
    try:
        cur = conn.cursor()
        cur.execute("SELECT ReaderId FROM READER WHERE EXISTS(SELECT ReaderId FROM READER WHERE ReaderId='?')",(card_num))
        row = cur.fetchone()
        if row is not None:
            return True
        else:
            print("That card number does not exist. ")
            return False
        cur.close()
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
        

def get_reader_reserve_list(conn,reader_id):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM RESERVES WHERE RID='?' ORDER BY DOCID", (reader_id))
        row = cur.fetchone()
        while row is not None:
            print(row)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)

def get_document_list(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM DOCUMENT ORDER BY DOCID")
        row = cur.fetchone()
        while row is not None:
            print(row)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
