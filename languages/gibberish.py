from lib.langlib import *

# Language information
LANGUAGE_ID = "gibberish"
LANGUAGE_TITLE = "Gibberish"
LANGUAGE_VERSION = "0.1"
LANGUAGE_CREDITS = "2024 by Punga"
LANGUAGE_DESCRIPTION = "In Gibberish, you typically add \"idig\" or \"idig\" (sometimes \"itherg\") before each vowel sound in a word."

# Translates a single word.
def translate_word(word) -> str:
    # Inspect word
    starts_with_vowel = check_starts_with_vowel(word)
    is_uppercase = check_is_first_char_uppercase(word)

    # Make word lower case
    word = word.lower()

    # Translate
    result_word = ""
    for c in word:
        if check_starts_with_vowel(c):
            result_word += "idig" + c
        else:
            result_word += c

    # Restore upper case
    if is_uppercase:
        result_word = result_word.capitalize()

    return result_word