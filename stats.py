"""
word_freq.py - change to stats.py 
compute frequency of mispelled words

TODO: 
 - Generalize statistics, give lists of documents for which incorrect words appear
"""
import csv
from collections import Counter, defaultdict

def average_col(csv_path):
    col_totals = Counter()
    with open(csv_path, "rb") as f:
        reader = csv.reader(f)
        row_cnt = 0.0
        for row in reader:
            for col_idx, col_val in enumerate(row):
                try:
                    n = float(col_val)
                    col_totals[col_idx] += n
                except ValueError:
                    pass
            row_cnt += 1.0
    row_cnt -= 1.0
    col_indexes = col_totals.keys()
    col_indexes.sort()

    averages = [col_totals[idx]/row_cnt for idx in col_indexes]
    return averages

def main():
    log_path = "log/log.csv"
    lines = 0.0
    cnt = 0.0
    with open(log_path) as f:
        log = csv.reader(f)
        for line in f:
            lines += 1
            if "ERR_RECUR" in line:
                cnt += 1
    averages = average_col(log_path)
    print "spelling_errors,grammar_errors"
    print str(averages[-2]) + "," + str(averages[-1])
    print "percent error (unparsed)"
    print str(cnt/lines)
    
main()
