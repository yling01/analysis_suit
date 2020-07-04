import numpy as np

def writeDummyPDB(hotLoop, cyclicPeptide):

    backbone = ['N', 'CA', 'C']

    hotLoop = np.loadtxt(hotLoop, comments=["REMARK", "TITLE", "MODEL", "TER", "ENDMDL"], usecols = [6,7,8], skiprows=5)
    with open(cyclicPeptide, "r") as fi_cyclic:
        lines_to_change = fi_cyclic.readlines()
    fo = open("dummy.pdb", "w+")

    lines_to_write = []
    counter = 0
    for line in lines_to_change:
        line_string = line.split()
        if line_string[0] == "ATOM" and counter < len(hotLoop):
            if line_string[2] == backbone[counter % 3]:
                for i in range(3):
                    string_to_replace = " " * (8 - len(line_string[5+i])) + line_string[5+i]
                    string_to_add = " " * (8 - len(str(hotLoop[counter][i]))) + str(hotLoop[counter][i])
                    line = line.replace(string_to_replace, string_to_add)
                counter += 1
        lines_to_write.append(line)        
            
    with open("dummy.pdb", "w+") as fo:
        for line in lines_to_write:
            fo.write(line)
#Here, SESE.pdb is the hotloop only file that only has the backbone atoms
#and frame.pdb is one frame from the simulation
writeDummyPDB("SESE.pdb", "frame.pdb") 
