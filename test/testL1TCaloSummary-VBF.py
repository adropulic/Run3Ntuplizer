import os
import FWCore.ParameterSet.Config as cms

process = cms.Process("L1TCaloSummaryTest")

#import EventFilter.L1TXRawToDigi.util as util

from FWCore.ParameterSet.VarParsing import VarParsing

options = VarParsing()
options.register('runNumber', 0, VarParsing.multiplicity.singleton, VarParsing.varType.int, 'Run to analyze')
options.register('lumis', '1-max', VarParsing.multiplicity.singleton, VarParsing.varType.string, 'Lumis')
options.register('dataStream', '/ExpressPhysics/Run2015D-Express-v4/FEVT', VarParsing.multiplicity.singleton, VarParsing.varType.string, 'Dataset to look for run in')
options.register('inputFiles', [], VarParsing.multiplicity.list, VarParsing.varType.string, 'Manual file list input, will query DAS if empty')
options.register('inputFileList', '', VarParsing.multiplicity.singleton, VarParsing.varType.string, 'Manual file list input, will query DAS if empty')
options.register('useORCON', False, VarParsing.multiplicity.singleton, VarParsing.varType.bool, 'Use ORCON for conditions.  This is necessary for very recent runs where conditions have not propogated to Frontier')
options.parseArguments()

def formatLumis(lumistring, run) :
    lumis = (lrange.split('-') for lrange in lumistring.split(','))
    runlumis = (['%d:%s' % (run,lumi) for lumi in lrange] for lrange in lumis)
    return ['-'.join(l) for l in runlumis]

print 'Getting files for run %d...' % options.runNumber
#if len(options.inputFiles) is 0 and options.inputFileList is '' :
#    inputFiles = util.getFilesForRun(options.runNumber, options.dataStream)
#elif len(options.inputFileList) > 0 :
#    with open(options.inputFileList) as f :
#        inputFiles = list((line.strip() for line in f))
#else :
#    inputFiles = cms.untracked.vstring(options.inputFiles)
#if len(inputFiles) is 0 :
#    raise Exception('No files found for dataset %s run %d' % (options.dataStream, options.runNumber))
#print 'Ok, time to analyze'


# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.Geometry.GeometryExtended2016Reco_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.RawToDigi_Data_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')

# To get L1 CaloParams
#process.load('L1Trigger.L1TCalorimeter.caloStage2Params_cfi')
# To get CaloTPGTranscoder
#process.load('SimCalorimetry.HcalTrigPrimProducers.hcaltpdigi_cff')
#process.HcalTPGCoderULUT.LUTGenerationMode = cms.bool(False)

process.load('L1Trigger.Configuration.SimL1Emulator_cff')
process.load('L1Trigger.Configuration.CaloTriggerPrimitives_cff')

process.load('EventFilter.L1TXRawToDigi.caloLayer1Stage2Digis_cfi')

process.load('L1Trigger.L1TCaloSummary.uct2016EmulatorDigis_cfi')

process.load("L1Trigger.Run3Ntuplizer.l1TRun3Ntuplizer_cfi")

process.l1NtupleProducer.isData = cms.bool(False)

process.uct2016EmulatorDigis.useECALLUT = cms.bool(False)
process.uct2016EmulatorDigis.useHCALLUT = cms.bool(False)
process.uct2016EmulatorDigis.useHFLUT = cms.bool(False)
process.uct2016EmulatorDigis.useLSB = cms.bool(True)
process.uct2016EmulatorDigis.verbose = cms.bool(False)
process.uct2016EmulatorDigis.ecalToken = cms.InputTag("l1tCaloLayer1Digis")
process.uct2016EmulatorDigis.hcalToken = cms.InputTag("l1tCaloLayer1Digis")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(12000) )

process.source = cms.Source("PoolSource",
                            #fileNames = cms.untracked.vstring(inputFiles)#,
                            #secondaryFileNames = cms.untracked.vstring(secondaryMap[options.inputFiles[0]])
                            fileNames = cms.untracked.vstring(
#'/store/mc/RunIIAutumn18MiniAOD/VBFHToTauTau_M125_13TeV_powheg_pythia8/MINIAODSIM/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/B3EC81A2-DCE0-2E48-974B-24F277A6570A.root',
'/store/mc/RunIIAutumn18MiniAOD/VBFHToTauTau_M125_13TeV_powheg_pythia8/MINIAODSIM/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/ABCCF610-63D3-7046-AA37-4D8B3F1D3494.root'
),
                            secondaryFileNames = cms.untracked.vstring(
                                
#'/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/80160B24-55DA-874F-87A9-6D9512BD276E.root', '/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/66F1AD9F-9214-3C46-818C-581AA7A5C428.root', '/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/8D5AE10A-3D1E-314C-BE05-C43861C5763F.root', '/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/04B4F306-BD50-6944-BD47-0CAE40918490.root', '/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/38725CB1-31A8-0E45-8D3C-7C20C3C305C3.root',

#'/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/8566F133-1F0C-D34F-A1AA-5283A017F656.root', '/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/03492BE8-1D1F-3349-878A-271C9105AF31.root', '/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/D595E2C7-6259-F845-B3F8-673BE3D7EBFF.root', '/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/1518D1B5-6C47-024D-A963-C859E7DC5A2A.root', '/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/0EEB6A78-2C39-AC4F-8C5D-36AACAABB9B1.root',

#'/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/CF9D4F70-3964-894D-ABF0-8227BB97D332.root', '/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/EC472937-6A08-664C-8F41-4D1AC1C5732C.root', '/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/963F1900-83FE-C342-BBFC-B8A7CA159A14.root', '/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/4AFF23C9-11C2-154F-8BB7-6541742961D5.root', '/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/5CCECE21-807C-CF45-8387-AAF8B351B2E2.root',

#'/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/F81ACACF-C8C9-CD49-883B-91021322D0F4.root', '/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/D7E6817A-93DD-624B-908B-B4E456DA9CE5.root', '/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/26A4D20D-98C7-3541-A36D-4BB500BD601D.root', '/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/B12E5D5A-6744-FB4C-ABDB-88C8FA5516F3.root', '/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/935BF122-A245-B74F-A22D-D14B916305F1.root',

#'/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/44C411AC-539F-D24E-92B2-396AA06237BC.root', '/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/035D6766-8845-A246-A174-EFDB3FF8CB81.root', '/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/1655229E-8A5D-FE4D-9D31-676A2F19A06A.root', '/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/690C10BE-2E38-AE4B-9133-1E4A89C6470B.root', '/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/F7788B30-34BC-7E46-91D1-F0D1DB7DF722.root',

#'/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/D5A030E0-747C-E64D-AD8B-899F17FCFF61.root', '/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/44466C1F-61FD-414C-90C4-8F7ECB766135.root', '/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/5BE5FEA9-3D88-FD49-A819-B1B2903D203D.root', '/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/05B08540-F169-DD42-84BD-02CF2C88CB42.root', '/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/9A98DF66-DADD-2D4F-B5B9-6499322776EF.root',

#'/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/B4989DAF-4398-A743-86D1-4D4A98B3947F.root', '/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/2279DF87-27AC-AC48-AF44-BDCB3D381B57.root', '/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/28F4349D-286F-934C-A581-0F728CCE0CB3.root', '/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60001/BFCB8052-CD00-A243-B688-C6372267EA11.root',

#second miniaod file

'/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/90091689-95C4-E44A-B681-2AFCE2F2F0DB.root', '/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/018EB922-D39E-C045-B7B9-F07C91216849.root', '/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/F25C6600-C8C9-BB46-8E33-7F755B79A93B.root', '/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/3FFEF5C8-A16B-CB46-98A9-49B8674E96E7.root', '/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/BC74B35D-B1CB-214B-9114-ECFA365539B9.root',

'/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/CD98C8C4-CAAD-C640-83D5-8205127A414B.root', '/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/B910EA72-5963-BE47-BF89-FB0A08E6EC9E.root', '/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/21159B7D-E5AE-E942-8CF3-AA29A905B650.root', '/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/A54F606C-0916-124F-A18C-ABB9B161B56A.root', '/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/DE0512FD-082D-6143-84EC-3EF5653B8E87.root', '/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/9EF53370-C22C-AB49-AC87-70491FDEBA05.root',

'/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/9CC1561F-2E4A-E043-85C3-A706091021E4.root', '/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60001/C8F8689B-0D1F-2440-AE8A-C066CEF51FCF.root', '/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60001/FD5FD406-A51C-7849-B256-FACE46429191.root'
				#'/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/018EB922-D39E-C045-B7B9-F07C91216849.root',
                                #'/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/018EB922-D39E-C045-B7B9-F07C91216849.root',
                                #'/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/3FFEF5C8-A16B-CB46-98A9-49B8674E96E7.root',
                                #'/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/90091689-95C4-E44A-B681-2AFCE2F2F0DB.root',
                                #'/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/BC74B35D-B1CB-214B-9114-ECFA365539B9.root',
                                #'/store/mc/RunIIAutumn18DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62NZS_102X_upgrade2018_realistic_v15-v1/60000/F25C6600-C8C9-BB46-8E33-7F755B79A93B.root'
                            )
)

#process.source.lumisToProcess = cms.untracked.VLuminosityBlockRange("1:3375","1:1443","1:2960","1:3805","1:3381","1:229","1:3531","1:583","1:1120","1:504","1:1454","1:874","1:1078","1:1087","1:121","1:1448","1:1456","1:177","1:2964")


process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step2 nevts:1'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)


process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string("l1TFullEvent.root"),
    outputCommands = cms.untracked.vstring('drop *') #'keep *_*_*_L1TCaloSummaryTest')
    #outputCommands = cms.untracked.vstring('drop *', 'keep *_l1tCaloLayer1Digis_*_*, keep *_*_*_L1TCaloSummaryTest' )
)


#Output
process.TFileService = cms.Service(
	"TFileService",
	fileName = cms.string("l1TNtuple-VBF-bdttest.root")
)

process.p = cms.Path(process.l1tCaloLayer1Digis*process.uct2016EmulatorDigis*process.l1NtupleProducer)

#process.e = cms.EndPath(process.out)

process.schedule = cms.Schedule(process.p)

from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion

#dump_file = open('dump.py','w')
#dump_file.write(process.dumpPython())
