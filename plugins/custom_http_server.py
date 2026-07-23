import requests
def fetch_server_manifest(server_info):
    """
    جلب قائمة الملفات والهاشات من سيرفر عادي عبر ملف manifest.json
    """
    base_url = server_info.get("base_url", "").rstrip("/")
    manifest_file = server_info.get("manifest_file", "manifest.json")
    manifest_url = f"{base_url}/{manifest_file}"
    headers = {"User-Agent": "Library-Checker-App"}
    manifest = {}
    try:
        response = requests.get(manifest_url, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            for file_path, file_hash in data.items():
                manifest[file_path] = {
                    "hash": file_hash,
                    "download_url": f"{base_url}/{file_path}"
                }
        else:
            print(f"\033[1;31m[!] Custom Server Error ({response.status_code})\033[0m")
    except Exception as e:
        print(f"\033[1;31m[!] Failed to connect to Custom Server: {e}\033[0m")
    return manifest