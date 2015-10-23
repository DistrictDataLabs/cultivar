# Trinket
**Multidimensional data explorer and visualization tool.**

[![Build Status][travis_img]][travis_href]
[![Coverage Status][coveralls_img]][coverals_href]
[![Stories in Ready][waffle_img]][waffle_href]

[![Colorful Wall](docs/img/wall.jpg)][wall.jpg]

## About

This is a dataset management and visualization tool that is being built as part of the DDL Multidimensional Visualization Research Lab. See: [Parallel Coordinates](http://homes.cs.washington.edu/~jheer//files/zoo/ex/stats/parallel.html) for more on the types of visualizations we're experimenting with.

### Contributing

Trinket is open source, but because this is an District Data Labs project, we would appreciate it if you would let us know how you intend to use the software (other than simply copying and pasting code so that you can use it in your own projects). If you would like to contribute (especially if you are a student or research labs member at District Data Labs), you can do so in the following ways:

1. Add issues or bugs to the bug tracker: [https://github.com/DistrictDataLabs/trinket/issues](https://github.com/DistrictDataLabs/trinket/issues)
2. Work on a card on the dev board: [https://waffle.io/DistrictDataLabs/trinket](https://waffle.io/DistrictDataLabs/trinket)
3. Create a pull request in Github: [https://github.com/DistrictDataLabs/trinket/pulls](https://github.com/DistrictDataLabs/trinket/pulls)

Note that labels in the Github issues are defined in the blog post: [How we use labels on GitHub Issues at Mediocre Laboratories](https://mediocre.com/forum/topics/how-we-use-labels-on-github-issues-at-mediocre-laboratories).

If you are a member of the District Data Labs Faculty group, you have direct access to the repository, which is set up in a typical production/release/development cycle as described in _[A Successful Git Branching Model](http://nvie.com/posts/a-successful-git-branching-model/)_. A typical workflow is as follows:

1. Select a card from the [dev board](https://waffle.io/DistrictDataLabs/trinket) - preferably one that is "ready" then move it to "in-progress".

2. Create a branch off of develop called "feature-[feature name]", work and commit into that branch.

        ~$ git checkout -b feature-myfeature develop

3. Once you are done working (and everything is tested) merge your feature into develop.

        ~$ git checkout develop
        ~$ git merge --no-ff feature-myfeature
        ~$ git branch -d feature-myfeature
        ~$ git push origin develop

4. Repeat. Releases will be routinely pushed into master via release branches, then deployed to the server.

### Attribution

The image used in this README, ["window#1"][wall.jpg] by [Namelas Frade](https://www.flickr.com/photos/zingh/) is licensed under [CC BY-NC-ND 2.0](https://creativecommons.org/licenses/by-nc-nd/2.0/)

<!-- References -->
[travis_img]: https://travis-ci.org/DistrictDataLabs/trinket.svg?branch=master
[travis_href]: https://travis-ci.org/DistrictDataLabs/trinket
[coveralls_img]: https://coveralls.io/repos/DistrictDataLabs/trinket/badge.svg?branch=master&service=github
[coverals_href]: https://coveralls.io/github/DistrictDataLabs/trinket?branch=master
[waffle_img]: https://badge.waffle.io/DistrictDataLabs/trinket.png?label=ready&title=Ready
[waffle_href]: https://waffle.io/DistrictDataLabs/trinket
[wall.jpg]: https://flic.kr/p/75C2ac
