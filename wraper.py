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
    print "usage: python wraper.py <data/>{mandatory} <-g>{optional} <-uc>{coptional} <-c cores>{optional}"

def argparse(argv):
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)
    data_dir = sys.argv[1]
    g = "-g" if "-g" in sys.argv else ""
    uc = "-uc" if "-uc" in sys.argv else ""
    c = 4
    return data_dir,g,uc,c

def main():
    cleaned_text = ""
    baseline = ()
    data_dir,g,uc,c = argparse(sys.argv)

    if not os.path.exists("result"):
        os.makedirs("result")

    with open("result/" + "log" + ".csv",'w') as f:
        csv_out = csv.writer(f)
        csv_out.writerow(["fname","sic","filing type", "filing date", "date", "cname", "length", "sp errors", "gm errors"])

    for report in os.listdir(data_dir):
        file_dir = data_dir + "/" + report
        # ignore some temporary text files
        if report == "error_log.txt" or report == "custom_dict.txt" or report == "sp_test.txt":
            continue;
        if report.endswith(".txt"):
            baseline = parse_lib.parse_file_meta(file_dir)

            with open("result/" + os.path.splitext(report)[0] + "_processed" + ".txt",'w') as f:
                print "cleaning text..."
                cmd = "python html2text.py -b 0 " + file_dir
                f.write(subprocess.check_output(cmd, shell=True))

            print "counting errors..."
            sp_cnt,gm_cnt = count_errors.enum_errs("result/" + os.path.splitext(report)[0] + "_processed" + ".txt",g)
            baseline = baseline + (sp_cnt,gm_cnt,)
            print baseline

        with open("result/" + "log" + ".csv",'a+') as f:
            csv_out = csv.writer(f)
            csv_out.writerow(baseline)

if __name__ == "__main__":
    main()
