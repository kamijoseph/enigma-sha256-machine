
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