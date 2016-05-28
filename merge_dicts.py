filenames = ['custom_dict.txt', 'loughran_mcdonald.txt']
with open('dict.txt', 'w') as outfile:
    words = []
    for fname in filenames:
        with open(fname) as infile:
            for line in infile:
        	words.append(line)        
    d = set(words)
    for word in sorted(d):
    	outfile.write(word) 
