import color

DESCRIPTION = "z-base32 Human-Oriented Encoder / Decoder"
GROUP_ID = 3  # Miscellaneous Tools
COLOR = color.CYAN

# z-base32 Alphabet (Designed to avoid easily confused characters like 0, O, 1, l, I)
ZBASE32_ALPHABET = "ybndrfg8ejkmcpqxot1uwisza345h769"
ZBASE32_MAP = {char: idx for idx, char in enumerate(ZBASE32_ALPHABET)}

def zbase32_encode(data: bytes) -> str:
    """Encode binary data/bytes to z-base32 string."""
    buffer = 0
    bits_in_buffer = 0
    result = []

    for byte in data:
        buffer = (buffer << 8) | byte
        bits_in_buffer += 8

        while bits_in_buffer >= 5:
            bits_in_buffer -= 5
            index = (buffer >> bits_in_buffer) & 0x1F
            result.append(ZBASE32_ALPHABET[index])

    if bits_in_buffer > 0:
        index = (buffer << (5 - bits_in_buffer)) & 0x1F
        result.append(ZBASE32_ALPHABET[index])

    return "".join(result)

def zbase32_decode(zstr: str) -> bytes:
    """Decode z-base32 string back to bytes."""
    buffer = 0
    bits_in_buffer = 0
    result = bytearray()

    for char in zstr.lower():
        if char not in ZBASE32_MAP:
            continue  # Ignore invalid whitespace/delimiters
        
        val = ZBASE32_MAP[char]
        buffer = (buffer << 5) | val
        bits_in_buffer += 5

        if bits_in_buffer >= 8:
            bits_in_buffer -= 8
            result.append((buffer >> bits_in_buffer) & 0xFF)

    return bytes(result)

def run():
    print(color.color_text("--- z-base32 Encoder / Decoder ---", COLOR))
    print(" [1] Encode text to z-base32")
    print(" [2] Decode z-base32 to text")

    choice = input("\nSelect an option: ").strip()

    if choice == "1":
        text = input("Enter text to encode: ").strip()
        if not text:
            print(color.color_text("[!] Text cannot be empty.", color.RED))
            return
        encoded = zbase32_encode(text.encode('utf-8'))
        print(color.color_text(f"\n[+] Encoded z-base32:\n{encoded}", color.GREEN))

    elif choice == "2":
        zstr = input("Enter z-base32 string to decode: ").strip()
        if not zstr:
            print(color.color_text("[!] Input cannot be empty.", color.RED))
            return
        try:
            decoded = zbase32_decode(zstr).decode('utf-8', errors='replace')
            print(color.color_text(f"\n[+] Decoded Text:\n{decoded}", color.GREEN))
        except Exception as e:
            print(color.color_text(f"\n[!] Decoding Error: {e}", color.RED))

    else:
        print(color.color_text("[!] Invalid option.", color.RED))
