def checkUser(conn,user,pw):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM ADMIN WHERE username=? AND password=?",(user,pw))
        row = cur.fetchone()
        if row is not None:
            result = True
        else:
            result = False
        return result
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)

def add_document_copy(conn,docid):
    try:
        cur = conn.cursor()
        cur.execute("SELECT DOCID FROM DOCUMENT WHERE DOCID=?",(docid))
        row = cur.fetchone()
        if row is not None:
            cur.execute("INSERT INTO DOCUMENT VALUES ?,(SELECT TITLE FROM DOCUMENT WHERE DocId=?),(SELECT PDATE FROM DOCUMENT WHERE DOCID=?),(SELECT PUBLISHERID FROM DOCUMENT WHERE DOCID=?)",(docid,docid,docid,docid))
        else:
            print("Document does not exist.")
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
 
#TODO: NEED FINAL DB           
def search_document_copy(conn,docid,copynum):
    try:
        cur = conn.cursor()
        cur.execute("SELECT DOCID,CopyNo,ResStatus FROM RESERVES,RESERVATION WHERE DOCID=? AND RESERVATION_NO=",(docid))
        row = cur.fetchone()
        while row is not None:
            print(row)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)

#add new reader
def add_new_reader(conn,reader_type,reader_name,reader_address,reader_phone):
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO READER VALUES (SELECT NEXTVAL(RID) FROM READER),?,?,?,?",(reader_type,reader_name,reader_address,reader_phone))
        while row is not None:
            print(row)
        print("Reader added")
        cur.close()
    except (Exception,psycopg2.DatabaseError) as e:
        print(e)
        
#print branch information by branch id
def branch_search_by_id(conn,bid):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM BRANCH WHERE BID=?",(bid))
        while row is not None:
            print(row)
        cur.close()
    except (Exception,psycopg2.DatabaseError) as e:
        print(e)

#print branch information by branch name
def branch_search_by_name(conn,bname):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM BRANCH WHERE LNAME=?",(bname))
        while row is not None:
            print(row)
        cur.close()
    except (Exception,psycopg2.DatabaseError) as e:
        print(e)
        
#print branch information by branch location
def branch_search_by_loc(conn,bloc):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM BRANCH WHERE LOCATION=?",(bloc))
        while row is not None:
            print(row)
        cur.close()
    except (Exception,psycopg2.DatabaseError) as e:
        print(e)
