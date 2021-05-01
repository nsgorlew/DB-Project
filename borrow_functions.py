import psycopg2
from decimal import *

#assuming reader id = library card number
def new_borrow(conn,reader_id,doc_id,copy):
        try:
            cur = conn.cursor()
#             cur.execute("INSERT INTO BORROWING (BOR_NO,BDTIME) VALUES (((SELECT BOR_NO FROM BORROWING ORDER BY BOR_NO DESC LIMIT 1)+1),CURRENT_DATE)")
            cur.execute("INSERT INTO BORROWING (BDTIME, RDTIME) VALUES (CURRENT_DATE, NULL)")
            cur.execute("INSERT INTO BORROWS (BOR_NO,DOCID,COPYNO,BID,RID) VALUES (((SELECT BOR_NO FROM BORROWING ORDER BY BDTIME DESC LIMIT 1)),%s,%s,(SELECT BID FROM COPY WHERE DOCID=%s AND COPYNO=%s),%s)" %(doc_id,copy,doc_id,copy,reader_id))
            print("Document successfully borrowed")
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as e:
            print(e)
            print("Document borrow request failed.")
        finally:
            if conn is not None:
                conn.close()

def return_doc(conn,bor_no):
    try:
        cur = conn.cursor()
        cur.execute("UPDATE BORROWING SET RDTIME = CURRENT_DATE WHERE BOR_NO = %s" % (bor_no))
        conn.commit()
        #Test function
        #cur.execute("SELECT * FROM BORROWS")
        ##############
        #while True:
        #    row = cur.fetchone()
        #    if row == None:
        #        break
        #    print(row)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)


def fine(conn,reader_id):
    try:
        cur = conn.cursor()
        #cur.execute("SELECT RDTIME FROM BORROWING WHERE RID=%s")
        cur.execute("SELECT (CURRENT_DATE-BDTIME) AS INTEGER FROM BORROWING,BORROWS WHERE BORROWING.BOR_NO=BORROWS.BOR_NO AND RID=%s AND EXISTS(SELECT RDTIME WHERE RDTIME IS NULL)"%(reader_id))
        differences = []
        while True:
            row = cur.fetchone()
            if row == None:
                break
            diff = row[0]
            differences.append(diff)
        fine_amount = Decimal(0)
        for difference in range(len(differences)):
            if differences[difference] > 20:
                fine_amount = fine_amount + Decimal((differences[difference]-20)*0.2)
        print("-"*40)
        print("Fines for unreturned documents: ${}".format(round(fine_amount,2)))
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
