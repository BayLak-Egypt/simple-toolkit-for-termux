import color

DESCRIPTION = "Cron Expression Generator & Explainer"
GROUP_ID = 4  # Generators & Security Utilities
COLOR = color.CYAN

def generate_cron(minute="*", hour="*", day_of_month="*", month="*", day_of_week="*") -> str:
    """Combine cron time parts into a standard 5-part cron expression."""
    return f"{minute} {hour} {day_of_month} {month} {day_of_week}"

def run():
    print(color.color_text("--- Cron Expression Generator ---", COLOR))
    print("Select a common preset or build custom:\n")
    print(" [1] Every minute (* * * * *)")
    print(" [2] Every hour at minute 0 (0 * * * *)")
    print(" [3] Every day at midnight (0 0 * * *)")
    print(" [4] Every Sunday at midnight (0 0 * * 0)")
    print(" [5] Custom Cron Expression")

    choice = input("\nSelect option: ").strip()

    if choice == "1":
        expr = generate_cron()
        desc = "Runs every single minute."
    elif choice == "2":
        expr = generate_cron(minute="0")
        desc = "Runs every hour, at minute 0."
    elif choice == "3":
        expr = generate_cron(minute="0", hour="0")
        desc = "Runs once a day at midnight (00:00)."
    elif choice == "4":
        expr = generate_cron(minute="0", hour="0", day_of_week="0")
        desc = "Runs once a week on Sunday at midnight (00:00)."
    elif choice == "5":
        min_in = input("Minute (0-59, *, or */N) [default *]: ").strip() or "*"
        hr_in = input("Hour (0-23, *, or */N) [default *]: ").strip() or "*"
        dom_in = input("Day of Month (1-31, *) [default *]: ").strip() or "*"
        mon_in = input("Month (1-12, *) [default *]: ").strip() or "*"
        dow_in = input("Day of Week (0-6, 0=Sun, *) [default *]: ").strip() or "*"
        
        expr = generate_cron(min_in, hr_in, dom_in, mon_in, dow_in)
        desc = f"Custom schedule configuration."
    else:
        print(color.color_text("[!] Invalid option.", color.RED))
        return

    print(color.color_text(f"\n[+] Generated Cron Expression:\n{expr}", color.GREEN))
    print(color.color_text(f"[*] Schedule Summary: {desc}", color.YELLOW))
