from lib.langlib import *

LANGUAGE_ID = "paffke"
LANGUAGE_TITLE = "Paffke"
LANGUAGE_VERSION = "0.1"
LANGUAGE_CREDITS = "2024 by Punga"
LANGUAGE_DESCRIPTION = "The Paffke language."

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
            result_word = ""
            for c in word:
                if check_starts_with_vowel(c):
                    result_word += c + "paff" + c
                else:
                    result_word += c
            result_word += ("e" if result_word[-1] == "k" else "") + "ke"

            # Restore upper case
            if is_uppercase:
                result_word = result_word.capitalize()

            result_words.append(result_word)
        else:
            result_words.append(word)

    return join_sentence(result_words)