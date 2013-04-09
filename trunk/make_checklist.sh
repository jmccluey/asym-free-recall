ls#!/bin/bash

if [[ $# == 0 ]]
then
    echo "Usage: $0 [SUBJID], where SUBJID is a string"
    echo "identifier for the subject and SESSNO is a zero-indexed"
    echo "session number for which the experiment prepare function"
    echo "has been run."
    echo "e.g. $0 ASM002"
    echo "will produce a checklist in data/ASM002/session_0"
    exit 0
fi

# hard-coded, must modify for each machine running experiments
ASYM_DIR=$HOME/experiments/asymFR/exp/asymFR
ARCHIVE="data"

SUBJID=$1
SESSNO='0'

# latex document with checklist
# must have %\input{lists} where the lists should be inserted
TEMPLATE=$ASYM_DIR/docs/asymfr_checklist.tex

# session dir
SESSDIR=$ASYM_DIR/$ARCHIVE/$SUBJID/session_$SESSNO

pd=`pwd`
cd $SESSDIR

# make a copy of the template in the session directory
# uncomment \input commands
CHECKFILE=`basename $TEMPLATE`
cat $TEMPLATE | sed 's/%\\input/\\input/' > $CHECKFILE

# fill in subject ID and session #
SESSION=$[ SESSNO+1 ]
# write counterbalanced buttons to checklist
SUBJECT_STR="Subject ID: \\rule\{1in\}\{0.4mm\} "
SESSION_STR="Session number: \\rule\{1in\}\{0.4mm\}"
BUFFER=`cat $CHECKFILE | sed 's/Subject ID.*mm} [^\n]/Subject ID: \\\textbf{'$SUBJID'} \\\hspace{0.1cm} /'`
echo "$BUFFER" > $CHECKFILE
BUFFER=`cat $CHECKFILE | sed 's/ession number.*mm}/Session number: \\\textbf{'$SESSION'}/'`
echo "$BUFFER" > $CHECKFILE

# generate latex code with the words on each list
OUTFILE=lists.tex
cat /dev/null > $OUTFILE

IFS=$'\n'

# write list items to checklist
# first 0.lst through 9.lst
LISTFILES=`ls [0-9].lst`
for l in $LISTFILES; do
    TRIAL=`echo $l | cut -c 1`
    echo '\textbf{Trial '$[TRIAL+1]'}:' >> $OUTFILE
    echo >> $OUTFILE
    echo '\begin{itemize}\itemsep0pt' >> $OUTFILE
    ITEMS=`cat $l`
    for i in $ITEMS; do
	echo '\item' $i >> $OUTFILE
	#echo >> $OUTFILE
    done
    echo '\end{itemize}' >> $OUTFILE
    echo >> $OUTFILE
    echo "\vspace{0.2in}" >> $OUTFILE
    echo Number of Items Recalled -- "\rule{0.3in}{0.25mm}"/16 >> $OUTFILE
    echo "\newpage">> $OUTFILE
done
# now 10.lst through 99.lst
LISTFILES=`ls [0-9][0-9].lst`
for l in $LISTFILES; do
    TRIAL=`echo $l | cut -c 1,2`
    echo '\textbf{Trial '$[TRIAL+1]'}:' >> $OUTFILE
    echo >> $OUTFILE
    echo '\begin{itemize}\itemsep0pt' >> $OUTFILE
    ITEMS=`cat $l`
    for i in $ITEMS; do
	echo '\item' $i >> $OUTFILE
	#echo >> $OUTFILE
    done
    echo '\end{itemize}' >> $OUTFILE
    echo >> $OUTFILE
    echo "\vspace{0.2in}" >> $OUTFILE
    echo Number of Items Recalled -- "\rule{0.3in}{0.25mm}"/16 >> $OUTFILE
    echo "\newpage">> $OUTFILE
done
# compile
pdflatex $CHECKFILE
pdflatex $CHECKFILE

# clean up
rm `echo $CHECKFILE | cut -d . -f 1`.{aux,log,tex}
cd $pd