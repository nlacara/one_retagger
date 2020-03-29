# Retagger for ‘one’

This is set of Python scripts that use the Natural Language Tool Kit (NLTK) to serach the British National Corpus (BNC) for tokens of the word *one* and their associated tags and then modify those tags because the automatic tagging in the BNC does a poor job of tagging them accurately. The main goal here is to identify uses of so-called anaphoric *one* when it occurs immediately following possessives in English (including *-'s*, *my*, *her*, *their*, and others; tags DPS and POS in the BNC). For more on this project, see [the discussion on my blog](https://nlacara.github.io/blog/one/bnc-search.html).

The included scripts are:

- get_poss_tokens.py - This script searches the tagged sentences in the BNC to find tokens of *one* after words tagged DPS or POS. When it finds a sentence with this collocation, it takes that sentence and several of the previous ones (to be used for context to aid later retagging) and adds them to a list which is subsequently dumped to poss_data.json, which is used as the input for the retagger retag_poss.py
- get_sample_tokens.py - This script samples the BNC for sentences containing tokens of *one*, aiming to get around 1000 tokens. These data are dumped to sample_data.json. These data are used as input for the retagger retag_sample.py
- retag_poss.py - This script allows the user to retag tokens of *one* in the data dumped by get_poss_tokens.py.
- retag_sample.py - This script allows the user to retag tokens of *one* in the data dumped by get_sample_tokens.py. The point of this is to create a sample of the corpus against which the retagged possessive data can me compared.

Some code shared by the retag scripts is contained in retagger_common.py