# Simple Assembler
# Author: Alexander Black
# Revision: 10OCT2023
# BLACK16A Architecture Machine Code Hex Converter
# command format: python assembler.py input.b16a output.hex

# This script is designed to be as simple as possible, first seeing use in the development of the BLACK16A architecture.  
# This is not a feature complete compiler, and consider it as little more as a way to get out of writing the hex by hand with an instruction table.
# Supported are raw instructions, and <address> markers to act as a jump point for the compiler. See example code for how this works.
# NOTICE: This script is was made in a couple hours for initial prototyping reasons and may have issues. No guarentees.

import sys
import re


op_dict = {
    "NOF" :"00",    
    "RST" :"01",
    "BRK" :"02",
    "ICL" :"04",
    "VDF" :"0B",
    "VDW" :"0C",
    "VCP" :"0D",
    "SET" :"0E",
    "CP"  :"0F",
    "JZ"  :"10",
    "JNZ" :"11",
    "JZF" :"12",
    "JOF" :"13",
    "JZOF":"14",
    "JMP" :"15",
    "ADD" :"20",
    "ADDI":"21",
    "ADDC":"22",
    "SUB" :"23",
    "NOT" :"24",
    "AND" :"25",
    "ANDI":"26",
    "OR"  :"27",
    "ORI" :"28",
    "XOR" :"29",
    "XORI":"2A",
    "SHL" :"2B",
    "SHR" :"2C",
    "ROL" :"2D",
    "ROR" :"2E"
}            

reg_dict = {        # DOES NOT YET INCLUDE VN32 VIRTUAL REGISTERS
    "PC"  :"00",
    "PCX" :"01",
    "GR0" :"02",
    "GR1" :"03",
    "GR2" :"04",
    "GR3" :"05",
    "GR4" :"06",
    "GR5" :"07",
    "GR6" :"08",
    "GR7" :"09",
    "GR8" :"0A",
    "GR9" :"0B",
    "GRA" :"0C",
    "GRB" :"0D",
    "GRC" :"0E",
    "GRD" :"0F",
    "GRE" :"10",
    "GRF" :"11",
    "PFR" :"12",
    "FR"  :"13",
    "ZRO" :"14",
    "ONE" :"15",
    "IJA" :"16",
    "PCP" :"17",
    "PCXP":"18",
    "SP"  :"19",
    "VPN" :"1A",
    "PO0" :"20",
    "PO1" :"21",
    "PO2" :"22",
    "PO3" :"23",
    "PI0" :"24",
    "PI1" :"25",
    "PI2" :"26",
    "PI3" :"27",
    "PIC0":"28",
    "PIC1":"29",
    "PIC2":"2A",
    "PIC3":"2B",
    "PI0" :"2C",
    "PI1" :"2D",
    "PI2" :"2E",
    "PI3" :"2F",
    "TCF" :"30",
    "TV0" :"31",
    "TV1" :"32",
    "TV2" :"33",
    "TV3" :"34",
    "TR0" :"35",
    "TR1" :"36",
    "TR2" :"37",
    "TR3" :"38",
    "TPR0":"39",
    "TPR1":"3A",
    "TPR2":"3B",
    "TPR3":"3C",
    "TPWM":"3D",
    "TIR" :"3E",
    "VPC" :"00",
    "VR0" :"02",
    "VR1" :"04",
    "VR2" :"06",
    "VR3" :"08",
    "VR4" :"0A",
    "VR5" :"0C",
    "VR6" :"0E",
    "VR7" :"10",
    "VZRO":"14",
    "VPCP":"16",
    "VPO0":"20",
    "VPO1":"22",
    "VPI0":"24",
    "VPI1":"26",
    "VPC0":"28",
    "VPC1":"2A",
    "VI0" :"2c",
    "VI1" :"2E",    
    "VTV0":"31",
    "VTV1":"33",
    "VTR0":"35",
    "VTR1":"37"
}           




def main():
    # Step 1: Load every single line into a list, where each element is split by a newline character
    args = sys.argv
    fi = open(args[1], "r")
    lines = fi.readlines()
    fi.close()

    # Step 2: Remove comments - delete all characters including and after the first ; character
    for i in range(0, len(lines)):
        lines[i] = lines[i].split(";", 1)[0]

    # Step 3: Remove all extraneous whitespace and lines
    # Removes empty lines and a few space lines
    i = 0
    while i < len(lines):
        if len(lines[i]) == 0 or lines[i].isspace():
            lines.pop(i)
        else:
            i = i + 1
    # Remove escaped characters, see https://stackoverflow.com/questions/8115261/how-to-remove-all-the-escape-sequences-from-a-list-of-strings
    i = 0
    while i < len(lines):
        lines[i] = remove_carriage_return(lines[i])
        lines[i] = re.sub("[\t ]{2,}", " ", lines[i])
        lines[i] = lines[i].strip()
        lines[i] = re.sub('[^a-zA-Z0-9<> \n\.]', ' ', lines[i])
        i = i + 1

    # Set 4: Convert to token arrays
    tokens = []
    for l in lines:
        tokens.append(l.split(" "))

    # Step 5: Look for <> address placeholders, note line in dictionary, and remove from parsed system
    jump_dict = {}
    i = 0
    while i < len(tokens):
        if "<" == tokens[i][0][0]:
            jump_dict[tokens[i][0]] = i
            tokens.pop(i)
        else:
            i = i + 1

    ## At this point what should be left can directly start instruction interpretation
    # Step 6: Go line by line and apply operation, register, address placeholder dictionaries and numeric->hex conversions where appropriate
    prog = ""

    for l in tokens:      
        acc = ""                        
        # Process operator
        acc = acc + op_dict[l.pop(0).upper()]
        usedbytes = 1

        # Process any remaining tokens:
        for t in l:
            if "<" in t:
                s = hex(int(jump_dict[t]))[2:]
                while len(s) < 4:
                    s = "0" + s
                acc = acc + s
            elif t.upper() in reg_dict.keys():
                acc = acc + reg_dict[t.upper()]
            else:       # It's a number
                if "b" in t:                        # Binary
                    h = hex(int(t[2:],2))[2:]
                    while len(h) < 4:
                        h = "0" + h
                    acc = acc + h
                elif "o" in t:                      # Octal
                    h = hex(int(t[2:],8))[2:]
                    while len(h) < 4:
                        h = "0" + h
                    acc = acc + h
                elif "x" in t:                      # Hex
                    h = hex(int(t[2:],16))[2:]
                    while len(h) < 4:
                        h = "0" + h
                    acc = acc + h
                else:                               # Decimal
                    h = hex(int(t))[2:]
                    while len(h) < 4:
                        h = "0" + h
                    acc = acc + h
        while len(acc) < 8:
            acc = acc + "00"
        prog = prog + acc.upper() + "\n"

    # Step 7: Save lines to target file
    fo = open(args[2], "w")
    fo.write(prog)
    fo.close()

def debug(list):
    for i in list:
        print(repr(i))

def remove_carriage_return(s):
    return "".join(ch for ch in s if ch not in ['\r', '\n'])

if __name__ == "__main__":
    main()