import socket
import color  # استدعاء ملف الألوان

DESCRIPTION = "Domain to IP Converter"
GROUP_ID = 1
COLOR = color.CYAN  # 🎨 تحديد لون الأداة

def run():
    print(color.color_text("\n--- أداة تحويل الدومين إلى IP ---", COLOR))
    domain = input("أدخل اسم الدومين: ").strip()
    if not domain:
        print(color.color_text("[!] لم يتم إدخال دومين.", color.RED))
        return

    domain = domain.replace("https://", "").replace("http://", "").split("/")[0]

    try:
        ip = socket.gethostbyname(domain)
        print(color.color_text(f"[+] IP الخاص بـ {domain} هو: {ip}", color.GREEN))
    except socket.gaierror:
        print(color.color_text(f"[!] تعذر الوصول إلى IP الخاص بـ {domain}", color.RED))
