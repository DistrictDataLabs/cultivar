# Trinket
**Multidimensional data explorer and visualization tool.**

[![Build Status][travis_img]][travis_href]
[![Coverage Status][coveralls_img]][coverals_href]
[![Documentation Status][rtfd_img]][rtfd_href]
[![Stories in Ready][waffle_img]][waffle_href]

[![Colorful Wall](docs/images/wall.jpg)][wall.jpg]

## About

This is a dataset management and visualization tool that is being built as part of the DDL Multidimensional Visualization Research Lab. See: [Parallel Coordinates](http://homes.cs.washington.edu/~jheer//files/zoo/ex/stats/parallel.html) for more on the types of visualizations we're experimenting with.

For more information, please enjoy the documentation found at [trinket.readthedocs.org](http://trinket.readthedocs.org/).

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

### Initial Setup (Mac OS X)

1. Clone the repository to your local computer.  To clone from the command line (instead of a windowed application) use the following bash command.  If you are cloning a forked copy then you will need to update the repository address.

```
git clone git@github.com:DistrictDataLabs/trinket.git
```

2. Install required services.  Trinket relies on PostgreSQL for the database layer and so please ensure that a recent version is installed and running.  If using a Mac, we recommend the excellent [PostgresApp](http://postgresapp.com/)

3. (Optional) Create and install your python virtual environment.  The bash commands below are provided as an example.

```
git checkout develop
virtualenv env
source env/bin/activate
```

4. Install the dependency libraries using the provided `requirements.txt` file.  The bash command is provided below:

```
pip install -r requirements.txt
```

5. Create the needed environment variables in the `.env` file.  `.env` files allow you to easily specify the environmental variables which Trinket requires for execution.

```
vim .env
```

The contents of the `.env` should be:

```
DJANGO_SETTINGS_MODULE=trinket.settings.development
SECRET_KEY=[INSERT A VALUE HERE]
EMAIL_HOST_USER=[INSERT A VALUE HERE]
EMAIL_HOST_PASSWORD=[INSERT A VALUE HERE]
```

6. Run `python manage.py runserver` and go to http://localhost:8000.  Optionally, you can use the Makefile by executing `make runserver` from the command line.

### Throughput

[![Throughput Graph](https://graphs.waffle.io/DistrictDataLabs/trinket/throughput.svg)](https://waffle.io/DistrictDataLabs/trinket/metrics)

### Attribution

The image used in this README, ["window#1"][wall.jpg] by [Namelas Frade](https://www.flickr.com/photos/zingh/) is licensed under [CC BY-NC-ND 2.0](https://creativecommons.org/licenses/by-nc-nd/2.0/)

## Changelog

The release versions that are sent to the Python package index (PyPI) are also tagged in Github. You can see the tags through the Github web application and download the tarball of the version you'd like. Additionally PyPI will host the various releases of Trinket (eventually).

The versioning uses a three part version system, "a.b.c" - "a" represents a major release that may not be backwards compatible. "b" is incremented on minor releases that may contain extra features, but are backwards compatible. "c" releases are bug fixes or other micro changes that developers should feel free to immediately update to.

### Version 0.2

* **tag**: [v0.2](https://github.com/DistrictDataLabs/trinket/releases/tag/v0.2)
* **deployment**: Wednesday, January 27, 2016
* **commit**: (see tag)

This minor update gave a bit more functionality to the MVP prototype, even though the version was intended to have a much more impactful feature set. However after some study, the workflow is changing, and so this development branch is being pruned and deployed in preparation for the next batch. The major achievement of this version is the documentation that discusses our approach, as well as the dataset search and listing page that is now available.

### Version 0.1

* **tag**: [v0.1](https://github.com/DistrictDataLabs/trinket/releases/tag/v0.1)
* **deployment**: Tuesday, October 13, 2015
* **commit**: [c863e42](https://github.com/DistrictDataLabs/trinket/commit/c863e421292be4eaeab36a9233f6ed7e0068679b)

MVP prototype type of a dataset uploader and management application. This application framework will become the basis for the research project in the DDL Multidimensional Visualization Research Labs. For now users can upload datasets, and manage their description, as well as preview the first 20 rows.

<!-- References -->
[travis_img]: https://travis-ci.org/DistrictDataLabs/trinket.svg?branch=master
[travis_href]: https://travis-ci.org/DistrictDataLabs/trinket
[coveralls_img]: https://coveralls.io/repos/DistrictDataLabs/trinket/badge.svg?branch=master&service=github
[coverals_href]: https://coveralls.io/github/DistrictDataLabs/trinket?branch=master
[waffle_img]: https://badge.waffle.io/DistrictDataLabs/trinket.png?label=ready&title=Ready
[waffle_href]: https://waffle.io/DistrictDataLabs/trinket
[rtfd_img]: https://readthedocs.org/projects/trinket/badge/?version=latest
[rtfd_href]: http://trinket.readthedocs.org/en/latest/?badge=latest
[wall.jpg]: https://flic.kr/p/75C2ac
