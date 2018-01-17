import FWCore.ParameterSet.Config as cms

import sys
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('standard')
options.register('granularity',  '090', VarParsing.multiplicity.singleton, VarParsing.varType.string, "granularity to use for EE")
options.register('input',        None,  VarParsing.multiplicity.singleton, VarParsing.varType.string, "input directory")
if(hasattr(sys, "argv")):
    options.parseArguments()
print options

process = cms.Process("HGCOcc")
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('Configuration.Geometry.GeometryExtended2023HGCalMuonReco_cff')
process.load('Configuration.Geometry.GeometryExtended2023HGCalMuon_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_PostLS1_cff')
process.load('Configuration.EventContent.EventContent_cff')
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'PH2_1K_FB_V6::All', '')
from FastSimulation.Event.ParticleFilter_cfi import *

for i in xrange(0,len(process.XMLIdealGeometryESSource.geomXMLFiles)):
        f=process.XMLIdealGeometryESSource.geomXMLFiles[i]
        if not 'v5/hgcalEE.xml' in f : continue
        print 'Replacing default hgcalEE.xml with different granularity',options.granularity
        f='RecoNtuples/HGCalAnalysis/data/granularity/%s/hgcalEE.xml'%options.granularity
        process.XMLIdealGeometryESSource.geomXMLFiles[i]=f
        print 'New file is',f
        break
print process.XMLIdealGeometryESSource.geomXMLFiles[i]

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )

import os
process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(os.listdir(options.input)),
                            duplicateCheckMode = cms.untracked.string("noDuplicateCheck")
                            )


process.ana = cms.EDAnalyzer("HGCOccupancyAnalyzer",
                             geometrySource   = cms.untracked.vstring('HGCalEESensitive','HGCalHESiliconSensitive',  'HGCalHEScintillatorSensitive'),
                             digiCollections  = cms.untracked.vstring('HGCDigisEE',      'HGCDigisHEfront',          'HGCDigisHEback'              )
                             )
                             
process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("occ_analysis_%s.root"%options.granularity)                                                      
                                   )
process.p = cms.Path(process.ana)
