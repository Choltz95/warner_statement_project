import sys
import re
import subprocess
def main():
    f = open(sys.argv[1])
    f_str = f.read()

    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', f_str)
    for sentence in sentences:
        cmd = "python ginger_python2.py " + sentence
        subprocess.check_output(cmd, shell=True)
main()
