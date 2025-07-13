
# command line entry
from .core import (
    EnigmaMachine, Rotor, Plugboard, Reflector, sha256_hash,
    drive_settings_from_hash, ROTORS, REFLECTOR_B
)

def enigma_cli():
    mode = input("Mode (Encryot/Decrypt): ").strip().lower()
    message = input('Enter Message: ').strip().upper()
    
    if mode == "encrypt":
        config_str = input('Enter Pass Phrase').strip()
        hashed = sha256_hash(config_str)
        settings = drive_settings_from_hash(hashed)
    elif mode == "decrypt":
        hashed = input("Enter the SHA256 hash of the config: ").strip()
        settings = drive_settings_from_hash(hashed)
    else:
        print("Invalid mode of Operation entered")
        return
    
    rotors = [Rotor(ROTORS[i], notch='Q', position=p) for i, p in zip(settings['rotors'], settings['positions'])]
    plugboard = Plugboard(settings['plugboard'])
    reflector = Reflector(REFLECTOR_B)
    machine = EnigmaMachine(rotors, reflector, plugboard)
    
    result = machine.encrypt_message(message)
    print(f"Result: {result}")
    print(f"Hash {hashed}")