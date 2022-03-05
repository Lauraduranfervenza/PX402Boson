#!/usr/bin/env python

#This file is the reference it uses bare muon for both the models and data
data_path = "/storage/epp2/phshgg/Public/MPhysProject_2021_2022/ProcessTuples/Wp_W_13TeV_SmearingOff_AlignCorrOff_MomScaleCorrOff.root"

from ROOT import gROOT
gROOT.SetBatch(True)
import ROOT as r
import numpy as np
from array import array

ifile = r.TFile(data_path)
tree = ifile.Get('DecayTree')

# tree.SetMaxEntryLoop(100000) #useful for quick tests
#define any relevant variables
w_boson_width_mev = 2028     #in MeV from https://arxiv.org/abs/0909.4814
masses = np.linspace(79000.,82000.,10)
mass_data = 80385

#create empty histograms from a histogram template
N_bin = 100
hist_template = r.TH1F('hist_template','Muon PT',N_bin,30.0,50.0)
data_hist = r.TH1F('hist_template','Data',N_bin,30.0,50.0)

#this gives all histograms different names
def hist_name(i): return f'template{i}'

hists = {}
for i,mass in enumerate(masses):
    name = 'template'+str(i)
    hist = hist_template.Clone(name)
    hists[hist_name(i)] = hist

#create templates and data
for i,mass in enumerate(masses):
    hist = hists[hist_name(i)]
    tree.Draw(f'mu_truth_bare_pt>>{hist.GetName()}',f'TMath::BreitWigner(V_TRUE_M*1e3,{mass},{w_boson_width_mev})/TMath::BreitWigner(V_TRUE_M*1e3,80385.,{w_boson_width_mev})*(Entry$%2!=0)','goff')
    
tree.Draw(f'mu_truth_born_pt>>{data_hist.GetName()}',f'TMath::BreitWigner(V_TRUE_M*1e3,{mass_data},{w_boson_width_mev})/TMath::BreitWigner(V_TRUE_M*1e3,80385.,{w_boson_width_mev})*(Entry$%2==0)','goff')

#normalisation as histograms are in diferent scales
for i,mass in enumerate(masses):
    hist = hists[hist_name(i)]
    hist.Scale(data_hist.Integral()/hist.Integral())

#Create graph of the muon PT distribution
c = r.TCanvas('muPT distribution')
for i, mass in enumerate(masses): 
    hist = hists[hist_name(i)]
    hist.Draw('HIST' if i == 0  else 'HIST SAME')
    hist.SetLineColor(i+1)
data_hist.Draw('same e1')
c.BuildLegend() #legend needs to be corrected
c.Print('born_models.png')

# chi2 = [data_hist.Chi2Test(hists[hist_name(i)],'CHI2 WW') for i in range(len(masses))] #to test if chi2 is empty
# print(chi2)

# import sys
# sys.exit()

data = []
templates = {}
chi = []
mass_chi = []

for i,mass in enumerate(masses):
    hist = hists[hist_name(i)]
    templates[hist_name(i)] = [hist.GetBinContent(j+1) for j in range(N_bin)]
data = [data_hist.GetBinContent(j+1) for j in range(N_bin)]

#function to calculate the chi square of each template
def chi_squared(data, template):
    chi_sqr = 0
    for i in range(len(data)):
        if data[i] > 0 and template[i] > 0:
            chi_sqr_sum = (data[i]-template[i])*(data[i]-template[i])/(template[i] + data[i])
            chi_sqr = chi_sqr + chi_sqr_sum
    return chi_sqr

#create the array of chi square values in order to plot it
for i,mass in enumerate(masses): #hewed
        template = templates[hist_name(i)]
        chi_result = chi_squared(data, template)
        chi.append(chi_result)
        mass_chi.append(mass)

#quadratic fit

def best_Mw(masses, chi):
    for i in range(len(mass_chi)):
        if chi[i]==min(chi):
            return mass_chi[i]

parabola = r.TF1("parabola", "[0] + TMath::Power((x-[1])/[2],2)", 79000, 82000)
# parabola = r.TF1("parabola", "[0] + [1]*x*x+[2]*x", 79,82)
parabola.SetParameter( 0, min(chi))
parabola.SetParameter( 1, best_Mw(masses, chi))
# parabola.SetParameter( 1, 85)
parabola.SetParameter( 2, 20) #in units of MeV !


graph = r.TGraph(len([i for i in enumerate(masses)]), array('f',mass_chi), array('f',chi) )
graph.Fit(parabola,"","",79000,82000)

mycanvas = r.TCanvas()
graph.Draw("ALP")
graph.SetTitle("Chi squared without QED")
graph.GetYaxis().SetTitle("Chi squared")
graph.GetXaxis().SetTitle("W mass (MeV)")
mycanvas.SetRightMargin(0.05)
mycanvas.SetLeftMargin(0.05)
mycanvas.SetBottomMargin(0.05)
graph.SetMarkerStyle(8)
mycanvas.Print("born_chi.png")

parameters = [parabola.GetParameter(0), parabola.GetParameter(1), parabola.GetParameter(2)]
print(parameters)
print(f'min chi2/ndf =  {min(chi)}/{len(data_hist)-2}')