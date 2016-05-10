import nltk
from nltk.corpus import words
nltk.data.path.append('./nltk_data/')
import wikipedia

with open("words.txt") as w:
    for word in w:
        if len(word) > 5:
	    d = wikipedia.search(word)
	    if len(d) > 5:
	        print word
