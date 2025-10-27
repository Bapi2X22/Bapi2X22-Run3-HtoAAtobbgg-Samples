import os

base_template = """import FWCore.ParameterSet.Config as cms

externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    nEvents = cms.untracked.uint32(5000),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh'),
    numberOfParameters = cms.uint32(1),
    args = cms.vstring('{gridpack_path}')
)

import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunesRun3ECM13p6TeV.PythiaCP5Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *

generator = cms.EDFilter("Pythia8HadronizerFilter",
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13600.),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        pythia8PSweightsSettingsBlock,
        processParameters = cms.vstring(
            'JetMatching:setMad = off',
            'JetMatching:scheme = 1',
            'JetMatching:merge = on',
            'JetMatching:jetAlgorithm = 2',
            'JetMatching:etaJetMax = 5.',
            'JetMatching:coneRadius = 1.',
            'JetMatching:slowJetPower = 1',
            'JetMatching:qCut = 45.',
            'JetMatching:nQmatch = 4',
            'JetMatching:nJetMax = 1',
            'JetMatching:doShowerKt = off'
        ),
        parameterSets = cms.vstring(
            'pythia8CommonSettings',
            'pythia8CP5Settings',
            'pythia8PSweightsSettings',
            'processParameters'
        )
    )
)

ProductionFilterSequence = cms.Sequence(generator)
"""

masses = [12, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]
base_path = "/eos/user/b/bbapi/genproductions/bin/MadGraph5_aMCatNLO/GridPacks/gridpack_hToaaTo2gamma2b"

for m in masses:
    gridpack = f"{base_path}/hToaaTo2gamma2b_ma{m}GeV_MLM_4f_max1j_el9_amd64_gcc11_CMSSW_13_2_9_tarball.tar.xz"
    fragment_name = f"hToaaTo2gamma2b_ma{m}GeV_TuneCP5_PSweights_13p6TeV-madgraphMLM-pythia8-fragment.py"
    with open(fragment_name, "w") as f:
        f.write(base_template.format(gridpack_path=gridpack))
    print(f"Created {fragment_name}")

