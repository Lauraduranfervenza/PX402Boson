# And the new columns are (with values from one random event):
# mu_truth_born_pt = 43.2375 //the pt of the signal muon "before" QED FSR
# mu_truth_bare_pt = 43.2375 //the pt of the signal muon “after” QED FSR, i.e. what the detector sees as the charged particle
# mu_truth_bare_eta = 2.03414 // the eta of “” "
# mu_truth_bare_phi = 0.185174 // the phi of “"
# mu_truth_leading_photon_pt = 0 // the pT of the highest pT photon near the muon (if there is one)
# mu_truth_subleading_photon_pt = 0// the pT of the second highest pT photon...
# mu_truth_leading_photon_delta_r = -1 // the DeltaR between the signal muon and the leading photon
# mu_truth_subleading_photon_delta_r = -1//and for the subheading photon

data_path = "/storage/epp2/phshgg/Public/MPhysProject_2021_2022/ProcessTuples/Wp_W_13TeV_SmearingOff_AlignCorrOff_MomScaleCorrOff.root"
# Week 4-5
#imports
from ROOT import gROOT
gROOT.SetBatch(True)
import ROOT as r
import numpy as np
from array import array #this is for the chi square plotting

ifile = r.TFile(data_path)
tree = ifile.Get('DecayTree')

#define any relevant variables
w_boson_width_gev = 2.028     #in GeV from https://arxiv.org/abs/0909.4814

#could try to undo the dictionary
#create masses for template
masses = {'1': 79.5, '2': 79.6, '3': 79.7, '4': 79.8, '5': 79.9,'6': 80.0, '7': 80.1, '8': 80.2, '9': 80.3, '10': 80.4, 'data':80.4}
color = {'1' : 1, '2': 2,'3': 3, '4': 4, '5': 5, '6' : 6, '7': 7,'8': 8, '9': 9, '10': 10, 'data' : 11}
#masses = np.linspace(80.,82.,5)
mass_trial = 80.4

#create empty histograms from a histogram template
N_bin = 100
hist_template = r.TH1F('hist_template','mu_PT',N_bin,30.0,50.0)
hists = {}
for name, mass in masses.items():
    hists[name] = hist_template.Clone(name)

#create templates and data
for mass_name , mass_hypothesis in masses.items():
    #odd entries will be used to create templates and even to create data

    #entry_split doesn't work currently
    #entry_split = f'(Entry$%2{"!=" if mass_name == "data" else "=="}0)'

    if mass_name != 'data':
        tree.Draw(f'mu_truth_bare_pt>>{mass_name}',f'TMath::BreitWigner(V_TRUE_M,{mass_hypothesis},{w_boson_width_gev})/TMath::BreitWigner(V_TRUE_M,80385.,{w_boson_width_gev})*(Entry$%2==0)','goff')

    else:
        tree.Draw(f'mu_truth_bare_pt>>{mass_name}',f'TMath::BreitWigner(V_TRUE_M,{mass_trial},{w_boson_width_gev})/TMath::BreitWigner(V_TRUE_M,80385.,{w_boson_width_gev})*(Entry$%2!=0)','goff')

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
c.Print('W_mass_QED.png')

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
mycanvas.Print("chi_QED.png")

print(f'min chi2/ndf =  {min(chi)}/{len(hists["data"])-2}')