data_path = "/storage/epp2/phshgg/Public/DVTuples__v24e/13TeV_2016_28r1_Down_W_Sim09h.root"

import ROOT as r
import math as m

ifile = r.TFile(data_path)
ifile.ls()
hist_PT = r.TH1F('hist','mu PT',100,0,100)

tree = ifile.Get('WpIso/DecayTree')
#tree.Show(0)

i=0
j=0
array_PT = []
array_w = []

#Relativistic Breit-Weigner function
def RBW(E, M, w):
    gamma = r.sqrt(M*M*(M*M+w*w))
    k = (2*r.sqrt(2)*M*w*gamma)/(m.pi*r.sqrt(M*M+gamma))
    f = k/((E*E-M*M)*(E*E-M*M)+M*M*w*w)
    return f

new_Mass = 80

#use event loop
for i, entry in enumerate(tree):
    PT = entry.mu_PT/1000
    w = RBW(PT,81,2.1)/RBW(PT,new_Mass,2.1)
    
    array_PT.append(PT)
    array_w.append(w)

    hist_PT.Fill(w)
    
    if i > 100:break

with open('weights.txt', 'w') as datafile:
    for j in range(len(array_w)):
        datafile.write("%s\n" % array_w[j])

datafile.close()

c = r.TCanvas('muPT')
hist_PT.Draw()
c.Print('muPT.png')


hist_PT.Scale(1./hist_PT.Integral())