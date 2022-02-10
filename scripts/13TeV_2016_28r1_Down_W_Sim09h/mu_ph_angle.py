data_path = "/storage/epp2/phshgg/Public/DVTuples__v24f/13TeV_2016_28r1_Down_W_Sim09h.root"

#imports
from ROOT import gROOT
gROOT.SetBatch(True)
import ROOT as r

ifile = r.TFile(data_path)
tree = ifile.Get('WpIso/DecayTree')

#create empty histograms from a histogram template
N_bin = 100
hist1 = r.TH1F('hist1','One Photon',N_bin,0.0,50.0)
# hist2 = r.TH1F('hist2','Highest Energy Photon',N_bin,0.0,100.0)

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

    PHI1 = entry.mu_MC_RELATION1_PHI
    PHI2 = entry.mu_MC_RELATION2_PHI
    PHI3 = entry.mu_MC_RELATION3_PHI
    PHI4 = entry.mu_MC_RELATION4_PHI
    PHI5 = entry.mu_MC_RELATION5_PHI
    PHI6 = entry.mu_MC_RELATION6_PHI
    PHI7 = entry.mu_MC_RELATION7_PHI
    PHI8 = entry.mu_MC_RELATION8_PHI
    PHI9 = entry.mu_MC_RELATION9_PHI
    array_PHI = [PHI1, PHI2, PHI3, PHI4, PHI5, PHI6, PHI7, PHI8, PHI9]

    counter = array_ID.count(22)
    if counter == 1:
        for j in range(len(array_ID)):
            if array_ID[j] == 22:
                PHI_ph = array_PHI[j]
                ETA_ph = array_ETA[j]
            if array_ID[j] == 13 or array_ID[j] == -13:
                PHI_mu = array_PHI[j]
                ETA_mu = array_ETA[j]
        dPHI = abs(PHI_ph - PHI_mu)
        dETA = ETA_ph - ETA_mu
        dR = sqrt(dETA*dETA + dPHI*dPHI)
        hist1.Fill(dR)
                
    # if i > 10000: break

hist1.Scale(1./hist1.Integral())
# hist2.Scale(1./hist2.Integral())

c = r.TCanvas('PT dependent on photon number')
# c.SetLogy()
hist1.SetLineColor(1)
# hist2.SetLineColor(2)
hist1.Draw('HIST')
# hist2.Draw('HIST SAME')
# c.BuildLegend()
hist1.SetTitle('Angle dR between muon and photon')
c.Print('images/photon_counter/mu_ph_angle.png')