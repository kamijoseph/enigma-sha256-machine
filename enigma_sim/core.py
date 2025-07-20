
# the enigma machine core code. the brain of the code
import hashlib
import string

# utility functions
def rotate_chars(c, offset):
    if c not in string.ascii_uppercase:
        return c
    return chr((ord(c) - 65 + offset) % 26 + 65)

def inverse_rotate_chars(c, offset):
    return rotate_chars(c, -offset)

def sha256_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def derive_settings_from_hash(hash_value):
    rotor_choices = [int(char, 16) % 5 for char in hash_value[:3]]
    positions = [string.ascii_uppercase[int(char, 16) % 26] for char in hash_value[3:6]]
    plugboard_pairs = [(string.ascii_uppercase[int(hash_value[i], 16) % 26],
                        string.ascii_uppercase[int(hash_value[i + 1], 16) % 26])
                       for i in range (6, 26, 2)]
    return {
        "rotors": rotor_choices,
        "positions": positions,
        "plugboard": plugboard_pairs
    }
    
# rotor method class
class Rotor:
    def __init__(self, wiring, notch, position='A'):
        self.wiring = wiring
        self.notch = notch
        self.position = position
        
    def encipher_forward(self, c):
        offset = string.ascii_uppercase.index(self.position)
        index = (string.ascii_uppercase.index(c) + offset) % 26
        return self.wiring[index]
    
    def encipher_backward(self, c):
        offset = string.ascii_uppercase.index(self.position)
        index = self.wiring.index(c)
        return string.ascii_uppercase[(index - offset) % 26]
    
    def step(self):
        self.position = rotate_chars(self.position, 1)
        return self.position == self.notch
    
# plugboard method class
class Plugboard:
    def __init__(self, connections):
        self.mapping = {a: b for a, b in connections}
        self.mapping.update({b: a for a, b in connections})
    
    def swap(self, c):
        return self.mapping.get(c, c)

# reflector method class   
class Reflector:
    def __init__(self, wiring):
        self.wiring = wiring
    
    def reflect(self, c):
        return self.wiring[string.ascii_uppercase.index(c)]

# main enigma machine class
class EnigmaMachine:
    def __init__(self, rotors, reflector, plugboard):
        self.rotors = rotors
        self.reflector = reflector
        self.plugboard = plugboard

    def encrypt_characters(self, c):
        if c not in string.ascii_uppercase:
            return c
        
        # step rotors
        rotate_next = self.rotors[-1].step()
        for i in reversed(range(len(self.rotors) - 1)):
            if rotate_next:
                rotate_next = self.rotors[i].step()
            else:
                break
        
        # plugboard in
        c = self.plugboard.swap(c)

        # forward rotors
        for rotor in reversed(self.rotors):
            c = rotor.encipher_forward(c)

        # reflect
        c = self.reflector.reflect(c)

        # backward rotors
        for rotor in self.rotors:
            c = rotor.encipher_backwards(c)

        # plugboard out
        return self.plugboard.swap(c)
    
    def message_encryption(self, message):
        return ''.join(self.encrypt_characters(c)
                       for c in message.upper()
                       if c in string.ascii_uppercase)

# default rtors and reflectors
ROTORS = [
    "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
    "AJDKSIRUXBLHWTMCQGZNPYFVOE",
    "BDFHJLCPRTXVZNYEIWGAKMUSQO",
    "ESOVPZJAYQUIRHXLNFTGKDCMWB",
    "VZBRGITYUPSDNHLXAWMJQOFECK"
]

NOTCHES = ['Q', 'E', 'V', 'J', 'Z']

REFLECTOR_B = "YRUHQSLDPXNGOKMIEBFZCWVJAT"