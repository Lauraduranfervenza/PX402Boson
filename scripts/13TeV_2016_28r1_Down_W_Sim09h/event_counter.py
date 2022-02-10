data_path = "/storage/epp2/phshgg/Public/DVTuples__v24f/13TeV_2016_28r1_Down_W_Sim09h.root"

#imports
from itertools import count
from ROOT import gROOT
gROOT.SetBatch(True)
import ROOT as r

ifile = r.TFile(data_path)
tree = ifile.Get('WpIso/DecayTree')

#create empty histograms from a histogram template
N_bin = 100
hist_counter = r.TH1F('hist_template','TEST counter',N_bin,0,5)

mum0 = 0
mup0 = 0
mum1 = 0
mup1 = 0
mum2 = 0
mup2 = 0
phmore = 0

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

    for j in range(len(array_ID)):
        photons = array_ID.count(22)
        mum_count = array_ID.count(13)
        mup_count = array_ID.count(-13)
    if photons == 0:
        mum0 = mum0 + mum_count
        mup0 = mup0 + mup_count
    if photons == 1:
        mum1 = mum1 + mum_count
        mup1 = mup1 + mup_count
    if photons == 2:
        mum2 = mum2 + mum_count
        mup2 = mup2 + mup_count
    if photons > 2: phmore = phmore + 1
    if i > 100000: break
# event_counter = [mum0, mum1, mum2, mup0, mup1, mup2]
print(phmore)