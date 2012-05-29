#!/usr/bin/env python

import ROOT as r
from plottingUtils import *

Directories = (["OneMuon_375_475",],)
hist = "AlphaT"
c1 = Print("./out/%s_DECAL.pdf"%hist)
c1.open()
leg = Legend()

for Dirs in Directories:
  Data = GetSumHist(File = ["./rootFiles/DataDECAL.root",], Directories = Dirs, Hist = "%s_all"%hist, Col = r.kBlack, Norm = None, LegendText = None)
  TTbar = GetSumHist(File = ["./rootFiles/AK5Calo_TTJetsDECAL.root",], Directories = Dirs, Hist = "%s_all"%hist, Col = r.kRed, Norm = [4430./100.], LegendText = None)
  QCD  = GetSumHist(File = ["./rootFiles/AK5Calo_QCDDECAL.root",], Directories = Dirs, Hist = "%s_all"%hist, Col = r.kGreen, Norm = [4430./100.], LegendText = None)
  DY  = GetSumHist(File = ["./rootFiles/AK5Calo_DYDECAL.root",], Directories = Dirs, Hist = "%s_all"%hist, Col = r.kCyan, Norm = [4430./100.], LegendText = None)
  WJets  = GetSumHist(File = ["./rootFiles/AK5Calo_WJetsToLNuDECAL.root",], Directories = Dirs, Hist = "%s_all"%hist, Col = r.kBlue, Norm = [4430./100.], LegendText = None)
  ZJets  = GetSumHist(File = ["./rootFiles/AK5Calo_ZJetsToNuNuDECAL.root",], Directories = Dirs, Hist = "%s_all"%hist, Col = r.kGreen+7, Norm = [4430./100.], LegendText = None)
  Data.HideOverFlow() 
  TTbar.HideOverFlow()
  QCD.HideOverFlow()  
  DY.HideOverFlow()  
  WJets.HideOverFlow()
  ZJets.HideOverFlow()
  if hist == "MHTovMET":
    Data.hObj.Rebin(5)
    TTbar.hObj.Rebin(5)
    QCD.hObj.Rebin(5)
    WJets.hObj.Rebin(5)
    DY.hObj.Rebin(5)
    ZJets.hObj.Rebin(5)
  aTbins = [.53,0.55,0.6]  
  if hist == "AlphaT":
    Data.hObj = Data.hObj.Rebin(len(aTbins)-1,"a",array.array('d',aTbins))
    TTbar.hObj = TTbar.hObj.Rebin(len(aTbins)-1,"b",array.array('d',aTbins))
    QCD.hObj = QCD.hObj.Rebin(len(aTbins)-1,"c",array.array('d',aTbins))
    WJets.hObj = WJets.hObj.Rebin(len(aTbins)-1,"d",array.array('d',aTbins))
    DY.hObj = DY.hObj.Rebin(len(aTbins)-1,"e",array.array('d',aTbins))
    ZJets.hObj = ZJets.hObj.Rebin(len(aTbins)-1,"f",array.array('d',aTbins))
  # print Data.hObj.Integral()
  TotalBKG = WJets.hObj.Clone()
  TotalBKG.Add(DY.hObj)
  TotalBKG.Add(QCD.hObj)
  TotalBKG.Add(TTbar.hObj)
  TotalBKG.Add(ZJets.hObj)

  Data.hObj.Draw("h")
  QCD.hObj.Draw("sameh")
  TTbar.hObj.Draw("sameh")
  WJets.hObj.Draw("sameh")
  DY.hObj.Draw("sameh")
  ZJets.hObj.Draw("sameh")
  TotalBKG.Draw("sameh")

  leg.AddEntry(Data.hObj,"Data","l")
  leg.AddEntry(TTbar.hObj,"TTBar","l")
  leg.AddEntry(DY.hObj,"DY","l")
  leg.AddEntry(WJets.hObj,"WJets","l")
  leg.AddEntry(QCD.hObj,"QCD","l")
  leg.AddEntry(ZJets.hObj,"ZJets","l")
  leg.AddEntry(TotalBKG,"Total","l")
  leg.Draw()
  c1.Print()

  DataNorm = Data.hObj.Clone()
  DataNormDenom = Data.hObj.Clone()
  
  DataNorm.Scale(1./Data.hObj.Integral())
  TotalBKGNorm = TotalBKG.Clone()
  TotalBKGNormDenom = TotalBKG.Clone()
  print TotalBKG.Integral()
  TotalBKGNorm.Scale(1./TotalBKG.Integral())
  for bin in range(DataNormDenom.GetNbinsX()+1):
    DataNormDenom.SetBinContent(bin,Data.hObj.Integral())
    DataNormDenom.SetBinError(bin,math.sqrt(Data.hObj.Integral()))
    TotalBKGNormDenom.SetBinContent(bin,TotalBKG.Integral())
    TotalBKGNormDenom.SetBinError(bin,math.sqrt(TotalBKG.Integral()))
  DataNorm.Divide(DataNormDenom)
  TotalBKGNorm.Divide(TotalBKGNormDenom)
  
  DataNorm.Draw("h")
  TotalBKGNorm.Draw("sameh")
  
  

  leg.Clear()
  leg.AddEntry(Data.hObj,"Data","l")
  leg.AddEntry(TotalBKG,"TotalBKG","l")
  leg.Draw()
  c1.Print()
  
  DataNorm.Divide(TotalBKGNorm)
  DataNorm.GetYaxis().SetRangeUser(0.,2.)
  DataNorm.Draw("h")
  c1.Print()
  
  DataCumu = MakeCumu(Data.hObj)
  BKGCumu = MakeCumu(TotalBKG)
  DataDenom = DataCumu.Clone()
  BKGDenom = BKGCumu.Clone()
  for bin in range(DataDenom.GetNbinsX()+1):
    DataDenom.SetBinContent(bin,Data.hObj.Integral())
    DataDenom.SetBinError(bin,math.sqrt(Data.hObj.Integral()))
    BKGDenom.SetBinContent(bin,TotalBKG.Integral())
    BKGDenom.SetBinError(bin,math.sqrt(TotalBKG.Integral()))
  DataCumu.Divide(DataDenom)
  BKGCumu.Divide(BKGDenom)
  DataCumu.GetYaxis().SetRangeUser(0.,2.)
  # DataCumu.Scale(1./Data.hObj.Integral())
  # BKGCumu.Scale(1./TotalBKG.Integral())
  DataCumu.Draw("h")
  BKGCumu.Draw("sameh")
  c1.Print()
  DataCumu.Divide(BKGCumu)
  DataCumu.Draw("h")
  c1.Print()
c1.close()
