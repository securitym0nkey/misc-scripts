#!/usr/bin/python
import re
import csv
import argparse
import sys

oui_re = re.compile("^([0-9A-F]{2}-[0-9A-F]{2}-[0-9A-F]{2})\s+\(hex\)\s+([^\r\n]+)")

def process(oui_txt,oui_csv,delimiter,duplicate_delimiter=None):
        oui_vendormapping = {}

        for line in oui_txt:
            m = oui_re.match(line)
            if m:
                oui = m.group(1)
                vendorname = m.group(2)
                if oui in oui_vendormapping:
                    print('[WARNING] Duplicate for "{0}". Listed for "{2}" and "{1}"'.format(oui,oui_vendormapping[oui],vendorname), file=sys.stderr)
                    if duplicate_delimiter:
                        vendorname = oui_vendormapping[oui] + duplicate_delimiter + vendorname
                oui_vendormapping[oui] = vendorname

        cvswriter = csv.writer(oui_csv,quoting=csv.QUOTE_ALL)
        for oui, vendorname in oui_vendormapping.items():
             cvswriter.writerow((oui.replace('-',delimiter),vendorname))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This tool read oui.txt and outputs a CSV file.')
    parser.add_argument('-i',dest='infile', type=argparse.FileType('r'), default=sys.stdin, help='Input file with format of http://standards-oui.ieee.org/oui/oui.txt. Default is stdin.')
    parser.add_argument('-o',dest='outfile', type=argparse.FileType('w'), default=sys.stdout, help='CSV output file. Default is stdout.' )
    parser.add_argument('--dash',dest='delimiter',action='store_const',const='-',default=':',help="Use dash(-) instead of colon(:) as OUI delimiter")
    parser.add_argument('--duplicate-delimiter',dest='duplicate_delimiter',action='store',default=None,help="If specified duplicate listings for one OUI vendornames will be concatenated using this delimiter.")
    args = parser.parse_args()

    process(args.infile,args.outfile,args.delimiter,duplicate_delimiter=args.duplicate_delimiter)

