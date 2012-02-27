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

c1 = Print("CMSSMVetosAndCleaning.pdf")
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
    nocuts = []
    AllCuts = []
    NoDeadEcal = []
    NoMHTovMET = []
    NoLeptonVetos = []
    for process in settings["SubProcesses"]:                
        p_xsec = GetHist(File =  r.TFile.Open("./NoLeptonVetosTanB10.root"),folder = ["mSuGraScan_before_scale1",], hist = "m0_m12_%s"%(process),Norm = 8. ,rebin= 2)
        p_xsec.Divide(GetHist(File =  r.TFile.Open("./NoLeptonVetosTanB10.root"),folder = ["mSuGraScan_before_scale1",], hist = "m0_m12_%s_noweight"%(process),Norm = 8. ,rebin= 2))
        p_xsec.SetTitle(process)
        processCrossSections.append(p_xsec)
        nocuts.append((GetHist(File =  r.TFile.Open("./NoLeptonVetosTanB10.root"),folder = ["mSuGraScan_before_scale1",], hist = "m0_m12_%s"%(process), Norm = None ,rebin= 2)))

        AllCuts.append((GetHist(File = r.TFile.Open("./NoLeptonVetosTanB10.root"),folder = ["mSuGraScan_AlphaT55_375_475_scale1","mSuGraScan_AlphaT55_475_575_scale1","mSuGraScan_AlphaT55_575_675_scale1",
                 "mSuGraScan_AlphaT55_675_775_scale1","mSuGraScan_AlphaT55_775_875_scale1","mSuGraScan_AlphaT55_875_scale1"],hist = "m0_m12_%s"%(process), Norm = None ,rebin= 2)))



        NoDeadEcal.append((GetHist(File = r.TFile.Open("./NoDeadEcalTanB10.root"),folder = ["mSuGraScan_NoDeadEcal_AlphaT55_375_475_scale1","mSuGraScan_NoDeadEcal_AlphaT55_475_575_scale1","mSuGraScan_NoDeadEcal_AlphaT55_575_675_scale1",
                 "mSuGraScan_NoDeadEcal_AlphaT55_675_775_scale1","mSuGraScan_NoDeadEcal_AlphaT55_775_875_scale1","mSuGraScan_NoDeadEcal_AlphaT55_875_scale1"],hist = "m0_m12_%s"%(process), Norm = None ,rebin= 2)))

        NoLeptonVetos.append((GetHist(File = r.TFile.Open("./NoLeptonVetosTanB10.root"),folder = ["mSuGraScan_NoLeptonVetos_AlphaT55_375_475_scale1","mSuGraScan_NoLeptonVetos_AlphaT55_475_575_scale1","mSuGraScan_NoLeptonVetos_AlphaT55_575_675_scale1",
                 "mSuGraScan_NoLeptonVetos_AlphaT55_675_775_scale1","mSuGraScan_NoLeptonVetos_AlphaT55_775_875_scale1","mSuGraScan_NoLeptonVetos_AlphaT55_875_scale1"],hist = "m0_m12_%s"%(process), Norm = None ,rebin= 2)))

        NoMHTovMET.append((GetHist(File = r.TFile.Open("./NoMHTovMETTanB10.root"),folder = ["mSuGraScan_NoMHTovMET_AlphaT55_375_475_scale1","mSuGraScan_NoMHTovMET_AlphaT55_475_575_scale1","mSuGraScan_NoMHTovMET_AlphaT55_575_675_scale1",
                 "mSuGraScan_NoMHTovMET_AlphaT55_675_775_scale1","mSuGraScan_NoMHTovMET_AlphaT55_775_875_scale1","mSuGraScan_NoMHTovMET_AlphaT55_875_scale1"],hist = "m0_m12_%s"%(process), Norm = None ,rebin= 2)))

        
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
    TotalEff =  NloEffHisto(AllCuts,nocuts,processCrossSections,totalXsec)
    TotalEff.SetTitle("Total Efficiency")
    TotalEff.Draw("COLZ")
    c1.Print()
    TotalEffNoDeadEcal = NloEffHisto(NoDeadEcal,nocuts,processCrossSections,totalXsec)

    TotalEffNoMHTovMET =  NloEffHisto(NoMHTovMET,nocuts,processCrossSections,totalXsec)
    TotalEffNoLeptonVeto =  NloEffHisto(NoLeptonVetos,nocuts,processCrossSections,totalXsec)

    EffOverNoDecal = TotalEff.Clone()
    EffOverNoDecal.Divide(TotalEffNoDeadEcal)
    EffOverNoDecal.SetTitle("Effect of DeadEcal")
    EffOverNoDecal.Draw("COLZ")
    EffOverNoDecal.SetMinimum(0.8)
    EffOverNoDecal.SetMaximum(1.2)
    c1.Print()
    # 
    EffOverNoMHTovMET = TotalEff.Clone()
    EffOverNoMHTovMET.Divide(TotalEffNoMHTovMET)
    EffOverNoMHTovMET.SetTitle("Effect of MHT over MET")
    EffOverNoMHTovMET.Draw("COLZ")
    EffOverNoMHTovMET.SetMinimum(0.8)
    EffOverNoMHTovMET.SetMaximum(1.2)
    c1.Print()
    # 
    EffOverNoLep = TotalEff.Clone()
    EffOverNoLep.Divide(TotalEffNoLeptonVeto)
    EffOverNoLep.SetTitle("Effect of LeptonVeto")
    EffOverNoLep.Draw("COLZ")
    # EffOverNoLep.SetMinimum(0.8)
    # EffOverNoLep.SetMaximum(1.2)
    c1.Print()
    
    # EffOverJESRan = TotalEff.Clone()
    # EffOverJESRan.Divide(TotalEffRan)
    # EffOverJESRan.SetTitle("JES variation for signal efficiency")
    # EffOverJESRan.Draw("COLZ")
    # for bin in range(EffOverJESRan.GetNbinsX()*EffOverJESRan.GetNbinsY()):
    #     if EffOverJESRan.GetBinContent(bin) > 1.05 or EffOverJESRan.GetBinContent(bin) < 0.95: EffOverJESRan.SetBinContent(bin,0.)
    # EffOverJESRan.SetMinimum(0.95)
    # EffOverJESRan.SetMaximum(1.05)
    # c1.Print()
    # 
    # 
    # 
    # oneDJesMinus = r.TH1D("oneDJesMinus","oneDJesMinus",1000,-5.,5.)
    # oneDJesPlus = r.TH1D("oneDJesPlus","oneDJesPlus",1000,-5.,5.)
    # oneDJesRan = r.TH1D("oneDJesRan","JES variation for signal efficiency 1D Projection",1000,-5.,5.)
    # 
    # 
    

    


c1.close()
