import os
import socket
from scapy.all import sniff, IP, TCP

# Fungsi untuk membersihkan tampilan terminal
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Fungsi untuk menampilkan header dengan tampilan custom
def show_header():
    print(r"""
██    ██ ██    ██ ██      ███    ██ ██   ██ 
██    ██ ██    ██ ██      ████   ██ ██  ██  
██    ██ ██    ██ ██      ██ ██  ██ █████   
██    ██ ██    ██ ██      ██  ██ ██ ██  ██  
 ██████   ██████  ███████ ██   ████ ██   ██ 
    """)
    print("Cybersecurity Tool\n")

# Fungsi untuk menampilkan menu dan mendapatkan pilihan pengguna
def show_menu():
    print("1. Port Scanner")
    print("2. Port Knock Detection")
    print("3. Service Enumerator")
    print("4. Exit\n")
    choice = input("Pilih fitur yang ingin Anda gunakan (1-4): ")
    return choice

# Fungsi untuk melakukan port scanning
def port_scanner(target):
    print(f"Memindai target: {target}")
    for port in range(1, 1025):  # Memindai port 1-1024
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            print(f"Port {port} terbuka")
        sock.close()

# Fungsi untuk enumerasi layanan pada port yang terbuka
def service_enumerator(target):
    print(f"Enumerasi layanan pada target: {target}")
    for port in range(1, 1025):  # Memindai port 1-1024
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            try:
                sock.send(b'HEAD / HTTP/1.0\r\n\r\n')
                banner = sock.recv(1024).decode('utf-8').strip()
                print(f"Port {port} menjalankan layanan: {banner}")
            except:
                print(f"Port {port} terbuka tetapi layanan tidak dapat diidentifikasi")
        sock.close()

# Fungsi untuk menangani paket yang diterima (Port Knock Detection)
def packet_handler(packet):
    if IP in packet and TCP in packet:
        ip_src = packet[IP].src
        port_dst = packet[TCP].dport
        print(f"Terdeteksi knock pada port {port_dst} dari {ip_src}")

# Fungsi untuk memonitor port knock
def port_knock_detector(interface, ports):
    print(f"Mendeteksi knock pada port {ports} di interface {interface}")
    sniff(iface=interface, prn=packet_handler, filter="tcp", store=0)

# Main program loop
def main():
    while True:
        clear_screen()
        show_header()
        choice = show_menu()
        
        if choice == '1':
            target = input("Masukkan IP address target: ")
            clear_screen()
            port_scanner(target)
        elif choice == '2':  # Ganti WHOIS Lookup dengan Port Knock Detection
            interface = input("Masukkan nama interface untuk dipantau: ")
            ports = input("Masukkan urutan port yang ingin dideteksi (pisahkan dengan koma, contoh: 22,80,443): ").split(',')
            ports = [int(port) for port in ports]
            clear_screen()
            port_knock_detector(interface, ports)
        elif choice == '3':
            target = input("Masukkan IP address target: ")
            clear_screen()
            service_enumerator(target)
        elif choice == '4':
            print("Terima kasih telah menggunakan VulnXplorer!")
            break  # Keluar dari loop untuk mengakhiri program
        else:
            print("Pilihan tidak valid, coba lagi.")
        
        post_action = input("Ingin kembali ke menu utama? (y/n): ")
        if post_action.lower() != 'y':
            print("Terima kasih telah menggunakan VulnXplorer!")
            break

if __name__ == "__main__":
    main()
