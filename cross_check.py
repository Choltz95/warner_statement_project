import sys
import re
import os
import csv
import parse_lib
import count_errors

def main():
    f_counter = 0
    with open("loughran_mcdonald.txt") as d:
    	lm_dict = d.read().splitlines()  
    for report in os.listdir("log"):
        cs_words = []
        if report.endswith(".sp_log"):
  	    f_counter+=1
	    if f_counter %500 == 0:
	        print(f_counter)
	    with open("log/" + os.path.splitext(report)[0] + ".sp_log",'r') as f:	
	        for line in f:
		    word = re.search('\*\*(.*)\*\*', line)
		    w = word.group(1)
		    if w in lm_dict:
		        #print w
		        cs_words.append(w)
 	    l = len(cs_words)
	    if l > 0:
	        with open("cc.txt",'a') as f:
	            f.write(report + " " + str(len(cs_words)) + "\n")
if __name__ == "__main__":
    main()

