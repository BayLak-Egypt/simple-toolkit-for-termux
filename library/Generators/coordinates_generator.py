import secrets
import color

DESCRIPTION = "Random GPS Coordinates & Geo-Location Generator"
GROUP_ID = 4  # Generators & Security Utilities
COLOR = color.CYAN

REGIONS = {
    "World (Global)": {"lat_range": (-90.0, 90.0), "lon_range": (-180.0, 180.0)},
    "Middle East": {"lat_range": (12.0, 37.0), "lon_range": (34.0, 60.0)},
    "North America": {"lat_range": (24.0, 71.0), "lon_range": (-168.0, -52.0)},
    "Europe": {"lat_range": (36.0, 71.0), "lon_range": (-10.0, 40.0)}
}

def generate_coordinates(region: str = "World (Global)") -> dict:
    """Generate random latitude and longitude within a specific regional bounding box."""
    if region not in REGIONS:
        region = "World (Global)"
        
    lat_min, lat_max = REGIONS[region]["lat_range"]
    lon_min, lon_max = REGIONS[region]["lon_range"]
    
    # Generate precise floating-point coordinates (6 decimal places ~ standard GPS precision)
    lat = lat_min + (lat_max - lat_min) * (secrets.randbelow(1000000) / 1000000.0)
    lon = lon_min + (lon_max - lon_min) * (secrets.randbelow(1000000) / 1000000.0)
    
    return {
        "Region": region,
        "Latitude": round(lat, 6),
        "Longitude": round(lon, 6),
        "Google Maps Link": f"https://maps.google.com/?q={lat:.6f},{lon:.6f}"
    }

def run():
    print(color.color_text("--- GPS Coordinates Generator ---", COLOR))
    print(" [1] World (Global)")
    print(" [2] Middle East")
    print(" [3] North America")
    print(" [4] Europe")

    choice = input("\nSelect region (default 1 - World): ").strip() or "1"
    mapping = {"1": "World (Global)", "2": "Middle East", "3": "North America", "4": "Europe"}
    region = mapping.get(choice, "World (Global)")

    try:
        count = int(input("How many coordinate sets to generate? (default 1): ").strip() or "1")
        if count < 1:
            count = 1
    except ValueError:
        count = 1

    print(color.color_text(f"\n[+] Generated Coordinates for {region}:\n", color.GREEN))
    for idx in range(1, count + 1):
        coord = generate_coordinates(region)
        print(color.color_text(f"--- Location #{idx} ---", color.YELLOW))
        print(f"  Latitude      : {coord['Latitude']}")
        print(f"  Longitude     : {coord['Longitude']}")
        print(f"  Maps URL      : {coord['Google Maps Link']}\n")
