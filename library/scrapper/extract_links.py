import urllib.request
import re
import color

DESCRIPTION = "Extract Links from Webpage"
GROUP_ID = 1  # أدوات الشبكات واستخراج البيانات
COLOR = color.MAGENTA

def run():
    print(color.color_text("--- أداة استخراج الروابط من صفحة ويب ---", COLOR))
    url = input("أدخل رابط الموقع: ").strip()
    
    if not url:
        print(color.color_text("[!] لم يتم إدخال رابط.", color.RED))
        return

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Android; Mobile)'}
        )
        with urllib.request.urlopen(req, timeout=6) as response:
            html = response.read().decode('utf-8', errors='ignore')
            
            # البحث عن جميع الروابط باستخدام Regular Expressions
            links = set(re.findall(r'href=["\'](https?://[^\s"\']+)["\']', html))
            
            print(color.color_text(f"\n[+] تم العثور على {len(links)} رابط فريد:\n", color.GREEN))
            for i, link in enumerate(links, 1):
                print(f"  [{i}] {color.CYAN}{link}{color.RESET}")

    except Exception as e:
        print(color.color_text(f"\n[!] تعذر جلب الروابط: {e}", color.RED))
