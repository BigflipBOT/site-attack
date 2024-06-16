import socket

def scan_ports(ip, start_port, end_port):
    open_ports = []
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    return open_ports

def main():
    ip = input("Podaj adres IP serwera: ")
    start_port = int(input("Podaj początkowy port do skanowania: "))
    end_port = int(input("Podaj końcowy port do skanowania: "))
    
    print(f"Skanowanie portów od {start_port} do {end_port} na serwerze {ip}")
    open_ports = scan_ports(ip, start_port, end_port)
    
    if open_ports:
        print("Otwarte porty:")
        for port in open_ports:
            print(port)
    else:
        print("Brak otwartych portów w podanym zakresie.")

if __name__ == "__main__":
    main()

