#!/bin/bash

mkdir -p cleaned_files
rm error_log.txt
for f in *.txt
do
    f_name=${f::-4}
    if [ "$f" == "error_log.txt" ] || [ "$f" == "custom_dict.txt" ] || [ "$f" == "sp_test.txt" ]; then
        continue;
    fi
    echo "converting ${f} to text..."
    python html2text.py -b 0 ${f} > "cleaned_files/${f_name}_processed.txt"
    echo "cleaning ${f}..."
    python clean.py "cleaned_files/${f_name}_processed.txt" > "cleaned_files/${f_name}_cleaned.txt"
    rm "cleaned_files/${f_name}_processed.txt"
    echo "counting spelling errors..."
    python count_errors.py "cleaned_files/${f_name}_cleaned.txt" >> "error_log.txt"

    awk '/./{line=$0} END{print line}' error_log.txt
done
