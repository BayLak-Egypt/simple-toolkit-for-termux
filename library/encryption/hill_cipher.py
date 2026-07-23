import numpy as np
import color

DESCRIPTION = "Hill Cipher (Matrix 2x2) Encoder / Decoder"
GROUP_ID = 3  # Miscellaneous Tools
COLOR = color.CYAN

def mod_inverse(a, m=26):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def text_to_nums(text):
    return [ord(c) - ord('A') for c in text.upper() if c.isalpha()]

def nums_to_text(nums):
    return "".join(chr(n + ord('A')) for n in nums)

def hill_encrypt(text, key_matrix):
    nums = text_to_nums(text)
    if len(nums) % 2 != 0:
        nums.append(ord('X') - ord('A'))  # Padding
    
    result = []
    for i in range(0, len(nums), 2):
        pair = np.array(nums[i:i+2])
        enc_pair = np.dot(key_matrix, pair) % 26
        result.extend(enc_pair)
        
    return nums_to_text(result)

def hill_decrypt(text, key_matrix):
    nums = text_to_nums(text)
    det = int(np.round(np.linalg.det(key_matrix))) % 26
    det_inv = mod_inverse(det, 26)
    
    if det_inv is None:
        return None
        
    # Adjugate matrix for 2x2
    adj = np.array([
        [key_matrix[1][1], -key_matrix[0][1]],
        [-key_matrix[1][0], key_matrix[0][0]]
    ]) % 26
    
    inv_matrix = (det_inv * adj) % 26
    
    result = []
    for i in range(0, len(nums), 2):
        pair = np.array(nums[i:i+2])
        dec_pair = np.dot(inv_matrix, pair) % 26
        result.extend(dec_pair)
        
    return nums_to_text(result)

def run():
    print(color.color_text("--- Hill Cipher (2x2 Matrix) ---", COLOR))
    print(" [1] Encrypt text")
    print(" [2] Decrypt text")
    
    choice = input("\nSelect an option: ").strip()
    
    if choice in ["1", "2"]:
        text = input("Enter text (letters only): ").strip()
        print("\nEnter 4 numbers for 2x2 matrix key (e.g. 3, 3, 2, 5):")
        try:
            k11 = int(input("K[0,0]: ").strip())
            k12 = int(input("K[0,1]: ").strip())
            k21 = int(input("K[1,0]: ").strip())
            k22 = int(input("K[1,1]: ").strip())
        except ValueError:
            print(color.color_text("[!] Key values must be integers.", color.RED))
            return

        key_matrix = np.array([[k11, k12], [k21, k22]])
        det = int(np.round(np.linalg.det(key_matrix))) % 26
        
        if mod_inverse(det, 26) is None:
            print(color.color_text("[!] Invalid matrix key: Determinant has no inverse modulo 26.", color.RED))
            return

        if choice == "1":
            output = hill_encrypt(text, key_matrix)
        else:
            output = hill_decrypt(text, key_matrix)

        print(color.color_text(f"\n[+] Result:\n{output}", color.GREEN))
    else:
        print(color.color_text("[!] Invalid option.", color.RED))
