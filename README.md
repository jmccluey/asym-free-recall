# Asymmetry Free Recall

A psychology study examining semantic relatedness and organization in memory.  This project expands on the basic structure introduced by the [immediate-free-recall](https://github.com/jmccluey/immediate-free-recall) project to show how it can be used to examine more developed scientific questions.

Some specific differences:
- Multiple experimental conditions, i.e., not all lists are the same, but differ in semantic relatedness (more related, less related, completely random).
- Participants made a pleasant judgment on each item using a keypress ('N'=pleasant,'M'=unpleasant).
- Counterbalancing of conditions, such that list types are spread out evenly throughout the study.
- A math distractor at the end of each list to prevent overt rehearsal of items.  This is known as delayed free recall.
- User-controlled breaks between each list.

In particular, this study examines a particular phenomenon in memory research regarding the order in which presented information is later recalled, and how the relatedness of information affects that organzation.  An example of related objects is "cat" and "dog" (more related), vs. "cat" and "spoon" (less related).  It is titled "Asymmetry" Free Recall because it examines the asymmetrical forward-going nature of contiguity effect, as described in the _Abstract_ below.

The paradigm is designed and written using [PyEPL](http://pyepl.sourceforge.net/), a Python-based experiment programming library.  The collected data is then organized and analyzed using MATLAB.

## Contents

The current project contains the code used to run the paradigm and prepare the data for further analysis.  In the research lab, various stages of analysis are contained in different SVN projects.  Those components currently reside in other projects, but they will be compiled into this project shortly.

This project will be expanded to include:
- [x] **_exp_**, **_bin_** - Paradigm code in PyEPL
- [x] **_data_prep_** - Data preparation scripts
- [x] **_beh_data_** - Behavioral data
- [ ] **_beh_analysis_** - Scripts for running primary analyses of interest (_to be updated_)
- [ ] **_comp_model_** - Basic computational modeling code (_to be added_)
- [ ] **_poster_** - An academic poster presented based on the results of this work (_to be added_)

Documentation shall be refined as various components are added.

## Design ##

There are two main studies associated with this project.

**_Experiment 1._** - 24 lists of 12 items each.  Half of the lists contain items that are highly related to each other.  The other half are composed of items from different categories.  After each list, the participant performs 10 seconds of math, then has 45 seconds to recall as many words from the most recent list.

**_Experiment 2._** - This study added a third condition where list items were drawn from a large wordpool of random words, rather than lists of "categorized" materials.  A semantic similarity score was used to ensure that no two words were too similar.  Each condition had 8 lists; otherwise, the design is very similar to study 1.

## Versions (Releases)

While the analysis code is designed to be somewhat backwards-compatible across released versions, the code for running the paradigm is not. As such, it is recommended that you download the specific release associated with each version of the study if you wish to run it.  This experiment involved one pilot and two main studies.

- **version_1.0: asymFR** - A basic pilot of the general concept of the paradigm.
- **version_2.0: asymFR2** - _Experiment 1._ This experiment presented lists of either semantically related or semantically less-related words.
- **version_3.0: asymFR3** - _Experiment 2._ This experiment expanded on _version_2.0_ by adding a third type of list of words drawn from an entirely random wordpool.  It also improved upon various design aspects that could affect interpretation of results of _version_2.0_.

For a brief overview of the main studies, see the poster under _Publications_ below.

## Dependencies

###Data Collection###
- [PyEPL](http://pyepl.sourceforge.net) - The Python Experiment-Programming Library is needed to run the paradigm and collect data.

###Data Analysis###
- [APERTURE](https://github.com/mortonne/aperture) - A MATLAB toolbox for organizing and analyzing experimental data.
- [Behavioral Toolbox](http://memory.psych.upenn.edu/Behavioral_toolbox) - A MATLAB toolbox containing scripts for analyzing data from free-recall studies.

###Computational Modeling###
- [NCMS Toolbox](https://memory.psy.vanderbilt.edu/w/index.php/NCMS_Toolbox) - A MATLAB toolbox for using computational models to test theories of cognitive processes.

## Publication ##

Preliminary results of this research were presented as a poster at the Context and Episodic Memory Symposium in May 2016.

McCluey, J. D., Collins, M. A., Kyle, G. M., and Polyn, S. M. (2016). Increased semantic similarity reduces the forward asymmetry in free recall. In _Context and Episodic Memory Symposium_. Philadelphia, PA. ([poster](https://memory.psy.vanderbilt.edu/files/pubs/McClEtal16.poster.pdf))


## Abstract

In free-recall studies, participants tend to successively recall items that were studied in nearby list positions.  Moreover, after recalling a particular item, participants will tend to recall the item from the next list position, rather than the preceding position, such that this contiguity effect is asymmetrical in the forward-going direction.  This asymmetrical contiguity effect is nearly ubiquitous in the free-recall literature and provides an important constraint for models of memory search.  Retrieved-context models of free recall, such as the Context Maintenance and Retrieval (CMR) model, describe a mechanism in which pre-experimental item information is integrated into a slowly changing contextual representation during study.  When an item is studied, pre-existing associative structures allow the item representation to influence the contextual representation, driving the steady evolution of context.  Meanwhile, new experimental/episodic associations are also formed linking the representation of each studied item to the current contextual state.  During memory search, this contextual state provides a cue that guides the retrieval process.  Therefore, when a specific item is remembered from the study list, the experimental and pre-existing associations have distinct influences with regard to the following transition.  The newly-formed experimental/episodic associations support symmetric transitions, while the pre-experimental associations support forward-going transitions.  If we can selectively manipulate these pre-experimental associations, we should be able to modulate the forward asymmetry of recall transitions. We did this by manipulating the semantic similarity of the items on the study list.  Highly semantically related items should activate similar pre-experimental associations, which should result in a reduced forward asymmetry.  We tested this prediction in two free-recall experiments in which participants studied lists of items either all drawn from a similar taxonomic category, or items each drawn from different categories.  In line with our predictions, we found that in lists where the studied items all came from the same category, the forward asymmetry of the contiguity effect was reliably diminished.  We use the CMR modeling framework to test different potential explanations for the cognitive mechanisms underlying this shift in temporal organization.  Specifically, we examine model variants in which the relative influence of pre-experimental and experimental associations is modulated, as well as models in which semantic structure is built into the item representations themselves.
