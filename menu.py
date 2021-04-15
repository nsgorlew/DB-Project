import socket
bool = True
i = 0

def reader_menu():
    reader_bool = True
    try:
        card_number = int(input("Input card number: "))
        #need function here to verify card number
        print("#" * 80)
        print("1. Search for a document")
        print("2. Document checkout")
        print("3. Document return")
        print("4. Document reserve")
        print("5. Check fines")
        print("6. Search for a document")
        print("7. Get reader reserve list")
        print("8. Get document list")
        print("0. Exit")
        print("#" * 80)
        while(reader_bool == True):
            try:
                sub_bool = True
                choice = int(input("Please enter your choice (0-8): "))
                if choice==1:
                    print("1. Search by Document ID")
                    print("2. Search by Document name")
                    print("0. Return to main menu")
                    print("#" * 80)
                    while(sub_bool == True):
                    try:
                        2nd_choice = int(input("Please enter an option (0-2): "))
                        #put in search functions
                        if 2nd_choice==1:
                            #TODO: search function by doc ID
                            sub_bool = False
                        elif 2nd_choice==2:
                            #TODO: search function by doc name
                            sub_bool = False
                        elif 2nd_choice==0:
                            sub_bool = False
                        else:
                            print("Please input a valid choice. ")
                    except:
                        print("Please input a valid choice. ")
                elif choice==2:
                    try:
                        docid = input("Input the document ID: ")
                        #TODO: put in search function
                        #placeholder boolean is "found"
                        found = True
                        if found==True:
                            #TODO: reserve function
                            pass
                        else:
                            print("Not a valid document ID.")
                    except:
                        print("Not a valid document ID.")
                elif choice==3:
                    pass

            except:
                print("Please input a valid choice. ")
    except:
        print("Please input a valid card number.")

while(bool == True):
    print("-" * 80)
    print("1. Reader")
    print("2. Admin")
    print("-" * 80)
    try:
        option_1 = int(input("Select an option: "))
        if option_1 == 1:
            print("1. Query")
            print("2. Update Reader")
            print("3. Update Document")
            print("4. Reserve Document")
            print("5. Borrow Document")
            print("6. Return Document")
            print("0. Exit")
            print("-" * 80)
            try:
                option = int(input("Select an option: "))
                if option == 1:
                    SQL_func = input("Input SQL statement: ")
                    query_result = SQL_func.execute()
                    print(query_result)
                    bool = True
                elif option == 2:
                    reader_name = input("Name of Reader: ")
                    question = input("Would you like to include another reader? Y/N: ")
                    if question == Y or y:
                                     reader2 = input("Enter next reader
                    print("-" * 80)
                    print("1. Name")

                    bool = True
                elif option == 3:
                    bool = True
                elif option == 0:
                    bool = False
                    break
            except:
                print("Invalid option. Please select an integer option from the menu.")
        if option_1 == 2:
            print("-" * 80)
            print("1. Add Reader")
            print("2. Edit Reader")
            print("3. Delete Reader")
