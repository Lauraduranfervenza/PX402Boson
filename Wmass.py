data_path = "/storage/epp2/phshgg/Public/DVTuples__v24e/13TeV_2016_28r1_Down_W_Sim09h.root"

#WpIso is w plus isolated
#!usr/bin/gnu python

import ROOT as r
import math as m

ifile = r.TFile(data_path)
ifile.ls()
hist_PT = r.TH1F('hist','mu PT',100,0,100)
hist_mass = r.TH1F('hist','W mass',100,0,100)

tree = ifile.Get('WpIso/DecayTree')
tree.Show(0)

i=0
arrayPT = []
arrayMass = []
#use event loop

def RBW(E, M, w):
    gamma = r.sqrt(M*M*(M*M+w*w))
    k = (2*r.sqrt(2)*M*w*gamma)/(m.pi*r.sqrt(M*M+gamma))
    f = k/((E*E-M*M)*(E*E-M*M)+M*M*w*w)
    return f

for i, entry in enumerate(tree):
    mass = entry.mu_MC_BOSON_M/1000
    hist_mass.Fill(mass)
    arrayMass.append(mass)

    PT = entry.mu_PT/1000
    w = RBW(PT,81,0.25)/RBW(PT,80,0.25)
    
    hist_PT.Fill(PT, w)
    arrayPT.append(PT)
    if i > 100:break
#with open('mass_test.txt', 'w') as f:
#        print(array[j]/n, file=f)

c = r.TCanvas('muPT')
hist_PT.Draw()
c.Print('muPT.png')

c2 = r.TCanvas('Wmass')
hist_mass.Draw()
c2.Print('mumass.png')


hist.Scale(1./hist.Integral())
#for i, entry in enumerate(tree):
#relativistic breit-wigner function
#expected around 81GeV
#plot muon PT and change mass

#Fill(x, weight)
#weigth = RBW(x, 83.0, 2.2)/RBW(x, 81, 2.2 ) need to see true values of width of W