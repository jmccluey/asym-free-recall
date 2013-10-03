#!/bin/bash
#asymFR.sh; run Asymmetry Free Recall paradigm

function usage () {
  echo "Usage: $0 [SUBJECT], where:"
  echo "SUBJECT is a subject identifier."
  echo
  echo "e.g.,"
  echo "$ $0 ASM005"
  echo
  echo "This will run subject ASM005 in a session of Task Switch."
}

# hard-coded; must modify for machine/screen running experiments
MATH_DIR=~/experiments/math_distract
ASYM_DIR=~/experiments/asymFR/exp/asymFR
RESOLUTION="1024x768"
ASYM_CONFIG="config_asymFR.py"
ARCHIVE="data"
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

export PYTHONPATH=$MATH_DIR:$PYTHONPATH

# call paradigm, specifying config and archive
cd $ASYM_DIR
python asymFR.py --resolution=$RESOLUTION --config=$ASYM_CONFIG \
                     --archive=$ARCHIVE -s $SUBJECT