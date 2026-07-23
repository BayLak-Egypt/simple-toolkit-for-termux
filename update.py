import os
import sys
import hashlib
import urllib.request
import urllib.parse
import urllib.error
import requests
import color

REPO_OWNER = "BayLak-Egypt"
REPO_NAME = "simple-toolkit-for-termux"
BRANCH = "main"

def calculate_github_sha1(file_path):
    """Calculate SHA-1 hash in the exact same way Git does"""
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
    """Download file while creating required directories and encoding space characters"""
    try:
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        safe_url = urllib.parse.quote(url, safe=':/?&=#%')
        req = urllib.request.Request(safe_url, headers={'User-Agent': 'Toolkit-Auto-Updater'})
        with urllib.request.urlopen(req, timeout=25) as response, open(target_path, 'wb') as f:
            f.write(response.read())
        return True
    except Exception as e:
        print(f"{color.RED}[!] Error downloading {target_path}: {e}{color.RESET}")
        return False

def fetch_repo_tree():
    """Fetch the repository file tree from GitHub excluding the 'library' directory"""
    api_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/git/trees/{BRANCH}?recursive=1"
    headers = {
        "User-Agent": "Toolkit-Auto-Updater",
        "Accept": "application/vnd.github.v3+json"
    }
    files_manifest = {}
    try:
        response = requests.get(api_url, headers=headers, timeout=15)
        if response.status_code == 200:
            tree_data = response.json().get("tree", [])
            for item in tree_data:
                item_path = item.get("path", "")
                if item_path == "library" or item_path.startswith("library/"):
                    continue
                if "__pycache__" in item_path or item_path.endswith(".pyc") or item_path.startswith(".git"):
                    continue
                if item.get("type") == "blob":
                    encoded_path = urllib.parse.quote(item_path)
                    raw_url = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH}/{encoded_path}"
                    files_manifest[item_path] = {
                        "sha": item.get("sha"),
                        "download_url": raw_url
                    }
        else:
            print(f"{color.RED}[!] GitHub API server error ({response.status_code}){color.RESET}")
    except Exception as e:
        print(f"{color.RED}[!] Server connection failed: {e}{color.RESET}")
    return files_manifest

def run():
    """Main update function"""
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"{color.BLUE}=========================================={color.RESET}")
    print(f"{color.WHITE}             Update Feature               {color.RESET}")
    print(f"{color.BLUE}=========================================={color.RESET}\n")
    print(f"{color.GREEN}[+] Connecting to GitHub and checking for updates...{color.RESET}")
    manifest = fetch_repo_tree()
    if not manifest:
        print(f"{color.RED}[!] Unable to fetch update files. Please check your internet connection.{color.RESET}")
        print(f"\n{color.BLUE}=========================================={color.RESET}")
        return
    downloaded_count = 0
    updated_count = 0
    up_to_date_count = 0
    for relative_path, file_info in manifest.items():
        target_path = os.path.normpath(relative_path)
        expected_sha = file_info.get("sha")
        url = file_info.get("download_url")
        if not os.path.exists(target_path):
            print(f"{color.YELLOW}[+] New file detected: {target_path}{color.RESET}")
            if download_file(url, target_path):
                print(f"{color.GREEN}[✓] Downloaded: {target_path}{color.RESET}")
                downloaded_count += 1
        elif expected_sha:
            local_sha = calculate_github_sha1(target_path)
            if local_sha != expected_sha:
                print(f"{color.YELLOW}[!] New update available for file: {target_path}{color.RESET}")
                if download_file(url, target_path):
                    print(f"{color.GREEN}[✓] Updated: {target_path}{color.RESET}")
                    updated_count += 1
            else:
                up_to_date_count += 1
    print(f"\n{color.BLUE}------------------------------------------{color.RESET}")
    if downloaded_count == 0 and updated_count == 0:
        print(f"{color.GREEN}[✓] Your current version is already up to date!{color.RESET}")
    else:
        print(f"{color.GREEN}[✓] Update completed successfully!{color.RESET}")
        print(f"{color.WHITE}- New files downloaded: {downloaded_count}{color.RESET}")
        print(f"{color.WHITE}- Files updated: {updated_count}{color.RESET}")
    print(f"{color.BLUE}=========================================={color.RESET}")

if __name__ == "__main__":
    run()
