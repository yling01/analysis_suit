import numpy as np
import matplotlib.pyplot as plt
import sys
RMSD = np.loadtxt(sys.argv[1], usecols = (1,), comments = ["#", "@"])
with open("stat.txt", "w+") as fo:
    fo.write("%.3f\n%.3f" % ((10 * np.mean(RMSD)), (10* np.std(RMSD))))
