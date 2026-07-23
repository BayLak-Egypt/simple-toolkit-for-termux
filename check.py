import os
import sys
import hashlib
import urllib.request
import urllib.error
class Color:
    GREEN = '\033[1;32m'
    RED = '\033[1;31m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[1;36m'
    BLUE = '\033[1;34m'
    WHITE = '\033[1;37m'
    RESET = '\033[0m'
print(f"\n{Color.YELLOW}[!] STARTING ADVANCED SYSTEM CHECK & DOWNLOAD...{Color.RESET}")
print(f"{Color.CYAN}[*] [1/2] Checking & Installing Python Libraries...{Color.RESET}")
try:
    import download_library
    for method in ['install_missing_libraries', 'download_all', 'main', 'install', 'check', 'run']:
        if hasattr(download_library, method) and callable(getattr(download_library, method)):
            print(f"{Color.GREEN}[+] Running library module: {method}(){Color.RESET}")
            getattr(download_library, method)()
            break
except Exception as e:
    print(f"{Color.RED}[!] Note in download_library: {e}{Color.RESET}")
print(f"\n{Color.CYAN}[*] [2/2] Fetching Manifest from GitHub Server...{Color.RESET}")
manifest = {}
try:
    import core_links
    if hasattr(core_links, 'get_combined_manifest'):
        manifest = core_links.get_combined_manifest()
    else:
        print(f"{Color.RED}[!] Function 'get_combined_manifest' not found in core_links.py!{Color.RESET}")
except Exception as e:
    print(f"{Color.RED}[!] Error loading core_links: {e}{Color.RESET}")
def calculate_github_sha1(file_path):
    """حساب الـ SHA-1 بنفس طريقة GitHub تماماً للمطابقة الدقيقة"""
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
        header = f"blob {len(content)}\0".encode('utf-8')
        return hashlib.sha1(header + content).hexdigest()
    except Exception:
        return None
def download_file(url, target_path):
    """تنزيل الملف وإنشاء المجلد تلقائياً"""
    try:
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        print(f"{Color.YELLOW}[*] Downloading: {target_path}...{Color.RESET}")
        req = urllib.request.Request(url, headers={'User-Agent': 'Library-Checker-App'})
        with urllib.request.urlopen(req, timeout=20) as response, open(target_path, 'wb') as f:
            f.write(response.read())
        print(f"{Color.GREEN}[✓] Downloaded successfully: {target_path}{Color.RESET}")
        return True
    except Exception as e:
        print(f"{Color.RED}[!] Failed to download {target_path}: {e}{Color.RESET}")
        return False
if not manifest:
    print(f"{Color.RED}[!] MANIFEST IS EMPTY! Check if 'libraryLinks.js' or 'plugins/github_server.py' exists.{Color.RESET}")
else:
    print(f"{Color.GREEN}[+] Manifest loaded! Found {len(manifest)} file(s) on GitHub.{Color.RESET}\n")
    downloaded_count = 0
    updated_count = 0
    for filename, file_info in manifest.items():
        target_path = os.path.join("library", filename)
        url = file_info.get("download_url") or file_info.get("url", "")
        expected_sha = file_info.get("hash") or file_info.get("sha")
        if not os.path.exists(target_path):
            print(f"{Color.RED}[!] Missing file detected: {target_path}{Color.RESET}")
            if url and download_file(url, target_path):
                downloaded_count += 1
        elif expected_sha:
            local_sha = calculate_github_sha1(target_path)
            if local_sha != expected_sha:
                print(f"{Color.YELLOW}[!] Update found on GitHub for: {target_path}{Color.RESET}")
                if url and download_file(url, target_path):
                    updated_count += 1
            else:
                print(f"{Color.GREEN}[✓] Up to date (SHA matched): {target_path}{Color.RESET}")
        else:
            print(f"{Color.GREEN}[✓] File exists: {target_path}{Color.RESET}")
    print(f"\n{Color.GREEN}[+] PROCESS COMPLETED! Summary: {downloaded_count} downloaded, {updated_count} updated.{Color.RESET}")
if __name__ == "__main__":
    pass