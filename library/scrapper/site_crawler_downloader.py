import urllib.request
import urllib.parse
import re
import os
import color

DESCRIPTION = "Same-Domain Web Crawler & Downloader Tool"
GROUP_ID = 5  # Scraper Tools
COLOR = color.BLUE

def crawl_and_download(start_url: str, max_pages: int = 20):
    """Crawl a website within the same domain and download its pages matching the site structure."""
    parsed_start = urllib.parse.urlparse(start_url)
    domain = parsed_start.netloc
    
    if not domain:
        print(color.color_text("[!] Invalid domain extracted from URL.", color.RED))
        return

    # Create directory for downloaded pages mimicking the domain structure
    output_dir = f"downloaded_{domain.replace(':', '_')}"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    visited = set()
    queue = [start_url]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print(color.color_text(f"\n[+] Starting crawler on domain: {color.color_text(domain, color.YELLOW)}", color.GREEN))
    print(color.color_text(f"[+] Output directory: {output_dir}\n", color.CYAN))

    downloaded_count = 0

    while queue and downloaded_count < max_pages:
        current_url = queue.pop(0)
        
        if current_url in visited:
            continue
            
        visited.add(current_url)
        print(color.color_text(f"[*] Crawling ({downloaded_count + 1}/{max_pages}): {current_url}", color.CYAN))

        try:
            req = urllib.request.Request(current_url, headers=headers)
            with urllib.request.urlopen(req, timeout=8) as response:
                content_type = response.headers.get("Content-Type", "")
                if "text/html" not in content_type:
                    continue
                    
                html_bytes = response.read()
                html_content = html_bytes.decode('utf-8', errors='ignore')

                # Determine file path based on URL path to mirror server structure
                parsed_current = urllib.parse.urlparse(current_url)
                path = parsed_current.path
                if path == "" or path.endswith("/"):
                    path += "index.html"
                elif not os.path.splitext(path)[1]:
                    path += ".html"

                # Clean path for local storage
                local_path = os.path.join(output_dir, path.lstrip("/"))
                local_dir = os.path.dirname(local_path)
                
                if not os.path.exists(local_dir):
                    os.makedirs(local_dir, exist_ok=True)

                with open(local_path, "wb") as f:
                    f.write(html_bytes)
                
                downloaded_count += 1
                print(f"    -> Saved to: {local_path}")

                # Extract internal links using robust Regex matching all href patterns
                raw_links = re.findall(r'href\s*=\s*(?:["\']([^"\']*)["\']|([^\s>]+))', html_content, re.IGNORECASE)
                flattened_links = [link[0] if link[0] else link[1] for link in raw_links]

                for link in flattened_links:
                    if not link or link.startswith(('#', 'javascript:', 'mailto:', 'tel:')):
                        continue

                    # Resolve relative links
                    full_link = urllib.parse.urljoin(current_url, link)
                    parsed_link = urllib.parse.urlparse(full_link)
                    
                    # Avoid heavy assets or unwanted extensions
                    if parsed_link.path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.css', '.js', '.pdf', '.zip', '.mp4', '.mp3', '.svg', '.ico', '.xml', '.rss')):
                        continue

                    # Clean URL fragment and parameters for unique collection
                    clean_link = f"{parsed_link.scheme}://{parsed_link.netloc}{parsed_link.path}"
                    clean_link = clean_link.rstrip('/')
                    
                    # Check if link belongs to the same domain and hasn't been visited
                    if parsed_link.netloc == domain and clean_link not in visited and clean_link not in queue:
                        queue.append(clean_link)

        except Exception as e:
            print(color.color_text(f"    [!] Failed to fetch {current_url}: {e}", color.RED))

    print(color.color_text(f"\n[+] Crawling completed! Successfully downloaded {downloaded_count} page(s).", color.GREEN))
    print(color.color_text(f"[+] Files are stored inside folder: {output_dir}", color.YELLOW))

def run():
    print(color.color_text("--- Same-Domain Web Crawler & Downloader Tool ---", COLOR))
    
    url = input("Enter target starting URL (e.g., https://example.com): ").strip()
    if not url:
        print(color.color_text("[!] URL cannot be empty.", color.RED))
        return

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    try:
        max_p = input("Enter maximum pages to crawl (default: 20): ").strip()
        max_pages = int(max_p) if max_p else 20
    except ValueError:
        max_pages = 20

    crawl_and_download(url, max_pages)
