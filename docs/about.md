# About Cultivar     

Cultivar is a dataset management, analysis and visualization tool that is being built as part of the DDL Multidimensional Visualization Research Lab. See: [Parallel Coordinates](http://homes.cs.washington.edu/~jheer//files/zoo/ex/stats/parallel.html) for more on the types of visualizations we're experimenting with.

## Contributing

Cultivar is open source, but because this is an District Data Labs project, we would appreciate it if you would let us know how you intend to use the software (other than simply copying and pasting code so that you can use it in your own projects). If you would like to contribute (especially if you are a student or research labs member at District Data Labs), you can do so in the following ways:

1. Add issues or bugs to the bug tracker: [https://github.com/DistrictDataLabs/Cultivar/issues](https://github.com/DistrictDataLabs/Cultivar/issues)
2. Work on a card on the dev board: [https://waffle.io/DistrictDataLabs/Cultivar](https://waffle.io/DistrictDataLabs/Cultivar)
3. Create a pull request in Github: [https://github.com/DistrictDataLabs/Cultivar/pulls](https://github.com/DistrictDataLabs/Cultivar/pulls)

Note that labels in the Github issues are defined in the blog post: [How we use labels on GitHub Issues at Mediocre Laboratories](https://mediocre.com/forum/topics/how-we-use-labels-on-github-issues-at-mediocre-laboratories).

If you are a member of the District Data Labs Faculty group, you have direct access to the repository, which is set up in a typical production/release/development cycle as described in _[A Successful Git Branching Model](http://nvie.com/posts/a-successful-git-branching-model/)_. A typical workflow is as follows:

1. Select a card from the [dev board](https://waffle.io/DistrictDataLabs/Cultivar) - preferably one that is "ready" then move it to "in-progress".

2. Create a branch off of develop called "feature-[feature name]", work and commit into that branch.

        ~$ git checkout -b feature-myfeature develop

3. Once you are done working (and everything is tested) merge your feature into develop.

        ~$ git checkout develop
        ~$ git merge --no-ff feature-myfeature
        ~$ git branch -d feature-myfeature
        ~$ git push origin develop

4. Repeat. Releases will be routinely pushed into master via release branches, then deployed to the server.

## Contributors

Thank you for all your help contributing to make Cultivar a great project!

### Maintainers

- Benjamin Bengfort: [@bbengfort](https://github.com/bbengfort/)
- Rebecca Bilbro: [@rebeccabilbro](https://github.com/rebeccabilbro)

### Contributors

- Tony Ojeda: [@ojedatony1616](https://github.com/ojedatony1616)

## Changelog

The release versions that are sent to the Python package index (PyPI) are also tagged in Github. You can see the tags through the Github web application and download the tarball of the version you'd like. Additionally PyPI will host the various releases of Cultivar (eventually).

The versioning uses a three part version system, "a.b.c" - "a" represents a major release that may not be backwards compatible. "b" is incremented on minor releases that may contain extra features, but are backwards compatible. "c" releases are bug fixes or other micro changes that developers should feel free to immediately update to.

### Version 0.2

* **tag**: [v0.2](https://github.com/DistrictDataLabs/Cultivar/releases/tag/v0.2)
* **deployment**: Wednesday, January 27, 2016
* **commit**: (see tag)

This minor update gave a bit more functionality to the MVP prototype, even though the version was intended to have a much more impactful feature set. However after some study, the workflow is changing, and so this development branch is being pruned and deployed in preparation for the next batch. The major achievement of this version is the documentation that discusses our approach, as well as the dataset search and listing page that is now available. 

### Version 0.1

* **tag**: [v0.1](https://github.com/DistrictDataLabs/Cultivar/releases/tag/v0.1)
* **deployment**: Tuesday, October 13, 2015
* **commit**: [c863e42](https://github.com/DistrictDataLabs/Cultivar/commit/c863e421292be4eaeab36a9233f6ed7e0068679b)

MVP prototype type of a dataset uploader and management application. This application framework will become the basis for the research project in the DDL Multidimensional Visualization Research Labs. For now users can upload datasets, and manage their description, as well as preview the first 20 rows.
