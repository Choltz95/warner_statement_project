import sys
import re
import count_errors
import python_ginger_api
def main():
    f = open(sys.argv[1])
    f_str = f.read()

    #sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', f_str)
    count_errors.enum_errs(sys.argv[1],g="-g")
    #for sentence in re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', f_str):
    #    count_errors.eval_sentence(sentence,g="-g")
    #    print python_ginger_api.wrap(sentence)
main()
