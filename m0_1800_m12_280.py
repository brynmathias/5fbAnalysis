#!/usr/bin/env python

from plottingUtils import *
import array


settings = {
    "Dirs":["575_675","675_775","775_875","875",],#"275_325","325_375","375_475","475_575",
    "hists":["AlphaT_all"]    
}


c1 = Print("LookAtM01800M12280.pdf")
c1.open()
leg = Legend()
bins = [0.,0.52,0.53,0.55,1.]
for h in settings['hists']:
    data = GetSumHist(File = ["./CMSSM_Skim_Plots.root"], Directories = settings['Dirs'], Hist = h, Col = r.kBlack, Norm = [1./10000.], LegendText = "No btag requirement")
    data_btag = GetSumHist(File = ["./CMSSM_Skim_Plots.root"], Directories = [ "btag_morethanone_"+s for s in settings['Dirs']], Hist = h, Col = r.kRed, Norm = [1./10000.], LegendText = "NBtag >= 1")
    data.hObj.SetTitle("%s_%s"%(h,settings['Dirs']))
    data_btag.HideOverFlow()
    data_btag.Rebin(len(bins)-1,array.array('d',bins))
    data_btag.hObj.GetXaxis().SetRangeUser(0.,2.5)


    data.HideOverFlow()
    data.Rebin(len(bins)-1,array.array('d',bins))
    data.hObj.GetXaxis().SetRangeUser(0.,2.5)
    data.hObj.SetMinimum(1.)
    data.Draw("hist")
    data_btag.Draw("histsame")
    c1.SetLog('y',True)
    leg.AddEntry(data.hObj,data.legendText,"l")
    leg.AddEntry(data_btag.hObj,data_btag.legendText,"l")
    leg.Draw("same")
    c1.Print()
    
c1.close()