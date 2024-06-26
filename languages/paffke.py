from lib.langlib import *

# Language information
LANGUAGE_ID = "paffke"
LANGUAGE_TITLE = "Paffke"
LANGUAGE_VERSION = "0.1"
LANGUAGE_CREDITS = "2024 by Punga"
LANGUAGE_DESCRIPTION = "The Paffke language."

# Translates a single word.
def translate_word(word) -> str:
    # Inspect word
    starts_with_vowel = check_starts_with_vowel(word)
    is_uppercase = check_is_first_char_uppercase(word)

    # Make word lower case
    word = word.lower()

    # Translate
    result_word = ""
    letters = list(iterate_letters_with_clusters(word))
    for c in letters:
        if check_starts_with_vowel(c):
            result_word += c + "paff" + c
        else:
            result_word += c
    result_word += ("e" if result_word[-1] == "k" else "") + "ke"

    # Restore upper case
    if is_uppercase:
        result_word = result_word.capitalize()

    return result_word