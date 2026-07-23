import color

DESCRIPTION = "Morse Code Encoder / Decoder"
GROUP_ID = 3  # Miscellaneous Tools
COLOR = color.CYAN

MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
    '9': '----.', '0': '-----', ' ': '/'
}

REVERSE_MORSE = {value: key for key, value in MORSE_CODE_DICT.items()}

def run():
    print(color.color_text("--- Morse Code Tool ---", COLOR))
    print(" [1] Encode text to Morse Code")
    print(" [2] Decode Morse Code to text")
    
    choice = input("\nSelect an option: ").strip()
    
    if choice == "1":
        text = input("Enter text to encode: ").strip().upper()
        encoded = ' '.join(MORSE_CODE_DICT.get(char, '') for char in text)
        print(color.color_text(f"\n[+] Encoded Morse Code:\n{encoded}", color.GREEN))
        
    elif choice == "2":
        morse_text = input("Enter Morse Code (space between letters, / for words): ").strip()
        try:
            words = morse_text.split(' / ')
            decoded_words = []
            for word in words:
                letters = word.split()
                decoded_word = ''.join(REVERSE_MORSE.get(letter, '') for letter in letters)
                decoded_words.append(decoded_word)
            
            print(color.color_text(f"\n[+] Decoded text:\n{' '.join(decoded_words)}", color.GREEN))
        except Exception:
            print(color.color_text("\n[!] Invalid Morse Code format.", color.RED))
    else:
        print(color.color_text("[!] Invalid option.", color.RED))
