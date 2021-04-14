import socket
bool = True
i = 0

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
