import re
import urllib.request
def get_social_links():
    """جلب الروابط وتنسيقها للرسم الملون"""
    url = "https://raw.githubusercontent.com/BayLak-Egypt/baylak-egypt.github.io/refs/heads/main/mysocial.txt"
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            content = response.read().decode("utf-8").strip()
        matches = re.findall(r"(\w+)\s*=\s*(\S+)", content)
        if not matches:
            return [("text", "⚠️ No social links found.")]
        formatted_data = [
            ("text", "🌐 MY SOCIAL MEDIA (Live Scrape):"),
            ("text", "------------------------------------"),
        ]
        for platform, raw_link in matches:
            clean_link = re.sub(r"^(https?://)?(www\.)?", "", raw_link).strip()
            platform_name = platform.capitalize().ljust(10)
            formatted_data.append(
                ("link", platform_name, f" : {clean_link}")
            )
        return formatted_data
    except Exception:
        return [
            ("text", "⚠️ CONNECTION ERROR:"),
            ("text", "------------------------------------"),
            ("text", "Failed to fetch links from GitHub."),
        ]