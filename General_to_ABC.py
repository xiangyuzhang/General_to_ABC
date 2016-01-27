#!/usr/bin/python
__author__ = 'xiangyuzhang'

import argparse
import os
import readline
import sys
import re
from subprocess import call, Popen, PIPE, STDOUT
import glob


def cmmd_and_path_complete(text, state):
    '''automatically complete path'''
    return (glob.glob(text + '*') + [None])[state] + '/'


def delete_comment(Vin):
    counter = -1
    for line_number in range(0, len(Vin)):
        if "#" in Vin[line_number]:
            counter += 1
        else:
            break
    Vin = Vin[counter + 1:]
    return Vin


def find_inout(line_str):
    name = re.findall("\(.*\)",line_str)[0].replace("(", "").replace(")", "")
    return name

def find_netname_in_brace(line_str):
    raw = re.findall("\(.*\)", line_str)[0].replace("(","").replace(")","")
    raw = raw.replace(" ","")
    if "," in raw:
        result = raw.split(",")
    else:
        result = raw
    return result

def collect_wire_info(inputs, outputs, wires, line_str):
    output_name = re.findall('.*\=',line_str)[0].replace(" ","").replace("=","")
    inputs_name = find_netname_in_brace(line_str)
    if output_name not in outputs and output_name not in wires:
        wires.append(output_name)
    for input_name in inputs_name:
        if input_name not in inputs and input_name not in wires:
            wires.append(input_name)

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

'''open file, read file, and delete comment line'''
with open(circuitPath, "r") as infile:
    Vin = infile.read().split("\n")
Vin = delete_comment(Vin)  # Vin: the modified raw verilog
Inputs = []  # Inputs: store the input nets name
Outputs = []  # Outputs: store the output nets name
Wires = []  # Wires: store the wires name
gates = []  # gates: store the gates info

for line in Vin:
    # collect input info
    if "INPUT" in line:
        Inputs.append(find_inout(line))
    # collect output info
    elif "OUTPUT" in line:
        Outputs.append(find_inout(line))
for line in Vin:
    # analyze gate line
    if "=" in line:
        collect_wire_info(Inputs, Outputs, Wires, line)
print ""
'''convert and store wire'''
