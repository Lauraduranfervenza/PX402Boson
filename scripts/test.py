# data_path = "/storage/epp2/phshgg/Public/DVTuples__v24f/13TeV_2016_28r1_Down_W_Sim09h.root"
# new_path = "/storage/epp2/phshgg/Public/MPhysProject_2021_2022/Wp_W_13TeV_SmearingOff_AlignCorrOff_MomScaleCorrOff.root" #2017-2018 data derived from data_path
data_path3 = "/storage/epp2/phshgg/Public/MPhysProject_2021_2022/Wp_W_13TeV_SmearingOff_AlignCorrOff_MomScaleCorrOff.root"
data_path4 = "/storage/epp2/phshgg/Public/MPhysProject_2021_2022/ProcessTuples/Wp_W_13TeV_SmearingOff_AlignCorrOff_MomScaleCorrOff.root"
#imports
from ROOT import gROOT
gROOT.SetBatch(True)
import ROOT as r
import numpy as np

#gDirectory->ls()
#WpIso decay tree
#mu_MC_Relation looking for 
#loop over events and see photons per event   x=no of photons y=no of events
#how often 2 relations of non zero ID
ifile = r.TFile(data_path4)
    #ifile.ls()
tree = ifile.Get('DecayTree')
tree.Show(41)