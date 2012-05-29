#!/usr/bin/env python
import sys
import os
import ROOT as r
from plottingstuff import *
from plottingUtils import Print
import math


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
models = ["T2bb","T1","T2","T2tt","T1tttt","T1bbbb"]
Cuts = ["DECAL","MHTovMET"]

for cut in Cuts:
  for model in models:

      xTitle = None
      yTitle = None
      if model == "T2bb":
        xTitle = "m_{sbottom} (GeV)"
        yTitle = "m_{LSP} (GeV)"
        maxi = .4
        mini = 0.01
        
      if model == "T2tt":
        xTitle = "m_{stop} (GeV)"
        yTitle = "m_{LSP} (GeV)"
        maxi = .4
        mini = 0.01

      if model == "T1":
        xTitle = "m_{gluino} (GeV)"
        yTitle = "m_{LSP} (GeV)"
        maxi = .4
        mini = 0.01
        
      if model == "T2":
        xTitle = "m_{squark} (GeV)"
        yTitle = "m_{LSP} (GeV)"
        maxi = .4
        mini = 0.01

        
      if model == "T1tttt":
        xTitle = "m_{gluino} (GeV)"
        yTitle = "m_{LSP} (GeV)"
        maxi = .4
        mini = 0.01

        
      if model == "T1bbbb":
        xTitle = "m_{gluino} (GeV)"
        yTitle = "m_{LSP} (GeV)"
        maxi = .4
        mini = 0.01

    
    
    
      c1 = Print("./out/%s_SMS%s.pdf"%(cut,model))
      c1.DoPageNum = False
      c1.open()
      r.gPad.SetRightMargin(0.175)
      r.gPad.SetLeftMargin(0.15)
      r.gPad.SetTopMargin(0.05)
      r.gPad.SetBottomMargin(0.15)
      print model, cut
      FullCutFlowRootFile100 = r.TFile.Open("./JESandLepVetoRootFiles/results_NEWSCAN_JESCEN_had_%s_100.root"%(model))
      NMinus1RootFile100 = r.TFile.Open("./MHTovMET_Signal/results_NEWSCAN_NO%s_had_%s_100.root"%(cut,model))





      # centalRootFile73.ls()
      # Make cross sections/ efficiencies
      for bin in settings["HTBins"]:        
          processCrossSections = []
          cuts = []
          cutsJESNeg = []
          cutsJESPlus = []
          # cutsJESRan = []
          nocuts = []

          nocuts = GetHist(File = FullCutFlowRootFile100,folder = ["smsScan_before",], hist = "m0_m12_mChi_noweight", Norm = None ,rebin= 2)
          nocuts = threeToTwo(nocuts)
   

          FullCutFlow = GetHist(File = FullCutFlowRootFile100,folder = ["smsScan_AlphaT55_375_475","smsScan_AlphaT55_475_575","smsScan_AlphaT55_575_675",
           "smsScan_AlphaT55_675_775","smsScan_AlphaT55_775_875","smsScan_AlphaT55_875"],hist = "m0_m12_mChi_noweight", Norm = None ,rebin= 2).Clone()
          FullCutFlow = threeToTwo(FullCutFlow)                                                    

          NMinus1 = GetHist(File = NMinus1RootFile100,folder = ["smsScan_AlphaT55_375_475","smsScan_AlphaT55_475_575","smsScan_AlphaT55_575_675",
      "smsScan_AlphaT55_675_775","smsScan_AlphaT55_775_875","smsScan_AlphaT55_875"],hist = "m0_m12_mChi_noweight", Norm = None ,rebin= 2).Clone()

          NMinus1 = threeToTwo(NMinus1)

                              
        
          l =  [i * 5 for i in range(301)]
          print l
          for a in l:
            for b in l:
              # m_sq (m_gl) - m_LSP >= 175 && m_sq (m_gl) >= 300
              if  a - b <= 175 or a < 300. :
                bin = FullCutFlow.FindBin(float(a),float(b))
                FullCutFlow.SetBinContent(bin,0.)
                NMinus1.SetBinContent(bin,0.)          

          x_width = FullCutFlow.GetXaxis().GetBinWidth(10)
          y_width = FullCutFlow.GetYaxis().GetBinWidth(10)
          cutValue = 250.
          print x_width,y_width
          #  use Y = mX + c

        

          c1.canvas.SetLogz()
          offset = 1.1
          # c1.Print()    
          c1.canvas.SetLogz(False)
          FullCutFlowEff = FullCutFlow.Clone()
          FullCutFlowEff.GetZaxis().SetTitle("Fraction of expected signal yield")
          FullCutFlowEff.GetZaxis().SetTitleOffset(offset)
          FullCutFlowEff.GetZaxis().SetTitleSize(0.05)
          FullCutFlowEff.GetXaxis().SetTitle(xTitle)

          # FullCutFlowEff.GetYaxis().SetLabelSize(0.04)
          FullCutFlowEff.GetYaxis().SetTitleOffset(1.3)
          FullCutFlowEff.GetYaxis().SetTitleSize(0.05)        
          FullCutFlowEff.GetYaxis().SetTitle(yTitle)
          # FullCutFlowEff.SetTitle("Efficiency (No JES)")
          FullCutFlowEff.Divide(nocuts)
          FullCutFlowEff.Draw("COLZ")
          c1.Print()



          NMinus1Eff = NMinus1.Clone()
          NMinus1Eff.GetZaxis().SetTitle("Fraction of expected signal yield")
          NMinus1Eff.GetZaxis().SetTitleOffset(offset)
          NMinus1Eff.GetZaxis().SetTitleSize(0.05)
          NMinus1Eff.GetXaxis().SetTitle(xTitle)
          NMinus1Eff.GetYaxis().SetTitleOffset(1.3)
          NMinus1Eff.GetYaxis().SetTitleSize(0.05)        
          NMinus1Eff.GetYaxis().SetTitle(yTitle)
          NMinus1Eff.Divide(nocuts)
          NMinus1Eff.Draw("COLZ")
          c1.Print()
          
          EffChange = r.TH2D(FullCutFlowEff)
          EffChange.Divide(NMinus1Eff)
          EffChange.GetZaxis().SetTitle("Inefficiency from %s cut"%cut)
          for bin in range(EffChange.GetNbinsX()*EffChange.GetNbinsY()):
            if EffChange.GetBinContent(bin) > 0.:
              EffChange.SetBinContent(bin, 1.- EffChange.GetBinContent(bin))
          
              
              

          # c1.Print()
         

          oneD = r.TH1D("OneD_Projection","",500,0,0.5)
          for bin in range(EffChange.GetNbinsX()*EffChange.GetNbinsY()):
            if EffChange.GetBinContent(bin) > 0. :
              oneD.Fill(EffChange.GetBinContent(bin))
          oneD.GetXaxis().SetTitle("Fraction of expected signal yield rejected")
          r.gStyle.SetOptStat(1111)
          r.gPad.SetRightMargin(0.05)
          oneD.SetName("")
          oneD.Draw("h")
          c1.Print()
          
          
          
          l =  [i * 25 for i in range(60)]


          binlist = []
          closeBins = []
          farBins = []
          closeToLine = r.TH1D("OneD_Projection_closeToLine","",500,0,0.5)
          farToLine = r.TH1D("OneD_Projection_farToLine","",500,0,0.5)
          line = 350.
          cutoff = 450.
          # if model == "T1tttt":
          #   line = 550.
          #   cutoff = 600.
          for a in l:
            for b in l:
              # m_sq (m_gl) - m_LSP >= 175 && m_sq (m_gl) >= 300
              bin = EffChange.FindBin(float(a),float(b))
              if  a - b >= line and a > cutoff :                
                # print bin
                if EffChange.GetBinContent(bin) > 0.:
                  farBins.append(bin)
              else:
                if EffChange.GetBinContent(bin) > 0.:
                  closeBins.append(bin)


          # 
          closeBins = set(closeBins)
          farBins = set(farBins)
          TestMe = r.TH2D(EffChange)
          TestMe.SetMinimum(0.)
          TestMe.SetMaximum(1.)
          for b in farBins: farToLine.Fill(EffChange.GetBinContent(b))
          for b in closeBins: closeToLine.Fill(EffChange.GetBinContent(b))
          closeToLine.Draw("h")
          c1.Print()
          farToLine.Draw("h")
          c1.Print()


          r.gStyle.SetOptStat(0)
          for b in range(TestMe.GetXaxis().GetNbins()*TestMe.GetYaxis().GetNbins()):
            # if b in closeBins: TestMe.SetBinContent(b,1.)
            if b in farBins: 
              TestMe.SetBinContent(b,0.5)
            elif b in closeBins: TestMe.SetBinContent(b,1.0)
            else:
              TestMe.SetBinContent(b,0.)
          
          TestMe.Draw("COLZ")
          c1.Print()

          
          
          
          r.gPad.SetRightMargin(0.175)

          for bin in range(EffChange.GetNbinsX()*EffChange.GetNbinsY()):
            if EffChange.GetBinContent(bin) > 0.:
              if EffChange.GetBinContent(bin) > maxi: EffChange.SetBinContent(bin,maxi)
              if EffChange.GetBinContent(bin) < mini: EffChange.SetBinContent(bin,mini)          

          c1.canvas.Clear()
          EffChange.Draw("COLZ")
          EffChange.SetMinimum(mini)
          EffChange.SetMaximum(maxi)
          EffChange.GetZaxis().SetTitle("Fraction of expected signal yield rejected")
          c1.canvas.SetLogz()
          c1.Print()




      c1.close()
