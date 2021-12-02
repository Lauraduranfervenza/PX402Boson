data_path = "/storage/epp2/phshgg/Public/DVTuples__v24e/13TeV_2016_28r1_Down_W_Sim09h.root"

from ROOT import gROOT
gROOT.SetBatch(True)

import ROOT as r
import math as m
import matplotlib.pyplot as plt

ifile = r.TFile(data_path)
  
def chi_squared(data, template):
    chi_sqr = 0
    for i in range(len(data)):
        if data >=0:
            chi_sqr_sum = (data[i]-template[i])*(data[i]-template[i])/data[i]
            chi_sqr = chi_sqr + chi_sqr_sum
    return chi_sqr

hist_template = r.TH1F('hist_template','mu_PT',100,0.0,100.0)

masses = {'original': 81.0,'less': 80.0, 'more': 82.0, 'data':81.0}
color = {'original': r.kBlue, 'less' : r.kGreen, 'more': r.kRed, 'data' : r.kBlack}

hists = {}

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

data = []
templates = {}
chi = []
Wmass = []

for i, mass_name in enumerate(list(masses.keys())):
    hist = hists[mass_name]
    if mass_name == 'data':
        data = [hist.GetBinContent(j+1) for j in range(100)]
    else:
        templates[mass_name] = [hist.GetBinContent(j+1) for j in range(100)]

for mass_name , mass_hypothesis in masses.items():
    mass_hypo_mev = mass_hypothesis*1.e3
    if mass_name != 'data':
        template = templates[mass_name]
        chi_result = chi_squared(data, template)
        chi.append(chi_result)
        Wmass.append(mass_hypo_mev)

p = 3
graph = r.TGraph(p, Wmass, chi, nullptr)

mycanvas = r.TCanvas()
graph.DrawClone("chi")
mycanvas.Print("chi_graph.png")

# plt.scatter(Wmass, chi)
# plt.ylabel('chi squared')
# plt.xlabel('Mw')
# plt.savefig('chi_plot.png', dpi=300)



# with open('chisquared.txt', 'w') as datafile:
#    for j in range(len(templates)):
#        datafile.write("%s\n" % template[j])

