#!/bin/python3
"""
Script for retagging data gathered from the BNC corpus. Specifically, it is
meant to help speed up retagging tokens of ‘one’ and ‘ones’ since (a) the 
automatic tagging used by the BNC is not very reliable and (b) the tags that 
are used are not precise enough for the issues I care about.

This particular version of the script is for retagging tokens in a sample of
the BNC. It processes data output by the script get_sample_tokens.py. 
Run that first.
"""

from retagger_common import *

## Data file loading ##

# Input and output files.
# Should probably make these CLI arguments, but whatever.
output_file = './sample_retagged.json'
input_file = './sample_data.json'


# Load the sample data from the BNC.
# These are files containing tokens of ‘one’/‘ones’
print("Loading data file:", input_file)
with open(input_file, 'r') as input_data:
    tagged_sents = json.load(input_data)
    
# We'll want to know the number of tagged sentences
# in the sample for various reasons.
tagged_count = len(tagged_sents)
print("{} example sentences loaded.".format(tagged_count))


# Load previously tagged sentences if they exist 
# so we can start where we left off...
if path.isfile(output_file):
    with open(output_file, 'r') as retag_data:
        retagged = json.load(retag_data)

    # We'll use the following number to make it
    # so that we start again where we left off
    retagged_count = len(retagged)
    print("{} previously retagged sentences loaded.".format(retagged_count))
    print('')
else:
    retagged = []
    retagged_count = 0
    print("No previously retagged sentences found.")
    print('')


# Keep track of running numbers for the tagging, just to keep track of things.
sentence_num = 0
sentence_num += retagged_count

## Retagging stuff ##

# Process each sentence
for sent_list in tagged_sents[retagged_count:tagged_count]:
    # Setting quit to True will cause lead to quitting.
    quit = False
    
    # Keep track of new tags and write them all at once.
    # This avoids writing the same sentence multiple times.
    new_tags = {}
    sent = sent_list[-1]
    context = []
    for sentence in sent_list[:-1]:
        for token in sentence:
            context.append(token)
    
    
    # Print the sentence number to keep track of progress
    print(Fore.YELLOW + "Sentence: " + str(sentence_num + 1) + " / " 
        + str(tagged_count) + Style.RESET_ALL
        + ' (' + str(round((sentence_num + 1) / tagged_count * 100)) + '%)')
    
    # Some sentences have more than one token of one,
    # so we need to retag each token.
    for token in range(len(sent) - 1):
        if sent[token][0].lower() in ['one', 'ones']:
            # Print the sentence and context:
            detag_print(sent, context, token)
            
            # Print previous tag information
            # There are cases where this needs to be changed
            if token > 0:
                print("Preceding tag:", Fore.LIGHTGREEN_EX +  sent[token - 1][1] + Style.RESET_ALL + '\t' + "Current tag:", Fore.LIGHTCYAN_EX + sent[token][1] + Style.RESET_ALL)
            else:
                print("Current tag:", Fore.LIGHTCYAN_EX + sent[token][1] + Style.RESET_ALL)
            
            # Tag options:    
            print("Tags: 1) Anaphoric SG  2) Anaphoric PL ",
                "3) Anaphoric Pn     4) Impersonal")
            print("      5) Cardinal      6) ?Ambiguous ",
                  "  7) Context unclear  8) Part of title/name")            
            print("      9) Part of num.  0) Part of comp.",
                  "10) Part of mod.    P) Re-tag prev tok.  Q) Quit ")            
            new_tag = input("New tag: ")
            
            if new_tag.lower() in ['q', 'quit']:
                quit = True
                pass
            
            if new_tag.lower() == 'p':
                prev_tag = input('Enter new tag for previous token: ')
                one_tag = input('Enter new tag (num) for _one_: ')
                new_tags[token - 1] = prev_tag
                if one_tag in [str(num) for num in range(0,11)]:
                    new_tags[token] = retagger(one_tag)
                else:
                    new_tags[token] = new_tag.upper()
            elif new_tag in [str(num) for num in range(0,11)]:
                new_tags[token] = retagger(new_tag)
            else:
                new_tags[token] = new_tag.upper()
            print('')
    if quit:
        # If the user decides to quit, write the new tags
        # to the output file and gtfo.
        write_out(retagged, output_file) 
        exit()
    sentence_num += 1

    # If we reach the end of the sentence,
    # write the new tags
    retagged_sent = sent
    for index in new_tags.keys():
        retagged_sent[index][1] = new_tags[index]
    
    retagged.append(retagged_sent)
    print('')

# If we get through all the sentences in the input data
# write the changed tags to the output file and quit.
write_out(retagged, output_file)
exit()
