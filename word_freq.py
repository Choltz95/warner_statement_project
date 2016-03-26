"""
word_freq.py - change to stats.py 
compute frequency of mispelled words

TODO: 
 - Generalize statistics, give lists of documents for which incorrect words appear
"""

from collections import defaultdict
def main():
	d = defaultdict(int)
	with open("sp_log","r") as log:
		for line in log:
			for word in line.split():
				d[word] += 1
	for key, value in sorted(d.iteritems(), key=lambda (k,v): (v,k)):
	    print "%s: %s" % (key, value)
main()
