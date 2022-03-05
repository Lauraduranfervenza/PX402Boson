data_path = "/storage/epp2/phshgg/Public/MPhysProject_2021_2022/ProcessTuples2/Wp_W_13TeV_SmearingOff_AlignCorrOff_MomScaleCorrOff.root"

from ROOT import gROOT
from ROOT import gStyle
gROOT.SetBatch(True)
import ROOT as r
# import numpy as np
from array import array
# palette = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# gStyle.SetPalette(len(palette), array('i',palette))

ifile = r.TFile(data_path)
tree = ifile.Get('DecayTree')
# tree.Show(1)
hist_005 = r.TH2F('hist_005','True leading photon PT vs Calorimeter detected r = 0.05',100,0,100,100,0,100)
hist_030 = r.TH2F('hist_030','True leading photon vs Calorimeter detected r = 0.30',100,0,100,100,0,100)
hist_050 = r.TH2F('hist_050','True leading photon vs Calorimeter detected r = 0.50',100,0,100,100,0,100)

tree.Draw(f'mu_ISO_NC_005:mu_truth_bare_pt+mu_truth_leading_photon_pt>>hist_005','','COLZ')
tree.Draw(f'mu_ISO_NC_030:mu_truth_bare_pt+mu_truth_leading_photon_pt>>hist_030','','COLZ')
tree.Draw(f'mu_ISO_NC_050:mu_truth_bare_pt+mu_truth_leading_photon_pt>>hist_050','','COLZ')


c1 = r.TCanvas('005 calorimeter')
c1.SetLogz()
hist_005.SetContour(30)
hist_005.Draw('COLZ')
hist_005.SetLineColor(1)
c1.Print('calorimeter_005/calorimeter_bare_photon_005.png')

c2 = r.TCanvas('030 calorimeter')
c2.SetLogz()
hist_030.SetContour(30)
hist_030.Draw('COLZ')
hist_030.SetLineColor(1)
c2.Print('calorimeter_030/calorimeter_bare_photon_030.png')

c3 = r.TCanvas('050 calorimeter')
c3.SetLogz()
hist_050.SetContour(5)
hist_050.Draw('COLZ')
hist_050.SetLineColor(1)
c3.Print('calorimeter_050/calorimeter_bare_photon_050.png')

