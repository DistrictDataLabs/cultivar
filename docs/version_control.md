# Version Control and Provenance  

## Overview    

Trinket offers state-of-the-art version control and provenance that are optimized for dataset management.

Duplication is the single most significant problem in versioning and version control (Mashtizadeh et al. 2013; Zhang et al. 2013; Ramasubramanian et al. 2009; Santry et al. 1999). For example, if minor changes are made to Version 1 of a file, and the updated Version 2 is then also saved to the data store, most of the information stored in Versions 1 and 2 is identical. That duplication corresponds directly to wasted storage space, which is directly correlated to monetary cost. On the other hand, partitioning files in such a way as to reduce duplication also makes the reconstitution of those files expensive in terms of memory processing power. These reasons are precisely why Cloud-based storage services prefer duplication and to pass the costs onto their customers.

## Architecture    

As such, Trinket provides a way for users not only to store datasets in stable Cloud-based repositories, but also to modify those datasets, share them with others, branch off new versions for testing and experimentation, and explore the data using the auto-analysis and visual analytics features. To support and sustain this kind of exploration, Trinket’s dataset versioning solution implements theories initially explored in Chervenak et al. (2000), Palankar et al. (2008), and Ramasubramanian et al. (2009). It aims to balance the tradeoff between the availability of the data (to which users want ready access), and the storage of that data (which becomes less accessible but much cheaper as it is increasingly compressed and archived).

## References    

Chervenak, A, Foster, I., Kesselman, C., Salisbury, C., & Tuecke, S. (2000). The data grid: Towards an architecture for the distributed management and analysis of large scientific datasets. Journal of network and computer applications 23.3, 187-200.

Mashtizadeh, A., Bittau, A., Huang, Y., & Mazieres, D. (2013). Replication, history, and grafting in the Ori file system. In Proceedings of the Twenty-Fourth ACM Symposium on Operating Systems Principles, 151–166.

Palankar, M.R., Iamnitchi, A., Ripeanu, M., et al. (2008). Amazon S3 for science grids: a viable solution?. Proceedings of the 2008 international workshop on Data-aware distributed computing. ACM.

Ramasubramanian, V., Rodeheffer, T., Terry, D., Walraed-Sullivan, M., Wobber, T., Marshall, C. & Vahdat, A. (2009). Cimbiosys: a platform for content-based partial replication. In Proceedings of the 6th USENIX symposium on Networked systems design and implementation, NSDI’09, 261–276.

Santry, D., Feeley, M., Hutchinson, N., Veitch, A., Carton, R., & Ofir, J. (1999). Deciding when to forget in the Elephant file system. In ACM SIGOPS Operating Systems Review 33,110–123.

Zhang, Y., Dragga, C., Arpaci-Dusseau, A. & Arpaci-Dusseau, R. (2013). -box: Towards reliability and consistency in dropbox-like file synchronization services. In Proceedings of the The Fifth Workshop on Hot Topics in Storage and File Systems, HotStorage ’13, Berkeley, CA, USA. USENIX Association.
