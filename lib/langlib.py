import re
import string

def split_sentence(sentence: str) -> list:
    # Regular expression to match words and separate punctuation
    pattern = r"\w+|[^\w\s]"
    return re.findall(pattern, sentence)

def check_starts_with_vowel(word: str) -> bool:
    vowels = {'a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U'}
    return word[0] in vowels if word else False

def check_is_first_char_uppercase(word: str) -> bool:
    return word[0].isupper() if word else False

def check_is_only_punctuation(s: str) -> bool:
    return all(char in string.punctuation for char in s)

def join_sentence(tokens: list[str]) -> str:
    result = ""
    for token in tokens:
        if len(result) > 0 and not check_is_only_punctuation(token):
            result += " "
        result += token
    return result
