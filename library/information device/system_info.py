import os
import platform
import color

DESCRIPTION = "Termux & System Info"
GROUP_ID = 3  # مجموعة الأدوات المتنوعة
COLOR = color.GREEN

def run():
    print(color.color_text("--- معلومات النظام والجهاز ---", COLOR))
    
    print(f"  {color.WHITE}النظام (OS):{color.RESET} {platform.system()} {platform.release()}")
    print(f"  {color.WHITE}المعالج (Architecture):{color.RESET} {platform.machine()}")
    print(f"  {color.WHITE}إصدار بايثون:{color.RESET} {platform.python_version()}")
    print(f"  {color.WHITE}المجلد الحالي:{color.RESET} {os.getcwd()}")
    
    # فحص المساحة المتبقية
    try:
        stat = os.statvfs('/')
        free_gb = (stat.f_bavail * stat.f_frsize) / (1024 ** 3)
        print(f"  {color.WHITE}المساحة المتاحة:{color.RESET} {free_gb:.2f} GB")
    except AttributeError:
        pass
