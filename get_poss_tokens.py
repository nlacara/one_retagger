#! /bin/python3

"""
This script searches the BNC corpus to find sentences containing tokens of the
word ‘one’ following a possessive (tags POS and DPS). It takes the sentence and
several previous ones for context and dumps them into a json file for later 
processing with retag_poss.py

Make sure that you point the bnc_reader (line 21) to the correct path to where
the BNC is stored on your system.
"""

# We'll use the NLTK BNC reader.
import nltk
# We'll save the results as a json list? Why not.
import json

# We're using the BNC, which is what Payne et. al (2013) use.
from nltk.corpus.reader.bnc import BNCCorpusReader
print('Loading BNC corpus')
bnc_reader = BNCCorpusReader(root="/home/nick/nltk_data/corpora/bnc/Texts", \
                             fileids=r'[A-K]/\w*/\w*\.xml')

# Write to this file
output_file = './poss_data.json'

# Get some tagged sentences
# The c5 tags provide more relevant information!
print('Preparing tagged sentences.')
tagged_sentences = bnc_reader.tagged_sents(c5=True)
print('Counting tagged sentences.')
#tagged_sentences_count = 0
#for sentence in tagged_sentences:
   #tagged_sentences_count += 1
   #print(tagged_sentences_count, end = '\r')
   
#Hard coding this because it takes so long:
tagged_sentences_count = 6026276

print('{} tagged sentences in corpus.'.format(tagged_sentences_count))

# Find tokens of possessives followed by ‘one’ or ‘ones’
print('Looking for POSS + one(s)')
poss_one_sents = []
sents_found = 0

# Search each sentence
for sentence in range(tagged_sentences_count):
    print('Sentence:', sentence, 
          "({}%)".format(round(sentence / tagged_sentences_count * 100)),
          'Sents found:', sents_found,
          end='\r')
    sentence_length = len(tagged_sentences[sentence])
    for word in range(0, sentence_length - 1):
        # Possessive tags in BNC c5 tags are DPS for "'s", and POS for pos determiners
        if tagged_sentences[sentence][word][1] in ['DPS', 'POS'] \
        and tagged_sentences[sentence][word + 1][0].lower() in ['one', 'ones']:
            sents_found += 1

            target = tagged_sentences[sentence - 8:sentence + 1]
            poss_one_sents.append(target)


# Report the results of the search:
print("")
print('{} results found.'.format(len(poss_one_sents)))

# Write the output to a file:
with open(output_file, 'w') as poss_data_file:
        json.dump(poss_one_sents, poss_data_file)
print("Data dumped to:", output_file)
