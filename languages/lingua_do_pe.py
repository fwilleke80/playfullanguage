from lib.langlib import *

LANGUAGE_ID = "linguadope"
LANGUAGE_TITLE = "Língua do Pê"
LANGUAGE_VERSION = "0.1"
LANGUAGE_CREDITS = "2024 by Punga"
LANGUAGE_DESCRIPTION = "Popular in Brazil and Portugal, this language involves inserting the letter \"p\" before each vowel and repeating the vowel."


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
                    result_word += c + "p" + c
                else:
                    result_word += c

            # Restore upper case
            if is_uppercase:
                result_word = result_word.capitalize()

            result_words.append(result_word)
        else:
            result_words.append(word)

    return join_sentence(result_words)