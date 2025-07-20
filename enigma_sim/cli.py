
# command line entry
from .core import (
    EnigmaMachine, Rotor, Plugboard, Reflector, sha256_hash,
    derive_settings_from_hash, ROTORS, REFLECTOR_B
)

def enigma_cli():
    print(">>>>> Enigma Machine Simulator <<<<<")
    mode = input("Mode (Encrypt/Decrypt): ").strip().lower()
    message = input('Enter Message: ').strip().upper()
    
    if mode == "encrypt":
        pass_phrase = input('Enter Pass Phrase').strip()
        hashed = sha256_hash(pass_phrase)
        settings = derive_settings_from_hash(hashed)
    elif mode == "decrypt":
        hashed = input("Enter the SHA256 hash of the config: ").strip()
        settings = derive_settings_from_hash(hashed)
    else:
        print("Invalid mode of operation. Enter 'Encrypt' or 'Decrypt'")
        return
    
    rotors = [Rotor(ROTORS[i], notch='Q', position=p) for i, p in zip(settings['rotors'], settings['positions'])]
    plugboard = Plugboard(settings['plugboard'])
    reflector = Reflector(REFLECTOR_B)
    machine = EnigmaMachine(rotors, reflector, plugboard)

    result = machine.message_encryption(message)

    print("\n>>>>> Results <<<<<")
    print(f"Result: {result}")
    print(f"Hash {hashed}")