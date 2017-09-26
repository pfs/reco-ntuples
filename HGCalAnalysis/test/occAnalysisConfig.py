import FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras

process = cms.Process("HGCOcc")
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
#process.load('Configuration.Geometry.GeometryExtended2023D17Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2023D13Reco_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.EventContent.EventContent_cff')
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('RecoLocalCalo.HGCalRecProducers.HGCalLocalRecoSequence_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic', '')
from FastSimulation.Event.ParticleFilter_cfi import *
from RecoLocalCalo.HGCalRecProducers.HGCalRecHit_cfi import dEdX_weights as dEdX

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring(
        '/store/relval/CMSSW_9_1_0_pre3/RelValDoubleMuPt15Eta17_27/GEN-SIM-RECO/91X_upgrade2023_realistic_v1_D13noSmearPU200-v1/10000/1CFC2232-0036-E711-B417-0025905B85DA.root'
        #'/store/relval/CMSSW_9_1_0_pre3/RelValDoubleMuPt15Eta17_27/GEN-SIM-RECO/91X_upgrade2023_realistic_v1_D13noSmearPU140-v1/10000/1418DDB5-FE35-E711-B4B8-0025905A60B6.root'
        #'/store/relval/CMSSW_9_1_0_pre3/RelValDoubleMuPt15Eta17_27/GEN-SIM-RECO/91X_upgrade2023_realistic_v1_D13noSmear-v1/10000/1E2EA7BF-B035-E711-BD66-0025905A60B8.root'
    ),
    duplicateCheckMode = cms.untracked.string("noDuplicateCheck")
)

process.ana = cms.EDAnalyzer("HGCOccupancyAnalyzer")
                             
process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("occ_analysis_pu200.root")
                                   #fileName = cms.string("occ_analysis_pu140.root")
                                   #fileName = cms.string("occ_analysis_pu0.root")                                                      
                                   )
process.p = cms.Path(process.ana)
