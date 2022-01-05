data_path = "/storage/epp2/phshgg/Public/DVTuples__v24e/13TeV_2016_28r1_Down_W_Sim09h.root"

import ROOT as r
import math as m

ifile = r.TFile(data_path)
ifile.ls()
hist_PT = r.TH1F('hist_PT','mu_PT',100,0,100)
hist_PT2 = r.TH1F('hist2','mu_PT',100,0,100)

tree = ifile.Get('WpIso/DecayTree')
#tree.Show(0)

i=0
j=0
array_w = []

#Relativistic Breit-Weigner function
def RBW(x, M, b):
    gamma = r.sqrt(M*M*(M*M+b*b))
    k = (2*r.sqrt(2)*M*b*gamma)/(m.pi*r.sqrt(M*M+gamma))
    f = k/(((x*x-M*M)*(x*x-M*M)) + M*M*b*b) #use k in numerator maybe
    return f

#ask for mases 
#make a dictionary of histograms
new_Mass = 80
new_Mass2 = 82
#use for loop for diferent masses

#use event loop
for i, entry in enumerate(tree):
    PT = entry.mu_PT/1000
    x = entry.mu_MC_BOSON_M/1000
    w = RBW(x,new_Mass,2)/RBW(x,81,2)
    w2 = RBW(x,new_Mass2,2)/RBW(x,81,2)

    array_w.append(w)

    #option 1 works fine for now
    bin = hist_PT.FindBin(PT)
    hist_PT.AddBinContent(bin, w)

    bin = hist_PT.FindBin(PT)
    hist_PT2.AddBinContent(bin, w2)
    
    #option 2 doesn't work but used to
    #hist_PT.Fill(PT,w)
    #hist_PT2.Fill(PT,w2)
    
    if i > 10000:break

with open('weights.txt', 'w') as datafile:
    for j in range(len(array_w)):
        datafile.write("%s\n" % array_w[j])

datafile.close()

hist_PT.Scale(1./hist_PT.Integral())
hist_PT2.Scale(1./hist_PT2.Integral())

c = r.TCanvas('muPT distribution')
c.Update()
hist_PT.Draw()
hist_PT2.SetLineColor(r.kRed)
hist_PT2.Draw("SAME")
c.Print('pngexample.png')





