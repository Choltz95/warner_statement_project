import sys
import string
import re
import htmlentitydefs

'''
Removes HTML or XML character references and entities from a text string.
@param text The HTML (or XML) source text.
@return The plain text, as a Unicode string, if necessary.
'''
def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

def main():
    page = ""
    replace_mapping = {'\n':' ', '\t':' ', '*':' '}
    f = open(sys.argv[1])
    for line in f:
        unescape(line)
        for k, v in replace_mapping.iteritems():
            line = line.replace(k, v)
        #line  = ' '.join(line.split())
        if len(line.split()) > 1 and line.find("END PRIVACY-ENHANCED MESSAGE") == -1 and line.find("exhibit") == -1 and line.find("Exhibit") == -1 and len(line) - line.count(' ') < 500:
            filter(lambda x: x in string.printable, line)
            page+=line
    print page
    f.close()
    return 0
main()
