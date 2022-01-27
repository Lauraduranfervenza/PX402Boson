data_path = "/storage/epp2/phshgg/Public/DVTuples__v24f/13TeV_2016_28r1_Down_W_Sim09h.root"

#imports
from ROOT import gROOT
gROOT.SetBatch(True)
import ROOT as r

#gDirectory->ls()
#WpIso decay tree
#mu_MC_Relation looking for 
#loop over events and see photons per event   x=no of photons y=no of events
#how often 2 relations of non zero ID
ifile = r.TFile(data_path)
#ifile.ls()
tree = ifile.Get('WpIso/DecayTree')
#tree.Show(41)

#create empty histograms from a histogram template
N_bin = 100
hist = r.TH1F('hist_template','mu_PT',N_bin,0,5)
#photon number is 22
for i, entry in enumerate(tree):
    counter = 0
    e1 = entry.mu_MC_RELATION1_ID
    e2 = entry.mu_MC_RELATION2_ID
    e3 = entry.mu_MC_RELATION3_ID
    e4 = entry.mu_MC_RELATION4_ID
    e5 = entry.mu_MC_RELATION5_ID
    e6 = entry.mu_MC_RELATION6_ID
    e7 = entry.mu_MC_RELATION7_ID
    e8 = entry.mu_MC_RELATION8_ID
    e9 = entry.mu_MC_RELATION9_ID
    array = [e1, e2, e3, e4, e5, e6, e7, e8, e9]
    
    # array = [entry.mu_MC_RELATION1_ID,entry.mu_MC_RELATION2_ID,entry.mu_MC_RELATION3_ID,entry.mu_MC_RELATION4_ID,entry.mu_MC_RELATION5_ID,entry.mu_MC_RELATION6_ID,entry.mu_MC_RELATION7_ID,entry.mu_MC_RELATION8_ID,entry.mu_MC_RELATION9_ID]

    for j in range(len(array)):
        if array[j] == 22:
            counter += 1
    # if counter == 0: photon_0 += 1

    hist.Fill(counter)
    # if i > 100000: break

#Prints number of events with x photons
c = r.TCanvas('Photon Counter')
hist.Draw()
c.Print('images/photon_counter.png')

# > * Look at /storage/epp2/phshgg/Public/DVTuples__v24f/13TeV_2016_28r1_Down_W_Sim09h.root
# > * Inside the file there is WpIso/DecayTree
# > * This tree contains *reconstructed* (the same way as for real data, after detector simulation) muon candidates.
# > * Since it is MC simulation we also have the “truth” information matching the muon candidates.
#       This is in the mu_MC_RELATION… variables.
# > * First step is to write some simple python script (for entry in tree: …)
#       and look at the variables like entry.mu_MC_RELATION1_ETA
# > * Note that you can always do tree.Show(entry_number) to see what variables are available.
# > * Refer to the MC particle numbering scheme to see the IDs. E.g. photon is 22, muon is +-13, muon neutrino is +-14.
# >  
# > I hope that helps. Please don’t hesitate to update me with questions or any plots/results etc… :~)
# >
# > The longer term goals, which we can split between you, will be:
# > 1) See if we can make the mW fit less sensitive to QED if we “dress” the muon with photons
#   (if they are high enough in pT such that we could see them in the detector)
# > 2) Do a really detailed study of how the QED radiation looks. How many photons are radiated,
#   what is the energy, angle w.r.t. the muon etc… This part could also extend to running the Pythia event generator
#   to ask more detailed questions than we could answer with the existing files.

