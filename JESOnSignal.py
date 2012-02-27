#!/usr/bin/env python
import sys
import os
import ROOT as r
from plottingstuff import *
from plottingUtils import Print

# Make central efficiency map
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



settings = {
    "HTBins":["a"],
    "SubProcesses":["nn","ns","ng","ss","ll","sb","tb","gg","bb","sg"]
}
def GetHist(File = None, folder = None, hist = None, Norm = None, rebin = None):
    h = None
    for f in folder:
        print f
        print hist
        directory = File.Get(f)    
        a = directory.Get(hist)
        if h is None:
            h = a.Clone()
        else: h.Add(a)
    return h
    
    
def nloTotalXsecMaker(individualXSecs = None):
    out = None
    for h in individualXSecs:
        if out is None: out = h.Clone()
        else: out.Add(h)
    return out

c1 = Print("JESSignal.pdf")
r.gPad.SetRightMargin(0.15)

c1.open()
centalRootFile73 = r.TFile.Open("./results_had_tanB10_73.7_.root")
centalRootFile86 = r.TFile.Open("./results_had_tanB10_86.7_.root")
centalRootFile100 = r.TFile.Open("./results_had_tanB10_100_.root")
jesPlusRootFile73 = r.TFile.Open("./results_had_tanB10_73.7_+ve.root")
jesPlusRootFile86 = r.TFile.Open("./results_had_tanB10_86.7_+ve.root")
jesPlusRootFile100 = r.TFile.Open("./results_had_tanB10_100_+ve.root")
jesNegRootFile73 = r.TFile.Open("./results_had_tanB10_73.7_-ve.root")
jesNegRootFile86 = r.TFile.Open("./results_had_tanB10_86.7_-ve.root")
jesNegRootFile100 = r.TFile.Open("./results_had_tanB10_100_-ve.root")
jesRanRootFile73 = r.TFile.Open("./results_had_tanB10_73.7_ran.root")
jesRanRootFile86 = r.TFile.Open("./results_had_tanB10_86.7_ran.root")
jesRanRootFile100 = r.TFile.Open("./results_had_tanB10_100_ran.root")



centalRootFile73.ls()
# Make cross sections/ efficiencies
RawEvNums = GetHist(File = centalRootFile73,folder = ["mSuGraScan_before_scale1",], hist = "m0_m12_mChi_noweight",Norm = 8. ,rebin= 2)
RawEvNums = threeToTwo(RawEvNums)
BinsToExclude = []
for bin in range(RawEvNums.GetNbinsX()*RawEvNums.GetNbinsY()):
    if RawEvNums.GetBinContent(bin) != 10000 : BinsToExclude.append(bin)

for bin in settings["HTBins"]:        
    processCrossSections = []
    cuts = []
    cutsJESNeg = []
    cutsJESPlus = []
    cutsJESRan = []
    nocuts = []
    for process in settings["SubProcesses"]:                
        p_xsec = GetHist(File = centalRootFile73,folder = ["mSuGraScan_before_scale1",], hist = "m0_m12_%s"%(process),Norm = 8. ,rebin= 2)
        p_xsec.Divide(GetHist(File = centalRootFile73,folder = ["mSuGraScan_before_scale1",], hist = "m0_m12_%s_noweight"%(process),Norm = 8. ,rebin= 2))
        p_xsec.SetTitle(process)
        processCrossSections.append(p_xsec)
        nocuts.append(GetHist(File = centalRootFile73,folder = ["mSuGraScan_before_scale1",], hist = "m0_m12_%s"%(process), Norm = None ,rebin= 2))


        cutsHist = GetHist(File = centalRootFile73,folder = ["mSuGraScan_AlphaT55_275_325_scale1"],hist = "m0_m12_%s"%(process), Norm = None ,rebin= 2).Clone()
        cutsHist.Add(GetHist(File = centalRootFile86,folder = ["mSuGraScan_AlphaT55_325_375_scale1"],hist = "m0_m12_%s"%(process), Norm = None ,rebin= 2))
        cutsHist.Add(GetHist(File = centalRootFile100,folder = ["mSuGraScan_AlphaT55_375_475_scale1","mSuGraScan_AlphaT55_475_575_scale1","mSuGraScan_AlphaT55_575_675_scale1",
                                                             "mSuGraScan_AlphaT55_675_775_scale1","mSuGraScan_AlphaT55_775_875_scale1","mSuGraScan_AlphaT55_875_scale1"],hist = "m0_m12_%s"%(process), Norm = None ,rebin= 2))
        cuts.append(cutsHist)
        cutsJESPlusHist = GetHist(File =   jesPlusRootFile73,folder = ["mSuGraScan_AlphaT55_275_325_scale1"],hist = "m0_m12_%s"%(process), Norm = None ,rebin= 2).Clone()
        cutsJESPlusHist.Add(GetHist(File = jesPlusRootFile86,folder = ["mSuGraScan_AlphaT55_325_375_scale1"],hist = "m0_m12_%s"%(process), Norm = None ,rebin= 2))
        cutsJESPlusHist.Add(GetHist(File = jesPlusRootFile100,folder = ["mSuGraScan_AlphaT55_375_475_scale1","mSuGraScan_AlphaT55_475_575_scale1","mSuGraScan_AlphaT55_575_675_scale1",
                                                             "mSuGraScan_AlphaT55_675_775_scale1","mSuGraScan_AlphaT55_775_875_scale1","mSuGraScan_AlphaT55_875_scale1"],hist = "m0_m12_%s"%(process), Norm = None ,rebin= 2))
        cutsJESPlus.append(cutsJESPlusHist)                                                     
                                                             


        cutsJESNegHist = GetHist(File =   jesNegRootFile73,folder = ["mSuGraScan_AlphaT55_275_325_scale1"],hist = "m0_m12_%s"%(process), Norm = None ,rebin= 2).Clone()
        cutsJESNegHist.Add(GetHist(File = jesNegRootFile86,folder = ["mSuGraScan_AlphaT55_325_375_scale1"],hist = "m0_m12_%s"%(process), Norm = None ,rebin= 2))
        cutsJESNegHist.Add(GetHist(File = jesNegRootFile100,folder = ["mSuGraScan_AlphaT55_375_475_scale1","mSuGraScan_AlphaT55_475_575_scale1","mSuGraScan_AlphaT55_575_675_scale1",
                                                             "mSuGraScan_AlphaT55_675_775_scale1","mSuGraScan_AlphaT55_775_875_scale1","mSuGraScan_AlphaT55_875_scale1"],hist = "m0_m12_%s"%(process), Norm = None ,rebin= 2))
        cutsJESNeg.append(cutsJESNegHist)                                                     
        
        
        cutsJESRanHist = GetHist(File =   jesRanRootFile73,folder = ["mSuGraScan_AlphaT55_275_325_scale1"],hist = "m0_m12_%s"%(process), Norm = None ,rebin= 2).Clone()
        cutsJESRanHist.Add(GetHist(File = jesRanRootFile86,folder = ["mSuGraScan_AlphaT55_325_375_scale1"],hist = "m0_m12_%s"%(process), Norm = None ,rebin= 2))
        cutsJESRanHist.Add(GetHist(File = jesRanRootFile100,folder = ["mSuGraScan_AlphaT55_375_475_scale1","mSuGraScan_AlphaT55_475_575_scale1","mSuGraScan_AlphaT55_575_675_scale1",
                                                             "mSuGraScan_AlphaT55_675_775_scale1","mSuGraScan_AlphaT55_775_875_scale1","mSuGraScan_AlphaT55_875_scale1"],hist = "m0_m12_%s"%(process), Norm = None ,rebin= 2))
        cutsJESRan.append(cutsJESRanHist)                                                     
        
        # cutsHist.Draw("COLZ")
        # c1.Print()
        # cutsJESPlusHist.Draw("COLZ")
        # c1.Print()
        # cutsJESNegHist.Draw("COLZ")
        # c1.Print()
        # cutsJESRanHist.Draw("COLZ")
        # c1.Print()
        
        
    totalXsec =  nloTotalXsecMaker(processCrossSections)
    for bin in BinsToExclude:
        totalXsec.SetBinContent(bin,0.)
    c1.canvas.SetLogz()
    totalXsec.Draw("COLZ")
    totalXsec.SetTitle("xs")
    totalXsec.SetMinimum(1E-2)
    totalXsec.SetMaximum(1E5)    
    c1.Print()    
    c1.canvas.SetLogz(False)
    TotalEff =  NloEffHisto(cuts,nocuts,processCrossSections,totalXsec)

    TotalEff.Draw("COLZ")
    c1.Print()
    TotalEffPlus = NloEffHisto(cutsJESPlus,nocuts,processCrossSections,totalXsec)

    TotalEffNeg =  NloEffHisto(cutsJESNeg,nocuts,processCrossSections,totalXsec)
    TotalEffRan =  NloEffHisto(cutsJESRan,nocuts,processCrossSections,totalXsec)

    EffOverJESNeg = TotalEff.Clone()
    EffOverJESNeg.Divide(TotalEffNeg)
    EffOverJESNeg.SetTitle("EffOverJESNeg")
    EffOverJESNeg.Draw("COLZ")
    # EffOverJESNeg.SetMinimum(0.8)
    # EffOverJESNeg.SetMaximum(1.2)
    c1.Print()

    EffOverJESPlus = TotalEff.Clone()
    EffOverJESPlus.Divide(TotalEffPlus)
    EffOverJESPlus.SetTitle("EffOverJESPlus")
    EffOverJESPlus.Draw("COLZ")
    # EffOverJESPlus.SetMinimum(0.8)
    # EffOverJESPlus.SetMaximum(1.2)
    c1.Print()

    EffOverJESRan = TotalEff.Clone()
    EffOverJESRan.Divide(TotalEffRan)
    EffOverJESRan.SetTitle("JES variation for signal efficiency")
    EffOverJESRan.Draw("COLZ")
    # for bin in range(EffOverJESRan.GetNbinsX()*EffOverJESRan.GetNbinsY()):
    #     if EffOverJESRan.GetBinContent(bin) > 1.05 or EffOverJESRan.GetBinContent(bin) < 0.95: EffOverJESRan.SetBinContent(bin,0.)
    # EffOverJESRan.SetMinimum(0.95)
    # EffOverJESRan.SetMaximum(1.05)
    c1.Print()



    oneDJesMinus = r.TH1D("oneDJesMinus","oneDJesMinus",1000,-5.,5.)
    oneDJesPlus = r.TH1D("oneDJesPlus","oneDJesPlus",1000,-5.,5.)
    oneDJesRan = r.TH1D("oneDJesRan","JES variation for signal efficiency 1D Projection",1000,-5.,5.)

    minf=0.9
    maxf=1.1
    fit =r.TF1("Gaussian","gaus",minf,maxf)
    
    totalBins = TotalEff.GetNbinsX()*TotalEff.GetNbinsY()
    print BinsToExclude
    for bin in range(totalBins):
        if bin in BinsToExclude: continue
        contentMinus = EffOverJESNeg.GetBinContent(bin)
        contentPlus =  EffOverJESPlus.GetBinContent(bin)
        contentRan =   EffOverJESRan.GetBinContent(bin)
        if contentMinus > 0.:oneDJesMinus.Fill(contentMinus)
        if contentPlus > 0.: oneDJesPlus.Fill(contentPlus)
        if contentRan > 0.: oneDJesRan.Fill(contentRan)
        if contentPlus > 1.2: print "Change = %f, Efficiency = %f, Efficiency of Plus Hist = %f"    %( EffOverJESPlus.GetBinContent(bin),TotalEff.GetBinContent(bin), TotalEffPlus.GetBinContent(bin))
        if contentRan > 1.2: print "Change = %f, Efficiency = %f, Efficiency of Ran Hist = %f"      %( EffOverJESRan.GetBinContent(bin),TotalEff.GetBinContent(bin), TotalEffRan.GetBinContent(bin))
        if contentMinus > 1.2: print "Change = %f, Efficiency = %f, Efficiency of Neg Hist = %f"    %( EffOverJESNeg.GetBinContent(bin),TotalEff.GetBinContent(bin), TotalEffNeg.GetBinContent(bin))


    # c1.canvas.SetLogy()
    r.gStyle.SetOptStat(1111)
    oneDJesMinus.GetXaxis().SetRangeUser(0.8,1.2)
    oneDJesMinus.Draw("hist")
    oneDJesMinus.Fit("Gaussian","RQ")
    fit.Draw("lsame")

    c1.Print()
    oneDJesPlus.GetXaxis().SetRangeUser(0.8,1.2)
    oneDJesPlus.Draw("hist")
    oneDJesPlus.Fit("Gaussian","RQ")
    fit.Draw("lsame")

    c1.Print()
    # minf=0.97
    # maxf=1.03
    # fit =r.TF1("Gaussian","gaus",minf,maxf)

    oneDJesRan.GetXaxis().SetRangeUser(0.8,1.2)
    oneDJesRan.Draw("hist")
    oneDJesRan.Fit("Gaussian","RQ")
    fit.Draw("lsame")
    # print "RMS is =", oneDJesRan.GetRMS()
    c1.Print()

    JesTotal = oneDJesPlus.Clone()
    JesTotal.Add(oneDJesMinus)
    JesTotal.SetTitle("Total (Sum of up and down)")
    JesTotal.Draw("hist")
    JesTotal.Fit("Gaussian","RQ")
    fit.Draw("lsame")
    # print "RMS is =", oneDJesRan.GetRMS()
    c1.Print()
    


c1.close()
