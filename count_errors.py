#coding UTF-8
import sys
import re
import string
import enchant
import time
import ATD
ATD.setDefaultKey("warner_findoc_research")
from enchant.checker import *

def enum_errs(cleaned_text):
    f = open(cleaned_text)
    f_str = f.read()
    f.seek(0)
    pwl = open("custom_dict.txt")
    chkr = SpellChecker("en_US")

    for w in pwl:
        chkr.add(w)

    text = ""
    tot_sp = 0
    for line in f:
        for word in line.split():
            if re.search('[a-zA-Z]', word) and len(word) > 1 and word.find(".com") == -1:
                text += word
                text += " "
    chkr.set_text(text)
    for err in chkr:
        if err.word[0].isupper() == False:
            #print "spelling error for: " + "**"+err.word+"**"
            tot_sp += 1
    #print "#Total spelling errors for file: " + str(cleaned_text) + ": " + str(tot_sp)

    tot_gm = 0
    for sentence in re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', f_str):
        time.sleep(1)
        errors = ATD.checkGrammar(sentence)
        for err in errors:
            if err.type == "grammar":
                print "%s error for: %s **%s**" % (err.type, err.precontext, err.string)
                tot_gm += 1
    #print "#Total grammatical errors for file: " + sys.argv[1] + ": " + str(tot_gm)

    f.close()
    return tot_sp, tot_gm

