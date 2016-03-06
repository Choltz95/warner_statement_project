import sys
import subprocess
import os
import csv
import parse_lib
import count_errors
def main():
    cleaned_text = ""
    errs = ""
    baseline = ()
    for report in os.listdir("."):
        if report == "error_log.txt" or report == "custom_dict.txt" or report == "sp_test.txt":
            continue;
        if report.endswith(".txt"):
            baseline = parse_lib.parse_file_meta(report)
            #print baseline

            with open("cleaned_files/" + os.path.splitext(report)[0] + "_processed" + ".txt",'w') as f:
                print "cleaning text..."
                cmd = "python html2text.py -b 0 " + report
                f.write(subprocess.check_output(cmd, shell=True))
            print "counting errors..."
            sp_cnt,gm_cnt = str(count_errors.enum_errs("cleaned_files/" + os.path.splitext(report)[0] + "_processed" + ".txt"))
            baseline = baseline + (errs,gm_cnt,)
            print baseline
        with open("cleaned_files/" + os.path.splitext(report)[0] + "_log" + ".txt",'w') as f:
            f.write(str(baseline))

if __name__ == "__main__":
    main()
