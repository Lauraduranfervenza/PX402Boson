from ROOT import gROOT
gROOT.SetBatch(True)
import ROOT as r
import numpy as np
from array import array

y = np.linspace(1,5,5)
y2 = np.linspace(1,6,6)
#order: reference, bare, born, herwig, photoss
best_mass_photon = [80405.5, 80614.5, 80946.8, 80614.5, 80616.9]
best_mass_photon_error = [1.62771, 1.35421, 1.53722, 1.3575, 1.35729]
# best_mass_photon_error = [16, 13, 15, 15, 13]
#order: reference, born, herwig with born, herwig, photos with born, photos
best_mass = [80405.5, 80694, 80689.2, 80418.2,  80690, 80425]
best_mass_error = [1.62771, 1.31627, 1.32098, 1.60391, 1.32229, 1.59031]

graph_photon = r.TGraphErrors(5,array('f',best_mass_photon),array('f',y),array('f',best_mass_photon_error))
graph = r.TGraphErrors(6,array('f',best_mass),array('f',y2),array('f',best_mass_error))

c1 = r.TCanvas()
graph_photon.Draw("ALP")
graph_photon.SetLineWidth(-2000)
graph_photon.SetTitle("Comparison Photon")
graph_photon.GetYaxis().SetTitle("Method")
graph_photon.GetXaxis().SetTitle("W mass (MeV)")
c1.SetRightMargin(0.10)
c1.SetLeftMargin(0.10)
c1.SetBottomMargin(0.10)
graph_photon.SetMarkerStyle(21)
graph_photon.SetMarkerColor(4)
c1.Print("comparison_photon.png")

c2 = r.TCanvas()
graph.Draw("ALP")
graph.SetLineWidth(-2000)
graph.SetTitle("Comparison")
graph.GetYaxis().SetTitle("Method")
graph.GetXaxis().SetTitle("W mass (MeV)")
c2.SetRightMargin(0.10)
c2.SetLeftMargin(0.10)
c2.SetBottomMargin(0.10)
graph.SetMarkerStyle(21)
graph.SetMarkerColor(4)
c2.Print("comparison.png")
#look at errors should be ~12