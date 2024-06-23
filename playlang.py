#######
#
# Playful language
#
#######

import os
import glob
import argparse
import importlib.util


language_plugins = {}


class MissingLanguageIDError(Exception):
    pass


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
        language_id = getattr(module, 'LANGUAGE_ID', None)
        if language_id is None:
            raise MissingLanguageIDError(f"{os.path.basename(plugin_file)} does not define LANGUAGE_ID.")

        # Retrieve additional language plugin info,
        # pack everything into new item in language_plugins
        language_plugins[language_id] = {
            'module': module,
            'id': language_id,
            'name': module_name,
            'title': getattr(module, 'LANGUAGE_TITLE', module_name),
            'version': getattr(module, 'LANGUAGE_VERSION', None),
            'credits': getattr(module, 'LANGUAGE_CREDITS', None),
            'description': getattr(module, 'LANGUAGE_DESCRIPTION', None)
        }

    return language_plugins


def call_plugin_function(module, function_name: str, *args, **kwargs):
    result = None
    if hasattr(module, function_name):
        func = getattr(module, function_name)
        result = func(*args, **kwargs)
    return result


def parse_args():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="A script with a rudimentary plugin system.")
    
    # Create a mutually exclusive group
    # group = parser.add_mutually_exclusive_group(required=True)
    
    # Add the -languages flag to the group
    parser.add_argument("-languages", "-l", action="store_true", help="List available language plugins.")
    
    # Add the LANG and INPUT arguments to the group
    parser.add_argument("lang", type=str, metavar="LANG", nargs='?', help=f"Which language {list(language_plugins.keys())}")
    parser.add_argument("input", type=str, metavar="INPUT", nargs='?', help="Input text")

    args = parser.parse_args()


    # Custom logic to enforce mutual exclusivity
    if args.languages:
        if args.lang or args.input:
            parser.error("'-languages' cannot be used with 'lang' and 'input' arguments.")
        print("Listing available language plugins...")
    else:
        if not args.lang or not args.input:
            parser.error("Both 'lang' and 'input' arguments are required unless using '-languages'.")
        print(f"Processing language: {args.lang} with input: {args.input}")

    return args


def main():
    # Load language plugins
    language_plugins = get_language_plugins()

    # Evaluate command line arguments
    args = parse_args()

    if args.languages:
        # If the -languages flag is set, print the available language plugins
        try:
            print(f"Found {len(language_plugins.items())} language plugins:")
            for plugin_name, plugin_info in language_plugins.items():
                print("")
                print(f"{plugin_info['title']} (ID: \"{plugin_info['id']}\")")
                print(f"Version {plugin_info['version']}") if plugin_info['version'] else _
                print(f"{plugin_info['credits']}") if plugin_info['credits'] else _
                print(f"{plugin_info['description']}\n") if plugin_info['description'] else _
        except MissingLanguageIDError as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        # If the -languages flag is not set, proceed with the normal functionality
        input_text = args.input
        languages = args.lang.split()

        print(f"Input   : {input_text}\n")

        for lang in languages:
            # Call a specific function (e.g., 'my_function') from all plugins
            if lang in language_plugins:
                # Your existing logic for processing the input with the specified language plugin
                print(f"Language: {language_plugins[lang]['title']}")
                result = call_plugin_function(language_plugins[lang]['module'], 'translate', input_text)
                print(f"Output  : {result}")
            else:
                print(f"Error: No language with ID \"{lang}\" found!")
            print("")

if __name__ == "__main__":
    main()