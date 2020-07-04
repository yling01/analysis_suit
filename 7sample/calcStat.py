import sys
import numpy as np
import matplotlib.pyplot as plt
fileName = sys.argv[2]
RMSD = np.loadtxt(sys.argv[1], usecols = (1,), comments = ["#", "@"])
print(fileName)
with open(fileName, "w+") as fo:
    fo.write("%.3f\n%.3f" % ((10 * np.mean(RMSD)), (10* np.std(RMSD))))
