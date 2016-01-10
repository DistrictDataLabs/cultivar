# Automated Analysis

## Overview    

Trinket is designed to mirror what experienced data scientists do when they take their first few passes through a new dataset by intelligently automating large portions of the wrangling and analysis/exploration phases of the data science pipeline, integrating them into the initial ingestion or uploading phase.

## Architecture    

The auto-analysis and text parsing features of Trinket are written in Python. They work by scanning columns of uploaded data and using `numpy`, `unicodecsv`, one-dimensional kernel density estimates, standard analyses of variance mechanisms and hypothesis testing (KDEs, ANOVAs).

![Seed dataset](../images/data_set.png)

This enables Trinket to do type identification, e.g. to identify and differentiate: discrete integers, floats, text data, normal distributions, classes, outliers, and errors. To perform this analysis quickly and accurately during the data ingestion process, Trinket includes a rules-based system trained from previously annotated data sets and coupled with heuristic rules determined in discussions with a range of experienced data scientists.
