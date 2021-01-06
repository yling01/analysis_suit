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
    axis.xaxis.set_major_locator(MultipleLocator(0.4))
    axis.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))

    # For the minor ticks, use no labels; default NullFormatter.
    axis.xaxis.set_minor_locator(MultipleLocator(0.2))
    axis.margins(x=0)
    axis.margins(y=0)
    axis.set_ylim(top=ymax)
    axis.set_xlim(right=xmax)

    axis.yaxis.set_major_locator(MultipleLocator(0.4))
    axis.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

    # For the minor ticks, use no labels; default NullFormatter.
    axis.yaxis.set_minor_locator(MultipleLocator(0.1))

    tickx = axis.xaxis.get_major_ticks()
    ticky = axis.yaxis.get_major_ticks()

    for tick in tickx:
        tick.label.set_fontsize(14)
    for tick in ticky:
        tick.label.set_fontsize(14)

def properWrapper(axis, sequence, probabilityCutoff, probability, peak_x):
    ax_seq = axis[0]
    ax_descrition = axis[1]
    description = "Pr(RMSD < %.1fÅ) = %.2f%% ± %.2f%%\n\
    Peaks At %.3fÅ ± %.3fÅ\n" % (probabilityCutoff,
                                                     probability[0],
                                                     probability[1],
                                                     peak_x[0],
                                                     peak_x[1])
    ax_descrition.text(0.5, 0.02, description, fontsize=14, va='bottom', ha='center')
    ax_seq.text(0.5, 0.25, sequence, fontsize=20, va='bottom', ha='center')

def calculateError(s1_metric, s2_metric):
    average = 0.5 * (s1_metric + s2_metric)
    errorBar = s1_metric - average if s1_metric > average else s2_metric - average
    return (average, errorBar)

def makeBlankFigure(NPX, NPY):

    plotW = 8.25
    plotH = 6 * NPY

    fig = plt.figure(figsize = (8.25, plotH), dpi = 300)

    left, bot, right, top = (0.1, 0.1, 0.90, 0.90)
    HSpace = 0.4 * (top - bot) / NPY
    WSpace = 0.4 * (right - left) / NPX

    SubPlotH = (top - bot - (NPY - 1) * HSpace) / NPY
    SubPlotW = (right - left - (NPX - 1) * WSpace) / NPX

    plot_axes = []
    text_axes = []


    for y in range(NPY):
        plot_axes_temp = []
        text_axes_temp = []
        for x in range(NPX):
            plot_l = left + x * (SubPlotW + WSpace)
            plot_b = bot + y * (SubPlotH + HSpace)

            plot_ax = fig.add_axes([plot_l, plot_b, SubPlotW, SubPlotH])
            text_ax_seq = fig.add_axes([plot_l, plot_b + SubPlotH + (0.3 / plotH), SubPlotW, 0.1])
            text_ax_description = fig.add_axes([plot_l, plot_b + SubPlotH, SubPlotW, 0.1])

            if x == 0:
                plot_ax.set_ylabel("Probability Density", fontsize=14)
            if y == 0:
                plot_ax.set_xlabel("RMSD (Å)", fontsize=14)
            text_ax_seq.axis('off')
            text_ax_description.axis('off')

            text_axes_temp.append((text_ax_seq, text_ax_description))
            plot_axes_temp.append(plot_ax)

        plot_axes.append(plot_axes_temp)
        text_axes.append(text_axes_temp)

    title_text_all_l = left
    title_text_all_b = bot + NPY * (SubPlotH + HSpace)
    title_text_all_ax = fig.add_axes([title_text_all_l,
                                  title_text_all_b,
                                  SubPlotW, 0.1])
    title_text_all_ax.text(0.5, 0, "All Frames", fontsize=24, va='bottom', ha='center', transform=title_text_all_ax.transAxes)
    title_text_all_ax.axis('off')

    title_text_all_l = left + (SubPlotW + WSpace)
    title_text_all_b = bot + NPY * (SubPlotH + HSpace)
    title_text_all_ax = fig.add_axes([title_text_all_l,
                                  title_text_all_b,
                                  SubPlotW, 0.1])
    title_text_all_ax.text(0.5, 0, "Frames with No Clash", fontsize=24, va='bottom', ha='center', transform=title_text_all_ax.transAxes)
    title_text_all_ax.axis('off')

    return fig, plot_axes, text_axes

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

    color = ['#e8173a', '#22dd34', '#260bf4', '#335cff', '#0a6902', '#0fa103', '#ae016c', '#fc019c','#be0a35', '#f76d8e']
    assert len(seq) <= len(color)

    fig, plot_axes, text_axes = makeBlankFigure(2, len(seq))

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

        HotLoopX, HotLoopAllY1, HotLoopNoClashY1, s1_all_prob, s1_noC_prob = drawAllAndNoClash(plot_axes[index][0],
                                                                                               plot_axes[index][1],
                                                                                               rmsdHotLoop_mtx1,
                                                                                               clash_mtx1,
                                                                                               seq[index],
                                                                                               color[index],
                                                                                               XTicksHotLoop,
                                                                                               probabilityCutoff)

        HotLoopX, HotLoopAllY2, HotLoopNoClashY2, s2_all_prob, s2_noC_prob = drawAllAndNoClash(plot_axes[index][0],
                                                                                               plot_axes[index][1],
                                                                                               rmsdHotLoop_mtx2,
                                                                                               clash_mtx2,
                                                                                               "",
                                                                                               color[index],
                                                                                               XTicksHotLoop,
                                                                                               probabilityCutoff)

        HotLoopAll_max_x1 = HotLoopX[np.argmax(HotLoopAllY1)]
        HotLoopAll_max_x2 = HotLoopX[np.argmax(HotLoopAllY2)]

        # plot_axes[index][0].axvline(HotLoopAll_max_x1, ls="--")
        # plot_axes[index][0].axvline(HotLoopAll_max_x2, ls="--")
        HotLoopNoClash_max_x1 = HotLoopX[np.argmax(HotLoopNoClashY1)]
        HotLoopNoClash_max_x2 = HotLoopX[np.argmax(HotLoopNoClashY2)]
        # plot_axes[index][1].axvline(HotLoopNoClash_max_x1, ls="--")
        # plot_axes[index][1].axvline(HotLoopNoClash_max_x2, ls="--")


        all_peak_x = calculateError(HotLoopAll_max_x1, HotLoopAll_max_x2)
        noC_peak_x = calculateError(HotLoopNoClash_max_x1, HotLoopNoClash_max_x2)

        peak_x.append((all_peak_x, noC_peak_x))

        all_prob = calculateError(s1_all_prob, s2_all_prob)
        noC_prob = calculateError(s1_noC_prob, s2_noC_prob)


        probability.append((all_prob, noC_prob))

        curr_max = max(np.amax(HotLoopAllY1), np.amax(HotLoopAllY2))
        if ymax < curr_max:
            ymax = curr_max

        drawShadow(plot_axes[index][1], HotLoopX, HotLoopNoClashY1, HotLoopNoClashY2, color[index])
        drawShadow(plot_axes[index][0], HotLoopX, HotLoopAllY1, HotLoopAllY2, color[index])

    ymax += 1.0

    for index in range(len(seq)):
        for i in range(2):
            properWrapper(text_axes[index][i],
                          seq[index],
                          probabilityCutoff,
                          probability[index][i],
                          peak_x[index][i])
            setTickes(plot_axes[index][i], 2.0, ymax)


    fig.savefig(filename="histogram.png", dpi=300, bbox_inches='tight')
