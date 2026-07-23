import color

DESCRIPTION = "Baconian Cipher Encoder / Decoder"
GROUP_ID = 3  # Miscellaneous Tools
COLOR = color.CYAN

# Baconian Dictionary (Standard 26-letter version)
BACON_DICT = {
    'A': 'AAAAA', 'B': 'AAAAB', 'C': 'AAABA', 'D': 'AAABB', 'E': 'AABAA',
    'F': 'AABAB', 'G': 'AABBA', 'H': 'AABBB', 'I': 'ABAAA', 'J': 'ABAAB',
    'K': 'ABABA', 'L': 'ABABB', 'M': 'ABBAA', 'N': 'ABBAB', 'O': 'ABBBA',
    'P': 'ABBBB', 'Q': 'BAAAA', 'R': 'BAAAB', 'S': 'BAABA', 'T': 'BAABB',
    'U': 'BABAA', 'V': 'BABAB', 'W': 'BABBA', 'X': 'BABBB', 'Y': 'BBAAA',
    'Z': 'BBAAB'
}

REVERSE_BACON = {value: key for key, value in BACON_DICT.items()}

def run():
    print(color.color_text("--- Baconian Cipher Tool ---", COLOR))
    print(" [1] Encode text to Baconian")
    print(" [2] Decode Baconian to text")
    
    choice = input("\nSelect an option: ").strip()
    
    if choice == "1":
        text = input("Enter text to encode: ").strip().upper()
        encoded_list = [BACON_DICT[char] for char in text if char in BACON_DICT]
        encoded_str = ' '.join(encoded_list)
        print(color.color_text(f"\n[+] Encoded Baconian Cipher:\n{encoded_str}", color.GREEN))
        
    elif choice == "2":
        bacon_text = input("Enter Baconian string (A/B groups): ").strip().upper()
        # Clean string and extract 5-character blocks
        clean_input = bacon_text.replace(" ", "")
        
        if len(clean_input) % 5 != 0:
            print(color.color_text("\n[!] Invalid Baconian string length (must be multiple of 5).", color.RED))
            return
            
        blocks = [clean_input[i:i+5] for i in range(0, len(clean_input), 5)]
        decoded = ''.join(REVERSE_BACON.get(block, '?') for block in blocks)
        print(color.color_text(f"\n[+] Decoded text:\n{decoded}", color.GREEN))
        
    else:
        print(color.color_text("[!] Invalid option.", color.RED))
