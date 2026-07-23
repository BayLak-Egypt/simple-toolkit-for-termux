import color

DESCRIPTION = "Solitaire / Pontifex Card-Based Cipher"
GROUP_ID = 3  # Miscellaneous Tools
COLOR = color.CYAN

# Initial deck setup (1 to 52 for cards, 53 for Joker A, 54 for Joker B)
def init_deck() -> list:
    return list(range(1, 55))

def key_stream_step(deck: list) -> int:
    """Perform one step of the Solitaire deck shuffle algorithm."""
    # 1. Move Joker A (53) down 1 position
    idx_a = deck.index(53)
    deck.pop(idx_a)
    deck.insert((idx_a + 1) % 53 if idx_a + 1 > 53 else idx_a + 1, 53)

    # 2. Move Joker B (54) down 2 positions
    idx_b = deck.index(54)
    deck.pop(idx_b)
    new_idx_b = (idx_b + 2) % 53 if idx_b + 2 > 53 else idx_b + 2
    deck.insert(new_idx_b, 54)

    # 3. Triple Cut around Jokers
    i_a = deck.index(53)
    i_b = deck.index(54)
    first_j = min(i_a, i_b)
    second_j = max(i_a, i_b)

    top = deck[:first_j]
    mid = deck[first_j:second_j + 1]
    bot = deck[second_j + 1:]
    deck[:] = bot + mid + top

    # 4. Count Cut using bottom card
    bot_card = deck[-1]
    val = 53 if bot_card in [53, 54] else bot_card
    deck[:] = deck[val:-1] + deck[:val] + [deck[-1]]

    # 5. Output key byte
    top_card = deck[0]
    output_idx = 53 if top_card in [53, 54] else top_card
    out_val = deck[output_idx]

    if out_val in [53, 54]:
        return key_stream_step(deck)  # Skip Jokers
    return out_val % 26

def solitaire_encrypt(text: str) -> str:
    deck = init_deck()
    clean_text = [c.upper() for c in text if c.isalpha()]
    result = []
    
    for char in clean_text:
        shift = key_stream_step(deck)
        p = ord(char) - ord('A')
        c = (p + shift) % 26
        result.append(chr(c + ord('A')))
        
    return "".join(result)

def solitaire_decrypt(cipher: str) -> str:
    deck = init_deck()
    clean_cipher = [c.upper() for c in cipher if c.isalpha()]
    result = []
    
    for char in clean_cipher:
        shift = key_stream_step(deck)
        c = ord(char) - ord('A')
        p = (c - shift) % 26
        result.append(chr(p + ord('A')))
        
    return "".join(result)

def run():
    print(color.color_text("--- Solitaire (Pontifex) Cipher Tool ---", COLOR))
    print(" [1] Encrypt text")
    print(" [2] Decrypt text")

    choice = input("\nSelect an option: ").strip()

    if choice in ["1", "2"]:
        text = input("Enter text (A-Z letters): ").strip()
        if not text:
            print(color.color_text("[!] Text cannot be empty.", color.RED))
            return

        if choice == "1":
            output = solitaire_encrypt(text)
        else:
            output = solitaire_decrypt(text)

        print(color.color_text(f"\n[+] Result:\n{output}", color.GREEN))
    else:
        print(color.color_text("[!] Invalid option.", color.RED))
