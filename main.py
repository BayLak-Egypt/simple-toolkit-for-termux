import os
import sys
import importlib.util
import json
import random
import color
LIBRARY_DIR = os.path.join(os.path.dirname(__file__), 'library')
GROUP_FILE_PATH = os.path.join(LIBRARY_DIR, 'group.js')
UPDATE_FILE_PATH = os.path.join(os.path.dirname(__file__), 'update.py')
ABOUT_FILE_PATH = os.path.join(os.path.dirname(__file__), 'about.py')
STAR_TXT_PATH = os.path.join(os.path.dirname(__file__), 'star.txt')
CHECK_FILE_PATH = os.path.join(os.path.dirname(__file__), 'check.py')
CHECK_CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'check.js')
_FIXED_THEME = None
def get_fixed_theme():
    """اختيار لون عشوائي وثبته طوال فترة تشغيل الأداة"""
    global _FIXED_THEME
    if _FIXED_THEME is None:
        themes = [
            ((255, 60, 0), (255, 220, 0)),
            ((255, 0, 100), (255, 150, 200)),
            ((0, 255, 150), (0, 220, 255)),
            ((180, 0, 255), (255, 100, 255)),
            ((255, 200, 0), (100, 255, 100)),
        ]
        _FIXED_THEME = random.choice(themes)
    return _FIXED_THEME
def apply_gradient_to_text(text, start_rgb, end_rgb):
    result = ""
    total_chars = len(text)
    for idx, char in enumerate(text):
        if char == " ":
            result += " "
            continue
        factor = idx / (total_chars - 1) if total_chars > 1 else 0
        r = int(start_rgb[0] + factor * (end_rgb[0] - start_rgb[0]))
        g = int(start_rgb[1] + factor * (end_rgb[1] - start_rgb[1]))
        b = int(start_rgb[2] + factor * (end_rgb[2] - start_rgb[2]))
        result += f"\033[1;38;2;{r};{g};{b}m{char}\033[0m"
    return result
def show_star_banner():
    """عرض البانر باللون الثابت الذي لا يتغير عند التنقل بين الصفحات"""
    if not os.path.exists(STAR_TXT_PATH):
        print(f"{color.BLUE}=========================================={color.RESET}")
        print(f"{color.WHITE}         Simple-ToolKit-For-Termux          {color.RESET}")
        print(f"{color.BLUE}=========================================={color.RESET}\n")
        return
    try:
        with open(STAR_TXT_PATH, 'r', encoding='utf-8') as file:
            lines = [line.rstrip() for line in file.readlines()]
        total_lines = len(lines)
        if total_lines == 0:
            return
        mid_index = total_lines // 2
        line1_index = mid_index - 1
        line2_index = mid_index
        star_start_color = (30, 80, 200)
        star_end_color = (120, 220, 255)
        text_start_color, text_end_color = get_fixed_theme()
        styled_termux = apply_gradient_to_text("Termux", text_start_color, text_end_color)
        styled_toolkit = apply_gradient_to_text("Toolkit V1.0", text_start_color, text_end_color)
        reset_color = "\033[0m"
        for i, line in enumerate(lines):
            factor = i / (total_lines - 1) if total_lines > 1 else 0
            r = int(star_start_color[0] + factor * (star_end_color[0] - star_start_color[0]))
            g = int(star_start_color[1] + factor * (star_end_color[1] - star_start_color[1]))
            b = int(star_start_color[2] + factor * (star_end_color[2] - star_start_color[2]))
            star_color = f"\033[38;2;{r};{g};{b}m"
            if i == line1_index:
                print(f"{star_color}{line}{reset_color} {styled_termux}")
            elif i == line2_index:
                print(f"{star_color}{line}{reset_color}  {styled_toolkit}")
            else:
                print(f"{star_color}{line}{reset_color}")
    except Exception as e:
        print(f"{color.RED}[!] Error displaying star banner: {e}{color.RESET}")
def load_auto_check_setting():
    """قراءة حالة الفحص التلقائي من ملف check.js (افتراضياً True إذا لم يوجد الملف)"""
    if not os.path.exists(CHECK_CONFIG_PATH):
        return True
    try:
        with open(CHECK_CONFIG_PATH, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if "=" in content:
                content = content.split("=", 1)[1].strip()
            if content.endswith(";"):
                content = content[:-1].strip()
            data = json.loads(content)
            return data.get("auto_check", True)
    except Exception:
        return True
def save_auto_check_setting(status):
    """حفظ حالة الفحص التلقائي داخل ملف check.js"""
    try:
        data = {"auto_check": status}
        with open(CHECK_CONFIG_PATH, 'w', encoding='utf-8') as f:
            f.write(f"const autoCheckConfig = {json.dumps(data, indent=4)};\n")
    except Exception as e:
        print(f"{color.RED}[!] Error saving check.js: {e}{color.RESET}")
def run_checker():
    """تشغيل ملف check.py يدوياً أو عند الحاجة"""
    os.system('clear' if os.name == 'posix' else 'cls')
    show_star_banner()
    print()
    if os.path.exists(CHECK_FILE_PATH):
        try:
            spec = importlib.util.spec_from_file_location("check_module", CHECK_FILE_PATH)
            if spec and spec.loader:
                check_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(check_module)
                if hasattr(check_module, "run"):
                    check_module.run()
                print(f"\033[1;32m[+] Environment check completed.\033[0m\n")
        except Exception as e:
            print(f"\033[1;31m[!] Error running check.py: {e}{color.RESET}")
    else:
        print(f"{color.RED}[!] check.py file not found.{color.RESET}")
    input(f"\n{color.WHITE}Press Enter to return...{color.RESET}")
def run_checker_at_startup():
    """تشغيل ملف check.py تلقائياً عند بدء التشغيل إذا كان الخيار مفعل"""
    if load_auto_check_setting() and os.path.exists(CHECK_FILE_PATH):
        try:
            spec = importlib.util.spec_from_file_location("check_module", CHECK_FILE_PATH)
            if spec and spec.loader:
                check_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(check_module)
                if hasattr(check_module, "run"):
                    check_module.run()
                print(f"\033[1;32m[+] Environment check completed.\033[0m\n")
        except Exception as e:
            print(f"\033[1;31m[!] Error running check.py: {e}{color.RESET}")
            input("\nPress Enter to continue anyway...")
def load_groups():
    if not os.path.exists(GROUP_FILE_PATH):
        return {}
    try:
        with open(GROUP_FILE_PATH, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if "=" in content:
                content = content.split("=", 1)[1].strip()
            if content.endswith(";"):
                content = content[:-1].strip()
            groups_data = json.loads(content)
            for g_id, g_info in groups_data.items():
                color_name = g_info.get('color', 'WHITE').upper()
                g_info['color'] = getattr(color, color_name, color.WHITE)
            return groups_data
    except Exception as e:
        print(f"{color.RED}[!] Error reading group.js: {e}{color.RESET}")
        return {}
def load_plugins():
    plugins = []
    if not os.path.exists(LIBRARY_DIR):
        os.makedirs(LIBRARY_DIR)
        return plugins
    for root, dirs, files in os.walk(LIBRARY_DIR):
        for filename in files:
            if filename == "group.js":
                continue
            if filename.endswith(".py") and not filename.startswith("__"):
                plugin_name = filename[:-3]
                module_path = os.path.join(root, filename)
                relative_path = os.path.relpath(module_path, LIBRARY_DIR)
                unique_module_name = relative_path.replace(os.sep, ".").replace(".py", "")
                try:
                    spec = importlib.util.spec_from_file_location(unique_module_name, module_path)
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        sys.modules[unique_module_name] = module
                        spec.loader.exec_module(module)
                        if hasattr(module, "run"):
                            description = getattr(module, "DESCRIPTION", plugin_name)
                            group_id = getattr(module, "GROUP_ID", 3)
                            tool_color = getattr(module, "COLOR", color.WHITE)
                            plugins.append({
                                "name": plugin_name,
                                "description": description,
                                "group_id": group_id,
                                "color": tool_color,
                                "module": module
                            })
                except Exception as e:
                    print(f"{color.RED}[!] Error loading file {filename}: {e}{color.RESET}")
    return plugins
def run_updater():
    os.system('clear' if os.name == 'posix' else 'cls')
    show_star_banner()
    print()
    if os.path.exists(UPDATE_FILE_PATH):
        try:
            spec = importlib.util.spec_from_file_location("update_module", UPDATE_FILE_PATH)
            if spec and spec.loader:
                update_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(update_module)
                if hasattr(update_module, "run"):
                    update_module.run()
                else:
                    print(f"{color.YELLOW}[!] update.py does not contain a run() function.{color.RESET}")
                    input(f"\n{color.WHITE}Press Enter to return...{color.RESET}")
        except Exception as e:
            print(f"{color.RED}[!] An error occurred during update: {e}{color.RESET}")
            input(f"\n{color.WHITE}Press Enter to return...{color.RESET}")
    else:
        print(f"{color.RED}[!] update.py file not found in the main directory.{color.RESET}")
        input(f"\n{color.WHITE}Press Enter to return...{color.RESET}")
def show_about():
    os.system('clear' if os.name == 'posix' else 'cls')
    show_star_banner()
    print()
    if os.path.exists(ABOUT_FILE_PATH):
        try:
            spec = importlib.util.spec_from_file_location("about_module", ABOUT_FILE_PATH)
            if spec and spec.loader:
                about_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(about_module)
                if hasattr(about_module, "run"):
                    about_module.run()
                else:
                    print(f"{color.YELLOW}[!] about.py does not contain a run() function.{color.RESET}")
                    input(f"\n{color.WHITE}Press Enter to return...{color.RESET}")
        except Exception as e:
            print(f"{color.RED}[!] An error occurred while opening About: {e}{color.RESET}")
            input(f"\n{color.WHITE}Press Enter to return...{color.RESET}")
    else:
        print(f"{color.RED}[!] about.py file not found in the main directory.{color.RESET}")
        input(f"\n{color.WHITE}Press Enter to return...{color.RESET}")
def show_group_menu(g_info, g_id):
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        show_star_banner()
        print()
        plugins = load_plugins()
        group_tools = [p for p in plugins if p["group_id"] == g_id]
        print(f"{g_info['color']}=========================================={color.RESET}")
        print(f"{g_info['color']}    {g_info['title']}    {color.RESET}")
        print(f"{color.WHITE}    {g_info['description']}    {color.RESET}")
        print(f"{g_info['color']}=========================================={color.RESET}\n")
        if not group_tools:
            print(f"{color.RED}[!] No tools currently available in this group.{color.RESET}")
        else:
            for idx, tool in enumerate(group_tools, 1):
                print(f"  [{idx}] {tool['color']}{tool['description']}{color.RESET}")
        print(f"\n{color.RED}[0] Return to Main Menu{color.RESET}")
        print(f"{g_info['color']}=========================================={color.RESET}")
        choice = input(f"{color.CYAN}Enter tool number: {color.RESET}").strip()
        if choice == "0":
            break
        if choice.isdigit() and 1 <= int(choice) <= len(group_tools):
            selected = group_tools[int(choice) - 1]
            os.system('clear' if os.name == 'posix' else 'cls')
            show_star_banner()
            print(f"\n{selected['color']}--- Running: {selected['description']} ---{color.RESET}\n")
            try:
                selected["module"].run()
            except Exception as e:
                print(f"{color.RED}[!] Error during execution: {e}{color.RESET}")
            print(f"\n{color.RED}[0] Press Enter or 0 to return to group menu...{color.RESET}")
            input()
        else:
            print(f"{color.RED}[!] Invalid choice, numbers only.{color.RESET}")
            input(f"{color.WHITE}Press Enter to continue...{color.RESET}")
def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    run_checker_at_startup()
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        show_star_banner()
        print()
        groups = load_groups()
        plugins = load_plugins()
        current_auto_check = load_auto_check_setting()
        if not plugins:
            print(f"{color.RED}[!] No extensions found inside library folder.{color.RESET}")
            check_status_str = f"{color.GREEN}true{color.RESET}" if current_auto_check else f"{color.RED}false{color.RESET}"
            print(f"  [1] auto check and download library ({check_status_str})")
            print(f"{color.BLUE}[2] check and download library{color.RESET}")
            print(f"{color.YELLOW}[3] Update Tool{color.RESET}")
            print(f"{color.CYAN}[4] About{color.RESET}")
            print(f"{color.RED}[0] Exit{color.RESET}")
            choice = input(f"\n{color.CYAN}Choose a number: {color.RESET}").strip()
            if choice == "1":
                save_auto_check_setting(not current_auto_check)
                continue
            if choice == "2":
                run_checker()
                continue
            if choice == "3":
                run_updater()
                continue
            if choice == "4":
                show_about()
                continue
            if choice == "0":
                break
            continue
        available_groups = []
        for g_id, g_info in groups.items():
            try:
                numeric_g_id = int(g_id)
            except ValueError:
                numeric_g_id = g_id
            tools_in_group = [p for p in plugins if p["group_id"] == numeric_g_id]
            if tools_in_group:
                available_groups.append((numeric_g_id, g_info))
        if not available_groups:
            print(f"{color.RED}[!] No tools linked to current groups in group.js.{color.RESET}")
            check_status_str = f"{color.GREEN}true{color.RESET}" if current_auto_check else f"{color.RED}false{color.RESET}"
            print(f"\n  [1] auto check and download library ({check_status_str})")
            print(f"{color.BLUE}[2] check and download library{color.RESET}")
            print(f"{color.YELLOW}[3] Update Tool{color.RESET}")
            print(f"{color.CYAN}[4] About{color.RESET}")
            print(f"{color.RED}[0] Exit{color.RESET}")
            choice = input(f"\n{color.CYAN}Choose a number: {color.RESET}").strip()
            if choice == "1":
                save_auto_check_setting(not current_auto_check)
                continue
            if choice == "2":
                run_checker()
                continue
            if choice == "3":
                run_updater()
                continue
            if choice == "4":
                show_about()
                continue
            if choice == "0":
                break
            continue
        for idx, (g_id, g_info) in enumerate(available_groups, 1):
            tools_count = len([p for p in plugins if p["group_id"] == g_id])
            print(f"  [{idx}] {g_info['color']}{g_info['title']}{color.RESET} {color.WHITE}({tools_count}){color.RESET}")
        auto_check_option_num = len(available_groups) + 1
        checker_button_num = len(available_groups) + 2
        update_option_num = len(available_groups) + 3
        about_option_num = len(available_groups) + 4
        check_status_str = f"{color.GREEN}true{color.RESET}" if current_auto_check else f"{color.RED}false{color.RESET}"
        print(f"\n  [{auto_check_option_num}] auto check and download library ({check_status_str})")
        print(f"{color.BLUE}[{checker_button_num}] check and download library{color.RESET}")
        print(f"{color.YELLOW}[{update_option_num}] Update {color.RESET}")
        print(f"{color.CYAN}[{about_option_num}] About{color.RESET}")
        print(f"{color.RED}[0] Exit{color.RESET}")
        print(f"{color.BLUE}=========================================={color.RESET}")
        choice = input(f"{color.CYAN}Enter group number: {color.RESET}").strip()
        if choice == "0":
            print(f"\n{color.GREEN}Exited successfully. Goodbye!{color.RESET}")
            break
        if choice.isdigit():
            choice_num = int(choice)
            if 1 <= choice_num <= len(available_groups):
                selected_g_id, selected_g_info = available_groups[choice_num - 1]
                show_group_menu(selected_g_info, selected_g_id)
            elif choice_num == auto_check_option_num:
                save_auto_check_setting(not current_auto_check)
            elif choice_num == checker_button_num:
                run_checker()
            elif choice_num == update_option_num:
                run_updater()
            elif choice_num == about_option_num:
                show_about()
            else:
                print(f"{color.RED}[!] Invalid number choice.{color.RESET}")
                input(f"{color.WHITE}Press Enter to continue...{color.RESET}")
        else:
            print(f"{color.RED}[!] Numbers only allowed.{color.RESET}")
            input(f"{color.WHITE}Press Enter to continue...{color.RESET}")
if __name__ == "__main__":
    main()
