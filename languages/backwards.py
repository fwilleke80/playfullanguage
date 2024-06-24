from lib.langlib import *

# Language information
LANGUAGE_ID = "backwards"
LANGUAGE_TITLE = "Backwards"
LANGUAGE_VERSION = "0.1"
LANGUAGE_CREDITS = "2024 by Punga"
LANGUAGE_DESCRIPTION = "A playful language where words are spoken or written backward."

# Translates a single word.
def translate_word(word) -> str:
    # Inspect word
    starts_with_vowel = check_starts_with_vowel(word)
    is_uppercase = check_is_first_char_uppercase(word)

    # Make word lower case
    word = word.lower()

    # Translate
    word = word[::-1]

    # Restore upper case
    if is_uppercase:
        word = word.capitalize()

    return word