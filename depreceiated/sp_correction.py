#coding UTF-8
import sys
import re
import collections
import requests
import string

def words(text):
    return re.findall('[a-z]+', text.lower())

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

#NWORDS = train(words(file('big.txt').read()))
#NWORDS = train(words(requests.get("http://norvig.com/big.txt").text))
NWORDS = train(words(file('/usr/share/dict/words').read()))
alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
    s = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes    = [a + b[1:] for a, b in s if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in s if len(b)>1]
    replaces   = [a + c + b[1:] for a, b in s for c in alphabet if b]
    inserts    = [a + c + b     for a, b in s for c in alphabet]
    return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words):
    return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or    known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)

def main():
    f = open(sys.argv[1])
    tot = 0
    for line in f:
        for word in line.split():
            if re.search('[a-zA-Z]', word) and len(word) > 1:
                #print word
                word = ''.join(ch for ch in word if ch.isalnum())
                word = word.lower()
                cor_lc = correct(word)
                cor_uc = correct(string.capwords(word))
                if cor_lc != word and cor_uc != word:
                    #print "bad word"
                    print word + " ",
                    tot = tot + 1
                #else:
                #    print "good word"
    print
    print "total spelling errors: " + tot
    return 0
main()

