#!/usr/bin/env python3
"""! @brief Defines some commonly used functions for use in language plugins."""

import re
import string


## A list of common consonant clusters that should be treated as one
DEFAULT_CONSONANT_CLUSTERS = {"sh", "ch", "th", "ph", "wh", "ck", "sch"}

## A list of common vowel clusters that should be treated as one
DEFAULT_VOWEL_CLUSTERS = {"oo", "ee", "ea", "au", "eu"}

## A list of vowels and umlauts
VOWELS = {'a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U', 'ä', 'ö', 'ü', 'Ä', 'Ö', 'Ü'}

def split_sentence(sentence: str) -> list:
    """! Tokenizes a sentence, and returns the results as a list.
    The list contains words and punctuation as seperate strings.
    """
    # Regular expression to match words and separate punctuation
    pattern = r"\w+|[^\w\s]"
    return re.findall(pattern, sentence)

def check_starts_with_vowel(word: str) -> bool:
    """! Returns true if the given word starts with a vowel.
    """
    return word[0] in VOWELS if word else False

def check_is_first_char_uppercase(word: str) -> bool:
    """! Returns true if the given word starts with an upper case letter.
    """
    return word[0].isupper() if word else False

def check_is_only_punctuation(s: str) -> bool:
    """! Returns true if the given string contains only punctuation.
    """
    return all(char in string.punctuation for char in s)

def iterate_letters_with_clusters(input_string: str, cluster_list: list[str] = DEFAULT_CONSONANT_CLUSTERS | DEFAULT_VOWEL_CLUSTERS):
    """! This generator yields the letters of a string, but considers clusters that are "spoken as one sound".
    For example, "school" will yield "sch" as a cluster. "Peanut" will yield "ea" as a cluster.
    It is recommended to use this function instead of naively iterating over the chars in a string.
    """
    i = 0
    while i < len(input_string):
        # Check for the longest matching consonant cluster
        match = None
        for length in range(3, 0, -1):  # Check clusters of length 3, 2, and 1
            if i + length <= len(input_string) and input_string[i:i+length] in cluster_list:
                match = input_string[i:i+length]
                break
        if match:
            yield match
            i += len(match)
        else:
            yield input_string[i]
            i += 1

def join_sentence(tokens: list[str]) -> str:
    """! Joins a list of tokens (retrieved from split_sentence(), and
    possibly translated after that) back into a string, respecting
    the punctuation.
    """
    result = ""
    for token in tokens:
        if len(result) > 0 and not check_is_only_punctuation(token[0]):
            result += " "
        result += token
    return result
