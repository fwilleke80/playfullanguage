import random
from lib.langlib import *

# Language information
LANGUAGE_ID = "berlin"
LANGUAGE_TITLE = "Berlinisch"
LANGUAGE_VERSION = "0.1"
LANGUAGE_CREDITS = "2024 by Punga"
LANGUAGE_DESCRIPTION = "Berlinischer Dialekt, mit Ach und Krach"

# Translates a single word.
def translate(input_text) -> str:
    words = split_sentence(input_text)
    result_words = []
    for word_index, word in enumerate(words):
        if not check_is_only_punctuation(word):
            result_word = translate_single_word(word)
            result_words.append(result_word)
        else:
            result_words.append(word)

    # Wa?
    if check_is_only_punctuation(words[-1]):
        if random.random() > 0.3:
            result_words[-1] = ", wa?"

    return join_sentence(result_words)


def translate_single_word(word):
    # Inspect word
    is_uppercase = check_is_first_char_uppercase(word)

    # Make word lower case
    word = word.lower()

    # Translate
    result_word = word.replace("ist", "is")
    result_word = result_word.replace("ich", "ick")
    result_word = result_word.replace("brötchen", "schrippe")
    result_word = result_word.replace("was", "wat")
    result_word = result_word.replace("dies", "dit")
    result_word = result_word.replace("das", "dit")
    result_word = result_word.replace("guck", "kiek")
    result_word = result_word.replace("alt", "oll")
    result_word = result_word.replace("drin", "drinne")
    result_word = result_word.replace("kein", "keen")
    result_word = result_word.replace("klein", "kleen")
    if result_word[:2] == "ge":
        result_word = "je" + result_word[2:]

    # Restore upper case
    if is_uppercase:
        result_word = result_word.capitalize()

    return result_word