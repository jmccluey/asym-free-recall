# Behavioral Data

This directory contains the actual data collected while running this
experiment, for _Experiment 1_ (asymFR2) and _Experiment 2_
(asymFR3).  These data have been saved in MATLAB files, and are a
byproduct of the scripts in the *data_prep* directory above, as
converted from indivual PyEPL session logs.

Each data file contains a MATLAB structure with a number of associated
fields.  Each field contains a cell array or matrix in which each row
corresponds to a single list (or trial) from a particular subject in a
particular session.  So, for example, the particular recall sequence
performed by subject 202 on his or her 3rd trial can be accessed by:
```
this_trial = data.subject==201 && data.pres.trial(:,1)==3;
data.recalls(this_trial, :);
```
These recall sequences allows us to observe the order in which items
are recalled.  See more information about the recalls field below.

A brief description of the two data files is provided below, followed
by a more exhaustive list of the fields available on these
structures. The fields are the same across both data_asymFR2.mat and
data_asymFR3.mat.

_Note:_ The main organizational differences between data_asymFR2.mat
and data_asymFR3.mat are:
* data_asymFR3.mat has a third listtype present on data.pres.listtype
* item and category numbers/indices may not be consistent across
studies, as they reflect different wordpools

## Data Structures

###data_asymFR2.mat
  Two conditions: uncategorized lists and categorized lists.
  Uncategorized lists contain one item from each of 12 categories.
  Categorized lists contain 12 items from a single category.  Note
  that uncategorized lists always used the same set of 12 categories.
  Some participants noticed this, and it is possible that some
  participants retrieved the category labels in a certain order, which
  would potentially lead to diminished temporal organization.

###data_asymFR3.mat
  Three conditions: Toronto noun pool lists (random words),
  uncategorized lists, categorized lists.  Uncategorized and
  categorized are as above, except that the uncategorized lists drew
  items from a larger set of categories, making their structure less
  predictable.

Note: For both data structures, data.pres.listtype indicates the condition for each trial.  
listtype == 0, categorized
listtype == 1, uncategorized
listtype == 2, Toronto noun pool (only appears in asymFR3) 


## Fields

The data structure contains information about the behavioral aspects
of the study:

* *subject* - A vector of subject ID numbers, where each row
   represents a separate trial.

* *subjid* - A cell array of subject IDs represented as strings.

* *session* - A vector indicating in which session number a trial was
   performed.

* *pres_items* - A cell array of item strings of the words presented
   to a participant on a particular trial.  Each row is
   data.listLength long, as there are that many items in each list.

* *pres_itemnos* - A matrix of item numbers/indices corresponding to
   the presented words on a particular trial.

* *rec_items* - A cell array of item strings of the words recalled by
   a participant on a particular trial.  Each row is as long as the
   longest recall sequence, and is padded with empty strings ([]) if a
   recall was not made (i.e., the participant did not make any more
   recalls).

* *rec_itemnos* - A matrix of item numbers/indices corresponding to
   the recalled words on a particular trial.  An index of 0 indicates
   that no recall was made.  A value of -1 indicates that a recalled
   item was not in the wordpool (this occurs when a participant
   incorrectly recalls a word they did not actually study).

* *recalls* - The original list position of the recalled item for a
   particular list.  A value of 0 indicates no recall was made (i.e.,
   the participant did not make any more recalls). E.g., if a
   participant recalled the third, then the fifth, then the eleventh
   item from the original study list, then data.recalls(i,:) would be
   [3 5 11 0 ... 0].  A value of -1 indicates that a recalled item was
   not on the original study list (see the _intrusions_ field below).

* *times* - A matrix of times (in milliseconds) that each recalled
   word was said, with reference to the start of the recall period.  A
   value of 0 indicates no recall was made.

* *intrusions* - A matrix indicating whether an item was incorrectly
   recalled on a list.  A positive value indicates that a recalled
   item was actually from a previous list (prior-list intrusion, e.g.,
   a value of 3 means that the item was from 3 lists ago).  A value of
   -1 indicates that  the item did not actually appear on a previous
   list (extra-list intrusion).

* *listLength* - A scalar indicating how many items were presented in
   each list.

* *pres* and *rec* - See below.

## Pres and Rec Fields

The top-level values are curated as such because they are the most
typical values used in basic analyses.  However, the _pres_ and _rec_
fields contain information about _each_ presented or recalled item.
As such, it can also contain some other relevant information for more
additional advanced analyses.

Both _pres_ and _rec_ fields convey the same information, but for
either the presented or recalled items for that trial, respectively.
Each row corresponds to a particular trial, and each column
corresponds to either a presented list position (for _pres_) or item in
a recall sequence (for _rec_).  For the _rec_ fields, each trial is
padded to the longest recall sequency made by any subject.  As such,
some values are padded with either 0's or []'s (empty strings) to
indicate no recall was made.

The _pres_ and _rec_ fields are:

* *subject* - A cell array of subject ID strings for each item.

* *session* - A matrix indicating the session number of each item.

* *trial* - A matrix indicating which trial number a particular item
   was presented/recalled.

* *type* - A cell array indicating what type of event each item was
   associated with (e.g., 'WORD' for presented item, 'REC_WORD' for
   recalled item).

* *category* - A cell array indicating the particular category pool
   from which each item was drawn, or 'TORONTO' for the random word
   pool (only for asymFR3).

* *catno* - A matrix indicating the number/index of the category for
   an item, or 0 for the random word pool (only for asymFR3).

* *resp* - A matrix indicating the participant's response to the
   pleasantness judgment for an item (0=unpleasant, 1=pleasant).

* *rt* - The response time (in milliseconds) of the participant's
   pleasantness judgment relative to when the item appeared on the
   screen.

* *listtype* - The type of stimuli used on the list (0=categorized,
   1=uncategorized, 2=Toronto noun pool).

* *serialpos* - A matrix indicating the original list position of a
   studied item.

* *endmathcorrect* - A matrix of then number of true/false math
   problems performed correctly at the end of a trial before the
   recall period.

* *endnumproblems* - A matrix of the total number of true/false math
   problems presented at the end of a trial before the recall period.

* *item* - A cell array indicating the string of the particular word
   item.

* *itemno* - The item's index in the wordpool for the study, or -1 if
   it is an incorrectly recalled word that does not appear in the
   wordpool.

* *recalled* - A matrix indicating whether a presented item was later
   recalled.

* *finalrecalled* - A matrix indicating whether a studied item was later
   recalled in the final recall period at the end of the session
   (where participants can recall words from any list).

* *rectime* - A matrix of times (in milliseconds) that each recalled
   word was said, with reference to the start of the recall period.  A
   value of 0 indicates no recall was made.

* *intrusion* - A matrix indicating whether an item was incorrectly
   recalled on a list.  A positive value indicates that a recalled
   item was actually from a previous list (prior-list intrusion, e.g.,
   a value of 3 means that the item was from 3 lists ago).  A value of
   -1 indicates that  the item did not actually appear on a previous
   list (extra-list intrusion).

* *mstime* - A matrix indicating the system time (in milliseconds)
   that an event occurred.

* *msoffset* - An extra value logged by PyEPL that is not used in
   any analyses.
