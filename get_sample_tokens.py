#! /bin/python3
"""
This script searches the BNC corpus to find sentences containing tokens of the
word ‘one’. It takes the sentence and several previous ones for context and
dumps them into a json file for later processing with retag_sample.py

Make sure that you set the bnc_reader (line 21) to the correct path to where
the BNC is stored on your system.
"""

# We'll use the NLTK BNC reader.
# Beware -- it's very slow!
import nltk

# We'll save the results using json
import json

# We're using the BNC, which is what Payne et. al (2013) use.
from nltk.corpus.reader.bnc import BNCCorpusReader
print('Loading BNC corpus')
bnc_reader = BNCCorpusReader(root="/home/nick/nltk_data/corpora/bnc/Texts", \
                             fileids=r'[A-K]/\w*/\w*\.xml')

# Write to this file:
output_file = './sample_data.json'

# Get some tagged sentences
# The c5 tags provide more relevant information
# than the default tags
print('Preparing tagged sentences.')
tagged_sentences = bnc_reader.tagged_sents(c5=True)

# Count the sentences (since we'll need this number)
print('Counting tagged sentences.')
#tagged_sentences_count = 0
#for sentence in tagged_sentences:
   #tagged_sentences_count += 1
   #print(tagged_sentences_count, end = '\r')

#Hard-coding this because it takes so long:
tagged_sentences_count = 6026276

print('{} tagged sentences in corpus.'.format(tagged_sentences_count))

# Find tokens of ‘one’ or ‘ones’
print('Sampling the corpus for tokens of ‘one’.')

# This is the list of sentences and their contexts:
one_sents = []

# This is for keeping track of what's going on
sent_count = 0  # The number of sentences that have been processed
sent_added = 0  # The number of sentences that have been added to one_sents

# This is the for loop where the magic happens
for sentence in range(tagged_sentences_count):
    # Give the user some feedback about the progress (the search takes a while)
    print('Sentence:', sentence, '/', tagged_sentences_count,
          "({}%)".format(round(sentence / tagged_sentences_count * 100)),
          'Sentences found:', sent_count, 'Sentences added:', sent_added,
          end='\r')
    
    # We check each sentence to see if it contains 'one'.
    targ_sent = [token[0] for token in tagged_sentences[sentence]]
    if 'one' in targ_sent or 'ones' in targ_sent:
        
        # If it contains one, we count it:
        sent_count += 1

        # Since we're only taking a sample (aiming for around 1000 tokens),
        # we only take every 270th sentence containing 'one'
        # Adjust this number if you want to change the
        # number of tokens in the sample
        if sent_count % 270 == 0:

            # We'll also take several preceding sentences for context
            # (Remember to re-edit the retagger........)
            target = tagged_sentences[sentence - 8:sentence + 1]
            one_sents.append(target)
            sent_added += 1


# Report the results of the search:
print("")
print('{} results found.'.format(len(one_sents)))

# Write the output to a file:
with open(output_file, 'w') as possfile:
        json.dump(one_sents, possfile)
print("Data dumped to:", output_file)


