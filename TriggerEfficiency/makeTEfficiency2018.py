import ROOT
import os
import numpy as np

#filein = ROOT.TFile.Open("SingleElectronTrees.root")

#test_tree = filein.Get("Cut1/Events")

#fileinhists = ROOT.TFile.Open("SingleEle2017PFMETPFMHT140.root")
#numhist = fileinhists.Get("Cut6/minMETMHT")
#denomhist = fileinhists.Get("Cut5/minMETMHT")

#teffhist = ROOT.TEfficiency(numhist,denomhist)
#teffhist.SetMarkerStyle(25)


xbins = [0.,10.,20.,30.,40.,50.,60.,70.,80.,90.,100.,110.,120.,130.,140.,150.,160.,170.,180.,190.,200.,210.,220.,240.,260.,280.,300.,350.,400.,450.,500.]


denominator = ROOT.TH1F("denominator",";min(MET,MHT) [GeV];",len(xbins)-1,np.array(xbins))
num_120 = ROOT.TH1F("num_120",";min(MET,MHT) [GeV];",len(xbins)-1,np.array(xbins))
denominator.Sumw2()
num_120.Sumw2()

for i in range(1,165):
  filein = ROOT.TFile.Open("./EfficiencyAnalyzerJobs/SingleElectron2018A-nano14dec/outputs/job%i.root"%i)
  testtree = filein.Get("Cut1/Events")

  denominator.SetDirectory(ROOT.gDirectory)
  num_120.SetDirectory(ROOT.gDirectory)

  testtree.Draw("min(MET_pt, MHT_pt)>>+denominator")

  if (testtree.GetBranchStatus("HLT_PFMET120_PFMHT120_IDTight")):
    testtree.Draw("min(MET_pt, MHT_pt)>>+num_120","HLT_PFMET120_PFMHT120_IDTight")

  denominator.SetDirectory(0)
  num_120.SetDirectory(0)

for i in range(1,70):
  filein = ROOT.TFile.Open("./EfficiencyAnalyzerJobs/SingleElectron2018B-nano14dec/outputs/job%i.root"%i)
  testtree = filein.Get("Cut1/Events")

  denominator.SetDirectory(ROOT.gDirectory)
  num_120.SetDirectory(ROOT.gDirectory)

  testtree.Draw("min(MET_pt, MHT_pt)>>+denominator")

  if (testtree.GetBranchStatus("HLT_PFMET120_PFMHT120_IDTight")):
    testtree.Draw("min(MET_pt, MHT_pt)>>+num_120","HLT_PFMET120_PFMHT120_IDTight")

  denominator.SetDirectory(0)
  num_120.SetDirectory(0)

for i in range(1,84):
  filein = ROOT.TFile.Open("./EfficiencyAnalyzerJobs/SingleElectron2018C-nano14dec/outputs/job%i.root"%i)
  testtree = filein.Get("Cut1/Events")

  denominator.SetDirectory(ROOT.gDirectory)
  num_120.SetDirectory(ROOT.gDirectory)

  testtree.Draw("min(MET_pt, MHT_pt)>>+denominator")

  if (testtree.GetBranchStatus("HLT_PFMET120_PFMHT120_IDTight")):
    testtree.Draw("min(MET_pt, MHT_pt)>>+num_120","HLT_PFMET120_PFMHT120_IDTight")

  denominator.SetDirectory(0)
  num_120.SetDirectory(0)

for i in range(1,348):
  filein = ROOT.TFile.Open("./EfficiencyAnalyzerJobs/SingleElectron2018D-nano14sep/outputs/job%i.root"%i)
  testtree = filein.Get("Cut1/Events")

  denominator.SetDirectory(ROOT.gDirectory)
  num_120.SetDirectory(ROOT.gDirectory)

  testtree.Draw("min(MET_pt, MHT_pt)>>+denominator")

  if (testtree.GetBranchStatus("HLT_PFMET120_PFMHT120_IDTight")):
    testtree.Draw("min(MET_pt, MHT_pt)>>+num_120","HLT_PFMET120_PFMHT120_IDTight")

  denominator.SetDirectory(0)
  num_120.SetDirectory(0)



denominator.SetLineColor(ROOT.kBlue)

teff120 = ROOT.TEfficiency(num_120,denominator)

teff120.SetMarkerStyle(20)

c0=ROOT.TCanvas()
leg0 = ROOT.TLegend(0.6,0.25,0.9,0.4)
denominator.Draw()
c0.SetLogy()
#leg0.Draw("SAME")
c0.SaveAs("denom_test_hist.pdf")

c2 = ROOT.TCanvas()
legend2 = ROOT.TLegend(0.6,0.25,0.9,0.4)
legend2.AddEntry(teff120, "HLT_PFMET120_PFMHT120_IDTight","P")
teff120.Draw("AP")
legend2.Draw("SAME")
c2.SaveAs("120_threshold.pdf")

fileout = ROOT.TFile.Open("DataEfficiencyHistos.root","RECREATE")
teff120.SetName("teff120")
teff120.Write()
fileout.Close()

