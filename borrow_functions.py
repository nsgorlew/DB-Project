import datetime


#assuming reader id = library card number
def new_borrow(conn,reader_id,doc_id):
        bdtime = datetime.date.now()
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO BORROWING VALUES NEXTVAL('BOR_NO'),?,?",(bdtime,NULL))
            sub_statement1 = cur.execute("SELECT MAX(BOR_NO) FROM BORROWING")
            sub_statement2 = cur.execute("SELECT DOCID,COPYNO,BID FROM COPY WHERE DOCID=?",(doc_id))
            cur.execute("INSERT INTO BORROWS ?,?,?",(reader_id,sub_statement1,sub_statement2))
            row = cur.fetchone()
            while row is not None:
                print(row)
                row = cur.fetchone()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as e:
            print(e)
        finally:
            if conn is not None:
                conn.close()
            
def return_doc(conn,bor_no):
    rdtime = datetime.date.now()
    try:
        cur = conn.cursor()
        cur.execute("UPDATE BORROWS SET RDTIME = ? WHERE BOR_NO = ?", (rdtime,bor_no))
        while row is not None:
            print(row)
            row = cur.fetchone()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()
            
def get_fine(conn,reader_id):
    try:
        cur = conn.cursor()
        cur.execute("SELECT FineAmount FROM BORROWS WHERE RID = ?", (reader_id))
        while row is not None:
            print(row)
            row = cur.fetchone()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)

