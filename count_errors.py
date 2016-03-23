#coding UTF-8
import sys
import re
import string
import enchant
import time
import multiprocessing as mp
from functools import partial
from enchant.checker import *
#import python_ginger_api as ginger
import language_check
import codecs

cleaned_text = ""
chkr = SpellChecker("en_US")
tool = language_check.LanguageTool('en-US')
def eval_sentence(sentence,g="",cs=""):
    text = ""
    tot_sp = 0
    tot_gm = 0
    if g == "-g":
        if len(sentence) < 200:
            matches = tool.check(sentence)
            if len(matches) > 0:
                with open(cleaned_text+ ".gm_log","a+") as log_f:
                    for match in matches:
                        log_f.write("spelling error for: **\n"+str(match.ruleId)+"**\n")
            tot_gm += len(matches)
    #    result = ginger.wrap(sentence)
    #    if result != -1:
    #        tot_gm += result
    for word in sentence.split():
        if re.search('[a-zA-Z]', word) and len(word) > 1 and len(word) < 34 and word.find(".com") == -1:
            text += word.encode("utf-8")#word.encode('ascii','ignore')
            text += " "
    chkr.set_text(text)
    for err in chkr:
        with open(cleaned_text+ ".sp_log","a+") as log_f,open("sp_log","a+") as log_a:
            if err.word[0].isupper() == False:
                log_a.write(err.word+" ")
                log_f.write("spelling error for: " + "**"+err.word+"**\n")
                tot_sp += 1
            else:
                if cs == "-uc":
                    log_a.write(err.word+" ")
                    log_f.write("spelling error for: " + "**"+err.word+"**\n")
                    tot_sp += 1
    return tot_sp,tot_gm

def enum_errs(clean_f,g="",cs=""):
    global cleaned_text
    global chkr
    global tool
    cleaned_text = clean_f
    #f = open(cleaned_text)
    f = codecs.open(cleaned_text,"r","utf-8")
    f_str = f.read()
    f.close()

    tot_sp = 0 # spelling errors
    tot_gm = -1 # grammatical errors -1 if no checking specified

    # add custom dict words to spell checker
    with open("custom_dict.txt") as pwl:
        for w in pwl:
            chkr.add(w)

    CORES = mp.cpu_count()
    pool = mp.Pool(processes = CORES)
    eval_sentence_p = partial(eval_sentence,g=g,cs=cs)
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', f_str)

    S = pool.map_async(eval_sentence_p,sentences)
    S = S.get(200)
    pool.close()
    pool.join()

    tot_sp = sum([pair[0] for pair in S])
    tot_gm = sum([pair[1] for pair in S]) if g == "-g" else -1
    """
    for sentence in re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', f_str):
        result = eval_sentence(sentence, g, cs)
        tot_sp += result[0]
        tot_gm += result[1]
    """
    return tot_sp, tot_gm
