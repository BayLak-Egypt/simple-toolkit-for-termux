import urllib.request
import color

DESCRIPTION = "HTTP Headers & Status Inspector"
GROUP_ID = 1  # مجموعة أدوات الشبكات
COLOR = color.MAGENTA

def run():
    print(color.color_text("--- أداة فحص ترويسات الموقع (HTTP Headers) ---", COLOR))
    url = input("أدخل رابط الموقع (مثال: https://example.com): ").strip()
    
    if not url:
        print(color.color_text("[!] لم يتم إدخال رابط.", color.RED))
        return

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Termux Utility)'}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            print(color.color_text(f"\n[+] حالة الاستجابة (Status Code): {response.status}", color.GREEN))
            print(color.color_text("\n--- الترويسات (Headers) ---", color.WHITE))
            for header, value in response.getheaders():
                print(f"  {color.CYAN}{header}{color.RESET}: {value}")

    except Exception as e:
        print(color.color_text(f"\n[!] تعذر الاتصال بالموقع: {e}", color.RED))
