#/usr/bin/env python3
"""
VERNAM CIPHER
It's a historical one-time pad cipher obtained by logical XOR between plaintext and a key with the same length.
"""

import string
import random
#from operator import xor


def generate_key(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))      # Generate a random string (letters and digits) of the length of the plaintext


def encrypt(text, key):
    return ''.join([chr(text[i] ^ key[i]) for i in range(len(key))]).encode()           # Merge the XOR values into an encoded string 
        

if __name__ == '__main__':
    text = input('Type your text: ')
    text = text.replace(' ', '').lower()

    key = generate_key(len(text))
    print(f'Random key: {key}')
    
    enc_text = encrypt(text.encode(), key.encode())
    print(f'\nCiphertext: {enc_text}')
