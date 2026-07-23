import time
import urllib.request
import color

DESCRIPTION = "Simple Connection Latency & Speed Test"
GROUP_ID = 1  # Networking Tools
COLOR = color.BLUE

def test_latency(host: str = "https://www.google.com", timeout: int = 5) -> float:
    """Measure HTTP response latency in milliseconds."""
    start_time = time.time()
    try:
        req = urllib.request.Request(host, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            if response.status == 200:
                end_time = time.time()
                return round((end_time - start_time) * 1000, 2)
    except Exception:
        pass
    return -1.0

def run():
    print(color.color_text("--- Simple Connection Latency Test ---", COLOR))
    
    hosts = [
        ("Google", "https://www.google.com"),
        ("Cloudflare", "https://1.1.1.1"),
        ("GitHub", "https://github.com")
    ]

    print(color.color_text(f"\n[+] Testing connection latency to popular servers...\n", color.GREEN))
    
    for name, url in hosts:
        latency = test_latency(url)
        if latency >= 0:
            print(f"  {name.ljust(12)} : {color.color_text(f'{latency} ms', color.YELLOW)}")
        else:
            print(f"  {name.ljust(12)} : {color.color_text('Timeout / Unreachable', color.RED)}")
