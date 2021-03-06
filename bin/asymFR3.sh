#!/bin/bash
#asymFR3.sh; run Asymmetry Free Recall 3 paradigm

function usage () {
  echo "Usage: $0 [SUBJECT], where:"
  echo "SUBJECT is a subject identifier."
  echo
  echo "e.g.,"
  echo "$ $0 ASM305"
  echo
  echo "This will run subject ASM305 in a session of asymFR3."
}

# hard-coded; must modify for machine/screen running experiments
EXPDES_DIR=~/experiments/expdesign
MATH_DIR=~/experiments/math_distract
ASYM_DIR=~/experiments/asymFR/exp/asymFR
RESOLUTION="1024x768"
ASYM_CONFIG="config_asymFR3.py"
ARCHIVE="data3"
LOGFILE=session.log
SUBJECT=$1

# only valid to call with 0 or 1 argument
if [[ $# != 0 && $# != 1 ]]
then
    echo "You did not specify a valid set of arguments..."
    usage
    exit 1;
fi

# usage
if [[ $# == 0 ]]
then
    usage
    exit 1;
fi

export PYTHONPATH=$EXPDES_DIR:$MATH_DIR:$PYTHONPATH

# call paradigm, specifying config and archive
cd $ASYM_DIR
python asymFR.py --resolution=$RESOLUTION --config=$ASYM_CONFIG \
                     --archive=$ARCHIVE --no-eeg -s $SUBJECT