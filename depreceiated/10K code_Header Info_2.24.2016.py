import win32com.client, os

import os, os.path
import re
import csv


def do_parse(dirtocheck, filename):
	fout = open(filename, 'wb')
	fwriter = csv.writer(fout)
	for root, _, files in os.walk(dirtocheck):

                n=len(files)-1
                m=(n%5000)+1
                w=int(n/5000)

                if m > 0:
                        w = w + 1
                else:
                        w = w

                for x in range(1, w+1):
                        print 'Iteration ' + str(x)
                        files2 = files[(x-1)*5000: x*5000]
                        i = 0
                        while i < len(files2):
                                f = files2[i]
                        	fullpath = os.path.join(root, f)
                                        try:
                                                lines = parse_file(fullpath)
                                        except StandardError as e:
                                                print r'StandardError in do_parse: ' + fullpath
                                                lines = []				
                                        except Exception:
                                                print r'Exception: ' + fullpath
                                                lines = []					
                                        for line in lines:
                                                fwriter.writerow(line)
                                        i = i+1
	fout.close()

def parse_file(fullpath):
	fin = open(fullpath, 'r')
	data = fin.read()
	fin.close()

	try:
		fmt = r'(?s)<(SEC|IMS)-HEADER>(.*)</(SEC|IMS)-HEADER>'
		header = re.findall(fmt,data,re.DOTALL)[0][1]
	except StandardError as e:
    		header=r''

	
	# Accession Number
	try:
		fmt = r'(?sm)ACCESSION NUMBER:\s+(\S+)\s*$'
		accession_num =  re.findall(fmt,header, re.DOTALL)[0]
	except StandardError as e:
		accession_num=r''
       
		
	# CIK Number
	try:
		fmt = r'(?sm)CENTRAL INDEX KEY:\s+(\d+)\s*$'
		cik =  re.findall(fmt,header,re.DOTALL)[0]
	except StandardError as e:
		cik=r''

	#EDGAR Form Type (i.e. 10-K or 10-K/A)
	try:
		fmt = r'(?sm)CONFORMED SUBMISSION TYPE:\s+(\S+)\s*$'
		form_type =  re.findall(fmt,header,re.DOTALL)[0]
	except StandardError as e:
		form_type=r''

	#Fiscal Year End
	try:
		fmt = r'(?sm)CONFORMED PERIOD OF REPORT:\s+(\d+)\s*$'
		fye =  re.findall(fmt,header,re.DOTALL)[0]
	except StandardError as e:
		fye =r''

	#Filing Date
	try:
		fmt = r'(?sm)FILED AS OF DATE:\s+(\d+)\s*$'
		file_date =  re.findall(fmt,header,re.DOTALL)[0]
	except StandardError as e:
		file_date=r''

	#Company Name
	try:
		fmt = r'(?sm)COMPANY CONFORMED NAME:\s+(.*)CENTRAL INDEX KEY'
		co_name =  re.findall(fmt,header,re.DOTALL)[0]
	except StandardError as e:
		co_name=r''
	co_name = co_name.rstrip()
	co_name = co_name.rstrip("\n")
	co_name = co_name.rstrip("\r")
	#co_name = co_name.rstrip(",")


	#SIC Code
	try:
		fmt = r'(?sm)STANDARD INDUSTRIAL CLASSIFICATION:\s+(\d+)\s*$'
		sic =  re.findall(fmt,header,re.DOTALL)[0]
	except StandardError as e:
		sic=r''

	if sic == r'':
		try:
			#fmt = r'(?sm)STANDARD INDUSTRIAL CLASSIFICATION:\s+[\d+]\s*$'
			#fmt = r'(?sm)STANDARD INDUSTRIAL CLASSIFICATION:\s+(.*)IRS NUMBER'

			fmt = r'(?sm)STANDARD INDUSTRIAL CLASSIFICATION:.*\[(\d+)\].*IRS NUMBER'
			sic =  re.findall(fmt,header,re.DOTALL)[0]
		except StandardError as e:
			sic=r''
		#print sic


	fmt = r'(?s)<DOCUMENT>(.*?)</DOCUMENT>'
	
	try:
		tbl = r'(?s)<TABLE>(.*?)</TABLE>'
	except StandardError as e:
		tbl = r''
	
	#Change Robert's code here. Add [0] at the end. Change to "body" from "bodies"
	bod = re.findall(fmt,data,re.DOTALL)[0]
	#print bod

	try:
		table = re.findall(tbl,data,re.DOTALL)[0] #Get rid of table of contents to identify beginning of MDA section correctly
	except StandardError as e:      
		table = r''
	
	#print table

	#body = re.sub(re.escape(table), r' ', bod) 
	#print body

	body = html_to_text(bod)
	mono = r'(?i)(?s)<font\nface="Monotype\s+Sorts">'
	#b =  re.findall(mono, body,re.DOTALL)
	#print b
	#print len(b)

	body=re.sub(mono, '', body)
	#print body[1:5000]

	mono1 = r'(?i)(?s)<font\nface="Monotype\s+Sorts"\s+size=\d+>'
	#b =  re.findall(mono1, body,re.DOTALL)
	#print b

	body=re.sub(mono1, '', body)

	#bracket = r'(?i)(?s)<{1}.*{^>}>{1}'
	bracket = r'(?i)(?s)</?.[^>]*>'
	#bracket = r'(?s)(?i)<([A-Z][A-Z0-9]*)\b[^>]*>(.*?)</\1>'
	#bracket = r'</?\w+\s+[^>]*>'
	#b =  re.findall(bracket, body,re.DOTALL)
	#print b

	body=re.sub(bracket, '', body)

	#print body[1:5000]

	try:
	    fmt = r'(?i)(?s)item\s*7.{0,1}(\s*(management|management\'s|managements\')\s*discussion)?(.*?)item\s*8.{0,1}(\s*financial\s*statements)?'
	    mda =  re.findall(fmt,body,re.DOTALL)[0][2]

	except StandardError as e:
		mda=r''

	#print mda

	#Length of MDA section to scale grammar errors
	try:
		length_mda = len(mda)
	except StandardError as e:
		length_mda=r''

	baseline = (accession_num, cik, form_type, fye, file_date, co_name, sic, length_mda)
	ln = Lines(baseline, mda, fullpath)
	return ln.Word_Grammar_Errors()

class Lines:
	def __init__(self, baseline, mda, fullpath):
		self.fullpath = fullpath
		self.baseline = baseline
		self.mda = mda

	def __del__(self):
		pass

	def Word_Grammar_Errors(self):
	    mda = self.mda
	    baseline=self.baseline
	    fullpath=self.fullpath

	    q1, q2, q3, q4, q5, q6, q7, q8 = self.baseline
	    
	    list_words = self.WordSplitter(mda)
	    wdDoNotSaveChanges = 0
	    path = os.path.abspath('snippet.txt')
	    snippet  = list_words

	    file = open(path, 'w')
	    file.write(snippet)
	    file.close()

	    app = win32com.client.gencache.EnsureDispatch('Word.Application')
	    doc = app.Documents.Open(path)
	    #errors_grammar = "Grammar: %d" % (doc.GrammaticalErrors.Count,)
	    #errors_spelling = "Spelling: %d" % (doc.SpellingErrors.Count,)

	    errors_grammar = doc.GrammaticalErrors.Count
	    errors_spelling = doc.SpellingErrors.Count

	    #errors = (errors_grammar, errors_spelling)

	    #To show results:
	    #print doc.CheckGrammar()
	    #print doc.CheckSpelling()
	    app.Quit(wdDoNotSaveChanges)

	    base = [q1,q2,q3,q4,q5,q6,q7,q8,fullpath, errors_grammar, errors_spelling]

	    return [base]

	def WordSplitter(self, mda):
	    list1=[]
	    list1a = []
	    list1b = []
	    words=mda.split()
	    #print words
	    
	    # Get rid of uppercase, proper nouns that may trigger spell check.

	    for word in words:
		    if word[0].isupper() or word == "to" or word == "the" or word == "of" or word == "e.g." or word == "and" or word == "an" or word == "a" or word == "sq." or word == "ft." or word[0]=='"' or "-" in word or word[0] == "(" or "." in word:
		    #if word[0].isupper() or word == "e.g." or word == "sq." or word == "ft." or word[0]=='"' or "-" in word or word[0] == "(":
		    #print word
			    continue
		    else:
			    list1.append(word)
	    #print list1

	    # Get rid of periods that will trigger grammar check false positives.

	    for i in list1:
		    if i[len(i)-1] == ".":
			    j = i[0:len(i)-1]
			    list1a.append(j)
		    else:
			    list1a.append(i)
		    #print list1a

	    last = list1a[0]
	    #print last
	    for j in list1a:
		    if j == last:
			    continue
		    else:
			    last = j
			    list1b.append(j)
		    #print list1b
	    
		
	    list2 = " ".join(list1b)
	    list3 = str(list2)
	    #print list3
	    return list3


def html_to_text(html):
    html = html.replace('<DESCRIPTION>','DESCRIPTION')
    html = re.sub(r'body{margin:0;}form{margin:0;padding:0;}.*?#lastArticle {page-break-after:avoid;}', '', html)
    html = html.replace('<b class="enHeadline">', 'HEADLINEOFTEXT:')
    html = html.replace('<TABLE', '\n****BEG TABLE*****\n<TABLE')
    html = html.replace('</TABLE>', '</TABLE>\n---**---\n') #CHANGED JOSH'S CODE HERE FROM XX TO **
    html = html.replace('<table', '\n****END TABLE*****\n<table')
    html = html.replace('</table>', '</table>\n---**---\n') #CHANGED JOSH'S CODE HERE FROM XX TO **
    html = html.replace('&#038;', '&')
    html = html.replace('&#043;', '+')
    html = html.replace('&#110;', ' ')
    html = html.replace('&#120;',' ')
    html = html.replace('&#134;', ' ')
    html = html.replace('&#146;', "'")
    html = html.replace('&#147;', ' ')
    html = html.replace('&#148;', ' ')
    html = html.replace('&#149;', ' ')
    html = html.replace('&#150;', '-')
    html = html.replace('&#151;', '-')
    html = html.replace('&#153;', 'TM')
    html = html.replace('&#160;', ' ')
    html = html.replace('&#160;', ' ')
    html = html.replace('&#167;', ' ')
    html = html.replace('&#168;', ' ')
    html = html.replace('&#169;', ' ')
    html = html.replace('&#173;', ' ')
    html = html.replace('&#179;', ' ')
    html = html.replace('&#183;', ' ')
    html = html.replace('&#183;', ' ')
    html = html.replace('&#215;', ' ')
    html = html.replace('&#216;', ' ')
    html = html.replace('&#243;', ' ')
    html = html.replace('&#252;', ' ')
    html = html.replace('&#253;', ' ')
    html = html.replace('&#36;', ' ') #Dollar sign
    html = html.replace('&#38;', '&')
    html = html.replace('&#8199;', ' ')
    html = html.replace('&#8206;', ' ')
    html = html.replace('&#8211;', '-')
    html = html.replace('&#8212;', '-')
    html = html.replace('&#8216;', ' ') #Leading Apostrophe
    html = html.replace('&#8217;', '') # Apostrophe
    html = html.replace('&#8220;', ' ') 
    html = html.replace('&#8221;', ' ')
    html = html.replace('&#8722;', '-')
    html = html.replace('&#9;', ' ')
    html = html.replace('&#916;', ' ')
    html = html.replace('&#961;', ' ')
    html = html.replace('&#9679;', '-')
    html = html.replace('&amp;', '&')
    html = html.replace('&nbsp;', ' ')
    html = html.replace('&#x2019;', "'")
    html = html.replace('&#x201C;', '"')
    html = html.replace('&#x201D;', '"')
    html = html.replace('&reg;', ' ')
    html = html.replace('&rsquo;', "'")
    html = re.sub(r'&#.*?;', ' ', html)
    html = re.sub(' +',' ',html) #Remove multiple spaces
    html = html.replace('<TR', '<tr')
    html = html.replace('</TR>', '</tr>')
    html = html.replace('<SUP', '<sup')
    html = html.replace('</SUP>', '</sup>')
    html = html.replace('<TD', '<td')
    html = html.replace('</TD>', '</td>')
    html = html.replace('<FONT', '<font')
    html = html.replace('</FONT>', '</font>')
    html = html.replace('<A NAME', '<a name')
    html = html.replace('</A>', '</a>')
    rows = html.split('<tr') # Split into rows
    new_html = []
    new_html.append(rows[0])
    for r,row in enumerate(rows):
        if r > 0:
            row = '<tr'+row
            row = re.sub(r'<sup.*?>', '', row)
            row = re.sub(r'</sup>', '', row)
            row = re.sub(r'<font.*?>', '', row)
            row = re.sub(r'</font>', '', row)
            row = re.sub(r'<a name.*?>', '', row)
            row = re.sub(r'</a>', '', row)
            row = re.sub(r'<td.*?>', '|', row)
            row = re.sub(r'</td>', '', row)
            rowsplit = row.split('</tr>')
            row1 = rowsplit[0]
            row2 = ''.join(rowsplit[1:])
            row1 = re.sub(r'<.*?>', ' ', row1)
            row = row1+' '+row2
            new_html.append(row)
    html = '\n'.join(new_html)
    html = re.sub(r'<td.*?>', '|', html)
    html = re.sub(r'</td>', '', html)
    html = re.sub(r'<sup.*?>', '', html)
    html = re.sub(r'</sup>', '', html)
    html = re.sub(r'<span.*?>', '', html)
    html = re.sub(r'</span>', '', html)
    html = re.sub(r'<font.*?>', '', html)
    html = re.sub(r'</font>', '', html)
    html = re.sub(r'<a name.*?>', '', html)
    html = re.sub(r'</a>', '', html)
    html = re.sub(r'<.*?>', '\n', html)
    #print html[0:5000]
    return html

# #################################################################################################################################################################
# Execution
# #################################################################################################################################################################

print "Starting NSAR Parsing"

# Test File Location
#Perform on a whole directory:

#do_parse(r'C:\Users\jacquelyn.gillette\Desktop\Tens_1\10Ks', r'C:\Users\jacquelyn.gillette\Desktop\Tens_1\10Ks\Parse_v1.csv')

do_parse(r'E:\GJZ', r'C:\Users\Jacquelyn\Desktop\Parse_Word_Grammar.csv')


# Perform on a single file:

#lines = parse_file(r'E:\GJZ\0000001985-96-000001.txt')
#print lines

#lines = parse_file(r'C:\Users\jacquelyn.gillette\Desktop\Tens_1\10Ks\0000002034-96-000004.txt')
#print lines

print "Ending NSAR Parsing"



