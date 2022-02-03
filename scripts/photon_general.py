data_path = "/storage/epp2/phshgg/Public/DVTuples__v24f/13TeV_2016_28r1_Down_W_Sim09h.root"

#imports
from ROOT import gROOT
gROOT.SetBatch(True)
import ROOT as r

ifile = r.TFile(data_path)
tree = ifile.Get('WpIso/DecayTree')

#create empty histograms from a histogram template
N_bin = 100
hist_counter = r.TH1F('hist_template','Photon counter',N_bin,0,5)
hist_ETA = r.TH1F('hist_template','Photon ETA',N_bin,0.0,5.0)
hist_PT = r.TH1F('hist_template','Photon PT',N_bin,0.0,100.0)
#photon number is 22
for i, entry in enumerate(tree):
    # counter = 0
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

    # for j in range(len(array_ID)):
    #     if array_ID[j] == 22:
    #         # hist_ETA.Fill(array_ETA[j])
    #         # hist_PT.Fill(array_PT[j])
    #         counter += 1
    counter = array_ID.count(22)
    hist_counter.Fill(counter)
    if i > 100: break

# c = r.TCanvas('TEST ETA')
# c.SetLogy()
# hist_ETA.Scale(1./hist_ETA.Integral())
# hist_ETA.Draw()
# c.Print('TEST_ETA.png')

# c2 = r.TCanvas('TEST counter')   
# c2.SetLogy()
# hist_counter.Scale(1./hist_counter.Integral())
# hist_counter.GetXaxis().SetMaxDigits(0)
# hist_counter.Draw()
# c2.Print('TEST_counter.png')

c3 = r.TCanvas('TEST PT')
c3.SetLogy()
# hist_counter.Scale(1./hist_counter.Integral())
hist_counter.Draw()
c3.Print('TEST_counter2.png')