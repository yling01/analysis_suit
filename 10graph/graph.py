import optparse
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math
import os
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

def chooseBinSize(length, std):
    return 10 * int(math.log2(length) + 1 + math.log2(1 + 1/std))

def calculateProbability(hist, probabilityCutoff, total=1):
    probability = 0
    for index, ele in enumerate(hist[1][1:]):
        if ele < probabilityCutoff:
            probability += hist[0][index]
        else:
            break
    return (probability / total)

def drawAllAndNoClash(ax_all, ax_noClash, rmsd_mtx, clash_mtx, sequence, color, XTicks, probabilityCutoff):
    assert len(rmsd_mtx) == len(clash_mtx)

    histAllFrames = np.histogram(rmsd_mtx, bins=XTicks)
    totalSum = np.sum(histAllFrames[0])
    ticks = histAllFrames[1]
    ticks_real = 0.5 * (ticks[:-1] + ticks[1:])
    base = ticks_real[1] - ticks_real[0]

    histNoClash = np.histogram(rmsd_mtx[clash_mtx == "No"], bins=XTicks)
    scatterNoClash = histNoClash[0]
    scatterAllFrames = histAllFrames[0]

    myfun =  np.vectorize(lambda x : x / totalSum / base)

    scatterNoClashNormalized = myfun(scatterNoClash)
    scatterAllFramesNormalized = myfun(scatterAllFrames)

    ax_all.plot(ticks_real,
                scatterAllFramesNormalized,
                linestyle='-',
                linewidth=1,
                label=sequence,
                color=color)

    ax_noClash.plot(ticks_real,
                    scatterNoClashNormalized,
                    linestyle='-',
                    linewidth=1,
                    label=sequence,
                    color=color)

    probabilityAllFrame = calculateProbability(histAllFrames, probabilityCutoff, totalSum) * 100
    probabilityNoClashFrame = calculateProbability(histNoClash, probabilityCutoff, totalSum) * 100
    return ticks_real, scatterAllFramesNormalized, scatterNoClashNormalized, probabilityAllFrame, probabilityNoClashFrame

def drawShadow(axis, x, y1, y2, color):
    axis.fill_between(x, y1, y2, facecolor=color, alpha=0.5, interpolate=True)

def setTickes(axis, xmax, ymax):
    # Make a plot with major ticks that are multiples of 20 and minor ticks that
    # are multiples of 5.  Label major ticks with '%d' formatting but don't label
    # minor ticks.
    axis.xaxis.set_major_locator(MultipleLocator(0.2))
    axis.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))

    # For the minor ticks, use no labels; default NullFormatter.
    axis.xaxis.set_minor_locator(MultipleLocator(0.1))
    axis.margins(x=0)
    axis.margins(y=0)
    axis.set_ylim(top=ymax)
    axis.set_xlim(right=xmax)

    axis.yaxis.set_major_locator(MultipleLocator(0.2))
    axis.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

    # For the minor ticks, use no labels; default NullFormatter.
    axis.yaxis.set_minor_locator(MultipleLocator(0.1))

    tickx = axis.xaxis.get_major_ticks()
    ticky = axis.yaxis.get_major_ticks()

    for tick in tickx:
        tick.label.set_fontsize(20)
    for tick in ticky:
        tick.label.set_fontsize(20)

def properWrapper(axis, title, xmax, ymax, index_curr_row, index_curr_col, total, sequence):
    # axis.legend(loc=1, prop={'family': 'monospace', 'size': 20})
    if index_curr_row == 0:
        title = title + "\n" + sequence
    else:
        title = sequence

    axis.set_title(title, fontsize=30)

    setTickes(axis, xmax, ymax)

    if index_curr_row == total - 1:
        axis.set_xlabel("RMSD (Å)", fontsize=25)

    if index_curr_col == 0:
        axis.set_ylabel("Probability Density", fontsize=25)


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("--clashFile_s1", dest = "clashFile_s1", default = "")
    parser.add_option("--clashFile_s2", dest = "clashFile_s2", default = "")
    parser.add_option("--RMSDFile_s1", dest = "RMSDFile_s1", default = "")
    parser.add_option("--RMSDFile_s2", dest = "RMSDFile_s2", default = "")
    parser.add_option("--RMSDCutoff", dest = "RMSDCutoff", default = "2.0")
    parser.add_option("--probabilityCutoff", dest = "probabilityCutoff", default = "0.5")
    parser.add_option("--seq", dest = "seq", default = "")
    (options, args) = parser.parse_args()
    clashFile_s1 = options.clashFile_s1.split(",")
    clashFile_s2 = options.clashFile_s2.split(",")
    RMSDFile_s1 = options.RMSDFile_s1.split(",")
    RMSDFile_s2 = options.RMSDFile_s2.split(",")
    seq = options.seq.split(",")

    assert len(seq) == len(clashFile_s1)
    assert len(clashFile_s1) == len(RMSDFile_s1)
    assert len(clashFile_s2) == len(RMSDFile_s2)
    assert len(clashFile_s1) == len(clashFile_s2)

    RMSDCutoff = float(options.RMSDCutoff)
    probabilityCutoff = float(options.probabilityCutoff)

    color = ['#0a6902', '#9c5808', '#233c9e', '#335cff', '#0a6902', '#0fa103', '#ae016c', '#fc019c','#be0a35', '#f76d8e']
    assert len(seq) <= len(color)
    fig, axs_all = plt.subplots(nrows=len(seq), ncols=2, sharex=True, sharey=True, figsize=(28, 14 * len(seq)))

    vf = np.vectorize((lambda x : 10 * x))
    ymax = 0.0

    probability = []
    peak_x = []
    for index in range(len(seq)):


        rmsdHotLoop_mtx1 = np.loadtxt(RMSDFile_s1[index], comments=["#", "@"], usecols=1)
        clash_mtx1 = np.loadtxt(clashFile_s1[index], usecols=0, dtype=str)

        rmsdHotLoop_mtx2 = np.loadtxt(RMSDFile_s2[index], comments=["#", "@"], usecols=1)
        clash_mtx2 = np.loadtxt(clashFile_s2[index], usecols=0, dtype=str)

        assert len(rmsdHotLoop_mtx1) == len(clash_mtx1)
        assert len(rmsdHotLoop_mtx2) == len(clash_mtx2)

        rmsdHotLoop_mtx1 = vf(rmsdHotLoop_mtx1)
        rmsdHotLoop_mtx2 = vf(rmsdHotLoop_mtx2)

        binSizeHotLoop = max(chooseBinSize(len(rmsdHotLoop_mtx1), np.std(rmsdHotLoop_mtx1)),
                             chooseBinSize(len(rmsdHotLoop_mtx2), np.std(rmsdHotLoop_mtx2)))

        XTicksHotLoop = np.linspace(0, max(np.amax(rmsdHotLoop_mtx1), np.amax(rmsdHotLoop_mtx2)), binSizeHotLoop)

        HotLoopX, HotLoopAllY1, HotLoopNoClashY1, s1_all_prob, s1_noC_prob = drawAllAndNoClash(axs_all[index][0],
                                                                                               axs_all[index][1],
                                                                                               rmsdHotLoop_mtx1,
                                                                                               clash_mtx1,
                                                                                               seq[index],
                                                                                               color[index],
                                                                                               XTicksHotLoop,
                                                                                               probabilityCutoff)

        HotLoopX, HotLoopAllY2, HotLoopNoClashY2, s2_all_prob, s2_noC_prob = drawAllAndNoClash(axs_all[index][0],
                                                                                               axs_all[index][1],
                                                                                               rmsdHotLoop_mtx2,
                                                                                               clash_mtx2,
                                                                                               "",
                                                                                               color[index],
                                                                                               XTicksHotLoop,
                                                                                               probabilityCutoff)

        HotLoopAll_max_x1 = HotLoopX[np.argmax(HotLoopAllY1)]
        HotLoopAll_max_x2 = HotLoopX[np.argmax(HotLoopAllY2)]

        axs_all[index][0].axvline(HotLoopAll_max_x1, ls="--")
        axs_all[index][0].axvline(HotLoopAll_max_x2, ls="--")
        HotLoopNoClash_max_x1 = HotLoopX[np.argmax(HotLoopNoClashY1)]
        HotLoopNoClash_max_x2 = HotLoopX[np.argmax(HotLoopNoClashY2)]
        axs_all[index][1].axvline(HotLoopNoClash_max_x1, ls="--")
        axs_all[index][1].axvline(HotLoopNoClash_max_x2, ls="--")
        all_peak_x = 0.5 * (HotLoopAll_max_x1 + HotLoopAll_max_x2)
        noC_peak_x = 0.5 * (HotLoopNoClash_max_x1 + HotLoopNoClash_max_x2)
        peak_x.append((all_peak_x, noC_peak_x))

        all_prob = 0.5 * (s1_all_prob + s2_all_prob)
        noC_prob = 0.5 * (s1_noC_prob + s2_noC_prob)

        probability.append((all_prob, noC_prob))

        curr_max = max(np.amax(HotLoopAllY1), np.amax(HotLoopAllY2))
        if ymax < curr_max:
            ymax = curr_max

        drawShadow(axs_all[index][1], HotLoopX, HotLoopNoClashY1, HotLoopNoClashY2, color[index])
        drawShadow(axs_all[index][0], HotLoopX, HotLoopAllY1, HotLoopAllY2, color[index])

    ymax += 1.0

    for index in range(len(seq)):
        properWrapper(axs_all[index][1], "No Clash Only", RMSDCutoff, ymax, index, 1, len(seq), "%s\nPr(RMSD < %.1fÅ | No Clash) = %.2f%%\nHighest Probability Found At %.3fÅ" % (seq[index], probabilityCutoff, probability[index][1], peak_x[index][1]))
        properWrapper(axs_all[index][0], "All Frames", RMSDCutoff, ymax, index, 0, len(seq), "%s\nPr(RMSD < %.1fÅ) = %.2f%%\nHighest Probability Found At %.3fÅ" % (seq[index], probabilityCutoff, probability[index][0], peak_x[index][0]))

    fig.savefig(filename="histogram.png", dpi=300)


