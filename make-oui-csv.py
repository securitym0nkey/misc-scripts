#!/usr/bin/python
import re
import csv
import argparse
import sys

oui_re = re.compile("^([0-9A-F]{2}-[0-9A-F]{2}-[0-9A-F]{2})\s+\(hex\)\s+(.*)")

def process(oui_txt,oui_csv,delimiter):
        cvswriter = csv.writer(oui_csv,quoting=csv.QUOTE_ALL)
        for line in oui_txt:
            m = oui_re.match(line)
            if m:
                cvswriter.writerow((m.group(1).replace('-',delimiter),m.group(2)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This tool read oui.txt and outputs a CSV file.')
    parser.add_argument('-i',dest='infile', type=argparse.FileType('r'), default=sys.stdin, help='Input file with format of http://standards-oui.ieee.org/oui/oui.txt. Default is stdin.')
    parser.add_argument('-o',dest='outfile', type=argparse.FileType('w'), default=sys.stdout, help='CSV output file. Default is stdout.' )
    parser.add_argument('--dash',dest='delimiter',action='store_const',const='-',default=':',help="Use dash(-) instead of colon(:) as OUI delimiter")
    args = parser.parse_args()

    process(args.infile,args.outfile,args.delimiter)

