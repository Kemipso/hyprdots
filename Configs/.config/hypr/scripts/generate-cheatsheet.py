#!/usr/bin/env python3
import os
import json, re
import argparse

def parse_keybinds(keybindsFile, categories={}):
    with open(os.path.expanduser(keybindsFile)) as f:
        lines = f.readlines()
        bindParams = ['mod','key','dispatcher','command','comment']
        delimiters = ",", "#"
        reDelimiters = '|'.join(map(re.escape, delimiters))
        reLineFilter = "^(?P<type>bind[lrenmt]*|source|#)[ =]*(?P<content>.*)$"
        previousLine = None

        for line in lines:
            line = line.strip()
            line = re.search(reLineFilter, line, flags=re.IGNORECASE)
            if not line:  # Not a new keybind or source > ignore
                previousLine = None
                continue

            line = line.groupdict()

            # For a new keybind, we check if the previous line is empty, or if it starts with #
            # If the previous line is empty, we consider the new keybind to be in the category "misc"
            # If the previous line is a comment, then we consider this comment to be a new category
            # (and the line to belong to that new category)
            if line["type"].startswith("bind"):
                if not previousLine:
                    currentCategory = "misc"
                elif previousLine["type"] == "#":
                    currentCategory = previousLine["content"]
                categories.setdefault(currentCategory, {"binds": []})  
                data = [item.strip() for item in re.split(reDelimiters, line["content"], maxsplit=4)] # Comments may contain delimiters, ignore these with maxsplit=4
                keybind = dict(zip(bindParams,data))
                categories[currentCategory]["binds"].append(keybind)
            
            # Recusirvely dig through source files to extract extra keybinds, if any.
            elif line["type"]=="source":
                new_source = line['content'].split('#')[0].strip() # The split('#') is to get rid of potential comments at the end of the source file definition
                parse_keybinds(new_source, categories)
            
            previousLine = line
                
    return categories

def parseArguments():
    parser = argparse.ArgumentParser(description='Parse a keybindings file from Hyprland, returns json data.')
    parser.add_argument('-c', '--config', type=file, required=False, default="~/.config/hypr/hyprland.conf",
                        help='A .conf file to read from. Defaults to ~/.config/Hypr/keybindings.conf if absent')
    parser.add_argument('-o', '--outfile', type=directory, required=False,
                        help='If defined, writes the json data to a file instead of printing it.')
    args = parser.parse_args()

    return args

def file(string):
    if os.path.isfile(os.path.expanduser(string)):
        return string
    else:
        raise argparse.ArgumentTypeError(f"Cannot read config: {string} does not exist.")

def directory(string):
    if os.path.isdir(os.path.dirname(string)):
        return string
    else:
        raise argparse.ArgumentTypeError(f"Cannot write json: The parent directory for {string} does not exist.")

def main():
    args = parseArguments()
    parsed_categories = parse_keybinds(args.config)

    if args.outfile:
        with open(args.outfile, 'w') as output:
            output.write(json.dumps(parsed_categories, indent=2))
    else:
        print(json.dumps(parsed_categories, indent=2))

if __name__ == "__main__":
    main()
