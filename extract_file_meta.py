import sys
import string
import re
import htmlentitydefs

def parse_file_meta(fullpath):
        fin = open(fullpath, 'r')
        data = fin.read()
        fin.close()

        try:
                fmt = r'(?s)<(SEC|IMS)-HEADER>(.*)</(SEC|IMS)-HEADER>'
                header = re.findall(fmt,data,re.DOTALL)[0][1]
        except StandardError as e:
                header=r''


        # Accession Number
        try:
                fmt = r'(?sm)ACCESSION NUMBER:\s+(\S+)\s*$'
                accession_num =  re.findall(fmt,header, re.DOTALL)[0]
        except StandardError as e:
                accession_num=r''


        # CIK Number
        try:
                fmt = r'(?sm)CENTRAL INDEX KEY:\s+(\d+)\s*$'
                cik =  re.findall(fmt,header,re.DOTALL)[0]
        except StandardError as e:
                cik=r''

        #EDGAR Form Type (i.e. 10-K or 10-K/A)
        try:
                fmt = r'(?sm)CONFORMED SUBMISSION TYPE:\s+(\S+)\s*$'
                form_type =  re.findall(fmt,header,re.DOTALL)[0]
        except StandardError as e:
                form_type=r''

        #Fiscal Year End
        try:
                fmt = r'(?sm)CONFORMED PERIOD OF REPORT:\s+(\d+)\s*$'
                fye =  re.findall(fmt,header,re.DOTALL)[0]
        except StandardError as e:
                fye =r''

        #Filing Date
        try:
                fmt = r'(?sm)FILED AS OF DATE:\s+(\d+)\s*$'
                file_date =  re.findall(fmt,header,re.DOTALL)[0]
        except StandardError as e:
                file_date=r''

        #Company Name
        try:
                fmt = r'(?sm)COMPANY CONFORMED NAME:\s+(.*)CENTRAL INDEX KEY'
                co_name =  re.findall(fmt,header,re.DOTALL)[0]
        except StandardError as e:
                co_name=r''
        co_name = co_name.rstrip()
        co_name = co_name.rstrip("\n")
        co_name = co_name.rstrip("\r")

        try:
                fmt = r'(?sm)STANDARD INDUSTRIAL CLASSIFICATION:\s+(\d+)\s*$'
                sic =  re.findall(fmt,header,re.DOTALL)[0]
        except StandardError as e:
                sic=r''

        if sic == r'':
                try:
                        fmt = r'(?sm)STANDARD INDUSTRIAL CLASSIFICATION:.*\[(\d+)\].*IRS NUMBER'
                        sic =  re.findall(fmt,header,re.DOTALL)[0]
                except StandardError as e:
                        sic=r''

        fmt = r'(?s)<DOCUMENT>(.*?)</DOCUMENT>'

        try:
                tbl = r'(?s)<TABLE>(.*?)</TABLE>'
        except StandardError as e:
                tbl = r''

        bod = re.findall(fmt,data,re.DOTALL)[0]

        try:
                table = re.findall(tbl,data,re.DOTALL)[0] #Get rid of table of contents to identify beginning of MDA section correctly
        except StandardError as e:
                table = r''

        #baseline  = (accession_num, cik, form_type, fye, file_date, co_name, sic)
        return (accession_num,cik,form_type,fye,file_Date,co_name,sic)
