import base64
import color

DESCRIPTION = "Base64 Encoder / Decoder"
GROUP_ID = 3  # أدوات متنوعة
COLOR = color.CYAN

def run():
    print(color.color_text("--- أداة Base64 ---", COLOR))
    print(" [1] تشفير نص إلى Base64")
    print(" [2] فك تشفير Base64 إلى نص")
    
    choice = input("\nاختر العملية: ").strip()
    
    if choice == "1":
        text = input("أدخل النص للتشفير: ").strip()
        encoded = base64.b64encode(text.encode()).decode()
        print(color.color_text(f"\n[+] النص المشفر:\n{encoded}", color.GREEN))
        
    elif choice == "2":
        encoded_text = input("أدخل نص Base64 لفك التشفير: ").strip()
        try:
            decoded = base64.b64decode(encoded_text.encode()).decode()
            print(color.color_text(f"\n[+] النص الأصلي:\n{decoded}", color.GREEN))
        except Exception:
            print(color.color_text("\n[!] كود Base64 غير صالح.", color.RED))
    else:
        print(color.color_text("[!] خيار غير صحيح.", color.RED))
