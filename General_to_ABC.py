#!/usr/bin/python
__author__ = 'xiangyuzhang'

import argparse
import os
import readline
import sys
from subprocess import call, Popen, PIPE, STDOUT
import glob


def cmmd_and_path_complete(text, state):
    '''automatically complete path'''
    return (glob.glob(text + '*') + [None])[state] + '/'


''' Commdline Parser'''

readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")
readline.set_completer(cmmd_and_path_complete)

parser = argparse.ArgumentParser(usage='python generaltoabc.py [-h] <general.v>', description="This is program will"
                                                                                              " convert general format verilog file to ABC format")
parser.add_argument('<general.v>', help="input verilog circuit")
args = parser.parse_args()
circuitIn = sys.argv[1]
circuitPath = os.path.abspath(circuitIn)  # input circuit path

if not os.path.abspath(circuitPath):
    print "Invalid input circuit path!!!\n"

'''open file and read file'''

'''collect input info'''

'''collect output info'''

'''analyze gate line'''

'''convert and store wire'''