data_path = "/storage/epp2/phshgg/Public/DVTuples__v24e/13TeV_2016_28r1_Down_W_Sim09h.root"

import ROOT as r
import math as m

ifile = r.TFile(data_path)
ifile.ls()
hists = {'original': r.TH1F('hist_original','mu_PT',100,0,100), 'less': r.TH1F('hist_less','mu_PT',100,0,100), 'more': r.TH1F('hist_more','mu_PT',100,0,100)}
color = {'original': r.kBlue, 'less' : r.kGreen, 'more': r.kRed}
c = r.TCanvas('muPT distribution')

tree = ifile.Get('WpIso/DecayTree')
#tree.Show(0)

i=0
j=0

#Relativistic Breit-Weigner function
def RBW(x, M, b):
    gamma = r.sqrt(M*M*(M*M+b*b))
    k = (2*r.sqrt(2)*M*b*gamma)/(m.pi*r.sqrt(M*M+gamma))
    f = k/(((x*x-M*M)*(x*x-M*M)) + M*M*b*b) #use k in numerator maybe
    return f

#masses 
masses = {'original': 81,'less': 80, 'more': 82}
#use for loop for diferent masses

#change loop
for key in masses:
    for i, entry in enumerate(tree):
        PT = entry.mu_PT/1000
        x = entry.mu_MC_BOSON_M/1000
        w = RBW(x,masses[key],2)/RBW(x,81,2)

        #option 1 works fine for now
        bin = hists[key].FindBin(PT)
        hists[key].AddBinContent(bin, w)
        
        #option 2 doesn't work but used to
        #hist_PT.Fill(PT,w)
        
        if i > 100:break

    hists[key].Scale(1./hists[key].Integral())

    #c.Update()
    hists[key].Draw("SAME")
    hists[key].SetLineColor(color[key])
c.Print('muPT.png')





