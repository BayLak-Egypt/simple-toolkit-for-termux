import color
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

DESCRIPTION = "LSB Image Steganography (Hide/Extract Text in PNG)"
GROUP_ID = 3  # Miscellaneous Tools
COLOR = color.CYAN

def text_to_bits(text: str) -> str:
    bits = bin(int.from_bytes(text.encode('utf-8'), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def bits_to_text(bits: str) -> str:
    try:
        n = int(bits, 2)
        return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode('utf-8', errors='replace')
    except Exception:
        return "[!] Invalid or corrupted binary data."

def hide_text_in_image(image_path: str, secret_text: str, output_path: str):
    image = Image.open(image_path).convert('RGB')
    
    # Append delimiter to know where message ends
    full_text = secret_text + "###END###"
    binary_secret = text_to_bits(full_text)
    
    pixels = list(image.getdata())
    if len(binary_secret) > len(pixels) * 3:
        raise ValueError("Secret text is too long for this image size.")

    new_pixels = []
    data_idx = 0

    for pixel in pixels:
        r, g, b = pixel
        channels = [r, g, b]

        for i in range(3):
            if data_idx < len(binary_secret):
                # Set LSB to secret bit
                channels[i] = (channels[i] & ~1) | int(binary_secret[data_idx])
                data_idx += 1

        new_pixels.append(tuple(channels))

    image.putdata(new_pixels)
    image.save(output_path, "PNG")

def extract_text_from_image(image_path: str) -> str:
    image = Image.open(image_path).convert('RGB')
    pixels = list(image.getdata())

    extracted_bits = []
    for pixel in pixels:
        for channel in pixel[:3]:
            extracted_bits.append(str(channel & 1))

    # Convert bits to string in chunks of 8
    all_bits = "".join(extracted_bits)
    bytes_data = bytearray()
    
    for i in range(0, len(all_bits), 8):
        byte = all_bits[i:i+8]
        if len(byte) < 8:
            break
        bytes_data.append(int(byte, 2))
        
        # Check for delimiter in recent output
        decoded_so_far = bytes_data.decode('utf-8', errors='ignore')
        if "###END###" in decoded_so_far:
            return decoded_so_far.split("###END###")[0]

    return "[!] No hidden message found or delimiter missing."

def run():
    print(color.color_text("--- LSB Image Steganography Tool ---", COLOR))

    if not PIL_AVAILABLE:
        print(color.color_text("[!] Pillow library is required for this tool.", color.RED))
        print("Install it using: pip install Pillow")
        return

    print(" [1] Hide secret text inside an image (PNG)")
    print(" [2] Extract secret text from an image")

    choice = input("\nSelect an option: ").strip()

    if choice == "1":
        img_path = input("Enter source image path (e.g. input.png): ").strip()
        secret = input("Enter secret message to hide: ").strip()
        out_path = input("Enter output image path (e.g. stego.png): ").strip()

        try:
            hide_text_in_image(img_path, secret, out_path)
            print(color.color_text(f"\n[+] Success! Hidden image saved to: {out_path}", color.GREEN))
        except Exception as e:
            print(color.color_text(f"\n[!] Error: {e}", color.RED))

    elif choice == "2":
        img_path = input("Enter stego image path (e.g. stego.png): ").strip()
        try:
            extracted = extract_text_from_image(img_path)
            print(color.color_text(f"\n[+] Extracted Secret Message:\n{extracted}", color.GREEN))
        except Exception as e:
            print(color.color_text(f"\n[!] Error: {e}", color.RED))

    else:
        print(color.color_text("[!] Invalid option.", color.RED))
