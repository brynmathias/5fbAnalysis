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
        # print directory.ls()
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

c1 = Print("NMinusOne.pdf")
c1.open()
r.gPad.SetRightMargin(0.15)

# centalRootFile100 = r.TFile.Open("./NMinusOneT2bb.root")




# centalRootFile73.ls()
# Make cross sections/ efficiencies

nocuts = threeToTwo(GetHist(File = r.TFile.Open("./NoLeptonVetosT2bb.root"),folder = ["smsScan_before",], hist = "m0_m12_mChi_noweight", Norm = None ,rebin= 2))
    
nocuts = threeToTwo(nocuts)
AllCuts = threeToTwo(GetHist(File = r.TFile.Open("./NoLeptonVetosT2bb.root"),folder = ["smsScan_AlphaT55_375_475","smsScan_AlphaT55_475_575","smsScan_AlphaT55_575_675",
                 "smsScan_AlphaT55_675_775","smsScan_AlphaT55_775_875","smsScan_AlphaT55_875"],hist = "m0_m12_mChi_noweight", Norm = None ,rebin= 2))



NoDeadEcal = threeToTwo(GetHist(File = r.TFile.Open("./NoDeadEcalT2bb.root"),folder = ["smsScan_NoDeadEcal_AlphaT55_375_475","smsScan_NoDeadEcal_AlphaT55_475_575","smsScan_NoDeadEcal_AlphaT55_575_675",
                 "smsScan_NoDeadEcal_AlphaT55_675_775","smsScan_NoDeadEcal_AlphaT55_775_875","smsScan_NoDeadEcal_AlphaT55_875"],hist = "m0_m12_mChi_noweight", Norm = None ,rebin= 2))

NoLeptonVetos = threeToTwo(GetHist(File = r.TFile.Open("./NoLeptonVetosT2bb.root"),folder = ["smsScan_NoLeptonVetos_AlphaT55_375_475","smsScan_NoLeptonVetos_AlphaT55_475_575","smsScan_NoLeptonVetos_AlphaT55_575_675",
                 "smsScan_NoLeptonVetos_AlphaT55_675_775","smsScan_NoLeptonVetos_AlphaT55_775_875","smsScan_NoLeptonVetos_AlphaT55_875"],hist = "m0_m12_mChi_noweight", Norm = None ,rebin= 2))

NoMHTovMET = threeToTwo(GetHist(File = r.TFile.Open("./NoMHTovMETT2bb.root"),folder = ["smsScan_NoMHTovMET_AlphaT55_375_475","smsScan_NoMHTovMET_AlphaT55_475_575","smsScan_NoMHTovMET_AlphaT55_575_675",
                 "smsScan_NoMHTovMET_AlphaT55_675_775","smsScan_NoMHTovMET_AlphaT55_775_875","smsScan_NoMHTovMET_AlphaT55_875"],hist = "m0_m12_mChi_noweight", Norm = None ,rebin= 2))


# Make the 4 efficiencies:
AllCuts.Divide(nocuts)
AllCuts.Draw("COLZ")
# c1.Print()
NoDeadEcal.Divide(nocuts)
NoDeadEcal.Draw("COLZ")
# c1.Print()
NoLeptonVetos.Divide(nocuts)
NoLeptonVetos.Draw("COLZ")
# c1.Print()
NoMHTovMET.Divide(nocuts)
NoMHTovMET.Draw("COLZ")
# c1.Print()

ChangeDueToMHTovMET = AllCuts.Clone()
ChangeDueToMHTovMET.Divide(NoMHTovMET)
ChangeDueToMHTovMET.SetTitle("ChangeDueToMHTovMET")
ChangeDueToMHTovMET.SetMinimum(0.8)
ChangeDueToMHTovMET.Draw("COLZ")
c1.Print()

ChangeDueToDeadEcal = AllCuts.Clone()
ChangeDueToDeadEcal.Divide(NoDeadEcal)
ChangeDueToDeadEcal.SetTitle("ChangeDueToDeadEcal")
ChangeDueToDeadEcal.SetMinimum(0.8)
ChangeDueToDeadEcal.Draw("COLZ")
c1.Print()

ChangeDueToLeptonVetos = AllCuts.Clone()
ChangeDueToLeptonVetos.Divide(NoLeptonVetos)
ChangeDueToLeptonVetos.SetTitle("ChangeDueToLeptonVetos")
ChangeDueToLeptonVetos.SetMinimum(0.8)
ChangeDueToLeptonVetos.Draw("COLZ")
c1.Print()



c1.close()
