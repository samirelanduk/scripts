#! /usr/bin/env python3

import sys
from collections import Counter

letters = {
    "a": 9, "e": 12, "i": 9, "o": 8, "u": 4, "y": 2,
    "b": 2, "c": 2, "d": 4, "f": 2, "g": 3, "h": 2, "j": 1,
    "k": 1, "l": 4, "m": 2, "n": 6, "p": 2, "q": 1, "r": 6,
    "s": 4, "t": 6, "v": 2, "w": 2, "x": 1, "z": 1
    }

if len(sys.argv) <= 1:
    print("Provide a phrase.")
else:
    phrase = " ".join(sys.argv[1:]).lower()

    needed = Counter([c for c in phrase if c.isalpha()])
    violations = []
    for letter in needed:
        if needed[letter] > letters[letter]:
            violations.append(letter)

    if not violations:
        print("Fine.")
    else:
        print("Not fine:")
        for violation in sorted(violations):
            print("\tNeed %i %s tiles but there are only %i" % (
             needed[violation],
             violation.upper(),
             letters[violation]
            ))
    

