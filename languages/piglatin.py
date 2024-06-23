from lib.langlib import *

LANGUAGE_ID = "pig"
LANGUAGE_TITLE = "Pig Latin"
LANGUAGE_VERSION = "0.1"
LANGUAGE_CREDITS = "2024 by Punga"
LANGUAGE_DESCRIPTION = "Igpay Atinlay. Good for English."


def translate(input_str: str) -> str:
    words = split_sentence(input_str)
    result_words = []
    for word in words:
        # Is this even a word?
        if not check_is_only_punctuation(word):
            # Inspect word
            starts_with_vowel = check_starts_with_vowel(word)
            is_uppercase = check_is_first_char_uppercase(word)

            # Make word lower case
            word = word.lower()

            # Word starts with a consonant
            if not starts_with_vowel:
                # Move first consonant (or consonant cluster) to end of word
                move_pos = 0
                for c in word:
                    if check_starts_with_vowel(c):
                        break
                    move_pos += 1
                move_chunk = word[0:move_pos]
                remaining_word = word[move_pos:]
                word = remaining_word + move_chunk + "lay"

                # Restore upper case
                if is_uppercase:
                    word = word.capitalize()
                
            else: # Word starts with a vowel
                word = word + "lay"

        result_words.append(word)

    return join_sentence(result_words)