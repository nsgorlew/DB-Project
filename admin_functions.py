import psycopg2
from decimal import *

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

def q1_most_frequent_borrowers_for_a_branch(conn,num_readers,branchid):
    try:
        cur = conn.cursor()
        cur.execute("Select r.rid, r.rname, count(b.bor_no) AS No_Books from \
        borrows b, reader r where r.rid = b.rid AND b.bid='%s' group by r.rid \
        order by r.rid desc limit %s;"%(branchid,num_readers))
        print("Reader ID | Reader Name | Number of books borrowed")
        print("-"*40)
        while True:
            row = cur.fetchone()
            if row == None:
                break
            print(row)
        cur.close()
    except (Exception,psycopg2.DatabaseError) as e:
        print(e)

def q2_most_frequent_borrowers(conn, num_readers):
    try:
        cur = conn.cursor()
        cur.execute("Select r.rid, r.rname, count(b.bor_no) AS No_Books from \
        borrows b, reader r where r.rid = b.rid group by r.rid \
        order by r.rid desc limit %s;"%(num_readers))
        print("Reader ID | Reader Name | Number of books borrowed")
        print("-"*40)
        while True:
            row = cur.fetchone()
            if row == None:
                break
            print(row)
        cur.close()
    except (Exception,psycopg2.DatabaseError) as e:
        print(e)

def q3_most_borrowed_books_for_a_branch(conn,num_books,branchid):
    try:
        cur = conn.cursor()
        cur.execute("Select d.docid, d.title from document d, borrows b \
        where d.docid = b.docid AND b.bid = '%s' group by d.docid \
        order by count(b.bor_no) desc LIMIT %s;"%(branchid, num_books))
        print("Document ID | Document Title")
        print("-"*40)
        while True:
            row = cur.fetchone()
            if row == None:
                break
            print(row)
        cur.close()
    except (Exception,psycopg2.DatabaseError) as e:
        print(e)

def q4_most_borrowed_books(conn,num_books):
    try:
        cur = conn.cursor()
        cur.execute("Select d.docid, d.title from document d, borrows b \
        where d.docid = b.docid group by d.docid \
        order by count(b.bor_no) desc LIMIT %s;"%(num_books))
        print("Document ID | Document Title")
        print("-"*40)
        while True:
            row = cur.fetchone()
            if row == None:
                break
            print(row)
        cur.close()
    except (Exception,psycopg2.DatabaseError) as e:
        print(e)

def q5_most_popular_books_by_year(conn,year):
    try:
        cur = conn.cursor()
        cur.execute("Select d.docid, d.title from document d, borrows b, borrowing b1 \
        where d.docid = b.docid AND b.bor_no = b1.bor_no AND b1.bdtime \
        between '%s-01-01' AND '%s-12-31' group by d.docid, b1.bdtime \
        order by count(b.bor_no) desc limit 10;"%(year,year))
        print("Document ID | Document Title")
        print("-"*40)
        while True:
            row = cur.fetchone()
            if row == None:
                break
            print(row)
        cur.close()
    except (Exception,psycopg2.DatabaseError) as e:
        print(e)
        
def annoying_query(conn,sdate,edate):
	#BETWEEN sdate and edate
	try:
	    cur = conn.cursor()
	    cur.execute("SELECT BRANCH.BID,BRANCH.LNAME,AVG(RDTIME-BDTIME) AS INTEGER FROM BORROWING,BORROWS,BRANCH WHERE BORROWING.BOR_NO=BORROWS.BOR_NO AND BORROWS.BID=BRANCH.BID AND (RDTIME BETWEEN '%s' AND '%s') AND (BDTIME BETWEEN '%s' AND '%s') GROUP BY BRANCH.BID" % (sdate,edate,sdate,edate))
	    print("Branch ID | Branch Name | Average")
	    print("-"*80)
	    while True:
	        datalist = []
	        row = cur.fetchone()
	        if row == None:
	            break
	        for item in row:
	    	    datalist.append(item)
	        if datalist[2] > 20:
	            datalist[2] = (datalist[2]-20)*Decimal(0.2)
	        else:
	            datalist[2] = 0
	        print("Branch ID: %s | Branch Name: %s | Average Fine: %s"%(datalist[0],datalist[1],round(datalist[2],2)))
	    cur.close()
	    #cur.execute("select name, id, avg (condition for avg. fine from sdate to edate) from borrows, borrowing, branch where borrows.bor_no = borrowing.bor_no and borrows.bid= branch.bid")
	    #day_num_list = []
	    #branch_id_list = []
	    #branch_name_list = []
	    #fine = 0

	    #while True:
	        #row = cur.fetchone()
	        #if row == None:
	            #break
	        #branch_id_list.append(row[0])
	        #branch_name_list.append(row[1])
	        #day_num_list.append(int(row[2]))
	    #index = 0
	    #for index in len(day_num_list):
	      #  if day_num_list[day] > 20:
	        #    fine = (day_num_list[day]-20)*0.20
	       # elif day_num_list[day] < 20:
	      #      fine = fine
	      #  index = index + 1
	    #average_fine = fine / len(day_num_list)
	   # for branch in branch_id_list:
	        #print("Branch ID: %s, Branch Name: %s, Average fine: %s" %(branch_id_list[branch],branch_name_list[branch],average_fine)
	except (Exception,psycopg2.DatabaseError) as e:
	    print(e)


