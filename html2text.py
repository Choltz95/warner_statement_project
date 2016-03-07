import multiprocessing
import parse_lib
import optparse
import urlparse
import HTMLParser
from functools import partial
from bs4 import BeautifulSoup
"""
mapping from html data, encoding type, possible url to de-tagged html
"""
def run_map(data, encoding, baseurl):
    soup = BeautifulSoup(data,"lxml")
    for table in soup.find_all("table"):
        table.extract()
    data = str(soup)
    if encoding is None:
        try:
            from chardet import detect
        except ImportError:
            detect = lambda x: {'encoding': 'utf-8'}
        encoding = detect(data)['encoding']
    data = data.decode('utf-8') # encoding
#    wrapwrite(html2text(data,baseurl))
    return parse_lib.html2text(data,baseurl)

if __name__ == "__main__":
    baseurl = ''
    p = optparse.OptionParser('%prog [(filename|url) [encoding]]')
    p.add_option("-d", "--dash-unordered-list", action="store_true", dest="ul_style_dash",
        default=False, help="use a dash rather than a star for unordered list items")
    p.add_option("-b", "--body-width", dest="body_width", action="store", type="int",
        default=78, help="number of characters per output line, 0 for no wrap")
    (options, args) = p.parse_args()

    # handle options
    if options.ul_style_dash:
        options.ul_item_mark = '-'
    else:
        options.ul_item_mark = '*'

    BODY_WIDTH = options.body_width

    # process input
    if len(args) > 0:
        file_ = args[0]
        encoding = None
        if len(args) == 2:
            encoding = args[1]
        if len(args) > 2:
            p.error('Too many arguments')

        data = open(file_, 'rb').read()
        file_len = len(data)
#        run_map(data,encoding,baseurl)

        ##parallelized solution from functools import partial
        CORES = 8
        pool = multiprocessing.Pool(processes = CORES)
        run_map_p = partial(run_map,encoding = encoding,baseurl = baseurl)
        division = file_len/CORES
        if division == 0:
            p.error("no text in file" + file_)
        divide_file = [data[i:i+division] for i in xrange(0,file_len,division)]
        process_list = map(str,divide_file)

        S = pool.map_async(run_map_p,process_list)
        S = S.get(10)
        pool.close()
        pool.join()
        S = [s for substring in S for s in substring] # flatten list
        S =  [x.encode('UTF8') for x in S]

        replace_mapping = {'\n':' ', '\t':' ', '*':' '}
        page = ""
        for line in ''.join(S):
            parse_lib.unescape(line)
            for k, v in replace_mapping.iteritems():
                line = line.replace(k, v)
            # filter out custom phrases
            if len(line.split()) > 1 and line.find("END PRIVACY-ENHANCED MESSAGE") == -1 and line.find("exhibit") == -1 and line.find("Exhibit") == -1 and len(line) - line.count(' ') < 500:
                filter(lambda x: x in string.printable, line)
            page+=line
        print page

    else:
        p.error("Too few arguments")
