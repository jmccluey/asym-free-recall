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
    cat_cats = [] # categories for categorized lists
    for c in range(0,nCatLists):
        cat_cats.extend([poss_cats.pop(0)])

    sess_co = []
    sess_cat = []
    for j in range(len(sess_conds)):
        list_co = []
        list_cat = []
        if sess_conds[j] == -1:
            # practice list
            list_co = [-1]*list_length
            list_cat = [pract_cat]*list_length

        elif sess_conds[j] == 0:
            # uncategorized list
            # sample from available categories
            list_co = random.sample(poss_cats, list_length)
            for j in list_co:
                list_cat.append(categories[j])
            
        elif sess_conds[j] == 1:
            # categorized list
            cat = cat_cats.pop(0)
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

def extractPools(pool_dir, name_file, pract_file):
    """
    Extract category and practice word pools from text files.
    """

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

    wpp = []

    # extract practice wordpool
    practin = open(pract_file, 'r')
    wppin = practin.readlines()
    for w in wppin:
        wpp.append(w.strip())

    return wps, wptot, wpp

def subjWordOrder(subj_co, wp_cat, wp_pract):
    """
    Create the order of presentation of stimuli for one subject.
    """
    wps_allowed = cpCatList(wp_cat)
    wpp_allowed = cpCatList(wp_pract)

    wps_temp = cpCatList(wps_allowed)
    wpp_temp = cpCatList(wpp_allowed)
    
    subj_wo = []
    for sess_co in subj_co:
        sess_wo = []
        
        for list_co in sess_co:
            list_wo = []
            
            for cat in list_co:
                if cat == -1:
                    # practice item
                    ind = random.choice(range(len(wpp_temp)))
                    item = wpp_temp.pop(ind)
                    list_wo.append(item)
                    wpp_allowed = cpCatList(wpp_temp)
                else:
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
