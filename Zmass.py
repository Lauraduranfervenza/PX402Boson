 data_path = "/storage/epp2/phshgg/Public/MPhysProject_2021_2022/13TeV__2018__magnet_down_data__Z_candidates.root"
print(data_path)

import ROOT as r
import math as m
input_file = r.TFile(data_path)
input_file.ls()
histp = r.TH1F('hist','',100,0.,100.)

tree = input_file.Get('DecayTree')

mass_muon=104 #in MeV

tree.Show(0)

for entry in tree:
    mup_PT = entry.mup_PT
    mup_ETA = entry.mup_ETA
    mup_PHI = entry.mup_PHI

    mup_p = mup_PT*r.cosh(mup_ETA)
    mup_theta = 2*m.atan(m.e**(-mup_ETA))
    mup_pz = p*r.cos(mup_theta)
    mup_px =mup_PT*r.cos(mup_PHI)
    mup_py =mup_PT*r.sin(mup_PHI)

    mup_E = r.sqrt(mup_p*mup_p + mass_muon*mass_muon)
    mup_mass= mup_E*mup_E-mup_px*mup_px-mup_py*mup_py-mup_pz*mup_pz
    histp.Fill(mup_mass)
c = r.TCanvas('wmass')
c.cd()
histp.Draw()
c.Print('wmass.png')

