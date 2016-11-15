#!/usr/bin/env python
import random
import string
import argparse


def gen_group(size,chars):
 return ''.join(random.choice(chars) for _ in range(size))

def gen_code(group_size,group_count,group_delimiter,chars):
 return group_delimiter.join(gen_group(group_size,chars) for _ in range(group_count) )

if __name__ == "__main__":
 argp = argparse.ArgumentParser(description='Generates a random passcode which is splitted in groups')
 argp.add_argument('group_size',metavar='GROUP_SIZE', type=int, help='The size of each group')
 argp.add_argument('group_count',metavar='GROUP_COUNT', type=int, help='The amount of groups to generate')
 argp.add_argument('--delimiter',nargs='?',default='-',help='Delimiter is put between groups. Default is -.')
 args = argp.parse_args()

 #possibilities=len(chars)**(args.group_size*args.group_count)
 chars=string.ascii_uppercase + string.digits
 print(gen_code(args.group_size,args.group_count,args.delimiter,chars))
