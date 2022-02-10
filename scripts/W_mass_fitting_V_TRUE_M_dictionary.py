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

#could try to undo the dictionary
#create masses for template
masses = {'3': 80.0, '4': 80.25, '5': 80.5, '6': 80.75, '7': 81,'8': 81.15, '9': 81.25, '10': 81.5, '1': 81.75, '2': 82, 'data':80.0}
color = {'1' : 1, '2': 2,'3': 3, '4': 4, '5': 5, '6' : 6, '7': 7,'8': 8, '9': 9, '10': 10, 'data' : 11}
#masses = np.linspace(80.,82.,5)
trial_mass = 81

#create empty histograms from a histogram template
N_bin = 100
hist_template = r.TH1F('hist_template','mu_PT',N_bin,0.0,100.0)
hists = {}
for name, mass in masses.items():
    hists[name] = hist_template.Clone(name)

#create templates and data
for mass_name , mass_hypothesis in masses.items():
    #odd entries will be used to create templates and even to create data

    #entry_split doesn't work currently
    #entry_split = f'(Entry$%2{"!=" if mass_name == "data" else "=="}0)'

    if mass_name != 'data':
        tree.Draw(f'mu_pt>>{mass_name}',f'TMath::BreitWigner(V_TRUE_M,{mass_hypothesis},{w_boson_width_gev})/TMath::BreitWigner(V_TRUE_M,80385.,{w_boson_width_gev})*(Entry$%2==0)','goff')

    else:
        tree.Draw(f'mu_pt>>{mass_name}',f'(Entry$%2!=0)','goff')

#normalisation as histograms are in diferent scales
for k in [x for x in masses.keys() if not x == 'data']:
    hists[k].Scale(hists['data'].Integral()/hists[k].Integral())
    #MIGHT CHANGE TO 1/BLAH BLAH

#Create graph of the muon PT distribution
c = r.TCanvas('muPT distribution')
for i, mass_name in enumerate(list(masses.keys())):
    if mass_name != 'data':
        hist = hists[mass_name]
        #hist.Scale(1./hist.Integral())
        hist.Draw('HIST' if i == 0  else 'HIST SAME')
        hist.SetLineColor(color[mass_name])
hists['data'].Draw('same e1')
c.BuildLegend() #legend needs to be corrected
c.Print('W_mass_V_TRUE_M.png')

data = []
templates = {}
chi = []
Wmass = []

#copy the data from the histograms in order to get the chi squared
#need to try if this can be done before data normalisation!!!!!!
for mass_name in list(masses.keys()):
    hist = hists[mass_name]
    if mass_name == 'data':
        data = [hist.GetBinContent(j+1) for j in range(N_bin)]
    else:
        templates[mass_name] = [hist.GetBinContent(j+1) for j in range(N_bin)]

#function to calculate the chi square of each template
def chi_squared(data, template):
    chi_sqr = 0
    for i in range(len(data)):
        if data[i] > 0:
            chi_sqr_sum = (data[i]-template[i])*(data[i]-template[i])/(data[i] + template[i])
            chi_sqr = chi_sqr + chi_sqr_sum
    return chi_sqr

#create the array of chi square values in order to plot it
for mass_name , mass_hypothesis in masses.items():
    if mass_name != 'data':
        template = templates[mass_name]
        chi_result = chi_squared(data, template)
        chi.append(chi_result)
        Wmass.append(mass_hypothesis)

#Graph chi square values
#N_points = len(chi)
#graph = r.TGraph(N_points, Wmass, chi, nullptr)
graph = r.TGraph(len([k for k in masses.keys() if not k == 'data']), array('f',Wmass), array('f',chi) )
mycanvas = r.TCanvas()
graph.Draw("ALP")
graph.SetTitle("Chi squared without QED")
graph.GetYaxis().SetTitle("Chi squared")
graph.GetXaxis().SetTitle("W mass (MeV)")
mycanvas.SetRightMargin(0.05)
mycanvas.SetLeftMargin(0.05)
mycanvas.SetBottomMargin(0.05)
graph.SetMarkerStyle(8)
mycanvas.Print("chi_V_TRUE_M.png")

print(f'min chi2/ndf =  {min(chi)}/{len(hists["data"])-2}')