import sys
import subprocess
import os
import csv
import parse_lib
import count_errors

"""
data: directory containing forms
-g: set flag if grammar checking is needed
-uc: set flag if case sensitivity (caped words checked)
-c: todo get #cores from command line
"""
def usage():
    print "usage: python wraper.py <data/>{mandatory} <-g>{optional} <-uc>{optional} <-c cores>{optional}"

def argparse(argv):
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)
    #data_dir = r'/run/media/choltz2/My Passport/GJZ3'
    data_dir = sys.argv[1]
    g = "-g" if "-g" in sys.argv else ""
    uc = "-uc" if "-uc" in sys.argv else ""
    c = 4
    return data_dir,g,uc,c

def main():
    cleaned_text = ""
    baseline = ()
    data_dir,g,uc,c = argparse(sys.argv)
    files = set()

    if not os.path.exists("result"):
        os.makedirs("result") 
    with open("result/" + "log" + ".csv",'w') as f:
        csv_out = csv.writer(f)
        if os.stat(f.name).st_size == 0:
            csv_out.writerow(["fname","sic","filing type", "filing date", "date", "cname", "length", "sp errors", "gm errors"])
    if os.path.isfile("file_log"):
        with open("file_log", "r") as f_log:
            # do stuff
	    for line in f_log:
	        files.add(line.rstrip())	
            #print "f_log open"
    for report in os.listdir(data_dir):
        if report.rstrip() in files: # file already parsed previously
	    continue
        file_dir = data_dir + "/" + report
        # ignore some temporary text files
        if report == "error_log.txt" or report == "custom_dict.txt" or report == "sp_test.txt":
            continue;
        if report.endswith(".txt"):
            baseline = parse_lib.parse_file_meta(file_dir)
            with open("file_log",'a+') as f_log:
                f_log.write(baseline[0].rstrip() + "\n")
            with open("result/" + os.path.splitext(report)[0] + "_processed" + ".txt",'w') as f:
                print "cleaning text..."
       		cmd = ["python","html2text.py","-b","0",file_dir]#"python html2text.py -b 0 " + file_dir	
		#f.write(subprocess.check_output(cmd, shell=True))
		output = subprocess.check_output(cmd)
		if output.rstrip() == "ERR_RECUR":
		    print "ERR_RECUR"
		    continue
		else:
		    f.write(output)
		#f.write(subprocess.check_output(cmd))
            print "counting errors..."
            sp_cnt,gm_cnt = count_errors.enum_errs("result/" + os.path.splitext(report)[0] + "_processed" + ".txt",g,uc)
            baseline = baseline + (sp_cnt,gm_cnt,)
            print baseline

        with open("result/" + "log" + ".csv",'a+') as f:
            csv_out = csv.writer(f)
            csv_out.writerow(baseline)

if __name__ == "__main__":
    main()
