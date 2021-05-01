import psycopg2
from decimal import *

#check if someone else reserved a document before allowing a reader to borrow
def check_reservations(conn,reader_id,doc_id,copy):
    try:
        cur = conn.cursor()
        cur.execute("SELECT EXISTS(SELECT RID FROM RESERVES WHERE DOCID=%s AND COPYNO=%s AND RID!=%s)"%(doc_id,copy,reader_id))
        row = cur.fetchone()
        if row[0] == True:
            return True
            print("Another reader has reserved this document")
        elif row[0] == False:
            return False
        conn.close()
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)

#assuming reader id = library card number
def new_borrow(conn,reader_id,doc_id,copy):
        try:
            cur = conn.cursor()
#             cur.execute("INSERT INTO BORROWING (BOR_NO,BDTIME) VALUES (((SELECT BOR_NO FROM BORROWING ORDER BY BOR_NO DESC LIMIT 1)+1),CURRENT_DATE)")
            #RDTIME WILL AUTOMATICALLY BE NULL IF NOT MENTIONED IN THE INSERT
            cur.execute("INSERT INTO BORROWING (BDTIME) VALUES (CURRENT_DATE)")
            cur.execute("INSERT INTO BORROWS (BOR_NO,DOCID,COPYNO,BID,RID) VALUES (((SELECT BOR_NO FROM BORROWING ORDER BY BDTIME DESC LIMIT 1)),%s,%s,(SELECT BID FROM COPY WHERE DOCID=%s AND COPYNO=%s),%s)" %(doc_id,copy,doc_id,copy,reader_id))
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
        cur.execute("SELECT (RDTIME-BDTIME) AS INTEGER FROM BORROWING,BORROWS WHERE BORROWING.BOR_NO=BORROWS.BOR_NO AND RID=%s" % (reader_id))
        return_differences = []
        while True:
            row = cur.fetchone()
            if row == None:
                break
            ret_diff = row[0]
            return_differences.append(ret_diff)
            for date_diff in range(len(return_differences)):
                if return_differences[date_diff] > 20:
                    fine_amount = fine_amount + Decimal((return_differences[date_diff]-20)*0.2)
        cur.close()
        print("-"*40)
        print("Fines: ${}".format(round(fine_amount,2)))
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
