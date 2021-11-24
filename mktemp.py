data_path = "/storage/epp2/phshgg/Public/DVTuples__v24e/13TeV_2016_28r1_Down_W_Sim09h.root"

from ROOT import gROOT
gROOT.SetBatch(True)

import ROOT as r
import math as m

ifile = r.TFile(data_path)

hist_template = r.TH1F('hist_template','mu_PT',100,0.0,100.0)

masses = {'original': 81.0,'less': 80.0, 'more': 82.0, 'data':81.0}
color = {'original': r.kBlue, 'less' : r.kGreen, 'more': r.kRed, 'data' : r.kBlack}

hists = {}
original_PT = []
for name, mass in masses.items():
    hists[name] = hist_template.Clone(name)

tree = ifile.Get('WpIso/DecayTree')

w_boson_width_mev = 2.1*1.e3
for mass_name , mass_hypothesis in masses.items():
    mass_hypo_mev = mass_hypothesis*1.e3
    if mass_name != 'data':
        tree.Draw(f'mu_PT*1.e-3>>{mass_name}',f'TMath::BreitWigner(mu_MC_BOSON_M,{mass_hypo_mev},{w_boson_width_mev})/TMath::BreitWigner(mu_MC_BOSON_M,80385.,{w_boson_width_mev})*(Entry$%2==0)','goff')
    else:
        tree.Draw(f'mu_PT*1.e-3>>{mass_name}',f'(Entry$%2!=0)','goff')

c = r.TCanvas('muPT distribution')
for i, mass_name in enumerate(list(masses.keys())):
    if mass_name != 'data':
        hist = hists[mass_name]
        hist.Scale(1./hist.Integral())
        hist.Draw('HIST' if i == 0  else 'HIST SAME')
        hist.SetLineColor(color[mass_name])
c.Print('muPT.png')

#Placeholder to continue coding while I cannot access the results from tree.Draw
data = []
templates = []
for i, entry in enumerate(tree):
    PT = entry.mu_PT*1.e-3
    if i%2==0:
        data.append(PT)
    else:
        data.append(PT*0.8)

#function to get chi squared        
def chi_squared(data, template):
    for i in range(len(data)):
       chi_sqr_sum = (data[i]-template[i])/data[i]
       chi_sqr = chi_sqr + chi_sqr_sum
    return chi_sqr

#an idea on how this would go
for mass_name , mass_hypothesis in masses.items():
    mass_hypo_mev = mass_hypothesis * 1e3
    chi[names] = chi_squared(data, templates[mass_name])

#with open('chisquared.txt', 'w') as datafile:
  #  for j in range(len(chi_sqr)):
   #     datafile.write("%s\n" % chi_sqr[j])

