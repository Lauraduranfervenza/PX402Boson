data_path = "/storage/epp2/phshgg/Public/DVTuples__v24f/13TeV_2016_28r1_Down_W_Sim09h.root"

#imports
from ROOT import gROOT
gROOT.SetBatch(True)
import ROOT as r

ifile = r.TFile(data_path)
#ifile.ls()
tree = ifile.Get('WpIso/DecayTree')
# tree.Show(41)

#create empty histograms from a histogram template
N_bin = 100
hist_counter = r.TH1F('hist_template','Photon counter',N_bin,0,5)
hist_ETA = r.TH1F('hist_template','Photon ETA',N_bin,0.0,5.0)
hist_PT = r.TH1F('hist_template','Photon PT',N_bin,0.0,100.0)
#photon number is 22
for i, entry in enumerate(tree):
    counter = 0
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

    ETA1 = entry.mu_MC_RELATION1_ETA
    ETA2 = entry.mu_MC_RELATION2_ETA
    ETA3 = entry.mu_MC_RELATION3_ETA
    ETA4 = entry.mu_MC_RELATION4_ETA
    ETA5 = entry.mu_MC_RELATION5_ETA
    ETA6 = entry.mu_MC_RELATION6_ETA
    ETA7 = entry.mu_MC_RELATION7_ETA
    ETA8 = entry.mu_MC_RELATION8_ETA
    ETA9 = entry.mu_MC_RELATION9_ETA
    array_ETA = [ETA1, ETA2, ETA3, ETA4, ETA5, ETA6, ETA7, ETA8, ETA9]

    PT1 = entry.mu_MC_RELATION1_PT
    PT2 = entry.mu_MC_RELATION2_PT
    PT3 = entry.mu_MC_RELATION3_PT
    PT4 = entry.mu_MC_RELATION4_PT
    PT5 = entry.mu_MC_RELATION5_PT
    PT6 = entry.mu_MC_RELATION6_PT
    PT7 = entry.mu_MC_RELATION7_PT
    PT8 = entry.mu_MC_RELATION8_PT
    PT9 = entry.mu_MC_RELATION9_PT
    array_PT = [PT1, PT2, PT3, PT4, PT5, PT6, PT7, PT8, PT9]

    for j in range(len(array_ID)):
        if array_ID[j] == 22 and array_ETA[j] != 0:
            hist_ETA.Fill(array_ETA[j])
            hist_PT.Fill(array_PT[j])
            counter += 1
    # if i > 10000: break

    hist_counter.Fill(counter)
#Prints number of events with x photons
c = r.TCanvas('Photon ETA')
hist_ETA.Draw()
c.Print('photon_ETA.png')

c2 = r.TCanvas('Photon counter')
hist_counter.GetXaxis().SetMaxDigits(0)
hist_counter.Draw()
c2.Print('photon_counter.png')

c3 = r.TCanvas('Photon PT')
hist_PT.Draw()
c3.Print('photon_PT.png')
