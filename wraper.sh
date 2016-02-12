#!/bin/bash

mkdir -p cleaned_files

for f in *.txt
do
    if [ "$f" == "error_log.txt" ] ; then
        continue;
    fi
    echo "converting ${f} to text..."
    python html2text.py -b 0 ${f} > "cleaned_files/${f}_processed.txt"
    echo "cleaning ${f}..."
    python clean.py "cleaned_files/${f}_processed.txt" > "cleaned_files/${f}_cleaned.txt"
    rm "cleaned_files/${f}_processed.txt"
    echo "counting spelling errors..."
    python count_errors.py "cleaned_files/${f}_cleaned.txt" >> "error_log.txt"
done
