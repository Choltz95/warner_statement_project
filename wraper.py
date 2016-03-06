import sys
import subprocess
import os
import csv
import parse_lib
import count_errors
def usage():
    print "usage: python wraper.py <data/>{mandatory} <-c cores>{optional} <-g>{optional}"

def main():
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)
    cleaned_text = ""
    baseline = ()
    data_dir = sys.argv[1]
    g = sys.argv[2] if len(sys.argv)>3 else ""
    if not os.path.exists("result"):
        os.makedirs("result")

    with open("result/" + "log" + ".csv",'w') as f:
        csv_out = csv.writer(f)
        csv_out.writerow(["fname","sic","filing type", "filing date", "date", "cname", "length", "sp errors", "gm errors"])
    for report in os.listdir(data_dir):
        file_dir = data_dir + "/" + report
        if report == "error_log.txt" or report == "custom_dict.txt" or report == "sp_test.txt":
            continue;
        if report.endswith(".txt"):
            baseline = parse_lib.parse_file_meta(file_dir)
            #print baseline

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
