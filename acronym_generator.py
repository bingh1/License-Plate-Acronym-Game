import random

word_bank = {
    'A': ['Amazing', 'Angry', 'Awesome'],
    'B': ['Brave', 'Blue', 'Broken'],
    'C': ['Cool', 'Crazy', 'Cosmic'],
    'D': ['Dangerous', 'Dancing', 'Dark'],
    'E': ['Electric', 'Epic', 'Energetic'],
    'F': ['Flying', 'Fast', 'Fearless'],
    'G': ['Golden', 'Great', 'Gigantic'],
    'H': ['Happy', 'Hyper', 'Hungry'],
    'I': ['Invisible', 'Intense', 'Icy'],
    'J': ['Jumpy', 'Jazzy', 'Joyful'],
    'K': ['King', 'Kind', 'Killer'],
    'L': ['Legendary', 'Lucky', 'Loud'],
    'M': ['Magic', 'Mega', 'Mystic'],
    'N': ['Noble', 'Neon', 'Ninja'],
    'O': ['Orange', 'Omega', 'Odd'],
    'P': ['Powerful', 'Purple', 'Pixel'],
    'Q': ['Quick', 'Quantum', 'Quiet'],
    'R': ['Rapid', 'Royal', 'Radical'],
    'S': ['Super', 'Silent', 'Savage'],
    'T': ['Turbo', 'Tiny', 'Thunder'],
    'U': ['Ultra', 'Unknown', 'Unique'],
    'V': ['Velvet', 'Vicious', 'Virtual'],
    'W': ['Wild', 'Warp', 'Wise'],
    'X': ['Extreme', 'Xeno', 'Xtreme'],
    'Y': ['Yellow', 'Young', 'Yelling'],
    'Z': ['Zany', 'Zero', 'Zen']
}


def generate_acronym(letters):
    phrase = []

    for letter in letters:
        if letter in word_bank:
            phrase.append(random.choice(word_bank[letter]))

    return ' '.join(phrase)