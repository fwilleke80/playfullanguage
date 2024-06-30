#######
#
# Playful language
#
#######

import os
import glob
import argparse
import importlib.util
from lib.langlib import *

SCRIPT_NAME: str = "Playful Language"
SCRIPT_VERSION: str = "1.1"

TEST_SENTENCE: str = "The big brown fox jumps over the lazy dog."

language_plugins = {}

# Error type used if a plugin doesn't define an ID string
class MissingLanguageIDError(Exception):
    pass

# Error type used if a plugin doesn't implement either translate() or translate_words()
class NoLanguageTranslateFunctionDefinedError(Exception):
    pass

# Loads the language plugins and populates global 'language_plugins'.
def get_language_plugins():
    # Get list of language plugin files
    script_folder = os.path.dirname(os.path.abspath(__file__))
    subfolder = os.path.join(script_folder, 'languages')
    plugin_files = glob.glob(os.path.join(subfolder, '**', '*.py'), recursive=True)

    # Create a module for each language plugin
    for plugin_file in plugin_files:
        # Load language plugin file and make it a module
        module_name = os.path.splitext(os.path.basename(plugin_file))[0]
        spec = importlib.util.spec_from_file_location(module_name, plugin_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Retrieve language ID
        language_id: str = getattr(module, 'LANGUAGE_ID', None)
        if language_id is None:
            raise MissingLanguageIDError(f"{os.path.basename(plugin_file)} does not define LANGUAGE_ID.")

        # Find translate function
        translate_function_name: str = ""
        if hasattr(module, "translate"):
            translate_function_name = "translate"
        elif hasattr(module, "translate_word"):
            translate_function_name = "translate_word"
        else:
            raise NoLanguageTranslateFunctionDefinedError(f"{os.path.basename(plugin_file)} does not implement a translate function (needs to be either translate() or translate_words()).")

        # Retrieve additional language plugin info,
        # pack everything into new item in language_plugins
        language_plugins[language_id] = {
            'module': module,
            'id': language_id,
            'name': module_name,
            'title': getattr(module, 'LANGUAGE_TITLE', module_name),
            'version': getattr(module, 'LANGUAGE_VERSION', None),
            'credits': getattr(module, 'LANGUAGE_CREDITS', None),
            'description': getattr(module, 'LANGUAGE_DESCRIPTION', None),
            'translate_function_name': translate_function_name
        }

    return language_plugins

# Sets up the argument parser, does the parsing, and applies argument logic.
def parse_args() -> None:
    # Parse command line arguments
    parser = argparse.ArgumentParser(description=f"Translates any sentence to up to {len(language_plugins.keys())} playful languages.")
    
    # Add the -languages flag
    parser.add_argument("-languages", "-l", action="store_true", help="List available language plugins.")
    
    # Add the LANG and INPUT arguments
    parser.add_argument("lang", type=str, metavar="LANG", nargs='?', help=f"Which language(s) {list(language_plugins.keys())}. (Specify multiple languages separated by space ' '.)")
    parser.add_argument("input", type=str, metavar="INPUT", nargs='?', default="", help="Input text to translate")

    args = parser.parse_args()

    # Custom logic to enforce mutual exclusivity
    if args.languages:
        if args.lang or args.input:
            parser.error("'-languages' cannot be used with 'lang' and 'input' arguments.")
        print("Listing available language plugins...\n")
    else:
        if not args.lang:
            print("'lang' has not been specified! Please specify language(s) now:")
            print(f"(Supported languages: {list(language_plugins.keys())})")
            args.lang = input(":: ")
            if not args.lang:
                parser.error("'lang' argument is required unless using '-languages'.")
            print("")
        if args.input == "":
            print("'input' has not been specified! Please write something now:")
            args.input = input(":: ")
            if not args.input:
                parser.error("Both 'lang' and 'input' arguments are required unless using '-languages'.")
            print("")
        print(f"Processing language{'s' if len(args.lang.split()) > 1 else ''}: '{args.lang}' with input: {args.input}")

    return args

# Calls a function in a plugin module
def call_plugin_function(module, function_name: str, *args, **kwargs):
    result = None
    if hasattr(module, function_name):
        func = getattr(module, function_name)
        result = func(*args, **kwargs)
    return result

# Returns a value that indicates what to pass to the translate function as arguments.
def get_translate_function_index(lang: str):
    function_name = language_plugins[lang]['translate_function_name']
    if function_name == "translate":
        return 0
    elif function_name == "translate_word":
        return 1
    return -1

def translate(input_str: str, lang: str):
    translate_function_index = get_translate_function_index(lang)
    if translate_function_index == 0:
        result = call_plugin_function(language_plugins[lang]['module'], language_plugins[lang]['translate_function_name'], input_text)
    elif translate_function_index == 1:
        words = split_sentence(input_str)
        result_words = []
        for word in words:
            if not check_is_only_punctuation(word):
                result_word = call_plugin_function(language_plugins[lang]['module'], language_plugins[lang]['translate_function_name'], word)
                result_words.append(result_word)
            else:
                result_words.append(word)
        result = join_sentence(result_words)
    else:
        result = None

    return result

# Does all the translation work and output.
def do_translate(input_text: str, languages) -> None:
    for lang in languages:
        # Call a specific function (e.g., 'my_function') from all plugins
        if lang in language_plugins:
            result = translate(input_text, lang)

            print(f"Language: {language_plugins[lang]['title']}")
            print(f"Output  : {result}")
        else:
            print(f"Error: No language with ID \"{lang}\" found!")
        print("")

# Prints a list of all language plugins, and their info.
def print_language_list() -> None:
    try:
        print(f"Found {len(language_plugins.items())} language plugins:")
        for plugin_name, plugin_info in language_plugins.items():
            print("")
            print(f"{plugin_info['title']} (ID: \"{plugin_info['id']}\")")
            print(f"Version {plugin_info['version']}") if plugin_info['version'] else _
            print(f"{plugin_info['credits']}") if plugin_info['credits'] else _
            print(f"{plugin_info['description']}") if plugin_info['description'] else _
            print(f"Test: {translate(TEST_SENTENCE, plugin_info['id'])}\n")
    except MissingLanguageIDError as e:
        print(f"Error: {e}")
        sys.exit(1)

def main() -> None:
    title_str = f"{SCRIPT_NAME} {SCRIPT_VERSION}"
    print(title_str)
    print("=" * len(title_str))
    print("")


    # Load language plugins
    language_plugins = get_language_plugins()

    # Evaluate command line arguments
    args = parse_args()

    if args.languages:
        # If the -languages flag is set, print the available language plugins
        print_language_list()
    else:
        # If the -languages flag is not set, proceed with the normal functionality
        do_translate(args.input, args.lang.split())


if __name__ == "__main__":
    main()