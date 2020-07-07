#!/bin/env python
import optparse
import os, sys
import numpy as np
import pickle as cp
import matplotlib
matplotlib.use('AGG')
import matplotlib.pyplot as plt
import matplotlib.font_manager as ftman
import matplotlib.colors as colors
import matplotlib.cm as cmx
import matplotlib.colorbar as cb

global nres_hl
nres_hl = 4

FesMax=0.005

def genColorMap(cmap):
    cvals = [('white')] + [(cmap(i)) for i in range(1,256)]
    new_map = colors.LinearSegmentedColormap.from_list('new_map',cvals, N=256)
    return new_map

def calcDensity2D (Xs, Ys, Ws=None):
    Bins = np.linspace(start=-180, stop=180, num=101)
    hist2D, xedges, yedges = np.histogram2d(Xs,Ys,bins=Bins,weights=Ws)
    density2D = hist2D/np.sum(hist2D)
    xstep = xedges[1] - xedges[0]
    xmidps = xedges[1:] - 0.5*xstep
    ystep = yedges[1] - yedges[0]
    ymidps = yedges[1:] - 0.5*ystep

    return xmidps, ymidps, density2D

def add_population_RMSD(Fig, x0, y0, SubPlotW, SubPlotH, population, RMSD):
    fi = open(population)
    population = float(fi.readline().strip())
    fi.close()
    fi = open(RMSD)
    RMSD = [float(i.strip()) for i in fi]
    fi.close()
    text_l = x0 - 3.5 * SubPlotW
    text_b = y0 + SubPlotH / 4
    text_w = SubPlotW
    text_h = SubPlotH / 2
    tax = Fig.add_axes([text_l, text_b, text_w, text_h])
    tax.text(0.1, 0, ("Population: %.1f%%\n\nRMSD(Å): %.3f $\pm$ %.3f" % (population, RMSD[0], RMSD[1])), fontsize = 20)
    tax.axis('off')

def add_aa(Fig, x0, y0, SubPlotW, SubPlotH, aa):
    text_l = x0 + 0.45 * SubPlotW
    text_b = y0 + 1.2 * SubPlotH
    text_w = SubPlotW
    text_h = 0.5 * SubPlotH
    tax = Fig.add_axes([text_l, text_b, text_w, text_h])
    tax.text(0, 0, aa, fontsize = 15)
    tax.axis('off')

def add_NIP(Fig, x0, y0, SubPlotW, SubPlotH, NIP):
    fi = open(NIP)
    NIP_total = float(fi.readline().strip())
    NIP_clean = float(fi.readline().strip())
    fi.close()
    text_l = x0 - 3.5 * SubPlotW
    text_b = y0 + SubPlotH * 2
    text_w = SubPlotW
    text_h = SubPlotH / 2
    tax = Fig.add_axes([text_l, text_b, text_w, text_h])
    tax.text(0, 0, "3D-NIP: total > %.4f | clean > %.4f" % (NIP_total, NIP_clean), fontsize = 20)
    tax.axis("off")

def MakeFigure(FigW, FigH, inp, out, numRes, WriteDescription, seq, degreeFile, NIP, population, RMSD):

    TitleFP    = ftman.FontProperties(size=18)
    LegendFP = ftman.FontProperties(size=18)
    LabelFP    = ftman.FontProperties(size=20)
    cvvals = np.loadtxt(inp,dtype=np.float32,usecols=list(range(2,(2 * numRes + 2))),unpack=True)


    nRes = len(cvvals) // 2
    ResNames = ['ALA','ALA','ALA', 'NMA','NMA']
    ResIDs = [1,2,3,4,5]

    NPX = nRes
    NPY = 1

    Fig = plt.figure(figsize = (FigW, FigH), dpi=300)

    left, bot, right, top = (0.3, 0.3, 0.90, 0.60)

    HSpace = 0.05 * (top - bot) / NPY
    WSpace = 0.10 * (right - left) / NPX

    SubPlotH = (top - bot - (NPY-1) * HSpace) / NPY
    SubPlotW = (right - left - (NPX - 1) * WSpace) / NPX

    add_population_RMSD(Fig, left, bot, SubPlotW, SubPlotH, population, RMSD)

    if WriteDescription:
        add_NIP(Fig, left, bot, SubPlotW, SubPlotH, NIP)

    for ires in range(nRes):
        x0 = left + (ires % NPX) * (SubPlotW + WSpace)
        y0 = bot
        if WriteDescription:
            add_aa(Fig, x0, y0, SubPlotW, SubPlotH, seq[ires])
        ax = Fig.add_axes([x0, y0, SubPlotW, SubPlotH])
        ax.set_xlabel("$\phi$", fontsize=20)
        if ires == 0: ax.set_ylabel("$\psi$", fontsize=20)
        else: ax.set_ylabel(" ")
        phi = cvvals[ires*2]
        psi = cvvals[ires*2+1]
        xmidps,ymidps,dens2d = calcDensity2D (phi, psi)
        yvals,xvals = np.meshgrid(xmidps, ymidps)

        xtlv = True

        if ires == 0:
            ytlv = True
        else:
            ytlv = False

        pc = MakeSubPlot(ax, xvals, yvals, dens2d, ires, degreeFile, xtlv, ytlv, 0, FesMax)


    cbl, cbb, cbw, cbh = left + NPX * (WSpace + SubPlotW), 0.5 * (top + bot) - 0.5 * SubPlotH, 0.02, SubPlotH
    cax = Fig.add_axes([cbl,cbb,cbw,cbh])
    cb = Fig.colorbar(pc,cax=cax,orientation='vertical')
    #cbticks = np.arange(0,FesMax+1,2)
    cbticks = np.linspace(0, FesMax, 5)
    cb.set_ticks(ticks=cbticks)
    cb.set_ticklabels(ticklabels=[str(i) for i in cbticks])

    Fig.savefig(out)


def MakeSubPlot(Axes, XVals, YVals, ColVals, ires, degreeFile, XTLVisible=False, YTLVisible=False, vmin=0, vmax=30):
    global nres_hl

    TickFP    = ftman.FontProperties(size=12)
    MTickFP = ftman.FontProperties(size=0)

    XTicks = np.array([-90,0,90]) #np.arange(-90,360, 90)
    YTicks = np.array([-90,0,90]) #np.arange(-90,360, 90)
    MXTicks = None
    MYTicks = None

    AxesPropWrapper(Axes,XTicks=XTicks,YTicks=YTicks, MXTicks=MXTicks, MYTicks=MYTicks,
                    XTLVisible=XTLVisible,YTLVisible=YTLVisible,XYRange=[-180,-180,180,180],
                    TickFP=TickFP,MTickFP=MTickFP)

    SpinceWidth=2
    [i.set_linewidth(SpinceWidth) for i in Axes.spines.values()]

    TickLineWidth=2
    for l in Axes.get_xticklines() + Axes.get_yticklines():
        l.set_markeredgewidth(TickLineWidth)

    pc = Axes.pcolormesh(XVals,YVals,ColVals,cmap=genColorMap(cmx.jet),vmin=vmin,vmax=vmax)

    hl_vals = np.loadtxt(degreeFile,dtype=np.float32,usecols=list(range(1,9)),unpack=True)

    if ires < nres_hl:
        if ires > 0:
            plt.vlines(hl_vals[2*ires],-180,180,colors='r')
        if ires < nres_hl - 1:
            plt.hlines(hl_vals[2*ires+1],-180,180,colors='r')

    return pc


################################################################################
def SetXTicks(Axes,Ticks=None,Minor=False, FP=20, Decimals=0, Visible=False):
    if Ticks is not None:
        Axes.set_xticks(ticks=Ticks,minor=Minor)
        TLabels = [str(x) for x in np.around(Ticks,decimals=Decimals)]
        if Visible:
            Axes.set_xticklabels(labels=TLabels,minor=Minor,fontproperties=FP)
        else:
            Axes.set_xticklabels(labels=TLabels,minor=Minor,visible=Visible,fontproperties=FP)


################################################################################
def SetYTicks(Axes,Ticks=None,Minor=False, FP=20, Decimals=0, Visible=False):
    if Ticks is not None:
        Axes.set_yticks(ticks=Ticks,minor=Minor)
        TLabels = [str(x) for x in np.around(Ticks,decimals=Decimals)]
        if Visible:
            Axes.set_yticklabels(labels=TLabels, minor=Minor, fontproperties=FP)
        else:
            Axes.set_yticklabels(labels=TLabels, minor=Minor, visible=Visible, fontproperties=FP)


def AxesPropWrapper(Axes,XTicks=None,YTicks=None,MXTicks=None,MYTicks=None,
                    XTLDecimals=0,MXTLDecimals=0,XTLVisible=True,MXTLVisible=False,
                    YTLDecimals=0,MYTLDecimals=0,YTLVisible=True,MYTLVisible=False,
                    XYRange=[0,0,1,1], TickFP=None, MTickFP=None):
    if TickFP is None: TickFP = ftman.FontProperties(18)
    if MTickFP is None: MTickFP = ftman.FontProperties(10)

    SetXTicks(Axes,XTicks, Minor=False,FP=TickFP, Decimals=XTLDecimals, Visible=XTLVisible)
    SetXTicks(Axes,MXTicks,Minor=True, FP=MTickFP,Decimals=MXTLDecimals,Visible=MXTLVisible)
    SetYTicks(Axes,YTicks, Minor=False,FP=TickFP, Decimals=YTLDecimals, Visible=YTLVisible)
    SetYTicks(Axes,MYTicks,Minor=True, FP=MTickFP,Decimals=MYTLDecimals,Visible=MYTLVisible)

    left, bot, right, top = XYRange
    Axes.set_xlim(left=left,right=right)
    Axes.set_ylim(bottom=bot,top=top)

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('--seq', dest = 'seq')
    parser.add_option('--WriteDescription', dest='WriteDescription')
    parser.add_option('--numRes', dest='numRes')
    parser.add_option('--input', dest='input')
    parser.add_option('--output', dest='output')
    parser.add_option('--degreeFile', dest='degreeFile')
    parser.add_option('--NIP', dest='NIP')
    parser.add_option('--RMSD', dest='RMSD')
    parser.add_option('--population', dest='population')
    (options,args) = parser.parse_args()
    INP = options.input
    OUT = options.output
    numRes = int(options.numRes)
    WriteDescription = options.WriteDescription
    seq = options.seq
    degreeFile = options.degreeFile
    NIP = options.NIP
    RMSD = options.RMSD
    population = options.population
    assert(len(seq) == numRes)

    if WriteDescription[0].upper() == "T":
        WriteDescription = True
    else:
        WriteDescription = False
    MakeFigure((2 * (numRes + 2)), 4, INP, OUT, numRes, WriteDescription, seq, degreeFile, NIP, population, RMSD)
