import os
import platform
import color

DESCRIPTION = "Termux & System Info"
GROUP_ID = 4  # Miscellaneous Tools
COLOR = color.GREEN

def run():
    print(color.color_text("--- System & Device Info ---", COLOR))
    
    print(f"  {color.WHITE}OS:{color.RESET} {platform.system()} {platform.release()}")
    print(f"  {color.WHITE}Architecture:{color.RESET} {platform.machine()}")
    print(f"  {color.WHITE}Python Version:{color.RESET} {platform.python_version()}")
    print(f"  {color.WHITE}Current Directory:{color.RESET} {os.getcwd()}")
    
    # Check available storage space
    try:
        stat = os.statvfs('/')
        free_gb = (stat.f_bavail * stat.f_frsize) / (1024 ** 3)
        print(f"  {color.WHITE}Available Space:{color.RESET} {free_gb:.2f} GB")
    except AttributeError:
        pass
