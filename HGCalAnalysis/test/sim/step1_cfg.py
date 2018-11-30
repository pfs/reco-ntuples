# Auto generated configuration file
# using: 
# Revision: 1.20 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: FourMuPt_1_200_cfi --conditions PH2_1K_FB_V6::All -n 10 --eventcontent FEVTDEBUG --relval 10000,100 -s GEN,SIM --datatier GEN-SIM --beamspot HLLHC --customise SLHCUpgradeSimulations/Configuration/combinedCustoms.cust_2023HGCalMuon --geometry Extended2023HGCalMuon,Extended2023HGCalMuonReco --magField 38T_PostLS1 --fileout file:step1.root
import FWCore.ParameterSet.Config as cms

import sys
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('standard')
options.register('granularity',  '090', VarParsing.multiplicity.singleton, VarParsing.varType.string, "granularity to use for EE")
options.register('pileup',       140,   VarParsing.multiplicity.singleton, VarParsing.varType.int, "pileup")
if(hasattr(sys, "argv")):
    options.parseArguments()
print options

process = cms.Process('SIM')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.Geometry.GeometryExtended2023HGCalMuonReco_cff')
process.load('Configuration.Geometry.GeometryExtended2023HGCalMuon_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_PostLS1_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedHLLHC_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.SimIdeal_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

import os
#cmssw_base=os.environ.get('CMSSW_BASE')                                                                                                                                                                    
for i in xrange(0,len(process.XMLIdealGeometryESSource.geomXMLFiles)):
        f=process.XMLIdealGeometryESSource.geomXMLFiles[i]
        if not 'v5/hgcalEE.xml' in f : continue
        print 'Replacing default hgcalEE.xml with different granularity',options.granularity
        #f=os.path.join(cmssw_base,'src','hgcalEE_%s.xml'%options.granularity)
        f='RecoNtuples/HGCalAnalysis/data/granularity/%s/hgcalEE.xml'%options.granularity
        process.XMLIdealGeometryESSource.geomXMLFiles[i]=f
        print 'New file is',f
        break
print process.XMLIdealGeometryESSource.geomXMLFiles[i]

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents)
)

# Input source
process.source = cms.Source("EmptySource")

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.20 $'),
    annotation = cms.untracked.string('FourMuPt_1_200_cfi nevts:10'),
    name = cms.untracked.string('Applications')
)

# Output definition

process.FEVTDEBUGoutput = cms.OutputModule("PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    outputCommands = process.FEVTDEBUGEventContent.outputCommands,
    fileName = cms.untracked.string('file:step1.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('GEN-SIM')
    ),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('generation_step')
    )
)

# Additional output definition

# Other statements
process.genstepfilter.triggerConditions=cms.vstring("generation_step")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'PH2_1K_FB_V6::All', '')

process.generator = cms.EDProducer("FlatRandomPtGunProducer",
                                   PGunParameters = cms.PSet(MaxPt = cms.double(20.1),
                                                             MinPt = cms.double(19.9),
                                                             PartID = cms.vint32(-13),
                                                             MaxEta = cms.double(3.0),
                                                             MinEta = cms.double(1.4),
                                                             MaxPhi = cms.double(3.14159265359),
                                                             MinPhi = cms.double(-3.14159265359)
                                                             ),
                                   Verbosity = cms.untracked.int32(0),
                                   psethack = cms.string('Four mu pt 1 to 200'),
                                   firstRun = cms.untracked.uint32(1),
                                   AddAntiParticle=cms.bool(False)
                                   )

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)

#set random seeds for this job                                                                                                                                                                             
from IOMC.RandomEngine.RandomServiceHelper import RandomNumberServiceHelper
randSvc = RandomNumberServiceHelper(process.RandomNumberGeneratorService)
randSvc.populate()

# Path and EndPath definitions
process.generation_step = cms.Path(process.pgen)
process.simulation_step = cms.Path(process.psim)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.FEVTDEBUGoutput_step = cms.EndPath(process.FEVTDEBUGoutput)

# Schedule definition
process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step,process.simulation_step,process.endjob_step,process.FEVTDEBUGoutput_step)
# filter all path with the production filter sequence
for path in process.paths:
	getattr(process,path)._seq = process.generator * getattr(process,path)._seq 

# customisation of the process.

# Automatic addition of the customisation function from SLHCUpgradeSimulations.Configuration.combinedCustoms
from SLHCUpgradeSimulations.Configuration.combinedCustoms import cust_2023HGCalMuon 

#call to customisation function cust_2023HGCalMuon imported from SLHCUpgradeSimulations.Configuration.combinedCustoms
process = cust_2023HGCalMuon(process)

# End of customisation functions
