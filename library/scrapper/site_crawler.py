import urllib.request
import urllib.parse
import re
import color

DESCRIPTION = "Fast Recursive Same-Domain Web Crawler"
GROUP_ID = 5  # Scraper Tools
COLOR = color.BLUE

def crawl_site(start_url: str, max_links: int = 50):
    """Crawl a website quickly to find all internal links with an improved link extractor."""
    parsed_start = urllib.parse.urlparse(start_url)
    domain = parsed_start.netloc

    visited = set()
    to_visit = [start_url]
    discovered_links = set([start_url])

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print(color.color_text(f"\n[+] Starting fast crawl on domain: {domain}\n", color.GREEN))

    while to_visit and len(visited) < max_links:
        current_url = to_visit.pop(0)
        if current_url in visited:
            continue

        visited.add(current_url)
        print(color.color_text(f"  [CRAWLING] {current_url}", color.CYAN))

        try:
            req = urllib.request.Request(current_url, headers=headers)
            with urllib.request.urlopen(req, timeout=5) as response:
                content_type = response.headers.get("Content-Type", "")
                if "text/html" not in content_type:
                    continue

                html_content = response.read().decode('utf-8', errors='ignore')
                
                raw_links = re.findall(r'href\s*=\s*(?:["\']([^"\']*)["\']|([^\s>]+))', html_content, re.IGNORECASE)
                
                flattened_links = [link[0] if link[0] else link[1] for link in raw_links]

                for link in flattened_links:
                    if not link or link.startswith(('#', 'javascript:', 'mailto:', 'tel:')):
                        continue

                    absolute_url = urllib.parse.urljoin(current_url, link)
                    parsed_link = urllib.parse.urlparse(absolute_url)
                    if parsed_link.path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.css', '.js', '.pdf', '.zip', '.svg', '.ico', '.xml', '.rss')):
                        continue
                    clean_url = f"{parsed_link.scheme}://{parsed_link.netloc}{parsed_link.path}"
                    clean_url = clean_url.rstrip('/')

                    if parsed_link.netloc == domain and clean_url not in discovered_links:
                        discovered_links.add(clean_url)
                        to_visit.append(clean_url)

        except Exception as e:
            continue

    print(color.color_text(f"\n[+] Crawling completed! Total unique internal links found: {len(discovered_links)}\n", color.GREEN))
    for link in sorted(discovered_links):
        print(f"  - {color.color_text(link, color.YELLOW)}")

def run():
    print(color.color_text("--- Fast Recursive Same-Domain Web Crawler ---", COLOR))
    
    url = input("Enter starting URL (e.g., https://example.com): ").strip()
    if not url:
        print(color.color_text("[!] URL cannot be empty.", color.RED))
        return

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    try:
        max_limit = int(input("Enter max links to crawl (default 50): ").strip() or "50")
    except ValueError:
        max_limit = 50

    crawl_site(url, max_limit)
