#!/usr/bin/env python
# encoding: utf-8
"""
printEventNosInAlphaTBins.py
Created by Bryn Mathias on 1-1-2012.

Request from oliver to tell the number of events in each alphaT bin from the HT triggers.
"""
from plottingUtils import *
import ROOT as r
import math
import sys
import os

htBins = {
  "275":{
    "File": ["HT275.root"],
    "Directories" : ["275_325"],
    "Histograms" : ["AlphaT_Zoomed_all","HT_all","AlphaT_all"],
    "Normilisation":None,
  },
  "325" : {
    "File" : ["HT325.root"],
    "Directories" : ["325_375"],
    "Histograms" : ["AlphaT_Zoomed_all","HT_all","AlphaT_all"],
    "Normilisation" : None,
  },
  "375" : {
    "File" : ["HT375.root"],
    "Directories" : ["375_475"],
    "Histograms" : ["AlphaT_Zoomed_all","HT_all","AlphaT_all"],
    "Normilisation" : None,
  },
  "475" : {
    "File" : ["HT375.root"],
    "Directories" : ["475_575"],
    "Histograms" : ["AlphaT_Zoomed_all","HT_all","AlphaT_all"],
    "Normilisation" : None,
  },
  "575" : {
    "File" : ["HT375.root"],
    "Directories" : ["575_675"],
    "Histograms" : ["AlphaT_Zoomed_all","HT_all","AlphaT_all"],
    "Normilisation" : None,
  },
  "675" : {
    "File" : ["HT375.root"],
    "Directories" : ["675_775"],
    "Histograms" : ["AlphaT_Zoomed_all","HT_all","AlphaT_all"],
    "Normilisation" : None,
  },
  "775" : {
    "File" : ["HT375.root"],
    "Directories" : ["775_875"],
    "Histograms" : ["AlphaT_Zoomed_all","HT_all","AlphaT_all"],
    "Normilisation" : None,
  },
  "875" : {
    "File" : ["HT375.root"],
    "Directories" : ["875_7000"],
    "Histograms" : ["AlphaT_Zoomed_all","HT_all","AlphaT_all"],
    "Normilisation" : None,
  },


}




def bin(val):
    """docstring for bin"""
    return int(val/0.01) + 1
    pass




def main():
  text = ""
  """docstring for main"""
  text += " Bin & alphat 0.51 - 0.52 & alphat 0.52 - 0.53 & alphat 0.53 - 0.54 & alphat 0.54 - 0.55 & alphat 0.55 - 0.56 & alphat 0.56 - 0.57 & alphat 0.57 - 0.58 & alphat 0.58 - 0.59 & alphat 0.59 - 0.60 & alphat 0.60 - inf  \\\\ \n"
  for key,settings in sorted( htBins.iteritems() ):
    c1 = Print("%s.pdf"%key)
    c1.open()

    print key , settings['File'],settings["Histograms"],settings["Normilisation"]
    for histogram in settings["Histograms"]:
      hist = GetSumHist(File = settings['File'], Directories = settings['Directories'], Hist = histogram, Col = r.kBlack, Norm = settings['Normilisation'], LegendText = "")
      hist.hObj.SetTitle("Bin = %s, Hist = %s"%(key,histogram[:-4]))
      if "AlphaT_all" == histogram:
        # print hist.hObj.Integral(0.51/0.01 + 1,0.52/0.01 +1)

        print hist.hObj.GetBinLowEdge(bin(0.51))
        text += "\\hline\n"
        text += " %s & %d & %d & %d & %d & %d & %d & %d & %d & %d & %d  \\\\ \n "%(key,hist.hObj.Integral(bin(0.51),bin(0.52)),hist.hObj.Integral(bin(0.52),bin(0.53)),hist.hObj.Integral(bin(0.53),bin(0.54)),hist.hObj.Integral(bin(0.54),bin(0.55)),hist.hObj.Integral(bin(0.55),bin(0.56)),hist.hObj.Integral(bin(0.56),bin(0.57)),hist.hObj.Integral(bin(0.57),bin(0.58)),hist.hObj.Integral(bin(0.58),bin(0.59)),hist.hObj.Integral(bin(0.59),bin(0.56)),hist.hObj.Integral(bin(0.60),bin(5.00)))
        hist.SetRange('x',0.,1.0)
      hist.Draw("hist")
      c1.SetLog('y',True)      
      c1.Print()
    c1.close()
  print text
if __name__ == '__main__':
  main()
