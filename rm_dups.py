seen = set()
of = open("words_new",'w')
with open("words",'r') as f:
    for line in f:
        if line not in seen:
	    of.write(line)
	    seen.add(line)
	    
