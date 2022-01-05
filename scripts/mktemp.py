data_path = "/storage/epp2/phshgg/Public/DVTuples__v24e/13TeV_2016_28r1_Down_W_Sim09h.root"

#imports
from ROOT import gROOT
gROOT.SetBatch(True)

import ROOT as r
import math as m
import matplotlib.pyplot as plt
import numpy as np

ifile = r.TFile(data_path)
tree = ifile.Get('WpIso/DecayTree')


masses = {'less': 79.0, 'original': 81.0, 'more': 82.0, 'data':81.0}
color = {'less' : r.kGreen, 'original': r.kBlue,  'more': r.kRed, 'data' : r.kBlack}
#masses = np.linspace(80.,82.,5)
trial_mass = 81

#create empty histograms
N_bin = 100
hist_template = r.TH1F('hist_template','mu_PT',N_bin,0.0,100.0)
hists = {}
for name, mass in masses.items():
    hists[name] = hist_template.Clone(name)

w_boson_width_mev = 2.1*1.e3
for mass_name , mass_hypothesis in masses.items():
    mass_hypo_mev = mass_hypothesis*1.e3
    entry_split = f'(Entry$%2{"!=" if mass_name == "data" else "=="}0)'# if mass_name == 'data' else
    #if mass_name != 'data':
    tree.Draw(f'mu_PT*1.e-3>>{mass_name}',f'TMath::BreitWigner(mu_MC_BOSON_M,{mass_hypo_mev},{w_boson_width_mev})/TMath::BreitWigner(mu_MC_BOSON_M,80385.,{w_boson_width_mev})*{entry_split}','goff')
    #else:
    #tree.Draw(f'mu_PT*1.e-3>>{mass_name}',f'(Entry$%2!=0)','goff')

for k in [x for x in masses.keys() if not x == 'data']:
    hists[k].Scale(hists['data'].Integral()/hists[k].Integral())

c = r.TCanvas('muPT distribution')
for i, mass_name in enumerate(list(masses.keys())):
    if mass_name != 'data':
        hist = hists[mass_name]
        #hist.Scale(1./hist.Integral())
        hist.Draw('HIST' if i == 0  else 'HIST SAME')
        hist.SetLineColor(color[mass_name])
hists['data'].Draw('same e1')
c.BuildLegend()
c.Print('muPT.png')

data = []
templates = {}
chi = []
Wmass = []

for mass_name in list(masses.keys()):
    hist = hists[mass_name]
    if mass_name == 'data':
        data = [hist.GetBinContent(j+1) for j in range(N_bin)]
    else:
        templates[mass_name] = [hist.GetBinContent(j+1) for j in range(N_bin)]

def chi_squared(data, template):
    chi_sqr = 0
    for i in range(len(data)):
        if data[i] > 0:
            chi_sqr_sum = (data[i]-template[i])*(data[i]-template[i])/(data[i] + template[i])
            chi_sqr = chi_sqr + chi_sqr_sum
    return chi_sqr


for mass_name , mass_hypothesis in masses.items():
    mass_hypo_mev = mass_hypothesis*1.e3
    if mass_name != 'data':
        template = templates[mass_name]
        chi_result = chi_squared(data, template)
        chi.append(chi_result)
        Wmass.append(mass_hypo_mev)

N_points = 3
#graph = r.TGraph(N_points, Wmass, chi, nullptr)
from array import array
graph = r.TGraph(len([k for k in masses.keys() if not k == 'data']), array('f',Wmass), array('f',chi) )


mycanvas = r.TCanvas()
graph.Draw("ALP")
graph.SetMarkerStyle(8)
mycanvas.Print("chi_graph.png")

print(f'min chi2/ndf =  {min(chi)}/{len(hists["data"])-2}')

# plt.scatter(Wmass, chi)
# plt.ylabel('chi squared')
# plt.xlabel('Mw')
# plt.savefig('chi_plot.png', dpi=300)



# with open('chisquared.txt', 'w') as datafile:
#    for j in range(len(templates)):
#        datafile.write("%s\n" % template[j])