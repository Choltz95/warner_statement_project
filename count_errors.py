#coding UTF-8
import sys
import re
import string
import enchant
from enchant.checker import *

def main():
    f = open(sys.argv[1])
    pwl = open("custom_dict.txt")
    chkr = SpellChecker("en_US")

    for w in pwl:
        chkr.add(w)

    text = ""
    tot = 0
    for line in f:
        for word in line.split():
            if re.search('[a-zA-Z]', word) and len(word) > 1 and word.find(".com") == -1:
                text += word
                text += " "
    chkr.set_text(text)
    for err in chkr:
        print err.word
        tot += 1
    print "#Total spelling errors for file: " + sys.argv[1] + ": " + str(tot)
    f.close()
    return 0
main()

