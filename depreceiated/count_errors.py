#coding UTF-8
import sys
import re
import string
import enchant
import time
import multiprocessing as mp
#import ATD
#ATD.setDefaultKey("warner_findoc_research")
from enchant.checker import *
import python_ginger_api as ginger

def enum_errs(cleaned_text,g="",cs=""):
    f = open(cleaned_text)
    f_str = f.read()
    f.seek(0)
    pwl = open("custom_dict.txt")
    chkr = SpellChecker("en_US")
    tot_sp = 0 # spelling errors
    tot_gm = -1 # grammatical errors -1 if no checking specified

    # add custom dict words to spell checker
    for w in pwl:
        chkr.add(w)

    text = ""
    for line in f:
        for word in line.split():
            if re.search('[a-zA-Z]', word) and len(word) > 1 and word.find(".com") == -1:
                text += word
                text += " "
    chkr.set_text(text)
    for err in chkr:
        if err.word[0].isupper() == False:
            with open(cleaned_text + ".log", "a+") as f:
                f.write("spelling error for: " + "**"+err.word+"**\n")
            tot_sp += 1
        else:
            if cs != "":
                f.write("spelling error for: " + "**"+err.word+"**\n")
    #print "#Total spelling errors for file: " + str(cleaned_text) + ": " + str(tot_sp)
    if g == "-g":
        for sentence in re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', f_str):
            result = ginger.wrap(sentence)
            if result == -1:
                continue
            else:
                tot_gm += result
            #time.sleep(1) # atd api only accepts requests max once every second
            #errors = ATD.checkGrammar(sentence)
            #for err in errors:
            #    if err.type == "grammar":
            #        with open(cleaned_text + ".log", "a+") as f:
            #            f.write("%s error for: %s **%s**\n" % (err.type, err.precontext, err.string))
            #        tot_gm += 1
        #print "#Total grammatical errors for file: " + sys.argv[1] + ": " + str(tot_gm)

    pwl.close()
    f.close()
    return tot_sp, tot_gm

