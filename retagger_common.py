#! /bin/python3
"""
Common functions for retaggers. I could probably throw more into this file
but this at least helps simplify retag_poss.py and retag_sample.py a bit.
"""

# Output will be stored in JSON format
import json

# Use RegEx to format output:
import re

# Used to see if file exists.
from os import path

# Color used to highlight important things.
from colorama import Fore, Back, Style

def proc_text(string):
    """ Remove some unnecessary spaces when displaying
    joined sentences and their contexts """
    string = re.sub(r'\s\.', '.', string)
    string = re.sub(r'\s\?', '?', string)
    string = re.sub(r'\s\,', ',', string)
    string = re.sub(r"\s'", "'", string)
    string = re.sub(r"\sn't", "n't", string)
    string = re.sub(r"\s’", "’", string)
    string = re.sub(r"‘\s", "‘", string)
    string = re.sub(r"\s\)", ")", string)
    string = re.sub(r"\(\s", "(", string)
    return string

 
def detag_print(sent, context, highlight):
    """For untagging and printing sentences
    in a human-readable format. The highlight argument
    tells colorama the index for the word to highlight.
    The context argument is a list of the tokens that gives
    the preceding for the sentence that needs to be retagged"""
    
    # Process tokens so that only the word and not the tag remain.
    untagged_context = list(token[0] for token in context)
    untagged_sent = list(token[0] for token in sent)
    
    # Find the index of the token that needs to be highlighted
    # and add color information to it.
    for word in range(len(untagged_sent)):
        if word == highlight:
            untagged_sent[word] = Fore.LIGHTCYAN_EX + untagged_sent[word] + Style.RESET_ALL
            
    # Join the words in the context and target sentence
    # and display them.
    joined_context = proc_text(" ".join(untagged_context))
    joined_sent = proc_text(" ".join(untagged_sent))
    print(Fore.LIGHTGREEN_EX + 'Context:' + Style.RESET_ALL, joined_context)
    print(Fore.LIGHTCYAN_EX + 'Token:' + Style.RESET_ALL, joined_sent)


def retagger(retag):
    """ Shortcuts for retagging things
    so you don't have to type out
    every tag from memory """
    tags = {"1": "1A1", # Ana Singular
            "2": "1A2", # Ana Plural
            "3": "1PA", # Ana Pronoun
            "4": "1PI", # Imp Pronoun
            "5": "1NC", # Num Cardinal
            "6": "1UA", # Unc Ambiguous
            "7": "1UC", # Unc Context
            "8": "1UN", # Unc Name/Title
            "9": "1NN", # Num Part of numeral
            "0": "1NP", # Num Part of compound
            "10": "1NM", # Num Part of mod
            }
    return tags[retag]

def write_out(data, output_file):
    """ Write the tagged data to a file """
    print('Writing output to:', output_file)
    with open(output_file, 'w') as retag_file:
        json.dump(data, retag_file)
    print('Goodbye!')        


