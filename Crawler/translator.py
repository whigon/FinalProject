"""
    Based on Python 3.7
    @author Yuexiang LI
"""

# /h/, /j/, /w/: unsigned
# /ŋ/ could be 2, 27 or 7, to avoid ambiguity, /ŋ/ represents 27
# g is not ɡ
consonants_map = {"s": 0, "z": 0, "t": 1, "d": 1, "n": 2, "m": 3, "r": 4, "l": 5, "tʃ": 6, "ʃ": 6, "dʒ": 6, "ʒ": 6,
                  "k": 7, "ɡ": 7, "g": 7, "f": 8, "v": 8, "p": 9, "b": 9, "ŋ": 27}


def covert2digit(consonant):
    """
    Convert consonants into digits and join them into a number
    :param consonant:
    :return:
    """
    number = ""

    for c in consonant:
        number += str(consonants_map[c])

    return number


def extract_consonant(phonetic_symbol):
    """
    Extract consonants from phonetic symbols

    :param phonetic_symbol:
    :return:
    """
    consonant = []
    # print(len(phonetic_symbol))

    i = 0
    while i < len(phonetic_symbol):
        if phonetic_symbol[i] in consonants_map.keys():
            if phonetic_symbol[i] != "t" and phonetic_symbol[i] != "d":
                consonant.append(phonetic_symbol[i])
            else:
                # Is last symbol
                if i == len(phonetic_symbol) - 1:
                    consonant.append(phonetic_symbol[i])
                else:
                    # To detect tʃ
                    if phonetic_symbol[i] == "t" and phonetic_symbol[i + 1] == "ʃ":
                        consonant.append("tʃ")
                        i += 1
                    elif phonetic_symbol[i] == "t":
                        consonant.append("t")
                    # To detect dʒ
                    if phonetic_symbol[i] == "d" and phonetic_symbol[i + 1] == "ʃ":
                        consonant.append("dʒ")
                        i += 1
                    elif phonetic_symbol[i] == "d":
                        consonant.append("d")
        i += 1

    print(consonant)
    return consonant


'''
if __name__ == '__main__':
    print(1)
    digit = covert2digit(extract_consonant("ˌæmbɪˈɡjuːəti"))
    print(digit)
    digit = covert2digit(extract_consonant("/'gri:n/"))
    print(digit)

    digit = covert2digit(extract_consonant("pensl"))
    print(digit)
    print("g")
'''
