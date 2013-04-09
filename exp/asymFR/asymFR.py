#!/usr/bin/python
from pyepl.locals import *
from pyepl import display

# other modules
import os
import sys
import shutil
import prep
reload(prep)
import math_distract as math

# Set the current version
VERSION = '0.0.1'
MIN_PYEPL_VERSION = '1.0.0'

def prepare(exp, config):
    """
    Prepare stimuli for the experiment.

    Stimuli are saved as part of the state vector.  Once prepare has
    been run and the state saved for a given subject, changes to the
    config file that deal with stimulus creation and presentation
    order will not affect the experiment.

    Inputs
    ------
    exp : Experiment
    config : Configuration

    State
    -----
    wp : list of strs
        A list containing the pool of words that the stimuli for this
        subject were chosen from.
    subjItems : str : [session][trial][item]
        Items to be presented during the study period (see
        prep.subjWordOrder).
    sessionNum : int
        Number of the current session.
    trialNum : int
        Number of the current trial
    """

    # verify that we have all the files
    prep.verifyFiles(config.files)

    # get the state
    state = exp.restoreState()

    # copy the word pool to the directory containing these sessions
    try:
        shutil.copy(config.wpfile, exp.session.fullPath())
    except:
        pass

    # svn version info
    svn_version = os.popen('svn info')
    vsn = open(str(exp.session.fullPath()) + config.svnVersionFile, 'w')
    vsn.write(svn_version.read())
    vsn.close()

    # set word order for this subject
    (wp, subjItems, subjListOrder) = prep.subjWordOrder(exp, config)

    # write out all the to-be-presented items to text files
    for i in range(config.nSessions):
        exp.setSession(i)
        for j in xrange(config.nLists):
            # each list written to data/[subject]/session_[i]/[j].lst
            listFile = exp.session.createFile('%d.lst' % j)

            # one word per line
            for k in xrange(config.listLength):
                listFile.write('%s\n' % subjItems[i][j][k])
            listFile.close()

    # create a number of math problem sets, one for each list
    terms = []
    ops = []
    answers = []
    proposed = []
    for i in range(config.nLists):
        set_config = math.prep_math_set(config.numVars,
            config.minNum, config.maxNum, config.maxProbs, 
            config.plusAndMinus, config.ansMod, config.ansProb,
            config.tfProblems, config.uniqueVars, 
            config.excludeRepeats)
        terms.append(set_config[0])
        ops.append(set_config[1])
        answers.append(set_config[2])
        proposed.append(set_config[3])

    # save the prepared data; set state to first session, trial
    exp.saveState(state,
                  wp=wp,
                  subjItems=subjItems,
                  subjListOrder=subjListOrder,
                  sessionNum=0,
                  trialNum=0,
                  blockNum=0,
                  terms=terms,
                  ops=ops,
                  answers=answers,
                  proposed=proposed,
                  tcorrect=0)

def formatStr(format, input):
    """
    Formats a string; if input is None, an empty string is returned.
    """
    if input or input==0:
        s = format % input
    else:
        s = ''
    return s

def logEvent(log, ts, type,
             trialno=None,
             listname=None,
             item=None,
             itemno=None):
    """
    Use standard formatting to log an event in session.log.

    Inputs
    ______
    log : LogTrack
    ts : int
        Time in the experiment that the event happened.
    type : str
        String identifier for the type of event.
    trialno : int
    item : str
    itemno : int
    """

    # format each input. If any input is None, it will be formatted
    # as an empty string.
    inputs = (formatStr('%s', type),
              formatStr('%s', trialno),
              formatStr('%s', listname),
              formatStr('%s', item),
              formatStr('%s', itemno))

    lineFormat = '%s\t' * (len(inputs) - 1) + '%s'
    log.logMessage(lineFormat % inputs, ts)

def trial(exp, config, clock, state, log, video, audio, mathlog,
          startBeep, stopBeep, tf_bc, fixationCross):
    """
    Present a list of words, followed by a free recall period.

    Inputs
    ______
    exp : Experiment
    config : Configuration
    clock : PresentationClock
    state :
    log : LogTrack
    video: VideoTrack
    audio : AudioTrack
    startBeep : Beep
    stopBeep : Beep
    fixationCross : Text

    Design
    ______
    This function runs immediate free recall (IFR).

    Code  Name                     Config Variable
    ______________________________________________
    PLD   pre-list delay           preListDelay
    W     word presentation        wordDuration
    ISI   inter-stimulus interval  wordISI + jitter
    PRD   pre-recall delay         preRecallDelay + jitterBeforeRecall
    R     recall period            recallDuration

    Immediate Free Recall:
    PLD W ISI W ISI ... W ISI PRD R
    """

    # get the list name
    listname = state.subjListOrder[state.sessionNum][state.trialNum]

    # PRESENT THE LIST
    for n in range(config.listLength):

        # PREPARE STIMULUS
        # prepare item text
        item = state.subjItems[state.sessionNum][state.trialNum][n]
        itemInd = state.wp.index(item) + 1 # itemnos are one-indexed
        itemText = Text(item, size=config.wordHeight)

        # PRESENT STIMULUS
        video.showProportional(itemText,.5,.5)

        # sending in the clock tares the clock
        ts = video.updateScreen(clock)
        clock.delay(config.wordDuration)

        # log the word 
        logEvent(log, ts, 'FR_PRES', trialno=state.trialNum, listname=listname,
                 item=item, itemno=itemInd)

        # show the fixation cross
        video.clear()
        fix = video.showCentered(fixationCross)
        video.updateScreen(clock)
        video.unshow(fix)

        # pause before we present the next word
        isi = config.wordISI
        jitter = config.jitter
        clock.delay(isi, jitter)

    # pre distractor delay
    clock.delay(config.preDistractDelay, config.preDistractJitter)

    # distractor period
    t = state.trialNum
    out = math.run_math_set(state.terms[t],
                            state.ops[t], 
                            state.answers[t],
                            state.proposed[t], clock = clock, 
                            mathlog = mathlog,
                            minProblemTime = config.minProblemTime,
                            textSize = config.wordHeight,
                            maxDistracterLimit = config.maxDistractorLimit,
                            trialNum = t,
                            tf_bc = tf_bc,
                            tfKeys = config.tfKeys,
                            fixation = fixationCross,
                            presentSeq = config.presentSeq,
                            numberDuration = config.numberDuration,
                            numberISI = config.numberISI,
                            probISI = config.probISI,
                            probJitter = config.probJitter)
    (nCorrect, nProblems, startTime, probTimes, fix) = out

    # log the distractor
    logEvent(log, startTime, 'DISTRACTOR', trialno=t, item=nProblems, itemno=nCorrect)
    # update tcorrect in state
    state.tcorrect += nCorrect
    exp.saveState(state)
    
    # get fixation ready to be cleared
    if fix is not None:
        video.unshow(fix)
            
    # pause before recall
    clock.delay(config.preRecallDelay, config.jitterBeforeRecall)

    # RECALL
    # show the recall start indicator
    startText = video.showCentered(Text(config.recallStartText,
                                        size=config.wordHeight))
    video.updateScreen(clock)
    startBeep.present(clock)

    # hide rec start text
    video.unshow(startText)
    video.updateScreen(clock)

    # show the fixation cross
    fix = video.showCentered(fixationCross)
    video.updateScreen(clock)
    video.unshow(fix)

    # Record responses, log the rec start
    (rec, timestamp) = audio.record(config.recallDuration,
                                    str(state.trialNum),
                                    t=clock)
    logEvent(log, timestamp, 'REC_START')

    # end of recall period
    stopBeep.present(clock)
    video.updateScreen(clock)

def run(exp, config):
    """
    Run a session of immediate free recall.

    If you break (Esc+F1 during presentation of a list or a recall
    period, starting that subject again will start at the beginning of
    the list.  Any part of the list they already went through will be
    presented again.  This will cause extra lines in the logfile;
    analysis scripts should be prepared to deal with this.
    """

    # verify that we have all the files
    prep.verifyFiles(config.files)

    # get the state
    state = exp.restoreState()

    # if all sessions have been run, exit
    if state.sessionNum >= config.nSessions:
        print "No more sessions!"
        return

    # set the session number
    exp.setSession(state.sessionNum)

    # create tracks
    video = VideoTrack("video")
    audio = AudioTrack("audio")
    keyboard = KeyTrack("keyboard")
    log = LogTrack("session")
    mathlog = LogTrack("math")

    # set the default font
    setDefaultFont(Font(config.defaultFont))

    # get a presentation clock
    clock = PresentationClock()

    # create the beeps
    startBeep = Beep(config.startBeepFreq,
                     config.startBeepDur,
                     config.startBeepRiseFall)
    stopBeep = Beep(config.stopBeepFreq,
                    config.stopBeepDur,
                    config.stopBeepRiseFall)

    # create the button chooser for math distraction
    tfkeys = config.tfKeys
    tf_bc = ButtonChooser(Key(tfkeys[0]), Key(tfkeys[1]))
    
    # get instructions buttons
    scroll = ButtonRoller(Key(config.downButton),
                          Key(config.upButton))
    exitbutton = Key(config.exitButton)

    # custom instructions function
    def customInstruct(filename, textDict=config.textFiles,
                       scroll=scroll, exitbutton=exitbutton,
                       clock=clock, instructISI=config.instructISI,
                       **args):
        """Run instruct with custom defaults."""
        f = textDict[filename]
        str = open(f, 'r').read()
        instruct(str, scroll=scroll, exitbutton=exitbutton, **args)

        # delay instructions to prevent skipping
        clock.tare()
        clock.delay(instructISI)
        clock.wait()
    # endfunction

    # create the fixation cross
    fixationCross = Text('+', size=config.fixationHeight)

    # soundcheck and instructions on first trial of each session
    if state.trialNum == 0:

        # log start of experiment
        timestamp = clock.get()
        logEvent(log, timestamp, 'SESS_START', trialno=state.sessionNum + 1)

        # do mictest
        if config.doMicTest:
            video.clear("black")
            soundgood = micTest(2000, 1.0)
            if not soundgood:
                return

        video.clear("black")

        # show complete instructions
        customInstruct('introSess')
        
        customInstruct('introMath')
        customInstruct('introMathResponses')
        customInstruct('introMathPractice')

        # practice math
        set_config = math.prep_math_set(config.numVars,
                                        config.minNum, 
                                        config.maxNum, 
                                        config.maxProbs, 
                                        config.plusAndMinus, 
                                        config.ansMod, 
                                        config.ansProb,
                                        config.tfProblems, 
                                        config.uniqueVars, 
                                        config.excludeRepeats)
        (terms, ops, answers, proposed) = set_config
        
        # present a fixed interval of math problems
        out = math.run_math_set(terms, ops, answers, proposed,
                                clock = clock, mathlog = mathlog,
                                minProblemTime = config.minProblemTime,
                                textSize = config.wordHeight,
                                maxDistracterLimit = config.maxPracticeMath,
                                trialNum = -1,
                                tf_bc = tf_bc,
                                tfKeys = tfkeys,
                                fixation = fixationCross,
                                presentSeq = config.presentSeq,
                                numberDuration = config.numberDuration,
                                numberISI = config.numberISI,
                                probISI = config.probISI,
                                probJitter = config.probJitter)
        (nCorrect, nProblems, startTime, probTimes, fixDisp) = out

        if fixDisp is not None:
            video.unshow(fixDisp)
            video.updateScreen(clock)

        
        customInstruct('introRecall')
        customInstruct('introFinal')

        # pause for questions
        customInstruct('introQuestions')
        # prepare screen
        customInstruct('introGetReady')

    # get the screen ready
    video.clear("black")
    video.updateScreen(clock)
    
    if state.blockNum==0:
        # check if we're still presenting lists
        while state.trialNum < config.nLists:
            
            if state.trialNum > 0:
                # minimum break duration
                breakText = Text(open(config.textFiles['trialBreak'],'r').read())
                breakStim = video.showCentered(breakText)
                video.updateScreen(clock)
                video.unshow(breakStim)
                clock.delay(config.breakDuration)
                
                # after break, wait for participant to continue
                if config.breakSubjectControl:
                    endBreakText = Text(open(config.textFiles['endBreak'],'r').read())
                    timestamp = waitForAnyKey(clock, endBreakText)
                    
                    # log break
                    logEvent(log, timestamp, 'REST')
                    
            # fixation cross
            fix = video.showCentered(fixationCross)
            video.updateScreen(clock)
            video.unshow(fix)
            
            # wait a bit before starting
            clock.delay(config.preListDelay)
            
            # run a trial (a trial is a word list)
            trial(exp, config, clock, state, log, video, audio, mathlog,
                  startBeep, stopBeep, tf_bc, fixationCross)
            
            # save the state after each trial
            state.trialNum += 1
            exp.saveState(state)

        # log math score
        logEvent(log, timestamp, 'MATH_TOTAL_SCORE', trialno=state.tcorrect)
        
        # move to next block, reset trial counter, save state
        state.blockNum += 1
        state.trialNum = 0
        state.tcorrect = 0
        exp.saveState(state)

    if state.blockNum==1:
        # screen before final free recall instructions
        msg = Text("Thank you!\nPress any key to continue.")
        waitForAnyKey(clock, msg, excludeKeys=config.exitButton)

        clock.delay(config.preFinalDelay)
        
        # ffr instructions
        customInstruct('prepareFFR')
        logEvent(log, clock.get(), 'FFR_START')

        clock.delay(config.preFinalDelay, config.jitterBeforeRecall)

        # RECALL
        # show the recall start indicator
        startText = video.showCentered(Text(config.recallStartText,
                                            size=config.wordHeight))
        video.updateScreen(clock)
        startBeep.present(clock)
        
        # hide rec start text
        video.unshow(startText)
        video.updateScreen(clock)
        
        # show the fixation cross
        fix = video.showCentered(fixationCross)
        video.updateScreen(clock)
        video.unshow(fix)
        
        # Record responses, log the rec start
        (rec, timestamp) = audio.record(config.ffrDuration,
                                        'ffr',
                                        t=clock)
        logEvent(log, timestamp, 'REC_START')

        # end of recall period
        stopBeep.present(clock)
        video.updateScreen(clock)

        # move to next block, save state
        state.blockNum += 1
        exp.saveState(state)


    # END OF SESSION
    # set the state for the beginning of the next session
    state.sessionNum += 1
    state.blockNum = 0
    exp.saveState(state)

    # tell the participant and log that we're done
    timestamp = waitForAnyKey(clock, Text(config.sessionEndText))

    logEvent(log, timestamp, 'SESS_END')
    
    # wait for the clock to catch up
    clock.wait()

# only do this if the experiment is run as a stand-alone program
# (not imported as a library)
if __name__ == "__main__":
    import sys, re

    # hack around the catch-22 that Experiment.__init__ creates by calling
    # Experiment.setup internally:
    arg_string = ''
    for arg in sys.argv:
        arg_string += arg

    arch_re = re.compile('archive=')
    if not arch_re.search(arg_string):
        raise ValueError("You didn't pass an archive! I need to be able to find any previous sessions for this version of the experiment.")

    # make sure we have the min pyepl version
    checkVersion(MIN_PYEPL_VERSION)

    # start PyEPL, parse command line options, and do subject housekeeping
    exp = Experiment()

    # get subj. config
    config = exp.getConfig()

    # allow users to break out of the experiment with escape-F1
    # (the default key combo)
    exp.setBreak()

    # if there was no saved state, run the prepare function
    if not exp.restoreState():
        print "*** CREATING NEW SUBJECT ***"
        prepare(exp, config)

    # now run the subject
    run(exp, config)
