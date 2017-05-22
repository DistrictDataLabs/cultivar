# Trinket

## Introduction

Over the last several years, Python developers interested in data science and analytics have acquired a variety of tools and libraries that aim to facilitate analytical processes. Libraries such as Pandas, Statsmodels, Scikit-learn, Matplotlib, Seaborn, and Yellowbrick have made tasks such as data wrangling, statistical modeling, machine learning, and data visualization much quicker and easier. They have accomplished this by automating and abstracting away some of the more tedious, repetitive processes involved with analyzing and modeling data.

Over the next few years, we are sure to witness the introduction of new tools that are increasingly intelligent and have the ability to automate more complex analytical processes. However, as we begin using these tools (and developing new ones), we should strongly consider the level of automation that is most appropriate for each case. Some analytical processes are technically difficult to automate, and therefore require large degrees of human steering. Others are relatively easy to automate but perhaps should not be due to the unpredictability of results or outputs requiring a level of compassionate decision-making that machines simply don’t possess. Such processes would benefit greatly from the collaboration between automated machine tasks and uniquely human ones. After all, it is often systems that utilize a combination of both human and machine intelligence that achieve better results than either could on their own.

## About the Framework

Exploratory data analysis (EDA) is an important pillar of data science, a critical step required to complete every project regardless of the domain or the type of data you are working with. It is exploratory analysis that gives us a sense of what additional work should be performed to quantify and extract insights from our data. It also informs us as to what the end product of our analytical process should be. Yet, in the decade that I've been working in analytics and data science, I've often seen people grasping at straws when it comes to exploring their data and trying to find insights.

Having witnessed the lack of structure in conventional approaches, I decided to document my own process in an attempt to come up with a framework for data exploration. I wanted the resulting framework to provide a more structured path to insight discovery: one that allows us to view insight discovery as a problem, break that problem down into manageable components, and then start working toward a solution.

![Framework](../docs/images/framework.png)

The following blogs go into the framework in more detail:

[Part 1](http://blog.districtdatalabs.com/data-exploration-with-python-1)

[Part 2](http://blog.districtdatalabs.com/data-exploration-with-python-2)

[Part 3](http://blog.districtdatalabs.com/data-exploration-with-python-3)

## Sprints

During these sprints, we would like to have participants to do the following:

1. Find a dataset you like that you think would be a good example dataset to use.

2. Use the steps from the Exploratory Data Analysis Framework on this dataset.  Any code created, results, and any insights or comments should be captured in a Jupyter notebook.  If you don't have it installed on your machine or know how to use it, you can refer to the following documentation:
  [https://jupyter.readthedocs.io/en/latest/install.html](https://jupyter.readthedocs.io/en/latest/install.html)

3. Each of these efforts will serve to provide examples of how to use the framework to explore and analyze an example dataset.  For the tool, the idea then is that folks could use these exercises to think about which steps can be automated and how they may be automated based on how folks ran through the steps and what code they created.

  These will then be used going forward to help develop a tool that can automate as much of this process as possible.
