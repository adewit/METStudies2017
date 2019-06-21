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

for i in range(1,22):
  filein = ROOT.TFile.Open("./EfficiencyAnalyzerJobs/WJetsToLNu_HT1200to2500/outputs/job%i.root"%i)
  testtree = filein.Get("Cut1/Events")

  denominator.SetDirectory(ROOT.gDirectory)
  num_120.SetDirectory(ROOT.gDirectory)

  testtree.Draw("min(MET_pt, MHT_pt)>>+denominator")


  if (testtree.GetBranchStatus("HLT_PFMET120_PFMHT120_IDTight")):
    testtree.Draw("min(MET_pt, MHT_pt)>>+num_120","HLT_PFMET120_PFMHT120_IDTight")

  denominator.SetDirectory(0)
  num_120.SetDirectory(0)

#print "entries: ",denominator.GetEntries()

#test_tree.Draw("min(MET_pt, MHT_pt)>>denominator","")
#test_tree.Draw("min(MET_pt, MHT_pt)>>num_140","HLT_PFMET140_PFMHT140_IDTight")
#test_tree.Draw("min(MET_pt, MHT_pt)>>num_140_250","(HLT_PFMET140_PFMHT140_IDTight||HLT_PFMET250_HBHECleaned)")
#test_tree.Draw("min(MET_pt, MHT_pt)>>num_250","HLT_PFMET250_HBHECleaned")
#test_tree.Draw("min(MET_pt, MHT_pt)>>num_200","HLT_PFMET200_HBHE_BeamHaloCleaned")
#test_tree.Draw("min(MET_pt, MHT_pt)>>num_120","HLT_PFMET120_PFMHT120_IDTight")
#test_tree.Draw("min(MET_pt, MHT_pt)>>num_120withht60","HLT_PFMET120_PFMHT120_IDTight_PFHT60")
#test_tree.Draw("min(MET_pt, MHT_pt)>>num_120ht60","(HLT_PFMET120_PFMHT120_IDTight||HLT_PFMET120_PFMHT120_IDTight_PFHT60)")

#tchain_test.Draw("min(MET_pt, MHT_pt)>>denominator","")
#tchain_test.Draw("min(MET_pt, MHT_pt)>>num_140","HLT_PFMET140_PFMHT140_IDTight")
#tchain_test.Draw("min(MET_pt, MHT_pt)>>num_140_250","((HLT_PFMET140_PFMHT140_IDTight>0)||(HLT_PFMET250_HBHECleaned>0))")
#tchain_test.Draw("min(MET_pt, MHT_pt)>>num_250","HLT_PFMET250_HBHECleaned")
#tchain_test.Draw("min(MET_pt, MHT_pt)>>num_200","HLT_PFMET200_HBHE_BeamHaloCleaned")
#tchain_test.Draw("min(MET_pt, MHT_pt)>>num_120","HLT_PFMET120_PFMHT120_IDTight")
#tchain_test.Draw("min(MET_pt, MHT_pt)>>num_120withht60","HLT_PFMET120_PFMHT120_IDTight_PFHT60")
#tchain_test.Draw("min(MET_pt, MHT_pt)>>num_120ht60","((HLT_PFMET120_PFMHT120_IDTight_PFHT60>0)||(HLT_PFMET120_PFMHT120_IDTight>0))")


#denomhist.SetLineColor(ROOT.kRed)
denominator.SetLineColor(ROOT.kBlue)

#print denomhist.GetEntries()
#print denominator.GetEntries()

#cm1 = ROOT.TCanvas()
#denomhist.Draw()
#denominator.Draw("SAME")
#cm1.SaveAs("testdenom.pdf")



teff120 = ROOT.TEfficiency(num_120,denominator)

teff120.SetMarkerStyle(20)
teff120.SetMarkerColor(ROOT.kGreen+3)

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
c2.SaveAs("120_thresholdMC.pdf")


triggerMET = ROOT.TF1("expo","[2]*(1e0-exp(-[0]*(x-[1])))",100,500)
triggerMET.SetParameter(0,5.27300e-02)
triggerMET.SetParameter(1,1.04024e+02)
triggerMET.SetParameter(2,9.76189e-01)
triggerMET.SetLineColor(ROOT.kGreen+3)
#c3 = ROOT.TCanvas()
#legend3 = ROOT.TLegend(0.6,0.25,0.9,0.4)
#legend3.AddEntry(teff120ht60, "OR (min 120 GeV)","P")
#legend3.AddEntry(teff140_250, "OR (min 140 GeV)","P")
#legend3.AddEntry(triggerMET, "2016 trigger efficiency","L")
#teff140_250.Draw("AP")
#teff120ht60.Draw("PSAME")
#triggerMET.Draw("LSAME")
#legend3.Draw("SAME")
#c3.SaveAs("120_vs_140MC.pdf")


fileout = ROOT.TFile.Open("DataEfficiencyHistosMC.root","RECREATE")
teff120.SetName("teff120")
teff120.Write()
fileout.Close()
