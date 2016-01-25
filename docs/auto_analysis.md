# Automated Analysis

## Overview    

Trinket is designed to mirror what experienced data scientists do when they take their first few passes through a new dataset by intelligently automating large portions of the wrangling and analysis/exploration phases of the data science pipeline, integrating them into the initial ingestion or uploading phase.

## Architecture    

The auto-analysis and text parsing features of Trinket are written in Python. They work by scanning columns of uploaded data and using `numpy`, `unicodecsv`, one-dimensional kernel density estimates, standard analyses of variance mechanisms and hypothesis testing (KDEs, ANOVAs).

![Seed dataset](../images/data_set.png)

This enables Trinket to do type identification, e.g. to identify and differentiate: discrete integers, floats, text data, normal distributions, classes, outliers, and errors. To perform this analysis quickly and accurately during the data ingestion process, Trinket includes a rules-based system trained from previously annotated data sets and coupled with heuristic rules determined in discussions with a range of experienced data scientists.

## Mechanics

Auto-analysis works by assigning each column/feature a data type (`dtype` in the parlance of NumPy and Pandas), e.g. categorical, numeric, real, integer, etc. These types must be automatically inferred from the dataset.

_Questions to answer:_

- How do other libraries like `pandas` and `messytables` do this?    

- What does column-major mean for Trinket?    

- What types are we looking for? s
string, datetime, float, integer, boolean

Attempt parsing from broadest type to narrowest:

```python
for val in colSample:
    if val.dtype.type is np.string_:
        colType = colType.astype('Sn') # where n is the max length value in col
    elif val.dtype.type is np.datetime64:
        colType = colType.astype('datetime64')   
    elif val.dtype.type is np.float_:
        colType = colType.astype('float64')      
    elif val.dtype.type is np.int_:
        colType = colType.astype('int64')   
    elif val.dtype.type is np.bool_:
        colType = colType.astype('bool')   
    else:
        # do something else
```
- How lightweight/heavyweight must this be?    

- Is there a certain density of data required to make a decision?    

- Do you have to go through the whole dataset to make a decision?    
Yes and no.

- Can we use a sample approach to reading the data?   
```python
for each col in fileTypeObject:
    max = row with the longest value
    min = row with the shortest value
    nonNaN = first 50 non-empty rows # ndarray.nonzero()
    sampleArray = ndarray(min, max, nonNaN)
```

- How do we detect if there is a header row or not?    

- Can we automatically detect delimiters and quote characters? (e.g. ; vs ,)

## Sources

[Datatypes in Python - 2.7](https://docs.python.org/2/library/datatypes.html)

[Datatypes in Python - 3.5](https://docs.python.org/3.5/library/datatypes.html)

[Numpy - dtypes](http://docs.scipy.org/doc/numpy/reference/arrays.dtypes.html)

[UnicodeCSV](https://github.com/jdunck/python-unicodecsv/blob/master/README.rst)

[Pandas](http://pandas.pydata.org/)

[MessyTables](https://messytables.readthedocs.org/en/latest/)

[Algorithms for Type Guessing - Stackoverflow](http://stackoverflow.com/questions/6824862/data-type-recognition-guessing-of-csv-data-in-python)

[Python Libraries for Type Guessing - Stackoverflow](http://stackoverflow.com/questions/3098337/method-for-guessing-type-of-data-represented-currently-represented-as-strings-in)
