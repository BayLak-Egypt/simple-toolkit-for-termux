import color

DESCRIPTION = "Historical Enigma Machine (I / M3) Simulator"
GROUP_ID = 3  # Miscellaneous Tools
COLOR = color.CYAN

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Historical Enigma Rotor Configurations (Wiring, Notch)
ROTORS = {
    'I':   {'wiring': 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'notch': 'Q'},
    'II':  {'wiring': 'AJDKSIRUXBLHWTMCQGZNPYFVOE', 'notch': 'E'},
    'III': {'wiring': 'BDFHJLCPRTXVZNYEIWGAKMUSQO', 'notch': 'V'},
    'IV':  {'wiring': 'ESOVPZJAYQUIRHXLNFTGKDCMWB', 'notch': 'J'},
    'V':   {'wiring': 'VZBRGITYUPSDNHLXAWMJQOFECK', 'notch': 'Z'}
}

# Reflector B Wiring
REFLECTOR_B = "YRUHQSLDPXNGOKMIEBFZCWVJAT"

class EnigmaRotor:
    def __init__(self, wiring: str, notch: str, pos='A', ring='A'):
        self.wiring = wiring
        self.notch = notch
        self.pos = ord(pos) - ord('A')
        self.ring = ord(ring) - ord('A')

    def step(self) -> bool:
        """Step rotor forward by 1 position. Returns True if notch is hit."""
        at_notch = (ALPHABET[self.pos] == self.notch)
        self.pos = (self.pos + 1) % 26
        return at_notch

    def forward(self, char_idx: int) -> int:
        shift = self.pos - self.ring
        index = (char_idx + shift) % 26
        wired_char = self.wiring[index]
        return (ord(wired_char) - ord('A') - shift) % 26

    def backward(self, char_idx: int) -> int:
        shift = self.pos - self.ring
        index = (char_idx + shift) % 26
        wired_char = ALPHABET[index]
        pos_in_wiring = self.wiring.index(wired_char)
        return (pos_in_wiring - shift) % 26

class EnigmaMachine:
    def __init__(self, rotor_names: list, positions: list, rings: list, plugboard_pairs: list):
        self.left = EnigmaRotor(ROTORS[rotor_names[0]]['wiring'], ROTORS[rotor_names[0]]['notch'], positions[0], rings[0])
        self.middle = EnigmaRotor(ROTORS[rotor_names[1]]['wiring'], ROTORS[rotor_names[1]]['notch'], positions[1], rings[1])
        self.right = EnigmaRotor(ROTORS[rotor_names[2]]['wiring'], ROTORS[rotor_names[2]]['notch'], positions[2], rings[2])
        self.reflector = REFLECTOR_B
        
        # Build plugboard map
        self.plugboard = {c: c for c in ALPHABET}
        for pair in plugboard_pairs:
            if len(pair) == 2:
                u, v = pair[0].upper(), pair[1].upper()
                self.plugboard[u] = v
                self.plugboard[v] = u

    def step_rotors(self):
        """Handle Enigma rotor stepping including double stepping mechanism."""
        middle_at_notch = (ALPHABET[self.middle.pos] == self.middle.notch)
        right_at_notch = (ALPHABET[self.right.pos] == self.right.notch)

        if middle_at_notch:
            self.left.step()
            self.middle.step()
            self.right.step()
        elif right_at_notch:
            self.middle.step()
            self.right.step()
        else:
            self.right.step()

    def process_char(self, char: str) -> str:
        if not char.isalpha():
            return char

        char = char.upper()
        self.step_rotors()

        # 1. Plugboard
        x = ord(self.plugboard[char]) - ord('A')

        # 2. Rotors (Right to Left)
        x = self.right.forward(x)
        x = self.middle.forward(x)
        x = self.left.forward(x)

        # 3. Reflector
        x = ord(self.reflector[x]) - ord('A')

        # 4. Rotors (Left to Right)
        x = self.left.backward(x)
        x = self.middle.backward(x)
        x = self.right.backward(x)

        # 5. Plugboard
        out_char = ALPHABET[x]
        return self.plugboard[out_char]

    def process_text(self, text: str) -> str:
        return "".join([self.process_char(c) for c in text])

def run():
    print(color.color_text("--- Enigma Machine Simulator (I / M3) ---", COLOR))
    
    text = input("Enter text to encrypt/decrypt: ").strip()
    if not text:
        print(color.color_text("[!] Text cannot be empty.", color.RED))
        return

    rotors_in = input("Select 3 Rotors (e.g. I II III): ").strip().upper().split()
    if len(rotors_in) != 3 or not all(r in ROTORS for r in rotors_in):
        rotors_in = ['I', 'II', 'III']
        print(color.color_text("[*] Defaulting to Rotors: I II III", color.YELLOW))

    positions_in = input("Enter Initial Rotor Positions (e.g. A B C): ").strip().upper().split()
    if len(positions_in) != 3:
        positions_in = ['A', 'A', 'A']
        print(color.color_text("[*] Defaulting Positions to: A A A", color.YELLOW))

    plugs_in = input("Enter Plugboard Pairs (e.g. AB CD EF or leave empty): ").strip().upper().split()

    machine = EnigmaMachine(
        rotor_names=rotors_in,
        positions=positions_in,
        rings=['A', 'A', 'A'],
        plugboard_pairs=plugs_in
    )

    output = machine.process_text(text)
    print(color.color_text(f"\n[+] Output Text:\n{output}", color.GREEN))
