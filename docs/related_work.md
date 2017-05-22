# Related Work

## Projects

Several projects exist that are related to Cultivar:

- [SailFish Exchange](https://gofishdata.net/): consolidate, share, and discover data-related findings to support your analysis.
- [Keshif](http://keshif.me/): with Keshif, you can explore and understand your data - interactively, visually & easily.
- [dat](http://dat-data.com/): an open source, decentralized data tool for sharing datasets, small and large.

## Research

### Advanced Analytics

[Arun Kumar](http://pages.cs.wisc.edu/~arun/) at the University of Wisconsin studies the intersection of database management with machine learning. He has published several papers about limiting bottlenecks in ML that arise from fundamental issues with databases, in particular _joins_. He showed that most ML requires a single table in order to fit a model, and as a result, data scientists working with normalized databases tended to join before training. His papers included a mechanism to _factorize_ generalized linear models so that multiple tables could be used during the training process (preventing a join). He even showed that in some cases, the use of only the foreign key as a feature was enough to eliminate _bias_ and based on the number of tuples in the table, a join could be skipped because it also minimized _variance_.

He has also presented a vision paper that discusses the HCI components of model selection (very relevant to Cultivar). He believes that an automatic system with a human in the loop is necessary for quality model development. We believe that visual analytics is that HCI mechanism. This vision paper can be found here:

Kumar, Arun, et al. "[Model Selection Management Systems: The Next Frontier of Advanced Analytics.](http://pages.cs.wisc.edu/~arun/vision/SIGMODRecord15.pdf)" ACM SIGMOD Record (2015).
