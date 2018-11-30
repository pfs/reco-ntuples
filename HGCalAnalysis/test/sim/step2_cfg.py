# Auto generated configuration file
# using: 
# Revision: 1.20 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step2 --conditions PH2_1K_FB_V6::All --pileup_input das:/RelValMinBias_TuneZ2star_14TeV/CMSSW_6_2_0_SLHC20_patch1-DES23_62_V1_refHGCALV5-v1/GEN-SIM -n 10 --eventcontent FEVTDEBUGHLT -s DIGI:pdigi_valid,L1,DIGI2RAW --datatier GEN-SIM-DIGI-RAW --pileup AVE_140_BX_25ns --customise SLHCUpgradeSimulations/Configuration/combinedCustoms.cust_2023HGCalMuon --geometry Extended2023HGCalMuon,Extended2023HGCalMuonReco --magField 38T_PostLS1 --filein file:step1.root --fileout file:step2.root
import FWCore.ParameterSet.Config as cms

import FWCore.ParameterSet.Config as cms

import sys
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('standard')
options.register('granularity',  '090', VarParsing.multiplicity.singleton, VarParsing.varType.string, "granularity to use for EE")
options.register('pileup',       140,   VarParsing.multiplicity.singleton, VarParsing.varType.int, "pileup")
if(hasattr(sys, "argv")):
    options.parseArguments()
print options

process = cms.Process('DIGI2RAW')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mix_POISSON_average_cfi')
process.load('Configuration.Geometry.GeometryExtended2023HGCalMuonReco_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_PostLS1_cff')
process.load('Configuration.StandardSequences.Digi_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.DigiToRaw_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

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
process.source = cms.Source("PoolSource",
    secondaryFileNames = cms.untracked.vstring(),
    fileNames = cms.untracked.vstring('file:step1.root')
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.20 $'),
    annotation = cms.untracked.string('step2 nevts:10'),
    name = cms.untracked.string('Applications')
)

# Output definition

process.FEVTDEBUGHLToutput = cms.OutputModule("PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    outputCommands = process.FEVTDEBUGHLTEventContent.outputCommands,
    fileName = cms.untracked.string('file:step2.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('GEN-SIM-DIGI-RAW')
    )
)

# Additional output definition

# Other statements
process.mix.input.nbPileupEvents.averageNumber = cms.double(float(options.pileup))
process.mix.bunchspace = cms.int32(25)
process.mix.minBunch = cms.int32(-12)
process.mix.maxBunch = cms.int32(3)
process.mix.digitizers = cms.PSet(process.theDigitizersValid)

import os
MinBiasDir="/eos/cms/store/cmst3/user/psilva/HGCal/MinBias_%s/GEN-SIM"%options.granularity
MinBiasFiles=['file:'+os.path.join(MinBiasDir,x) for x in os.listdir(MinBiasDir)]
import random
random.shuffle(MinBiasFiles)
process.mix.input.fileNames = cms.untracked.vstring(MinBiasFiles)

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'PH2_1K_FB_V6::All', '')

# Path and EndPath definitions
process.digitisation_step = cms.Path(process.pdigi_valid)
process.L1simulation_step = cms.Path(process.SimL1Emulator)
process.digi2raw_step = cms.Path(process.DigiToRaw)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.FEVTDEBUGHLToutput_step = cms.EndPath(process.FEVTDEBUGHLToutput)

# Schedule definition
process.schedule = cms.Schedule(process.digitisation_step,process.L1simulation_step,process.digi2raw_step,process.endjob_step,process.FEVTDEBUGHLToutput_step)

# customisation of the process.

# Automatic addition of the customisation function from SLHCUpgradeSimulations.Configuration.combinedCustoms
from SLHCUpgradeSimulations.Configuration.combinedCustoms import cust_2023HGCalMuon 

#call to customisation function cust_2023HGCalMuon imported from SLHCUpgradeSimulations.Configuration.combinedCustoms
process = cust_2023HGCalMuon(process)

# End of customisation functions
