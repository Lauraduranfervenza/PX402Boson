data_path = "/storage/epp2/phshgg/Public/DVTuples__v24f/13TeV_2016_28r1_Down_W_Sim09h.root"

#imports
from ROOT import gROOT
gROOT.SetBatch(True)
import ROOT as r

ifile = r.TFile(data_path)
tree = ifile.Get('WpIso/DecayTree')

#create empty histograms from a histogram template
N_bin = 100
hist0 = r.TH1F('hist0','No Photons',N_bin,0.0,100.0)
hist1 = r.TH1F('hist1','One Photon',N_bin,0.0,100.0)
hist2 = r.TH1F('hist2','Two or More Photons',N_bin,0.0,100.0)

#photon number is 22
for i, entry in enumerate(tree):
    ID1 = entry.mu_MC_RELATION1_ID
    ID2 = entry.mu_MC_RELATION2_ID
    ID3 = entry.mu_MC_RELATION3_ID
    ID4 = entry.mu_MC_RELATION4_ID
    ID5 = entry.mu_MC_RELATION5_ID
    ID6 = entry.mu_MC_RELATION6_ID
    ID7 = entry.mu_MC_RELATION7_ID
    ID8 = entry.mu_MC_RELATION8_ID
    ID9 = entry.mu_MC_RELATION9_ID
    array_ID = [ID1, ID2, ID3, ID4, ID5, ID6, ID7, ID8, ID9]

    PT1 = entry.mu_MC_RELATION1_PT*1e-3
    PT2 = entry.mu_MC_RELATION2_PT*1e-3
    PT3 = entry.mu_MC_RELATION3_PT*1e-3
    PT4 = entry.mu_MC_RELATION4_PT*1e-3
    PT5 = entry.mu_MC_RELATION5_PT*1e-3
    PT6 = entry.mu_MC_RELATION6_PT*1e-3
    PT7 = entry.mu_MC_RELATION7_PT*1e-3
    PT8 = entry.mu_MC_RELATION8_PT*1e-3
    PT9 = entry.mu_MC_RELATION9_PT*1e-3
    array_PT = [PT1, PT2, PT3, PT4, PT5, PT6, PT7, PT8, PT9]

    counter = array_ID.count(22)
    for j in range(len(array_ID)):
        if array_ID[j] == 13 or array_ID[j] == -13:
            if counter == 0: hist0.Fill(array_PT[j])
            elif counter == 1: hist1.Fill(array_PT[j])
            elif counter > 1: hist2.Fill(array_PT[j])
    # if i > 10000: break

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
hist0.SetTitle('PT dependent on photon number')
c.Print('images/photon_counter/mu_ph_PT.png')