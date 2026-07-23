import curses
import random
import time
try:
    from social import get_social_links
except ImportError:
    def get_social_links():
        return [("text", "Error: social.py file not found!")]
INFO_WHO_ME = [
    "I only help people, I am not a hacker or anything harmful to society. 🥺",
    "Name        : Baylak",
    "Country     : Egypt 🇪🇬",
    "Age         : 19",
    "Created     : 2026/07/23",
    "Version     : 1.0",
    "",
    "This project was created to help beginners and those with limited resources,",
    "so you might find the library you need right here! 🙂 Without needing a PC.",
    "",
    "Contribution Idea:",
    "Anyone can contribute and build tools, then send them via GitHub.",
    "We simply add them to a file called 'library'. It's very easy! 🙂",
    "Just contribute if you have coding experience. Note that library tools",
    "will NEVER be encrypted or suspicious—just standard clean Python code.",
]
INFO_DONATE = [
    "💖 DONATE / SUPPORT THE PROJECT:",
    "------------------------------------",
    "If you love this tool and want to support free open-source tools,",
    "you can support me via PayPal, Visa, or Crypto through the link below:",
    "",
    "🔗 baylak-egypt.blogspot.com/p/donate.html",
]
def load_frames():
    try:
        with open("Ascii_earth.txt", "r", encoding="utf-8") as f:
            raw = f.read().split("===FRAME===")
            return [frame for frame in raw if frame.strip()]
    except FileNotFoundError:
        return []
def get_animated_name(name="baylak", step=0):
    chars = list(name.lower())
    idx = step % len(chars)
    chars[idx] = chars[idx].upper()
    return "".join(chars)
def draw_static_menu(win, animated_name, color_green, color_white, color_cyan):
    max_y, max_x = win.getmaxyx()
    win.erase()
    border = "─" * max(0, max_x - 2)
    try:
        win.addstr(0, 0, border[: max_x - 1], color_cyan | curses.A_BOLD)
        header_str = f"DEV: {animated_name} "
        win.addstr(1, 1, header_str[: max_x - 2], color_cyan | curses.A_BOLD)
        win.addstr(
            3,
            2,
            f"[1] Who me?    [2] My Social"[: max_x - 3],
            color_white | curses.A_BOLD,
        )
        win.addstr(
            4,
            2,
            f"[3] Donate Me  [4] Back (Clear)"[: max_x - 3],
            color_white | curses.A_BOLD,
        )
        win.addstr(5, 2, f"[Q] Back to Main Menu"[: max_x - 3], color_green)
        win.addstr(6, 0, border[: max_x - 1], color_cyan | curses.A_BOLD)
    except curses.error:
        pass
    win.noutrefresh()
def animate_matrix_text(win, items):
    win.erase()
    max_y, max_x = win.getmaxyx()
    for i, item in enumerate(items):
        if i >= max_y:
            break
        if isinstance(item, tuple) and item[0] == "link":
            platform, link = item[1], item[2]
            line_str = f"{platform}{link}"
            for x, char in enumerate(line_str[: max_x - 3]):
                try:
                    color = (
                        curses.color_pair(4)
                        if x >= len(platform) + 2
                        else curses.color_pair(2)
                    )
                    win.addch(i, x + 2, char, color | curses.A_BOLD)
                except curses.error:
                    pass
                win.refresh()
                time.sleep(0.001)
        else:
            line = item[1] if isinstance(item, tuple) else item
            for x, char in enumerate(line[: max_x - 3]):
                try:
                    win.addch(
                        i, x + 2, char, curses.color_pair(2) | curses.A_BOLD
                    )
                except curses.error:
                    pass
                win.refresh()
                time.sleep(0.001)
        time.sleep(0.01)
def redraw_text_instantly(win, items):
    win.erase()
    max_y, max_x = win.getmaxyx()
    for i, item in enumerate(items):
        if i >= max_y:
            break
        try:
            if isinstance(item, tuple) and item[0] == "link":
                platform, link = item[1], item[2]
                win.addstr(
                    i, 2, platform, curses.color_pair(2) | curses.A_BOLD
                )
                win.addstr(
                    i,
                    2 + len(platform),
                    link[: max_x - 3 - len(platform)],
                    curses.color_pair(4) | curses.A_BOLD,
                )
            else:
                line = item[1] if isinstance(item, tuple) else item
                win.addstr(
                    i,
                    2,
                    line[: max_x - 3],
                    curses.color_pair(2) | curses.A_BOLD,
                )
        except curses.error:
            pass
    win.noutrefresh()
def about_main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, curses.COLOR_WHITE, -1)
    curses.init_pair(3, curses.COLOR_CYAN, -1)
    curses.init_pair(4, curses.COLOR_BLUE, -1)
    c_green = curses.color_pair(1)
    c_white = curses.color_pair(2)
    c_cyan = curses.color_pair(3)
    frames = load_frames()
    if not frames:
        stdscr.addstr(0, 0, "Error: Ascii_earth.txt not found!")
        stdscr.refresh()
        time.sleep(2)
        return
    current_text = None
    trigger_typewriter = False
    frame_idx = 0
    direction = 1
    name_step = 0
    stdscr.clear()
    while True:
        max_y, max_x = stdscr.getmaxyx()
        menu_height = 7
        key = stdscr.getch()
        if key == ord("1"):
            current_text = INFO_WHO_ME
            trigger_typewriter = True
        elif key == ord("2"):
            current_text = get_social_links()
            trigger_typewriter = True
        elif key == ord("3"):
            current_text = INFO_DONATE
            trigger_typewriter = True
        elif key == ord("4"):
            current_text = None
            trigger_typewriter = False
            stdscr.clear()
        elif key in [ord("q"), ord("Q")]:
            break
        if current_text is not None:
            earth_height = min(11, len(frames[0].strip().split("\n"))) if frames else 10
            text_height = max(1, max_y - earth_height - menu_height)
            earth_win = curses.newwin(earth_height, max_x, 0, 0)
            text_win = curses.newwin(text_height, max_x, earth_height, 0)
            menu_win = curses.newwin(
                menu_height, max_x, earth_height + text_height, 0
            )
        else:
            earth_height = max(1, max_y - menu_height)
            text_win = None
            earth_win = curses.newwin(earth_height, max_x, 0, 0)
            menu_win = curses.newwin(menu_height, max_x, earth_height, 0)
        if random.random() < 0.15:
            direction *= -1
        frame_idx += direction
        if frame_idx >= len(frames):
            frame_idx = max(0, len(frames) - 2)
            direction = -1
        elif frame_idx < 0:
            frame_idx = min(1, len(frames) - 1)
            direction = 1
        lines = frames[frame_idx].strip("\n").split("\n")
        if current_text is not None and text_win is not None:
            if trigger_typewriter:
                animate_matrix_text(text_win, current_text)
                trigger_typewriter = False
            else:
                redraw_text_instantly(text_win, current_text)
        earth_win.erase()
        for y in range(min(earth_height, len(lines))):
            line = lines[y]
            for x in range(min(max_x - 1, len(line))):
                char = line[x]
                if char not in [" ", "\n", "\r"]:
                    color_attr = (
                        c_green | curses.A_BOLD
                        if random.random() < 0.25
                        else c_green
                    )
                    try:
                        earth_win.addch(y, x, char, color_attr)
                    except curses.error:
                        pass
        earth_win.noutrefresh()
        name_step += 1
        animated_name = get_animated_name("Baylak", name_step)
        draw_static_menu(menu_win, animated_name, c_green, c_white, c_cyan)
        curses.doupdate()
        time.sleep(0.07)
def run():
    """Standard run function called by the main script"""
    try:
        curses.wrapper(about_main)
    except Exception:
        pass
if __name__ == "__main__":
    run()