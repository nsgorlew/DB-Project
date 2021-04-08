import socket
bool = True
i = 0

while(bool == True):
    print("-" * 80)
    print("1. Query")
    print("2. Update Reader")
    print("3. Update Document")
    print("4. Reserve Document")
    print("5. Borrow Document")
    print("6. Return Document")
    print("7. Admin")
    print("0. Exit")
    print("-" * 80)
    try:
        option = int(input("Select an option: "))
        if option == 1:
            bool = True
        elif option == 2:
            bool = True
        elif option == 3:
            bool = True
        elif option == 0:
            bool = False
            break
    except:
        print("Invalid option. Please select an integer option from the menu.")

