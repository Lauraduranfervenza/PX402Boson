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
tree.Show(41)