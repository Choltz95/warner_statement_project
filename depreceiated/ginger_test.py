import sys
import re
import count_errors
import python_ginger_api
import language_check
import codecs
def main():
    f = codecs.open(sys.argv[1],"r","utf-8")
    f_str = f.read()
    tool = language_check.LanguageTool('en-US')
    t = 0
    #sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', f_str)
    #count_errors.enum_errs(sys.argv[1],g="-g")
    for sentence in re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', f_str):
        #python_ginger_api.wrap(sentence)]
        if len(sentence) < 200:
            matches = tool.check(sentence)
            t += len(matches)
    print t
    #    count_errors.eval_sentence(sentence,g="-g")
    #    print python_ginger_api.wrap(sentence)
main()
