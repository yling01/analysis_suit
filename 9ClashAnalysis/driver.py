import os
import sys
if os.path.exists("result.txt"):
  os.remove("result.txt")
counter = 0
with open(sys.argv[1], "r") as pdb:
    text = pdb.readlines()
length = len(text)
for lines in text:
    counter += 1
    if lines == "ENDMDL\n":
        break
for frame in range(0, length, counter):
    with open("out.pdb", "w+") as pdbWrite:
        for items in text[frame:(frame + counter)]:
            pdbWrite.write(items)
    #os.system("/Applications/Chimera.app/Contents/MacOS/chimera --script chimScript.py --nogui")
    os.system("/cluster/home/yling01/.local/UCSF-Chimera64-1.14/bin/chimera --nogui --script chimScript.py --silent")
