data_path = "/storage/epp2/phshgg/Public/MPhysProject_2021_2022/13TeV__2018__magnet_down_data__Z_candidates.root"
print(data_path)

import ROOT as r
import math as m
input_file = r.TFile(data_path)
input_file.ls()
hist = r.TH1F('hist','',100,0,100.)

tree = input_file.Get('DecayTree')

mass_muon=104 #in MeV

tree.Show(0)

for entry in tree:
    mup_PT = entry.mup_PT
    mup_ETA = entry.mup_ETA
    mup_PHI = entry.mup_PHI

    mup_p = mup_PT*r.cosh(mup_ETA)
    mup_theta = 2*m.atan(m.e**(-mup_ETA))
    mup_pz = mup_p*r.cos(mup_theta)
    mup_px =mup_PT*r.cos(mup_PHI)
    mup_py =mup_PT*r.sin(mup_PHI)

    mum_PT = entry.mum_PT
    mum_ETA = entry.mum_ETA
    mum_PHI = entry.mum_PHI

    mum_p = mum_PT*r.cosh(mum_ETA)
    mum_theta = 2*m.atan(m.e**(-mum_ETA))
    mum_pz = mum_p*r.cos(mum_theta)
    mum_px =mum_PT*r.cos(mum_PHI)
    mum_py =mum_PT*r.sin(mum_PHI)

    mup_E = r.sqrt(mup_p*mup_p + mass_muon*mass_muon)/100
    mum_E = r.sqrt(mum_p*mum_p + mass_muon*mass_muon)/100

    E = mup_E
    px = mup_px + mum_px
    py = mup_py + mum_py
    pz = mup_pz + mum_pz

    mass= r.sqrt(E*E-px*px-py*py-pz*pz)
    hist.Fill(mass)
c = r.TCanvas('')
hist.Draw()
c.Print('zmass.png')
