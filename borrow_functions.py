import psycopg2
from decimal import *

#check if someone else reserved a document
def check_reservations(conn,reader_id,doc_id,copy):
    try:
        cur = conn.cursor()
        cur.execute("SELECT EXISTS(SELECT RID FROM RESERVES WHERE DOCID=%s AND COPYNO=%s AND RID<>%s)"%(doc_id,copy,reader_id))
        result = cur.fetchone()[0]
        conn.close()
        return result
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)

#check if someone else borrowed the document
def check_borrows(conn,doc_id,copy):
    try:
        cur = conn.cursor()
        cur.execute("SELECT EXISTS(SELECT RID FROM BORROWS WHERE DOCID=%s AND COPYNO=%s)"%(doc_id,copy))
        result = cur.fetchone()[0]
        conn.close()
        return result
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)

#assuming reader id = library card number
def new_borrow(conn,reader_id,doc_id,copy):
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO BORROWING (BDTIME, RDTIME) VALUES (CURRENT_DATE, NULL)")
            conn.commit()
            cur.execute("INSERT INTO BORROWS (BOR_NO,DOCID,COPYNO,BID,RID) VALUES ((currval(pg_get_serial_sequence('BORROWING','bor_no'))),%s,%s,(SELECT BID FROM COPY WHERE DOCID=%s AND COPYNO=%s),%s)" %(doc_id,copy,doc_id,copy,reader_id))
            print("-"*80)
            print("Document successfully borrowed")
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as e:
            print(e)
            print("Document borrow request failed.")
        finally:
            if conn is not None:
                conn.close()

def return_doc(conn,reader_id,doc_id,copynum):
    try:
        cur = conn.cursor()
        cur.execute("UPDATE BORROWING SET RDTIME = CURRENT_DATE WHERE BOR_NO = (SELECT BOR_NO FROM BORROWS WHERE DOCID=%s AND COPYNO=%s AND RID=%s ORDER BY BOR_NO DESC LIMIT 1)" % (doc_id,copynum,reader_id))
        print("-"*80)
        print("Document returned")
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
        cur.execute("SELECT (CURRENT_DATE-BDTIME) AS INTEGER FROM BORROWING,BORROWS WHERE BORROWING.BOR_NO=BORROWS.BOR_NO AND RID=%s AND RDTIME IS NULL"%(reader_id))
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
        cur.execute("SELECT (RDTIME-BDTIME) AS INTEGER FROM BORROWING,BORROWS WHERE BORROWING.BOR_NO=BORROWS.BOR_NO AND RID=%s AND RDTIME IS NOT NULL" % (reader_id))
        return_differences = []
        while True:
            row = cur.fetchone()
            if row == None:
                break
            ret_diff = row[0]
            if ret_diff == None:
                break
            return_differences.append(ret_diff)
            for date_diff in range(len(return_differences)):
                if return_differences[date_diff] > 20:
                    fine_amount = fine_amount + Decimal((return_differences[date_diff]-20)*0.2)
        cur.close()
        print("-"*80)
        print("Fines: ${}".format(round(fine_amount,2)))
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
