import requests
from urllib.parse import quote
def fetch_server_manifest(server_info):
    """
    جلب كافة الملفات من GitHub مع معالجة المسافات وتجاهل ملفات pycache
    """
    owner = server_info.get("owner")
    repo = server_info.get("repo")
    branch = server_info.get("branch", "main")
    target_path = server_info.get("path", "").strip("/")
    api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    headers = {
        "User-Agent": "Library-Checker-App",
        "Accept": "application/vnd.github.v3+json"
    }
    manifest = {}
    try:
        response = requests.get(api_url, headers=headers, timeout=15)
        if response.status_code == 200:
            tree_data = response.json().get("tree", [])
            for item in tree_data:
                item_path = item.get("path", "")
                if "__pycache__" in item_path or item_path.endswith(".pyc") or ".git" in item_path:
                    continue
                if item.get("type") == "blob":
                    if not target_path or item_path.startswith(f"{target_path}/"):
                        relative_path = item_path[len(target_path)+1:] if target_path else item_path
                        encoded_item_path = quote(item_path)
                        raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{encoded_item_path}"
                        manifest[relative_path] = {
                            "hash": item.get("sha"),
                            "download_url": raw_url
                        }
        else:
            print(f"\033[1;31m[!] GitHub API Error ({response.status_code}): {response.text}\033[0m")
    except Exception as e:
        print(f"\033[1;31m[!] Connection Error with GitHub: {e}\033[0m")
    return manifest