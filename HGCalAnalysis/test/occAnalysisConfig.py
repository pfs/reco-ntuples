import FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras

process = cms.Process("HGCOcc")
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('Configuration.Geometry.GeometryExtended2023D17Reco_cff')
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
    fileNames = cms.untracked.vstring(
        '/store/relval/CMSSW_9_3_0_pre4/RelValSingleMuPt100Extended/GEN-SIM-RECO/93X_upgrade2023_realistic_v0_2023D17noPU-v1/00000/782F3F08-D787-E711-8377-0CC47A7C357A.root'
        #'/store/relval/CMSSW_9_3_0_pre4/RelValSingleMuPt100Extended/GEN-SIM-RECO/PU25ns_93X_upgrade2023_realistic_v0_D17PU200-v1/00000/F29815C1-9E89-E711-849C-0242AC130002.root'
    ),
    duplicateCheckMode = cms.untracked.string("noDuplicateCheck")
)

process.ana = cms.EDAnalyzer("HGCOccupancyAnalyzer")
                             
process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("occ_analysis_pu0.root")                                                      
                                   #fileName = cms.string("occ_analysis_pu200.root")
                                   )
process.p = cms.Path(process.ana)
