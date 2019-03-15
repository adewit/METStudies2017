import os

from efficiency_analyzer import EfficiencyAnalyzer

cuts = [
    'Vtype == 3 && Electron_pt[0]>35 && nJet >= 2 && Sum$(Jet_Pt > 20 && abs(Jet_eta) < 2.5 && Jet_lepFilter) >= 2 && HLT_Ele32_WPTight_Gsf && abs(TVector2::Phi_mpi_pi(Electron_phi[0] - MET_phi)) < 2.5 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_BadChargedCandidateFilter && Flag_ecalBadCalibFilter',
]

histograms = [
    ('RawMET', 'RawMET_pt', 50, 0, 500),
    ('MET', 'MET_pt', 50, 0, 500),
    ('TkMET', 'TkMET_pt', 50, 0, 500),
    ('PuppiMET', 'PuppiMET_pt', 50, 0, 500),
    ('MHT', 'MHT_pt', 50, 0, 500),
    ('minMETMHT', 'min(MET_pt, MHT_pt)', 50, 0, 500),
    ('Vtype', 'Vtype', 7, -1, 6),
    ('Jet1Pt', 'Jet_Pt[0]', 50, 0, 500),
    ('Jet2Pt', 'Jet_Pt[1]', 50, 0, 500),
    ('Jet1Eta', 'Jet_eta[0]', 100, -5, 5),
    ('Jet2Eta', 'Jet_eta[1]', 100, -5, 5),
    ('Jet1CMVA', 'Jet_btagCMVA[0]', 100, -1, 1),
    ('Jet2CMVA', 'Jet_btagCMVA[1]', 100, -1, 1),
    ('absDeltaPhiJetMET', 'MinIf$(abs(TVector2::Phi_mpi_pi(Jet_phi - MET_phi)), Jet_pt > 30 && Jet_puId > 0)', 32, 0, 3.2),
]

analyzer = EfficiencyAnalyzer()

analyzer.submit(
    name='SingleElectron2018A-nano14dec',
    src='/EGamma/acalandr-Run2018A-Nano14Dec2018-v188-0cddb9e2402d2a936e94a815e9296873/USER',
    dbs_instance='phys03',
    cuts=cuts,
    histograms=histograms,
    commands={
        'x509userproxy': os.environ['X509_USER_PROXY']
    },
    no_submit = False
)
