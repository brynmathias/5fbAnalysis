#!/usr/bin/env python

from plottingUtils import *
import ROOT as r

def threeToTwo(h3) :
    name = h3.GetName()
    binsz = h3.GetNbinsZ()
    print binsz
    h2 = r.TH2D(name+"_2D",h3.GetTitle(),
                h3.GetNbinsX(), h3.GetXaxis().GetXmin(), h3.GetXaxis().GetXmax(),
                h3.GetNbinsY(), h3.GetYaxis().GetXmin(), h3.GetYaxis().GetXmax(),
                )
                
    for iX in range(1, 1+h3.GetNbinsX()) :
        for iY in range(1, 1+h3.GetNbinsY()) :
            content = h3.GetBinContent(iX, iY, 1) + h3.GetBinContent(iX, iY, 2)+ h3.GetBinContent(iX, iY, 0)
            h2.SetBinContent(iX, iY, content)
    h2.GetZaxis().SetTitle(h3.GetZaxis().GetTitle())
    return h2

c1 = Print("T1bbbbAllBins.pdf")
c1.open()


for f in ["results_had_T1bbbb_100.root","results_had_T1bbbb_73.7.root","results_had_T1bbbb_86.7.root"]:
    histo = GetSumHist(File = [f], Directories = ["smsScan_before"], Hist = "m0_m12_mChi_noweight", Col = r.kBlack, Norm = None, LegendText = "No btag requirement")
    a = threeToTwo(histo.hObj)
    a.SetTitle(f)
    a.Draw("COLZ")
    c1.Print()

c1.close()