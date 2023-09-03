#!/usr/bin/env python3
import os
import json, re
import argparse
from dataclasses import dataclass, field, asdict

@dataclass
class Category:
    name: str
    keybinds: list

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}

@dataclass(order=True)
class keybindclass():
    sort_index: int = field(init=False, repr=False)
    mod: str
    key: str
    dispatcher: str
    command: str
    comment: str = ""

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}
    
    def __post_init__(self):
        self.sort_index = self.key

#keybindsFile = '/home/hvigne/Git/Dots/kemipso/Configs/.config/hypr/keybindings-short.conf'
def parse_keybinds(keybindsFile=os.getenv('HOME')+"/.config/hypr/keybindings.conf"):
    with open(keybindsFile) as f:
        lines = f.readlines()
        columns = ['mod','key','dispatcher','command','comment']
        delimiters = ",", "#"
        regexp = '|'.join(map(re.escape, delimiters))
        categories = {}
        testClassCategories = {}
        currentCategory = ""

        for index, line in enumerate(lines):
            line = line.strip() 

            if not line.startswith('bind'):  # Not a new keybind > ignore
                continue

            if index > 0 and lines[index-1].startswith('#'): # Comment followed by binds > a new category
                currentCategory = lines[index-1]
                currentCategory = currentCategory[currentCategory.find('#')+1:].strip() # Cleanup
            elif index == 0 or (index > 0 and not lines[index-1].strip()): # Binds without a category (previous line is empty)
                currentCategory = "misc"

            if currentCategory not in categories:
                categories[currentCategory] = {"binds": []}

            keybind = {}
            line = line[line.find('=')+1:] # Snip until after the first =
            newitem = map(keybindclass, (item.strip() for item in re.split(regexp, line, maxsplit=4)))
            #data = [item.strip() for item in re.split(regexp, line, maxsplit=4)] # Comments may contain delimiters - ignore these.

            keybind = map(lambda sub: (item.strip() for item in re.split(regexp, line, maxsplit=4)))
            #for index, elem in enumerate(data):

                #keybind[columns[index]] = data[index]

            categories[currentCategory]["binds"].append(newitem)
            #categories[currentCategory]["binds"].append(keybind)
            #testClassCategories[currentCategory].append(newitem)
                
    return categories


def main():

    category1 = Category("misc",[1, 2, 3])
    print(category1)
    parsed_categories = parse_keybinds()
    # Print the output
    myvar = list(parsed_categories(sub) for sub in parsed_categories)
    mydic = dict(parsed_categories())
    print(list(parsed_categories))
    print(json.dumps(vars(parsed_categories), indent=4))

if __name__ == "__main__": 
    main()
