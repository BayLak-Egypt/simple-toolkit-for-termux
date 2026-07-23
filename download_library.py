import os
import requests
import core_links
def download_file(filename, file_info, output_dir="library"):
    """تنزيل أو تحديث الملف داخل مجلد library"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    filepath = os.path.join(output_dir, filename)
    custom_res = core_links.execute_custom_download(filename, file_info, output_dir)
    if custom_res is not None:
        return custom_res
    download_url = file_info.get("download_url")
    if not download_url:
        print(f"\033[1;31m[!] No download URL or custom downloader found for {filename}\033[0m")
        return False
    print(f"\033[1;34m[*] Downloading '{filename}' directly...\033[0m")
    try:
        response = requests.get(download_url, timeout=15)
        if response.status_code == 200:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, "wb") as f:
                f.write(response.content)
            print(f"\033[1;32m[+] Successfully updated: {filepath}\033[0m")
            return True
        else:
            print(f"\033[1;31m[!] Download failed for {filename} (HTTP {response.status_code})\033[0m")
    except Exception as e:
        print(f"\033[1;31m[!] Connection error while downloading {filename}: {e}\033[0m")
    return False