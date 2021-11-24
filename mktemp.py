data_path = "/storage/epp2/phshgg/Public/DVTuples__v24e/13TeV_2016_28r1_Down_W_Sim09h.root"

from ROOT import gROOT
gROOT.SetBatch(True)

import ROOT as r
import math as m

ifile = r.TFile(data_path)

hist_template = r.TH1F('hist_template','mu_PT',100,0.0,100.0)

masses = {'original': 81.0,'less': 80.0, 'more': 82.0}
color = {'original': r.kBlue, 'less' : r.kGreen, 'more': r.kRed}

hists = {}
for name, mass in masses.items():
    hists[name] = hist_template.Clone(name)

tree = ifile.Get('WpIso/DecayTree')

w_boson_width_mev = 2.1*1.e3
for mass_name , mass_hypothesis in masses.items():
    mass_hypo_mev = mass_hypothesis*1.e3
    tree.Draw(f'mu_PT*1.e-3>>{mass_name}',f'TMath::BreitWigner(mu_MC_BOSON_M,{mass_hypo_mev},{w_boson_width_mev})/TMath::BreitWigner(mu_MC_BOSON_M,80385.,{w_boson_width_mev})*(Entry$%2==0)','goff')
#can use the weigth 2nd argument to also get half the data and do a cut, weight*boolean function
#boolean Entry$%2==0
c = r.TCanvas('muPT distribution')
for i, mass_name in enumerate(list(masses.keys())):
    hist = hists[mass_name]
    hist.Scale(1./hist.Integral())
    hist.Draw('HIST' if i == 0 else 'HIST SAME')
    hist.SetLineColor(color[mass_name])
c.Print('muPT.png')