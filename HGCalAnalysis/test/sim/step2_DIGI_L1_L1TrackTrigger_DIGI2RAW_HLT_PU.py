# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step2 --conditions auto:phase2_realistic --pileup_input das:/RelValMinBias_14TeV/1/GEN-SIM -n 10 --era Phase2 --eventcontent FEVTDEBUGHLT -s DIGI:pdigi_valid,L1,L1TrackTrigger,DIGI2RAW,HLT:@fake2 --datatier GEN-SIM-DIGI-RAW --pileup AVE_35_BX_25ns --geometry Extended2023D17 --filein file:step1.root --fileout file:step2.root
import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('analysis')
options.register ('pu',
                  140,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "pileup")
options.register ('tdcBusy',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "tdcBusy")
options.register ('tdcRecovery',
                  2,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "tdcRecovery")
options.register ('skipEvents',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "skip events")
options.parseArguments()

from Configuration.StandardSequences.Eras import eras

process = cms.Process('HLT',eras.Phase2)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mix_POISSON_average_cfi')
process.load('Configuration.Geometry.GeometryExtended2023D17Reco_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.Digi_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.L1TrackTrigger_cff')
process.load('Configuration.StandardSequences.DigiToRaw_cff')
process.load('HLTrigger.Configuration.HLT_Fake2_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(25)
)

# Input source
process.source = cms.Source("PoolSource",
                            dropDescendantsOfDroppedBranches = cms.untracked.bool(False),
                            fileNames = cms.untracked.vstring(options.inputFiles),
                            skipEvents=cms.untracked.uint32(options.skipEvents),
                            inputCommands = cms.untracked.vstring('keep *', 
                                                                  'drop *_genParticles_*_*', 
                                                                  'drop *_genParticlesForJets_*_*', 
                                                                  'drop *_kt4GenJets_*_*', 
                                                                  'drop *_kt6GenJets_*_*', 
                                                                  'drop *_iterativeCone5GenJets_*_*', 
                                                                  'drop *_ak4GenJets_*_*', 
                                                                  'drop *_ak7GenJets_*_*', 
                                                                  'drop *_ak8GenJets_*_*', 
                                                                  'drop *_ak4GenJetsNoNu_*_*', 
                                                                  'drop *_ak8GenJetsNoNu_*_*', 
                                                                  'drop *_genCandidatesForMET_*_*', 
                                                                  'drop *_genParticlesForMETAllVisible_*_*', 
                                                                  'drop *_genMetCalo_*_*', 
                                                                  'drop *_genMetCaloAndNonPrompt_*_*', 
                                                                  'drop *_genMetTrue_*_*', 
                                                                  'drop *_genMetIC5GenJs_*_*'),
                            secondaryFileNames = cms.untracked.vstring()
                            )
process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step2 nevts:10'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.FEVTDEBUGHLToutput = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('GEN-SIM-DIGI-RAW'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('file:step2.root'),
    outputCommands = process.FEVTDEBUGHLTEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition

# Other statements
process.mix.input.nbPileupEvents.averageNumber = cms.double(options.pu)
process.mix.bunchspace = cms.int32(25)
process.mix.minBunch = cms.int32(-12)
process.mix.maxBunch = cms.int32(3)
import os
import random
minbiasDir='/eos/cms/store/cmst3/user/psilva/HGCal/MinBias/CMSSW_9_3_0_pre4/SIM'
mixFiles=[os.path.join(minbiasDir.replace('/eos/cms',''),f) for f in os.listdir(minbiasDir)]
random.shuffle(mixFiles)
print 'First mixing file is',mixFiles[0]
process.mix.input.fileNames = cms.untracked.vstring(mixFiles)
process.mix.digitizers = cms.PSet(process.theDigitizersValid)
process.mix.digitizers.hgceeDigitizer.digiCfg.feCfg.tdcBusy_bx=cms.uint32(options.tdcBusy)
process.mix.digitizers.hgceeDigitizer.digiCfg.feCfg.tdcForcedRecovery_bx=cms.uint32(options.tdcRecovery)
process.mix.digitizers.hgchefrontDigitizer.digiCfg.feCfg.tdcBusy_bx=cms.uint32(options.tdcBusy)
process.mix.digitizers.hgchefrontDigitizer.digiCfg.feCfg.tdcForcedRecovery_bx=cms.uint32(options.tdcRecovery)

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic', '')

# Path and EndPath definitions
process.digitisation_step = cms.Path(process.pdigi_valid)
process.L1simulation_step = cms.Path(process.SimL1Emulator)
process.L1TrackTrigger_step = cms.Path(process.L1TrackTrigger)
process.digi2raw_step = cms.Path(process.DigiToRaw)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.FEVTDEBUGHLToutput_step = cms.EndPath(process.FEVTDEBUGHLToutput)

# Schedule definition
process.schedule = cms.Schedule(process.digitisation_step,process.L1simulation_step,process.L1TrackTrigger_step,process.digi2raw_step)
process.schedule.extend(process.HLTSchedule)
process.schedule.extend([process.endjob_step,process.FEVTDEBUGHLToutput_step])
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# customisation of the process.

# Automatic addition of the customisation function from HLTrigger.Configuration.customizeHLTforMC
from HLTrigger.Configuration.customizeHLTforMC import customizeHLTforMC 

#call to customisation function customizeHLTforMC imported from HLTrigger.Configuration.customizeHLTforMC
process = customizeHLTforMC(process)

# End of customisation functions

# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
