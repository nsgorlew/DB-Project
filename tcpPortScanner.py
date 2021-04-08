import socket
boolean = True
i = 0

def getHostName(hostIP):
    try:
        print(socket.gethostbyaddr(hostIP))
    except:
        print("-" * 80)
        print("Cannot resolve %s" % hostIP)

def getIP(hostname):
    try:
        print(socket.gethostbyname(hostname))
    except:
        print("-" * 80)
        print("Cannot resolve %s" % hostname)

def portScanner(ports):
    print("-" * 80)
    for i in range(len(ports)):
        if s.connect_ex((host, ports[i])):
            print("Port %s is closed" % (ports[i]))
        else:
         print("Port %s is open" % (ports[i]))
        i = i + 1

def portScannerSpecific(sp_port):
    print("-" * 80)
    if s.connect_ex((host, sp_port)):
        print("Port %s is closed" % (sp_port))
    else:
        print("Port %s is open" % (sp_port))

while(boolean == True):
    print("-" * 80)
    print("1. Get hostname from IP Address")
    print("2. Get host IP from hostname ")
    print("3. Scan for open ports on a host")
    print("0. Exit Program")
    print("-" * 80)
    try:
        option = int(input("Select an option: "))
        if option == 1:
            sec_opt = input("Enter an IP Address: ")
            getHostName(sec_opt)
            boolean = True
        elif option == 2:
            third_opt = input("Enter a hostname: ")
            getIP(third_opt)
            boolean = True
        elif option == 3:
            host = input("Enter host IP Address: ")
            print("-" * 80)
            print("1. Scan ports 1-500")
            print("2. Scan a specific port")
            print("3. Exit to main menu")
            print("-" * 80)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            port_option = int(input("Select an option: "))
            if port_option == 1:
                ports = list(range(1, 501))
                portScanner(ports)
            elif port_option == 2:
                spec_port = int(input("Enter a port: "))
                portScannerSpecific(spec_port)
            elif port_option == 3:
                pass
            else:
                print("Not a valid option")
            boolean = True
        elif option == 0:
            boolean = False
            break
    except:
        print("Invalid option. Please select an integer option from the menu.")

