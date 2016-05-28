import sys
import csv
import collections

counter = 0

with open("cc.txt", 'r') as infile, open("old_log.csv",'r') as logfile, open("log.csv","w") as outfile:
    reader = csv.DictReader(logfile)
    result = collections.OrderedDict()
    for row in reader:
        key = row.pop('fname')
	result[key] = row
            
    for row in infile:
        file_name,correction = row.split()
	file_name = file_name.split('_process',1)[0]
	try:
	    cur_errors = result[file_name]["sp errors"]
	    corrected_errors = int(cur_errors) - int(correction)
	    result[file_name]["sp errors"] = str(corrected_errors)
        except:
	    print file_name + " key err"
    header = reader.fieldnames 
    writer = csv.writer(outfile,header)
    writer.writerow(header)
    header.remove('fname')
    for row in result:
        r = (row,)
	for h in header:
   	#for k, v in result[row].items():
	    r = r + (result[row][h],)
        writer.writerow(r)
