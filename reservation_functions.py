import datetime

#assuming reader id = library card number

def new_reservation_num(conn,reader_id,doc_id):
    res_time = datetime.date.now()
    try:
        cur = conn.cursor()
        sub_statement1 = cur.execute("SELECT NEXTVAL(RES_NO) FROM RESERVATION")
        sub_statement2 = cur.execute("SELECT DOCID,COPYNO,BID FROM COPY WHERE DOCID=?",(doc_id))
        cur.execute("INSERT INTO RESERVES ?,?,?",(reader_id,sub_statement1,sub_statement2))
        row = cur.fetchone()
        while row is not None:
            print(row)
            row = cur.fetchone()
        cur.close()
    except (Exception,psycopg2.DatabaseError) as e:
        print(e)
