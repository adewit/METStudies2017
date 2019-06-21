import ROOT
import math
import os
import numpy as np
from scipy.stats import norm

def doubleGauss(x, par):
    x      = x[0]
    mu1    = par[0]
    sigma1 = par[1]
    scale1 = par[2]
    mu2    = par[3]
    sigma2 = par[4]
    scale2 = par[5]
    return _doubleGauss(x, mu1, sigma1, scale1, mu2, sigma2, scale2)


def doubleGaussSameMean(x, par):
    x      = x[0]
    mu     = par[0]
    sigma1 = par[1]
    scale1 = par[2]
    sigma2 = par[3]
    scale2 = par[4]
    return _doubleGauss(x, mu, sigma1, scale1, mu, sigma2, scale2)


def crystalball(x, par):
    x     = x[0]
    alpha = par[0]
    n     = par[1]
    mu    = par[2]
    sigma = par[3]
    scale = par[4]
    return _crystalball(x, alpha, n, mu, sigma, scale)


def doubleSidedCrystalball(x, par):
    x      = x[0]
    mu     = par[0] # common gaussian core
    sigma  = par[1] # common gaussian core

    alpha1 = par[2]
    n1     = par[3]
    scale1 = par[4]
    alpha2 = par[5]
    n2     = par[6]
    
    # impose continuity by joining the two halves at the gauss peak. 
    # Derivability comes for free. Thanks Karl Friedrich!
    scale2 = _crystalball(mu, alpha1, n1, mu, sigma, scale1) / _crystalball(mu, alpha2, n2, mu, sigma, 1.)

    if x > mu:
        if alpha1 < 0:
            return _crystalball(x, alpha1, n1, mu, sigma, scale1)
        elif alpha2 < 0:
            return _crystalball(x, alpha2, n2, mu, sigma, scale2)
        else: 
            raise ValueError('The two alpha paremters must have opposite sign!')
    elif x <= mu:
        if alpha1 > 0:
            return _crystalball(x, alpha1, n1, mu, sigma, scale1)
        elif alpha2 > 0:
            return _crystalball(x, alpha2, n2, mu, sigma, scale2)
        else: 
            raise ValueError('The two alpha paremters must have opposite sign!')


def crystalballEfficiency(x, par):
    x     = x[0]
    m0    = par[0]
    sigma = par[1]
    alpha = par[2]
    n     = par[3]
    norm  = par[4]
    return _crystalballEfficiency( x, m0, sigma, alpha, n, norm )


def doubleCrystalballErrfEfficiency(x, par):
    x     = x[0]
    m0_1    = par[0]
    sigma_1 = par[1]
    alpha_1 = par[2]
    n_1     = par[3]
    norm_1  = par[4]
    m0_2    = par[5]
    sigma_2 = par[6]
    alpha_2 = par[7]
    n_2     = par[8]
    norm_2  = par[9]
    return _crystalballEfficiency( x, m0_1, sigma_1, alpha_1, n_1, norm_1 ) + \
           _crystalballEfficiency( x, m0_2, sigma_2, alpha_2, n_2, norm_2 )


def crystalballEfficiencyWithRelaxation(x, par):
    '''
    Convolution of a CrystalBall resolution function with a step function
    plus the addition of a linear relaxation term
    '''
    x      = x[0]
    m0     = par[0]
    sigma  = par[1]
    alpha  = par[2]
    n      = par[3]
    norm   = par[4]
    relax  = par[5]
    slope  = par[6]
    floating_norm = norm * (1. + slope * max(0., x - relax))
    return _crystalballEfficiency( x, m0, sigma, alpha, n, floating_norm )


def _doubleGauss(x, mu1, sigma1, scale1, mu2, sigma2, scale2):
    
    gaus1 = scale1 * norm(mu1, sigma1).pdf(x)
    gaus2 = scale2 * norm(mu2, sigma2).pdf(x)

    return gaus1 + gaus2


def _crystalballPositiveAlpha( x, alpha, n, mu, sigma):
    '''
    https://en.wikipedia.org/wiki/Crystal_Ball_function
    ''' 
    
    expArg = -0.5 * ROOT.TMath.Power(abs(alpha), 2.)
    gauss  = ROOT.TMath.Exp(expArg)
        
    A = ROOT.TMath.Power( (n/abs(alpha)), n) * gauss
    B = n / abs(alpha) - abs(alpha)
    C = n / (abs(alpha) * (n - 1.)) * gauss
    D = math.sqrt(math.pi/2.) * (1. + ROOT.TMath.Erf(abs(alpha)/math.sqrt(2.))) 
    N = 1. / (sigma * (C + D))

    pull = (x - mu)/sigma 
        
    if pull > -alpha:
        func = N * ROOT.TMath.Gaus(x, mu, sigma)
    else:
        func = N * A * ROOT.TMath.Power( (B - pull), -n )

    return func


def _crystalball( x, alpha, n, mu, sigma, scale ):
    
    if alpha > 0.:
        return scale * _crystalballPositiveAlpha( x, alpha, n, mu, sigma ) 
    else:
        x1     = 2 * mu - x
        alpha1 = -alpha
        return scale * _crystalballPositiveAlpha( x1, alpha1, n, mu, sigma ) 


def _crystalballEfficiency(m, m0, sigma, alpha, n, norm):
  
    sqrtPiOver2 = math.sqrt(ROOT.TMath.PiOver2())
    sqrt2       = math.sqrt(2.)
    sig         = abs(sigma)
    t           = (m - m0)/sig * alpha / abs(alpha)
    absAlpha    = abs(alpha/sig)
    a           = ROOT.TMath.Power(n/absAlpha, n) * ROOT.TMath.Exp(-0.5 * absAlpha * absAlpha)
    b           = absAlpha - n/absAlpha
    arg         = absAlpha / sqrt2;
  
    if   arg >  5.: ApproxErf =  1.
    elif arg < -5.: ApproxErf = -1.
    else          : ApproxErf = ROOT.TMath.Erf(arg)
  
    leftArea    = (1. + ApproxErf) * sqrtPiOver2
    rightArea   = ( a * 1./ROOT.TMath.Power(absAlpha-b, n-1) ) / (n - 1)
    area        = leftArea + rightArea
  
    if t <= absAlpha:
        arg = t / sqrt2
        if   arg >  5.: ApproxErf =  1.
        elif arg < -5.: ApproxErf = -1.
        else          : ApproxErf = ROOT.TMath.Erf(arg)
        return norm * (1 + ApproxErf) * sqrtPiOver2 / area
  
    else:
        return norm * (leftArea + a * (1/ROOT.TMath.Power(t-b,n-1) - \
                                       1/ROOT.TMath.Power(absAlpha - b,n-1)) / (1 - n)) / area



datafile = ROOT.TFile.Open("DataEfficiencyHistos.root")
mcfile = ROOT.TFile.Open("DataEfficiencyHistosMCincl.root")

teffdata = datafile.Get("teff120")
teffmc = mcfile.Get("teff120")


xbins = [0.,10.,20.,30.,40.,50.,60.,70.,80.,90.,100.,110.,120.,130.,140.,150.,160.,170.,180.,190.,200.,210.,220.,240.,260.,280.,300.,350.,400.,450.,500.]
effdata = ROOT.TH1F("effdata",";min(MET,MHT) [GeV];",len(xbins)-1,np.array(xbins))
effmc = ROOT.TH1F("effmc",";min(MET,MHT) [GeV];",len(xbins)-1,np.array(xbins))

for i in range(1, len(xbins)+1):
  effdata.SetBinContent(i,teffdata.GetEfficiency(i))
  effmc.SetBinContent(i,teffmc.GetEfficiency(i))


effdata.Divide(effmc)

data_eff_func=ROOT.TF1("data_eff_func",crystalballEfficiency,100,500,5)
data_eff_func.SetParameters(161.4,36.26,72.15,3.517,0.9969)
mc_eff_func=ROOT.TF1("mc_eff_func",crystalballEfficiency,100,500,5)
mc_eff_func.SetParameters(149.1,30.35,70.51,6.293,0.9964)

def function_sum(x):
    xx=x[0]
    return data_eff_func.Eval(xx)/mc_eff_func.Eval(xx)


scale_factor=ROOT.TF1("scale_factor",function_sum,100,500)
effdata.SetStats(0)


c1 = ROOT.TCanvas()
effdata.Draw()
scale_factor.Draw("LSAME")
legend = ROOT.TLegend(0.5,0.3,0.9,0.4)
legend.AddEntry(effdata, "Scale factor from binned efficiencies","L")
legend.AddEntry(scale_factor, "Scale factor from fits","L")
legend.Draw("SAME")
c1.SaveAs("BinnedEfficiency.pdf")
