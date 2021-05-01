import psycopg2
from reservation_functions import new_reservation_num
from borrow_functions import new_borrow,return_doc,fine,check_reservations
from reader_functions import check_card_number,get_reader_reserve_list,get_document_list
from admin_functions import checkUser,add_document_copy,search_document_copy,add_new_reader,branch_search_by_id,branch_search_by_name,branch_search_by_loc,create_new_document
from admin_functions import q1_most_frequent_borrowers_for_a_branch, q2_most_frequent_borrowers, q3_most_borrowed_books_for_a_branch, q4_most_borrowed_books, q5_most_popular_books_by_year

#connect to db
def connect_db():
    conn = None
    try:
        conn = psycopg2.connect("dbname=libcs631 user=postgres password=postgres")
    except Error as e:
        print(e)
    return conn

#search for document by docID
def search_by_docID(conn,doc):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM DOCUMENT WHERE DOCID=%s ORDER BY DOCID" %(doc))
        row = cur.fetchone()
        while row is not None:
            print(row)
            row = cur.fetchone()
        cur.close()
        return True
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)

#search for document by title
def search_by_doc_title(conn,doc):
    try:
        docTitle = doc.replace("'","''")
        cur = conn.cursor()
        cur.execute("""SELECT * FROM DOCUMENT WHERE TITLE='%s' ORDER BY DOCID""" %(docTitle))
        row = cur.fetchone()
        while row is not None:
            print(row)
            row = cur.fetchone()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)

#search for document by publisher name
def search_by_doc_pub(conn,pub):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM DOCUMENT WHERE PUBLISHERID=%s ORDER BY TITLE" %(pub))
        row = cur.fetchone()
        while row is not None:
            print(row)
            row = cur.fetchone()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)

#main document search function
def doc_search(choice):
    if choice == 1:
        docID = input("Enter a document ID: ")
        search_by_docID(connect_db(),docID)
        sub_boolean = False
    elif choice == 2:
        docTitle = str(input("Enter a document title: "))
        search_by_doc_title(connect_db(),docTitle)
        sub_boolean = False
    elif choice == 3:
        docPub = input("Enter the publisher ID: ")
        search_by_doc_pub(connect_db(),docPub)
        sub_boolean = False
    elif choice == 0:
        sub_boolean = False
    return sub_boolean


#reader menu function
def reader_menu():
    primary_bool = True
    reader_bool = True
    try:
        #reader id == card_number
        card_number = str(input("Input reader ID: "))
        check = check_card_number(connect_db(),card_number)
        if check == False:
            primary_bool = False
        else:
            while(primary_bool==True):
                while(reader_bool == True):
                    print("-" * 80)
                    print("1. Search for a document by ID, title, or publisher name")
                    print("2. Document checkout")
                    print("3. Document return")
                    print("4. Document reserve")
                    print("5. Check fines")
                    print("6. Get reader reserve list")
                    print("7. Get document list")
                    print("0. Exit")
                    print("-" * 80)
                    choice = int(input("Please enter your choice (0-7): "))
                    try:
                        if choice==1:
                            print("1. Search by document ID")
                            print("2. Search by document name")
                            print("3. Search by publisher ID")
                            print("0. Return to main menu")
                            print("-" * 80)
                            sub_bool = True
                            while(sub_bool == True):
                                secondchoice = int(input("Please enter your choice (0-3): "))
                                try:
                                    sub_bool = doc_search(secondchoice)
                                except:
                                    print("Please input a valid choice. ")
                        elif choice==2:
                            try:
                                docid = input("Enter the document ID: ")
                                cp = input("Enter the copy number: ")
                                taken = check_reservations(connect_db(),card_number,docid,cp)
                                if taken == False:
                                    print("Good")
                                    new_borrow(connect_db(),card_number,docid,cp)
                                elif taken == True:
                                    print("-" * 80)
                                    print("Document is already reserved by another reader")
                            except:
                                print("Not a valid document ID.")
                        elif choice==3:
                            bor_number = input("Borrow number: ")
                            return_doc(connect_db(),bor_number)
                        elif choice==4:
                            doc_reserve_id = input("Enter the document ID: ")
                            copnum = input("Enter the copy number: ")
                            new_reservation_num(connect_db(),card_number, doc_reserve_id,copnum)
                        elif choice==5:
                            fine(connect_db(),card_number)
                        elif choice==6:
                            get_reader_reserve_list(connect_db(),card_number)
                        elif choice==7:
                            get_document_list(connect_db())
                        elif choice==0:
                            reader_bool = False
                            primary_bool = False
                    except:
                        print("Please input a valid choice. ")
    except:
        print("Please input a valid card number.")

#admin menu function
def admin_menu():
    admin_login_bool = False
    while admin_login_bool == False:
        username = input("Username: ")
        password = input("Password: ")
        admin_login_bool = checkUser(connect_db(),username,password)
    admin_menu_bool = True
    while admin_menu_bool == True:
        print("-" * 80)
        print("1. Add a document copy")
        print("2. Search a document copy and check its status")
        print("3. Add a new reader")
        print("4. Print branch information")
        print("5. Add new document")
        print("6. Get most frequent borrowers of a branch")
        print("7. Get most frequent borrowers")
        print("8. Get most borrowed books for a branch")
        print("9. Get most borrowed books")
        print("10. Get most popular books by year")
        print("11. TODO")
        print("0. Exit")
        print("-" * 80)
        admin_choice = int(input("Select an option (0-11): "))
        try:
            if admin_choice == 1:
                print("-" * 80)
                add_doc = input("Enter the document ID: ")
                add_branch = input("Enter the branch ID: ")
                add_position = input("Enter the position: ")
                add_document_copy(connect_db(),add_doc,add_branch,add_position)
            elif admin_choice == 2:
                print("-" * 80)
                search_doc_copy = input("Enter the Document ID: ")
                search_doc_copy_num = input("Enter the document copy number: ")
                search_document_copy(connect_db(),search_doc_copy,search_doc_copy_num)
            elif admin_choice == 3:
                print("-" * 80)
                rtype = input("Type of reader: ")
                rname = input("Name of reader: ")
                raddress = input("Address of reader: ")
                rphone = input("Phone number of reader: ")
                add_new_reader(connect_db(),rtype,rname,raddress,rphone)
            elif admin_choice == 4:
                print("-" * 80)
                print("1. Search by branch ID")
                print("2. Search by branch name")
                print("3. Search by branch location")
                print("-" * 80)
                branch_search_choice = int(input("Enter your search choice (0-3)): "))
                try:
                    if branch_search_choice == 1:
                        branch_id_search = input("Enter the branch ID: ")
                        branch_search_by_id(connect_db(),branch_id_search)
                    elif branch_search_choice == 2:
                        branch_name_search = input("Enter the branch name: ")
                        branch_search_by_name(connect_db(),branch_name_search)
                    elif branch_search_choice == 3:
                        branch_loc_search = input("Enter the branch location: ")
                        branch_search_by_loc(connect_db(),branch_loc_search)
                except:
                    print("Not a valid choice")
            elif admin_choice == 5:
                docname = input("Name of document: ")
                pubdate = input("Published date: ")
                pubid = input("Publisher ID: ")
                branchid = input("Branch ID: ")
                docposition = input("Document position: ")
                create_new_document(connect_db(),docname,pubdate,pubid,branchid,docposition)
            elif admin_choice == 6:
                num_readers = input("Number of top entries: ")
                branchid = input("Branch ID: ")
                q1_most_frequent_borrowers_for_a_branch(connect_db(),num_readers,branchid)
            elif admin_choice == 7:
                num_readers = input("Number of top entries: ")
                q2_most_frequent_borrowers(connect_db(), num_readers)
            elif admin_choice == 8:
                num_books = input("Number of top entries: ")
                branchid = input("Branch ID: ")
                q3_most_borrowed_books_for_a_branch(connect_db(),num_books,branchid)
            elif admin_choice == 9:
                num_books = input("Number of top entries: ")
                q4_most_borrowed_books(connect_db(),num_books)
            elif admin_choice == 10:
                year = input("Year (YYYY): ")
                q5_most_popular_books_by_year(connect_db(),year)
            elif admin_choice == 11:
                print('Function not implemented')
            elif admin_choice == 0:
                admin_menu_bool == False
                break
        except:
            print("Not a valid choice")

def main_menu():
    menu_bool = True
    while menu_bool == True:
        print("-"*80)
        print("1. Reader menu")
        print("2. Admin menu")
        print("0. Exit")
        print("-"*80)
        menu_choice = int(input("Enter an option (0-2): "))
        try:
            if menu_choice == 1:
                reader_menu()
            elif menu_choice == 2:
                admin_menu()
            elif menu_choice == 0:
                menu_bool = False
            else:
                print("-"*80)
                print("Not a valid option")
        except:
            print("Not a valid option")

main_menu()
