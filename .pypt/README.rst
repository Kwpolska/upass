===============================================
Python Project Template.  INSERT TAGLINE HERE.™
===============================================
:Info: This is the README file for the Python Project Template.
:Author: Chris Warrick <chris@chriswarrick.com>
:Copyright: © 2013-2015, Chris Warrick.
:Date: 2015-07-03
:Version: 1.3.1

.. index: README
.. image:: https://travis-ci.org/Kwpolska/python-project-template.png?branch=master

USING THE TEMPLATE
------------------

Requirements
============

* ``zsh`` installed (required by ``/release`` and ``/.pypt/localegen`` scripts)
* Python with ``requests`` (required by ``/.pypt/{commitlog,ghrel}``) and ``twine`` (required by ``/release``) installed
* `git-flow extensions by nvie <https://github.com/nvie/gitflow>`_ (alternatively yo can manually alter the ``/release`` script, and that is much harder than
  installing the extensions)
* A git repository.  The PyPT is ready to go if you use GitHub.  If you do not
  want GitHub, edit the ``/PKGBUILD{,-2}{,-git}`` files and any other places
  where GitHub is mentioned, including this document which you should edit
  mentally.

Recommended possessions
=======================

* Travis CI account (if you do not want Travis CI, remove ``/.travis.yml``)

Contents
========

The template contains the following files to get you started:

* pre-configured Sphinx with:

  * ``CONTRIBUTING.rst`` guide (used by GitHub when sending a pull request or an issue)
  * ``LICENSE.rst``
  * an empty ``CHANGELOG.rst``
  * this (worthless for most people) ``README.rst`` and a bare-bones ``index.rst`` page

* The exact same files in ``/``, which are fragile and **MAY NOT** be modified
  as they are replaced with copies in ``/docs`` by the ``release``
  script
* ``__init__.py`` and ``template.py`` files in the Python package directory
* A good-enough ``setup.py`` file
* ``tests/`` containing some *Is My Python Sane?*-style tests (using ``py.test``)
* An automated global update script (``.pypt/PYPT-UPDATE``)
* Entry points configuration ready to be uncommented
* Addons for Qt users
* PKGBUILDs for the Arch Linux User Repository (AUR)
* A state-of-the-art ``release`` script, the operations of which are:

  * querying the current branch for version number
  * updating ``/docs/CHANGELOG.rst``
  * bumping the version number in all the files, changing dates where necessary
  * copying over ``/docs/README.rst``,  ``/docs/CHANGELOG.rst`` and ``/docs/CONTRIBUTING.rst`` to ``/``
  * locale generation (via the ``.pypt/localegen`` script)
  * running ``import $project`` and the testsuite
  * uploading a source distribution and a wheel to PyPI
  * committing into git, finishing the ``git flow`` release
  * creating a GitHub Releases entry

Getting up to speed in 16 easy steps
====================================

1. Create the repository for the project on GitHub and enable it on Travis CI.
2. Manually change ``Kwpolska`` to your GitHub name in the following files:

   1. ``/docs/README.rst``, line 10
   2. ``/docs/CHANGELOG.rst``, line 10
   3. ``/setup.py``, line 14
   4. ``/PKGBUILD{,-2}{,-git}``, in ``url`` and ``source`` (git only)

3. Manually change the ``Maintainer`` line in ``/PKGBUILD{,-2}{,-git}``.
4. Replace the following patterns (eg. with sed), in all files, **excluding
   dotfiles**:

   1. ``TEMPLATE`` with the full name of the project
   2. ``tEmplate`` with a “light” name of the project [a-z0-9\_\\-], which will
      be used in the PyPI, AUR, and a few other places.  You can use capital
      letters if you feel like it, but it is discouraged and was not tested.
   3. ``python-project-template`` with the GitHub repo name
   4. ``INSERT TAGLINE HERE.`` with a tagline of your choice
   5. ``chris@chriswarrick.com`` with your e-mail address
   6. ``Kwpolska`` and/or ``Chris Warrick`` with your name (affects mostly copyright notices)

   WARNING: some files are in the copyright of Chris Warrick and must stay this
   way!  They are listed in the license, please keep my name there, otherwise
   you risk breaking the law.

4. Rename ``/tEmplate`` to the name used in 4.2.
5. Modify ``/docs/README.rst`` to reflect your project and not the Template
   (and make a copy if you are reading it locally from those files)
6. Copy: (when using the included ``release`` script, it happens automatically)

   1. ``/docs/README.rst`` to ``/README.rst`` and ``/README``
   2. ``/docs/CHANGELOG.rst`` to ``/CHANGELOG.rst``

7. Modify ``/.pypt/config``.
8. Generate a `GitHub Personal Access Token <https://github.com/settings/tokens>`_ and write it to a ``/.pypt/gh-token`` file.
9. Customize ``/setup.py`` to your liking.  You should pay attention to the
   classifiers and the commented parts.
10. Customize ``requirements.txt``.
11. If you are using PyQt4 or PySide, make sure to put your UI code in a ``ui``
    submodule.  Copy over the ``/QT-ADDONS/resources.py`` file to that
    submodule, even if you are not using resources now.
12. Remove the ``/QT-ADDONS/`` directory.
13. If you are using Qt, make sure to create a ``.pro`` file with your sources
    and locales.
14. Read the COPYRIGHT section below (or ``LICENSE.PyPT``) and remove
    ``/LICENSE.PyPT`` and ``/README.PyPT``.  If you believe the BSD license presented by the
    ``/LICENSE`` file is not the license you want, here is a list of files you
    should modify:

    1. ``/tests.py``
    2. Everything in the Python package directory (twice in many cases)
    3. Everything in ``/docs``
    4. ``/LICENSE``, which is **not** equivalent to ``/docs/LICENSE.rst``

    PS. GNU GPL is not a good idea.  You can use it, but the world would be
    much happier if you did not.

15. If you have a ``PYPT-UPDATE`` script, add your new project to the list
    there.  If not, you may want to copy it from ``.pypt`` and set it up.
16. Run the following commands::

        rm -rf .git .pypt/PYPT-UPDATE
        source .pypt/config
        git init
        git remote add origin git@github.com:$GITUSER/$GITREPO
        git flow init #(change version tag prefix to `v`)
        git add *
        git checkout develop
        git commit -sm 'initial commit via @Kwpolska’s Python Project Template'
        git checkout master
        git merge --ff-only develop
        git push -u origin master develop

COPYRIGHT
---------

Python Project Template is licensed under a BSD-like license.  You are free to
relicense your code to another open source license.  If you want to apply a
commercial (a.k.a. proprietary) license, you must contact me first.

**However, the following files must remain under the BSD license:**

* /.pypt/commitlog
* /.pypt/ghrel
* /.pypt/localegen
* /.pypt/PYPT-UPDATE
* /.pypt/README.rst
* /.pypt/LICENSE.PyPT
* /docs/CONTRIBUTING.rst
* /CONTRIBUTING.rst
* /release

**This README file MAY NOT be relicensed.**

Copyright © 2013-2015, Chris Warrick.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

1. Redistributions of source code must retain the above copyright
   notice, this list of conditions, and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions, and the following disclaimer in the
   documentation and/or other materials provided with the distribution.

3. Neither the name of the author of this software nor the names of
   contributors to this software may be used to endorse or promote
   products derived from this software without specific prior written
   consent.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
