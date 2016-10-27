# Asymmetry Free Recall: prep.py

"""
This module prepares stimuli to be used by ifr.py.
"""

import random
import os
import sys
import re
from copy import copy
from expdesign import balanceSessions

def sessCatOrder(sess_conds, subj_cbcat, categories, pract_cat, list_length):
    """
    """

    # sort categories for use
    poss_cats = subj_cbcat[:]
    nCatLists = sess_conds.count(1)

    # categories for categorized lists
    cat_cats = []
    for c in range(0,nCatLists):
        cat_cats.extend([poss_cats.pop(0)])

    nUncatLists = sess_conds.count(0)
    uncat_catlists = balanceSessions(poss_cats, list_length,
                                     nUncatLists, 'set')
    
    sess_co = []
    sess_cat = []
    for j in range(len(sess_conds)):
        list_co = []
        list_cat = []
        if sess_conds[j] == -1:
            # practice list
            # TORONTO, use category 0
            cat = pract_cat
            list_co = [cat]*list_length
            list_cat = [categories[cat]]*list_length

        elif sess_conds[j] == 0:
            # uncategorized list
            # sample from available categories
            list_co = uncat_catlists.pop(0)
            for j in list_co:
                list_cat.append(categories[j])
            
        elif sess_conds[j] == 1:
            # categorized list
            cat = cat_cats.pop(0)
            list_co = [cat]*list_length
            list_cat = [categories[cat]]*list_length

        elif sess_conds[j] == 2:
            # TORONTO, use category 0
            cat = 0
            list_co = [cat]*list_length
            list_cat = [categories[cat]]*list_length
            
        else:
            print "ERROR: Invalid list condition.\n\n"

        sess_co.append(list_co[:])
        sess_cat.append(list_cat[:])

    return sess_co, sess_cat

def subjCatOrder(exp, config):
    """
    Sets the order of categories for a subject.

    INPUTS:
    ------
    exp : Experiment object.
    config: : Configuration
    """

    # set categorized lists by subject order
    subjnumRegex = re.compile('(\d+)')

    subjID = exp.options['subject']
    #subjID = 'ASM005'
    subjnum = subjnumRegex.search(subjID)

    listOrder = []
    lofile = open(config.cofile, 'r')
    loLines = lofile.readlines()
    for loLine in loLines:
        listOrder.append(loLine.strip().split('\t'))

    # order balanced by subject number
    if config.defaultBlockOrder or subjnum is None:
        # if no subject number, use default
        subjnum = 0;
    else:
        subjnum = int(subjnum.group(1))

    # subjnums are 1-indexed, make 0-indexed
    order = (subjnum - 1) % len(listOrder)

    # counterbalanced category set
    subj_cbcat = listOrder[order][:]
    for n in xrange(len(subj_cbcat)):
        subj_cbcat[n] = int(subj_cbcat[n])

    
    # category condition
    subj_conds = balanceSessions(config.catCond, config.nLists,
                                 config.nSessions, shuffleType='set')
    
    # add practice to first session
    pract_conds = [-1]*config.nPractLists
    fs_conds = pract_conds[:]
    fs_conds.extend(subj_conds[0][:])
    subj_conds[0] = fs_conds[:]

    #print 'Preparing subject...'

    subj_co = []
    subj_cat = []
    for i in range(len(subj_conds)):
        #print i
        sess_co = []
        sess_cat = []
        
        (sess_co, sess_cat) = sessCatOrder(subj_conds[i],
                                           subj_cbcat,
                                           config.categories,
                                           config.practCat,
                                           config.listLength)

        subj_co.append(sess_co[:])
        subj_cat.append(sess_cat[:])

    return subj_co, subj_cat
    
def cpCatList(catlist):
    """
    Make a copy of a list of lists
    """
    cat_copy = []
    for cat in range(len(catlist)):
	cat_copy.append(catlist[cat][:])
    return cat_copy

def extractPools(pool_dir, name_file, wasfile):
    """
    Extract category word pools from text files.
    """
    
    global semMat
    
    wps = []
    wptot = []

    # extract wordpools
    filenames = []
    nmfile = open(name_file, 'r')
    nmLines = nmfile.readlines()
    for nmLine in nmLines:
        filenames.append(nmLine.strip())

    for fname in filenames:
        cat_wp = []

        catin = open(pool_dir+fname,'r')
        wpin = catin.readlines()
        for w in wpin:
            cat_wp.append(w.strip())

        wps.append(cat_wp)
        wptot.extend(cat_wp)

    # read in WAS values for each possible pair of words
    semMat = []
    wasfile = open(wasfile, 'r')
    for word in wasfile:
        wordVals = []
        wordValsString = word.split()
        for val in wordValsString:
            thisVal = float(val)
            wordVals.append(thisVal)
        semMat.append(wordVals)

    return wps, wptot

def listWAScheck(wordInds, WASthresh):
    """
    Check if similarity between any two words in a list exceeds some
    threshold.
    """
    # check to make sure no two words in the list are too similar
    listGood = True
    for word1 in wordInds:
        for word2 in wordInds:
            val = semMat[word1][word2]
            if val >= WASthresh and val < 1:
                listGood = False
                return listGood
    return listGood

def subjWordOrder(subj_co, wp_cat, WASthresh, maxTries):
    """
    Create the order of presentation of stimuli for one subject.
    """
    
    wps_allowed = cpCatList(wp_cat)

    wps_temp = cpCatList(wps_allowed)
    
    subj_wo = []
    for sess_co in subj_co:
        sess_wo = []
        
        for list_co in sess_co:
            list_wo = []

            if list_co[0] == 0:
                # create a list with random words; if it fails, try again
                listPass = False
                nTries = 0
                list_inds = []

                while not listPass:
                    nTries += 1
                    if nTries == maxTries:
                        print 'Warning: maximum tries to create list reached.'
                        break
                    
                    listPass = True
                    wps_temp = cpCatList(wps_allowed)
                    for cat in list_co:
                        # get item
                        ind = random.choice(range(len(wps_temp[cat])))
                        item = wps_temp[cat].pop(ind)
                        cat_ind = wp_cat[cat].index(item)
                        list_wo.append(item)
                        list_inds.append(cat_ind)

                    # test: no two words on list too similar
                    if not listWAScheck(list_inds, WASthresh):
                        listPass = False
                        list_wo = []
                        list_inds = []
                        continue
            else:
                for cat in list_co:
                    # categoried item
                    ind = random.choice(range(len(wps_temp[cat])))
                    item = wps_temp[cat].pop(ind)
                    list_wo.append(item)

            wps_allowed = cpCatList(wps_temp)
            sess_wo.append(list_wo)

        subj_wo.append(sess_wo)

    return subj_wo
    

def verifyFiles(files):
    """
    Verify that all the files specified in the config are there so
    that there is no random failure in the middle of the experiment.
    This will call sys.exit(1) if any of the files are missing.
    """

    for f in files:
        if not os.path.exists(f):
            print "\nERROR:\nPath/File does not exist: %s\n\nPlease verify the config.\n" % f
            sys.exit(1)

## def estimateTotalTime(config):
##     """
##     Calculates time (in minutes) from the start of the experiment to
##     the end of the experiment, including rewetting time.

##     Timing of one list:

##     Code  Name                     Config Variable
##     ______________________________________________
##     PLD   pre-list delay           preListDelay
##     W     word presentation        wordDuration
##     ISI   inter-stimulus interval  wordISI + jitter/2
##     PRD   pre-recall delay         preRecallDelay + jitterBeforeRecall/2
##     R     recall period            recallDuration

##     IFR:
##     PLD W ISI W ISI ... W ISI PRD R
##     """
    
##     # mean time for list items
##     itemTime = config.wordDuration + config.wordISI + config.jitter/2
##     print 'Item: ' + str(itemTime)

##     # mean list time
##     listTime = config.preListDelay + itemTime*config.listLength + \
##                (config.preRecallDelay + config.jitterBeforeRecall/2) + \
##                config.recallDuration
##     print 'List: ' + str(listTime)

##     instruct = 300000 # getting through instructions
##     listBreak = config.breakDuration # break after each list

##     # total session time
##     sessionTime = instruct + (listTime + listBreak)*config.nTotalLists

##     # convert to minutes
##     sessionTime = sessionTime*(1./1000)*(1./60)

##     return sessionTime
