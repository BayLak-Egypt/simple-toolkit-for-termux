import os
import platform
import color

DESCRIPTION = "Host Latency & Ping Check"
GROUP_ID = 2  # أدوات الفحص والتحليل
COLOR = color.YELLOW

def run():
    print(color.color_text("--- أداة فحص زمن الاستجابة (Ping) ---", COLOR))
    target = input("أدخل IP أو الدومين: ").strip()
    
    if not target:
        print(color.color_text("[!] لم يتم إدخال هدف.", color.RED))
        return

    # تنظيف المدخلات
    target = target.replace("https://", "").replace("http://", "").split("/")[0]

    # تحديد خيار عدد مرات البينج حسب نظام التشغيل
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = f"ping {param} 4 {target}"

    print(color.color_text(f"\n[i] جاري إرسال الطلبات إلى {target}...\n", color.WHITE))
    response = os.system(command)
    
    if response == 0:
        print(color.color_text(f"\n[+] الاتصال بـ {target} ناجح!", color.GREEN))
    else:
        print(color.color_text(f"\n[!] فشل الاتصال بـ {target}.", color.RED))
