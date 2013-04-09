# Configuration for Asymmetry Free Recall

"""
This module sets options for running Immediate Free Recall.
"""

### experiment structure ###
nSessions = 1

nLists = 16 # number of unique word lists
listLength = 16
wpfile = '../pools/asymfr_wordpool.txt'

# word order
lofile = 'list_order.txt'
listDir = '../pools/'
namefile = '../pools/list_names.txt'
practList = 'pract.txt'
defaultBlockOrder = False
#allowPrevSessWords = True

# version file name
svnVersionFile = 'version.txt'

# break control
breakSubjectControl = True

### stimuli ###

# stimulus display settings
doMicTest = True
sessionEndText = "Thank you!\nYou have completed the session."
recallStartText = '*******'
wordHeight = .08 # Word Font size (percentage of vertical screen)
defaultFont = '../fonts/Verdana.ttf'
fixationHeight = .07

# beep at start and end of recording (freq,dur,rise/fall)
startBeepFreq = 800
startBeepDur = 500
startBeepRiseFall = 100
stopBeepFreq = 400
stopBeepDur = 500
stopBeepRiseFall = 100

# instruction keys
downButton = 'DOWN'
upButton = 'UP'
exitButton = 'RETURN'

# Instructions
textFiles = dict()

textFiles['introSess'] = 'text/introSess.txt'
textFiles['introMath'] = 'text/introMath.txt'
textFiles['introMathResponses'] = 'text/introMathResponses.txt'
textFiles['introMathPractice'] = 'text/introMathPractice.txt'
textFiles['introRecall'] = 'text/introRecall.txt'
textFiles['introQuestions'] = 'text/introQuestions.txt'
textFiles['introGetReady'] = 'text/introGetReady.txt'
textFiles['trialBreak'] = 'text/trialBreak.txt'
textFiles['endBreak'] = 'text/endBreak.txt'

files = [wpfile]
files.extend(textFiles.values())

### timing ###

# breaks
instructISI = 500
preListDelay = 1000
breakDuration = 5000

# study
wordDuration = 3000
wordISI = 1000
jitter = 0

# distractor
preDistractDelay = 1000
preDistractJitter = 0

# retention
preRecallDelay = 1000
jitterBeforeRecall = 0

# test
recallDuration = 75000

# DISTRACTOR
# math problem options
#numSets = 10 # using nLists instead
numVars = 2
minNum = 1
maxNum = 9
maxProbs = 10
plusAndMinus = False
ansMod = [0,1,-1,2,-1]
ansProb = [.5,.125,.125,.125,.125]
tfProblems = True
uniqueVars = True
excludeRepeats = True

# presentation options
# maximum rest time with no problems (number ISI is 0):
# (allocated ISI - actual ISI) + term 1 + term 2 + '=' + [min resp time]
# (500 - [300-500]) + 400 + 400 + 400 + 400 =
# [0-200] + 400 + 400 + 400 + 400 = [1600-1800]

# note: the actual ISI doesn't contribute to the rest, since it isn't
# clear to the participant at that point that they have reached a rest
# point

# so, for example, participants are distracted for at least 6.6
# seconds out of the 8.5 second distraction period. The actual
# distribution of times will depend on the specific timing parameters
displayCorrect = False
presentSeq = True
maxDistractorLimit = 10000
minProblemTime = 400
numberDuration = 400
numberISI = 0
probISI = 400
probJitter = 0
setISI = 2000
setJitter = 0

maxPracticeMath = 15000

# responses
tfKeys = ['N','M']




fastConfig = False
if fastConfig:
    listLength = 6
    recallDuration = 10000
