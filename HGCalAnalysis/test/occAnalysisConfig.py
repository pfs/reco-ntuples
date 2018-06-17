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

import os
tag='DIGI_PU0_0p0'
baseDir='/eos/cms/store/cmst3/user/psilva/HGCal/H125gg_EE/CMSSW_9_3_2/%s'%tag
fList = ['file:'+os.path.join(baseDir,f) for f in os.listdir(baseDir)]

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(fList),
    duplicateCheckMode = cms.untracked.string("noDuplicateCheck")
)

process.ana = cms.EDAnalyzer("HGCOccupancyAnalyzer")
                             
process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("occ_analysis_%s.root"%tag)
                                   )
process.p = cms.Path(process.ana)
