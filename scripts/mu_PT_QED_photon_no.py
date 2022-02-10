
# 1) Try to make some plots of the distribution of the number of photons using TTree::Draw.
# You could write an expression like “int(mu_truth_leading_photon_pt > 0) + int(mu_truth_subleading_photon_pt > 0)"
# 2) Make plots of the bare muon pT for events with 0,1,2 photons
# 3) Try to get the W mass fitting code to work with these variables. Use mu_truth_bare_pt and V_TRUE_M (for the weight).
# mu_truth_leading_photon_pt = 0 // the pT of the highest pT photon near the muon (if there is one)
# mu_truth_subleading_photon_pt = 0// the pT of the second highest pT photon...
data_path = "/storage/epp2/phshgg/Public/MPhysProject_2021_2022/ProcessTuples/Wp_W_13TeV_SmearingOff_AlignCorrOff_MomScaleCorrOff.root"
# Week 4-5
#imports
from ROOT import gROOT
gROOT.SetBatch(True)
import ROOT as r
import numpy as np
from array import array #this is for the chi square plotting

ifile = r.TFile(data_path)
tree = ifile.Get('DecayTree')

#define any relevant variables
w_boson_width_gev = 2.028     #in GeV from https://arxiv.org/abs/0909.4814

#create empty histograms from a histogram template
N_bin = 100
hist0 = r.TH1F('hist0','No Photons',N_bin,0.0,100.0)
hist1 = r.TH1F('hist1','One Photon',N_bin,0.0,100.0)
hist2 = r.TH1F('hist2','Two or More Photons',N_bin,0.0,100.0)

#photon number is 22
for i, entry in enumerate(tree):
    if  entry.mu_truth_leading_photon_pt == 0: hist0.Fill(entry.mu_truth_bare_pt)#no photons
    elif  entry.mu_truth_subleading_photon_pt == 0: hist1.Fill(entry.mu_truth_bare_pt) # 1 photon
    else: n_photons = hist2.Fill(entry.mu_truth_bare_pt) # more than 1 photon
    # if i > 1000: break

hist0.Scale(1./hist0.Integral())
hist1.Scale(1./hist1.Integral())
hist2.Scale(1./hist2.Integral())

c = r.TCanvas('PT dependent on photon number')
c.SetLogy()
hist0.SetLineColor(1)
hist1.SetLineColor(2)
hist2.SetLineColor(3)
hist0.Draw('HIST')
hist1.Draw('HIST SAME')
hist2.Draw('HIST SAME')
c.BuildLegend()
hist0.SetTitle('PT after QED dependent on photon number')
c.Print('mu_PT_QED_photon_no.png')