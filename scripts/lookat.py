#!/usr/bin/env python
# fit chi squared with quadratic and try to extract best fit values and 1 sigma uncertainty.
# try to use other weights and born and bare on data hist in the data file. and compare how much things shift.
data_path = "/storage/epp2/phshgg/Public/MPhysProject_2021_2022/ProcessTuples/Wp_W_13TeV_SmearingOff_AlignCorrOff_MomScaleCorrOff.root"

from ROOT import gROOT
gROOT.SetBatch(True)
import ROOT as r
import numpy as np
from array import array

ifile = r.TFile(data_path)
tree = ifile.Get('DecayTree')

tree.SetMaxEntryLoop(100000) #useful for quick tests

#define any relevant variables
w_boson_width_gev = 2.028     #in GeV from https://arxiv.org/abs/0909.4814
masses = np.linspace(79.,83.,10)
mass_data = 80.4

#create empty histograms from a histogram template
N_bin = 100
hist_template = r.TH1F('hist_template','mu_PT',N_bin,30.0,50.0)
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
    tree.Draw(f'mu_truth_bare_pt>>{hist.GetName()}',f'TMath::BreitWigner(V_TRUE_M,{mass},{w_boson_width_gev})/TMath::BreitWigner(V_TRUE_M,80385.,{w_boson_width_gev})*(Entry$%2==0)','goff')
    
tree.Draw(f'mu_truth_bare_pt>>{data_hist.GetName()}',f'TMath::BreitWigner(V_TRUE_M,{mass_data},{w_boson_width_gev})/TMath::BreitWigner(V_TRUE_M,80385.,{w_boson_width_gev})*(Entry$%2==0)','goff')

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
c.Print('W_mass_QED.png')


# chi2 = [data_hist.Chi2Test(hists[hist_name(i)],'CHI2 WW') for i in range(len(masses))] #to test if chi2 is empty
# print(chi2)


# import sys
# sys.exit()

data = []
templates = {}
chi = []
Wmass = []

#copy the data from the histograms in order to get the chi squared
#need to try if this can be done before data normalisation!!!!!!
for i,mass in enumerate(masses):
    hist = hists[hist_name(i)]
    templates[hist_name(i)] = [hist.GetBinContent(j+1) for j in range(N_bin)]
data = [data_hist.GetBinContent(j+1) for j in range(N_bin)]

#function to calculate the chi square of each template
def chi_squared(data, template):
    chi_sqr = 0
    for i in range(len(data)):
        if data[i] > 0:
            chi_sqr_sum = (data[i]-template[i])*(data[i]-template[i])/(data[i] + template[i])
            chi_sqr = chi_sqr + chi_sqr_sum
    return chi_sqr

#create the array of chi square values in order to plot it
for i,mass in enumerate(masses): #hewed
        template = templates[hist_name(i)]
        chi_result = chi_squared(data, template)
        chi.append(chi_result)
        Wmass.append(mass)

#quadratic fit
# func = r.TF1("quadratic", "[0]*x*x+[1]*x+[2]", 79,83)

def fit_func(x, par):
    return par[0]*x[0]*x[0] + par[1]*x[0] + par[2]

func = r.TF1("quadratic",fit_func,80,82,4)
func.SetParameters(1,0,-5)
# func.SetParameter(0,2)
# func.SetParameter(1,1)
# func.SetParameter(2,-5)

#Graph chi square values
#N_points = len(chi)
graph = r.TGraph(len([i for i in enumerate(masses)]), array('f',Wmass), array('f',chi) )
graph.Fit(func,"","",79,83)

mycanvas = r.TCanvas()
graph.Draw("ALP")
graph.SetTitle("Chi squared without QED")
graph.GetYaxis().SetTitle("Chi squared")
graph.GetXaxis().SetTitle("W mass (MeV)")
mycanvas.SetRightMargin(0.05)
mycanvas.SetLeftMargin(0.05)
mycanvas.SetBottomMargin(0.05)
graph.SetMarkerStyle(8)
mycanvas.Print("chi_QED.png")

print(f'min chi2/ndf =  {min(chi)}/{len(data_hist)-2}')

