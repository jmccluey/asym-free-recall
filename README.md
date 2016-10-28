# Asymmetry Free Recall

A psychology study examining semantic relatedness and organization in memory.

This study examines a particular phenomenon in memory research regarding the order in which presented information is later recalled, and how the relatedness of information affects that organzation.  An example of related objects is "cat" and "dog" (more related), vs. "cat" and "spoon" (less related).  It is titled "Asymmetry" Free Recall because it examines the asymmetrical forward-going nature of contiguity effect, as described in the abstract below.

The paradigm is designed and written using [PyEPL](http://pyepl.sourceforge.net/), a Python-based experiment programming library.  The collected data is then organized and analyzed using MATLAB.

## Contents

The current project contains the code used to run the paradigm and prepare the data for further analysis.

This project will be expanded to include:
- [x] Paradigm code in PyEPL
- [x] Data preparation scripts
- [ ] Behavioral data
- [ ] Scripts for running primary analyses of interest
- [ ] Basic computational modeling code using the [NeuroCognitive Memory Search](https://memory.psy.vanderbilt.edu/w/index.php/NCMS_Toolbox) toolbox
- [ ] An academic poster presented based on the results of this work

As this study was developed and performed by the researchers who designed it, stand-alone documentation is under development.

## Versions (Releases)

While analysis code can be performed on any variant of the study, to run the paradigm it is recommended that you download the specific release associated with each version of the study.  This experiment involved one pilot and two main studies.

- **version_1.0** - A basic pilot of the general concept of the paradigm.
- **version_2.0** - _Main experiment 1._ This experiment presented lists of either semantically related or semantically less-related words.
- **version_3.0** - _Main experiment 2._ This experiment expanded on _version_2.0_ by adding a third type of list of words drawn from an entirely random wordpool.  It also improved upon various design aspects that could affect interpretation of results of _version_2.0_.

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
