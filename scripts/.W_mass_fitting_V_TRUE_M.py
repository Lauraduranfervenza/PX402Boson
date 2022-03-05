# Week 4-5
# Then use “mu_pt” as your fit variable and “V_TRUE_M” for the Breit-Wigner weights
#imports
from ROOT import gROOT
gROOT.SetBatch(True)
import ROOT as r
import numpy as np
from array import array #this is for the chi square plotting

data_path = "/storage/epp2/phshgg/Public/MPhysProject_2021_2022/Wp_W_13TeV_SmearingOff_AlignCorrOff_MomScaleCorrOff.root"
ifile = r.TFile(data_path)
tree = ifile.Get('DecayTree')

#define any relevant variables
w_boson_width_gev = 2.028     #in GeV from https://arxiv.org/abs/0909.4814

#create masses and histograms
masses = np.linspace(80.,82.,5)
trial_mass = 81
N_bin = 100
hist_template = r.TH1F('hist_template','mu_pt',N_bin,0.0,100.0)
hists = {}
for i in range(len(masses)):
    hists[i] = hist_template.Clone(f'template{i}')  #need to change names
data_hist = hist_template.Clone("data_hist")


#create templates and data
for i in range(len(masses)):
    tree.Draw(f'mu_pt>>{hists[i].GetName()}',f'TMath::BreitWigner(V_TRUE_M,{masses[i]},{w_boson_width_gev})/TMath::BreitWigner(V_TRUE_M,80385.,{w_boson_width_gev})*(Entry$%2==0)','goff')
tree.Draw(f'mu_pt>>{data_hist}',f'(Entry$%2!=0)','goff')


data = []
templates = {}
chi = []
Wmass = []

#copy the data from the histograms in order to get the chi squared
#need to try if this can be done before data normalisation!!!!!!
for i in range(len(masses)):
    hist = hists[i]
    templates[i] = [hist.GetBinContent(k+1) for k in range(N_bin)]
data = [data_hist.GetBinContent(k+1) for k in range(N_bin)]
#try getting rid of +1

# normalisation as histograms are in diferent scales
for i in range(len(masses)):
    hists[i].Scale(1/hists[i].Integral())

# #Create graph of the muon PT distribution
c = r.TCanvas('muPT distribution')
for i in range(len(masses)):
        color = i+1
        hist = hists[i]
        #hist.Scale(1./hist.Integral())
        hist.Draw('HIST' if i == 0  else 'HIST SAME')
        hist.SetLineColor(color)

data_hist.Draw('same e1')
c.BuildLegend() #legend needs to be corrected
c.Print('Wmassfit.png')

with open('empty.txt', 'w') as datafile:
    for j in range(len(data)):
        datafile.write("%s\n" % data[j])

#function to calculate the chi square of each template
def chi_squared(data, template):
    chi_sqr = 0
    for i in range(len(data)):
        if data[i] > 0:
            chi_sqr_sum = (data[i]-template[i])*(data[i]-template[i])/(data[i] + template[i])
            chi_sqr = chi_sqr + chi_sqr_sum
    return chi_sqr

# #create the array of chi square values in order to plot it
for i in range(len(masses)):
        template = templates[i]
        chi_result = chi_squared(data, template)
        chi.append(chi_result)
        Wmass.append(masses[i])

# #Graph chi square values
#N_points = len(chi)
#graph = r.TGraph(N_points, Wmass, chi, nullptr)
graph = r.TGraph(len(masses), array('f',Wmass), array('f',chi) )
# graph = r.TGraph(len([k for k in masses.keys() if not k == 'data']), array('f',Wmass), array('f',chi) )
mycanvas = r.TCanvas()
graph.Draw("ALP")
graph.SetMarkerStyle(8)
mycanvas.Print("chitest.png")

# print(f'min chi2/ndf =  {min(chi)}/{len(hists["data"])-2}')