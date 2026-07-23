import color

DESCRIPTION = "Rail Fence (Zig-Zag) Cipher Tool"
GROUP_ID = 3  # Miscellaneous Tools
COLOR = color.CYAN

def encrypt_rail_fence(text: str, key: int) -> str:
    if key <= 1:
        return text

    rail = [['\n' for _ in range(len(text))] for _ in range(key)]
    dir_down = False
    row, col = 0, 0

    for char in text:
        if row == 0 or row == key - 1:
            dir_down = not dir_down
        rail[row][col] = char
        col += 1
        row += 1 if dir_down else -1

    result = []
    for i in range(key):
        for j in range(len(text)):
            if rail[i][j] != '\n':
                result.append(rail[i][j])
    return "".join(result)

def decrypt_rail_fence(cipher: str, key: int) -> str:
    if key <= 1:
        return cipher

    rail = [['\n' for _ in range(len(cipher))] for _ in range(key)]
    dir_down = None
    row, col = 0, 0

    for i in range(len(cipher)):
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False
        rail[row][col] = '*'
        col += 1
        row += 1 if dir_down else -1

    index = 0
    for i in range(key):
        for j in range(len(cipher)):
            if rail[i][j] == '*' and index < len(cipher):
                rail[i][j] = cipher[index]
                index += 1

    result = []
    row, col = 0, 0
    for i in range(len(cipher)):
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False
        if rail[row][col] != '*':
            result.append(rail[row][col])
            col += 1
        row += 1 if dir_down else -1
    return "".join(result)

def run():
    print(color.color_text("--- Rail Fence Cipher Tool ---", COLOR))
    print(" [1] Encrypt text")
    print(" [2] Decrypt text")
    
    choice = input("\nSelect an option: ").strip()
    
    if choice in ["1", "2"]:
        text = input("Enter text: ").strip()
        try:
            rails = int(input("Enter number of rails (key >= 2): ").strip())
        except ValueError:
            print(color.color_text("[!] Rails count must be an integer.", color.RED))
            return

        if rails < 2:
            print(color.color_text("[!] Key/Rails must be at least 2.", color.RED))
            return

        if choice == "1":
            output = encrypt_rail_fence(text, rails)
        else:
            output = decrypt_rail_fence(text, rails)

        print(color.color_text(f"\n[+] Result:\n{output}", color.GREEN))
    else:
        print(color.color_text("[!] Invalid option.", color.RED))
