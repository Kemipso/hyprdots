#!/usr/bin/env python3
import json
import re

category = {}

with open('/home/hvigne/Git/Dots/kemipso/Configs/.config/hypr/keybindings-short.conf') as f:
    lines = f.readlines()
    columns = ['mod','key','dispatcher','command','comment']
    delimiters = ",", "#"
    regexp = '|'.join(map(re.escape, delimiters))

    for index, line in enumerate(lines):
        line = line.strip() # remove leading/trailing white spaces
        if line.startswith("#") and lines[index+1].startswith('bind'): # Comment followed by binds = a new category
            if category:
                # Do something smart here, we'll work on the next category
                #category['Binds'].append(my_list)
                #print(category)
                break
            category = {"category": line, "binds": []}

        elif line.startswith('bind'):  # New keybind to add to a category
            keybind = {} # dictionary to store keybind data (each line)
            line = line[line.find('=')+1:] # Snip until after the =
            data = [item.strip() for item in re.split(regexp, line, maxsplit=4)]
            for index, elem in enumerate(data):
                keybind[columns[index]] = data[index]
            # If for some reason we're in a section with no category whatsoever, then put it in a "misc" category
            if not category['binds']:
                category = {"category": "misc", "binds": []}
            category['binds'].append(keybind)
 
                
    
# pretty printing list of dictionaries
####my_list[].append(d) # append dictionary to list
print(json.dumps(category, indent=4))

