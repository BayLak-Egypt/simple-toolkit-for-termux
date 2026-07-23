import secrets
import color

DESCRIPTION = "Random User-Agent String Generator"
GROUP_ID = 4  # Generators & Security Utilities
COLOR = color.CYAN

USER_AGENTS = {
    "Chrome / Windows": [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    ],
    "Chrome / macOS": [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    ],
    "Firefox / Windows": [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0"
    ],
    "Safari / macOS": [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15"
    ],
    "Safari / iOS (iPhone)": [
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/605.1.15"
    ],
    "Chrome / Android": [
        "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.64 Mobile Safari/537.36"
    ]
}

def get_random_user_agent(category: str = None) -> str:
    """Get a random User-Agent string from specified or all categories."""
    if category and category in USER_AGENTS:
        return secrets.choice(USER_AGENTS[category])
    
    all_agents = [ua for list_ua in USER_AGENTS.values() for ua in list_ua]
    return secrets.choice(all_agents)

def run():
    print(color.color_text("--- User-Agent String Generator ---", COLOR))
    
    categories = list(USER_AGENTS.keys())
    print("Select Category:")
    print(" [0] Completely Random (Any Platform)")
    for idx, cat in enumerate(categories, 1):
        print(f" [{idx}] {cat}")

    choice = input("\nSelect option: ").strip()

    if choice == "0":
        ua = get_random_user_agent()
        print(color.color_text(f"\n[+] Generated User-Agent:\n{ua}", color.GREEN))
    elif choice.isdigit() and 1 <= int(choice) <= len(categories):
        selected_cat = categories[int(choice) - 1]
        ua = get_random_user_agent(selected_cat)
        print(color.color_text(f"\n[+] Generated {selected_cat} User-Agent:\n{ua}", color.GREEN))
    else:
        print(color.color_text("[!] Invalid option.", color.RED))
