#USAGE: python rmsd.py hotloop.xvg star.xvg clash.xvg sequence
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
import math
import os
def chooseBinSize(length, std):
    return 10 * int(math.log2(length) + 1 + math.log2(1 + 1/std))

def calculateProbability(hist, cutoff, total):
    probability = 0
    for index, ele in enumerate(hist[1][1:]):
        if ele < cutoff:
            probability += hist[0][index] 
        else:
        	break
    return int(probability / total * 100)

def findMid(arr):
	midTicks = []
	for index in range(len(arr) - 1):
		midTicks.append(0.5 * (arr[index] + arr[index + 1]))
	return midTicks

def drawAllAndNoClash(ax, rmsd_mtx, clash_mtx, sequence, color, flag):
	cutoff = 0.5
	vf = np.vectorize((lambda x : 10 * x))
	#convert nm to A
	rmsd_mtx = vf(rmsd_mtx)

	binSize = chooseBinSize(len(rmsd_mtx), np.std(rmsd_mtx))
	XTicks = np.linspace(0, np.amax(rmsd_mtx), binSize)

	histAllFrames = np.histogram(rmsd_mtx, bins=XTicks)
	totalSum = np.sum(histAllFrames[0])
	ticks = histAllFrames[1]
	ticks_real = np.array([])
	for i in range(len(ticks) - 1):
		ticks_real = np.append(ticks_real, 0.5*(ticks[i] + ticks[i+1]))
	base = ticks_real[1] - ticks_real[0]
	myfun =  np.vectorize(lambda x : x / totalSum / base)

	histNoClash = np.histogram(rmsd_mtx[clash_mtx == "No"], bins=XTicks)
	scatterNoClash = histNoClash[0]
	scatterAllFrames = histAllFrames[0]

	myfun =  np.vectorize(lambda x : x / totalSum / base)
	scatterNoClashNormalized = myfun(scatterNoClash)
	scatterAllFramesNormalized = myfun(scatterAllFrames)

	label1 = sequence + ": all"
	label2 = sequence + ": no clash"

	ax.plot(ticks_real, scatterAllFramesNormalized, linestyle='--', linewidth=1, label=label1, color=color)
	ax.plot(ticks_real, scatterNoClashNormalized, linestyle='-', linewidth=1, label=label2, color=color)


	ax.set_xlabel("RMSD ($\AA$)", fontsize="x-large")
	ax.set_ylabel("Probability Density", fontsize="x-large")

	probabilityAllFrame = ("P(RMSD < " + 
		str(cutoff) + ") = " + 
		str(calculateProbability(histAllFrames, cutoff, totalSum)) + 
		"%")

	probabilityNoClashFrame = ("P(RMSD < " + 
		str(cutoff) + 
		" | no clash) = " + 
		str(calculateProbability(histNoClash, cutoff, totalSum)) + 
		"%")

	with open("probability.txt", "a") as probabilityFile:
		if flag == 1:
			probabilityFile.write(sequence + ":\nto hotloop\n")
			probabilityFile.write(probabilityAllFrame) 
			probabilityFile.write("\n")
			probabilityFile.write(probabilityNoClashFrame)
			probabilityFile.write("\n")
		else:
			probabilityFile.write("to SESEGGGG\n")
			probabilityFile.write(probabilityAllFrame) 
			probabilityFile.write("\n")
			probabilityFile.write(probabilityNoClashFrame)
			probabilityFile.write("\n")
			probabilityFile.write("\n")


def main():
	#color = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
	color = ['red', 'orange', 'green', 'blue', 'indigo', 'violet', 'black']
	fig, axs = plt.subplots(nrows=2, ncols=1, sharex=False, sharey=False, figsize=(14,14))
	filesHotLoop = []
	filesCluster = []
	fileClash = []
	sequence = []
	for argsIndex in range(1, len(sys.argv) - 1, 4):
		filesHotLoop.append(sys.argv[argsIndex])
		filesCluster.append(sys.argv[argsIndex + 1])
		fileClash.append(sys.argv[argsIndex + 2])
		sequence.append(sys.argv[argsIndex + 3])

	if float(len(sequence)) > 0.5 * len(color):
		sys.exit("Color Choices Is Not Enough!")

	for index in range(len(sequence)):

		rmsdHotLoop_mtx = np.loadtxt(filesHotLoop[index], comments=["#", "@"], usecols=1)
		rmsdCluster_mtx = np.loadtxt(filesCluster[index], comments=["#", "@"], usecols=1)
		clash_mtx = np.loadtxt(fileClash[index], usecols=0, dtype=str)
		rmsdHotLoop_mtx = rmsdHotLoop_mtx[0:len(clash_mtx)]
		rmsdCluster_mtx = rmsdCluster_mtx[0:len(clash_mtx)]

		drawAllAndNoClash(axs[0], rmsdHotLoop_mtx, clash_mtx, sequence[index], color[index], 1)
		drawAllAndNoClash(axs[1], rmsdCluster_mtx, clash_mtx, sequence[index], color[index], 2)


	axs[0].legend(loc=4)
	axs[1].legend(loc=4)
	axs[0].set_title("To Hotloop")
	axs[1].set_title("To SESEGGGG") 
	fig.savefig(fname="histogram.png", dpi=300)

if __name__ == "__main__":
	main()
