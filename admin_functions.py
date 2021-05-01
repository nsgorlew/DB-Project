import psycopg2

def registerAdmin(conn,user,pw):
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO ADMIN (username, password) VALUES ('%s','%s')" %(user,pw))
        print('Admin %s registered'.format(user))
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)

def checkUser(conn,user,pw):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM ADMIN WHERE username='%s' AND password='%s'" %(user,pw))
        row = cur.fetchone()
        if row is not None:
            result = True
        else:
            result = False
        return result
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)

def add_document_copy(conn,docid,branchid,position):
    try:
        cur = conn.cursor()
        cur.execute("SELECT DOCID FROM COPY WHERE DOCID=%s AND BID=%s" %(docid,branchid))
        row = cur.fetchone()
        if row is not None:
            cur.execute("SELECT MAX(COPYNO)+1 FROM COPY WHERE DOCID=%s AND BID=%s" %(docid,branchid))
            new_copy = cur.fetchone()
            cur.execute("INSERT INTO COPY (DOCID,COPYNO,BID,POSITION) VALUES (%s,%s,%s,'%s')" %(docid,new_copy[0],branchid,position))
            conn.commit()
            print("Copy added successfully")
        else:
            print("Document doesn't exist in this branch")
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)

def search_document_copy(conn,docid,copynum):
    try:
        cur = conn.cursor()
        cur.execute("SELECT RDTIME FROM BORROWING,BORROWS WHERE BORROWING.BOR_NO=BORROWS.BOR_NO AND DOCID=%s AND COPYNO=%s" %(docid,copynum))
        row = cur.fetchone()
        if row is not None:
            print("-"*40)
            print("Document is currently NOT being borrowed")
        else:
            print("-"*40)
            print("Document is currently borrowed")
        #cur.execute("SELECT RID FROM RESERVES,RESERVATION WHERE RESERVATION_NO=RES_NO AND DOCID=%s AND COPYNO=%s" %(docid,copynum))
        #cur.execute("SELECT RDTIME FROM BORROWS,BORROWING WHERE BORROWS.BOR_NO=BORROWING.BOR_NO AND BOR_NO=%s" %())
        cur.close()
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)

#add new reader
def add_new_reader(conn,reader_type,reader_name,reader_address,reader_phone):
    try:
        cur = conn.cursor()
#         cur.execute("SELECT MAX(RID)+1 FROM READER")
#         new_rid = cur.fetchone()
        cur.execute("INSERT INTO READER (RTYPE, RNAME, RADDRESS, PHONE_NO) VALUES ('%s','%s','%s','%s')" %(reader_type,reader_name,reader_address,reader_phone))
        conn.commit()
        cur.execute("SELECT currval(pg_get_serial_sequence('READER','rid'))")
        row = cur.fetchone()
        if row is not None:
            print("Reader added with RID: %s" % (row))
        else:
            print("Failed to add the new reader.")
        cur.close()
    except (Exception,psycopg2.DatabaseError) as e:
        print(e)

#print branch information by branch id
def branch_search_by_id(conn,bid):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM BRANCH WHERE BID=%s" %(bid))
        row = cur.fetchone()
        cur.close()
        print("Branch ID | Branch Name | Branch Location")
        print("-"*40)
        print(row)
    except (Exception,psycopg2.DatabaseError) as e:
        print(e)

#print branch information by branch name
def branch_search_by_name(conn,bname):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM BRANCH WHERE LNAME='%s'" %(bname))
        print("Branch ID | Branch Name | Branch Location")
        print("-"*40)
        while True:
            row = cur.fetchone()
            if row == None:
                break
            print(row)
        cur.close()
    except (Exception,psycopg2.DatabaseError) as e:
        print(e)

#print branch information by branch location
def branch_search_by_loc(conn,bloc):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM BRANCH WHERE LOCATION='%s'" %(bloc))
        print("Branch ID | Branch Name | Branch Location")
        print("-"*40)
        while True:
            row = cur.fetchone()
            if row == None:
                break
            print(row)
        cur.close()
    except (Exception,psycopg2.DatabaseError) as e:
        print(e)

#add new document to database
def create_new_document(conn,docname,pubdate,pubid,branchid,docposition):
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO DOCUMENT (title,pdate,publisherid) VALUES ('%s','%s',%s)" %(docname,pubdate,pubid))
        cur.execute("INSERT INTO COPY (DOCID,COPYNO,BID,POSITION) VALUES ((SELECT DOCID FROM DOCUMENT WHERE TITLE='%s'),1,%s,'%s')" %(docname,branchid,docposition))
        conn.commit()
        print("Document successfully added")
        cur.close()
    except (Exception,psycopg2.DatabaseError) as e:
        print(e)
