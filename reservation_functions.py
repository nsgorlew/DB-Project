import datetime
import psycopg2
#assuming reader id = library card number

def new_reservation_num(conn,reader_id,doc_id,copynum):
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO RESERVATION (DTIME) VALUES (CURRENT_TIMESTAMP)")
        cur.execute("INSERT INTO RESERVES (RID,RESERVATION_NO,DOCID,COPYNO,BID) VALUES (%s,(SELECT RES_NO FROM RESERVATION ORDER BY DTIME DESC LIMIT 1),%s,%s,(SELECT BID FROM COPY WHERE DOCID=%s AND COPYNO=%s))" %(reader_id,doc_id,copynum,doc_id,copynum))
        conn.commit()
        #print("(Reader ID,Reservation #,Document ID, Copy #, Book ID)")
        #Tests###############
        #cur.execute("SELECT * FROM RESERVES")
        #cur.execute("SELECT * FROM RESERVATION")
        #cur.execute("SELECT RES_NO FROM RESERVATION ORDER BY DTIME DESC LIMIT 1")
        #####################
        #while True:
        #    row = cur.fetchone()
        #    if row == None:
        #        break
        #    print(row)
        cur.close()
    except (Exception,psycopg2.DatabaseError) as e:
        print(e)
