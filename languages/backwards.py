from lib.langlib import *

# Language information
LANGUAGE_ID = "backwards"
LANGUAGE_TITLE = "Backwards"
LANGUAGE_VERSION = "0.1"
LANGUAGE_CREDITS = "2024 by Punga"
LANGUAGE_DESCRIPTION = "A playful language where words are spoken or written backward."

# Translates a string, and returns the result.
def translate(input_str: str) -> str:
    words = split_sentence(input_str)
    result_words = []
    for word in words:
        if not check_is_only_punctuation(word):
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

            result_words.append(word)
        else:
            result_words.append(word)

    return join_sentence(result_words)