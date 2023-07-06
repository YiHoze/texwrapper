from spellchecker import SpellChecker

spell = SpellChecker(language='en')

# find those words that may be misspelled
sentence = ['Helo', 'good', 'moning', 'the', 'indicator', 'illuminats']

misspelled = spell.unknown(sentence)
print(misspelled)

