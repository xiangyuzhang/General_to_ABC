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

def rebuild(Inputs,Outputs,Wires,gates,circuitIn):

    circuit_type = re.search("[A-Za-z0-9]*",circuitIn).group()

    module = "module " + circuit_type + " (" + (",").join(Inputs) + "," + (",").join(Outputs) + ");\n\n"

    input = "input " + (",").join(Inputs) + ";\n\n"

    output = "output " + (",").join(Outputs) + ";\n\n"

    wire = "wire " + (",").join(Wires) + ";\n\n"

    gate_list = ("").join(gates)

    result = module + input + output + wire + gate_list + "\nendmodule\n"

    return result


def gate_converter(gate_type, nets_info):
    gate = ""
    output = nets_info["output"]
    inputs = nets_info["input"]
    gate = gate_type + " gate("
    dict = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h', 8:'i', 9:'j', 10:'k', 11:'l', 12:'m', 13:'n', 14:'o', 15:'p',
            16:'q', 17:'r', 18:'s', 19:'t', 20:'u', 21:'v', 22:'w', 23:'x', 24:'y', 25:'z'}
    for index in range(0, len(inputs)):
        gate += " ." + dict[index] + "(" + inputs[index] + "),"
    gate += " .O(" + output + ") );\n"
    return gate
    print ""

def collect_wire_info(inputs, outputs, wires, line_str):
    output_name = re.findall('.*\=',line_str)[0].replace(" ","").replace("=","")
    inputs_name = find_netname_in_brace(line_str)
    if output_name not in outputs and output_name not in wires:
        wires.append(output_name)
    for input_name in inputs_name:
        if input_name not in inputs and input_name not in wires:
            wires.append(input_name)
    nets_info = {"input":inputs_name,"output":output_name}
    return nets_info

def find_gate_type(line_str):
    type = re.findall("\=.*\(",line_str)[0].replace(" ",'').replace("=",'').replace("(",'')
    fanin_number = len(find_netname_in_brace(line_str))
    return type + str(fanin_number)

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
# analyze gate line: store wire and convert
for line in Vin:
    if "=" in line:
        nets_info = collect_wire_info(Inputs, Outputs, Wires, line)
        gate_type = find_gate_type(line)
        gates.append(gate_converter(gate_type,nets_info))

result = rebuild(Inputs,Outputs,Wires,gates,circuitIn)

with open(re.search("[A-Za-z0-9]*",circuitIn).group() + "-abcmap-fmt.v", "w") as outfile:
    outfile.write(result)



