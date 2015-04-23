import FWCore.ParameterSet.Config as cms

def customisePerf(process):
    process.Timing = cms.Service("Timing")
    process.load("FWCore.MessageService.MessageLogger_cfi")
    process.MessageLogger.categories.append("TimeModule")
    process.options.wantSummary = cms.untracked.bool(True)

    #process.genMuons = cms.EDProducer("GenParticlePruner",
    #    src = cms.InputTag("genParticles"),
    #    select = cms.vstring('drop *',
    #        'keep abs(pdgId) == 13',
    #        'drop pt <= 0',
    #    ),
    #)
    #process.out.outputCommands.append('keep *_genMuons_*_*')

    return process

