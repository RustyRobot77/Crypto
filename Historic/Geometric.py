#!/usr/bin/env python3

"""
GEOMETRIC SHAPE CIPHER
A classic transposition cipher.
The text is first mapped in a table, usualy row by row, padded if necessary.
Then, the cipher is formed by proceeding through the table in secret path, until all letters are covered.

The receiver can decrypt the cipher by simply following the reverse path.

This is sometimes called "route cipher".
"""

import math
import secrets
import pandas as pd


TEXT = 'Type your text here...'

# Setup values for padding                                              # I have chosen to square the text before encryption to avoid exposing the tail as plaintext
PADDING_CHAR = '_'                                                      # Select the char for the padding
RANDOM_PADDING = False                                                  # If False, the text is padded at the end; if True, the text is padded at random positions                                               
REMOVE_PADDING = True                                                   # If True, all the padding chars are removed after encryption


def squaring(text):
    side = math.sqrt(len(text))                                         # Approximate the side of the squared text from its length
    if not side.is_integer():                                           # If the text does not produce a perfect square, adjust the side and add padding
        side = int(side) + 1
        while len(text) < pow(side, 2):                                 # Pad until the text is long enough for a perfect square
            if RANDOM_PADDING:
                index = secrets.randbelow(len(text))                    # Produce a random index in the text
                text = text[:index] + PADDING_CHAR + text[index:]       # Add the pad
            else:
                text += PADDING_CHAR
    else:
        side = int(side)
        
    text = list(text)
    chunks = [text[side*i:side*i + side] for i in range(len(text[::side]))]         # Chunk the text in pieces as long as the side of the square
    table = pd.DataFrame(columns=range(side))                                       # Create a pandas table as wide as the square side
    for i in range(side):                                                           # Feed the table with the text chunks
        table.loc[i] = chunks[i]
    return table


def snake(text):
    enc_text = ''
    table = squaring(text)                                                # Square the text
    for y in range(len(table)):
        if y % 2 == 0:                                                    # If columns are even, proceed downwards
            for x in range(len(table)):
                enc_text += table.loc[x, y]
        else:                                                             # If the columns are odd, proceed upwards
            for x in range(len(table) - 1, -1, -1):
                enc_text += table.loc[x, y]
    return enc_text


def diagonal(text):
    table = squaring(text)                                                # Square the text
    enc_text = ''
    for x in range(len(table) - 1, -1, -1):                               # Start from the bottom left corner and proceed upwards
        y = 0
        for i in range(x, len(table)):                                    # This process encrypts untill the top left diagonal, then stops
            enc_text += table.loc[i, y]
            y += 1
    for y in range(1, len(table)):                                        # Conclude the other half of the square, proceed from top left to bottom right
        x = 0
        for i in range(y, len(table)):                                    # Concludes at the top right corner
            enc_text += table.loc[x, i]
            x += 1
    return enc_text


def geometric_encrypt(text):                                              # I created two examples, one following diagonal path, the other snaking through from left to right
    enc_text = diagonal(text)                                             
    enc_text = snake(enc_text)
    if REMOVE_PADDING:
        return enc_text.replace(PADDING_CHAR, '')
    else:
        return enc_text

    
if __name__ == '__main__':
    # Encryption
    TEXT = TEXT.replace(' ', '')                                        # Remove spaces between words
    enc_text = geometric_encrypt(TEXT)
    print(f'\nCiphertext: {enc_text}')
