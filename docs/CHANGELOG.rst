=====================
Appendix C. Changelog
=====================
:Info: This is the changelog for upass.
:Author: Chris Warrick <chris@chriswarrick.com>
:Copyright: © 2015-2018, Chris Warrick.
:License: BSD (see /LICENSE or :doc:`Appendix B <LICENSE>`.)
:Date: 2018-08-28
:Version: 0.3.0

.. index:: CHANGELOG

GitHub holds releases, too
==========================

More information can be found on GitHub in the `releases section
<https://github.com/Kwpolska/upass/releases>`_.

Version History
===============

0.3.0
    * Add password generation (by Patrick Schneeweis)

0.2.1
    * Also show “no passwords” error message if only dotfiles exist (fix #19)

0.2.0
    More granular copying features: users can now choose between copying the first line (old default), copying the entire text, or copying specific fields that are separated with ``: `` (colon, space).

0.1.10
    * Respect ``PASSWORD_STORE_DIR`` environment variable (if it’s set)

0.1.9
    * Include missing data files

0.1.8
    * Universal color scheme (for dark and light terminals)
    * Restore Python 2 compatibility

0.1.7
    * Fix mouse support (Issue #13)

0.1.6
    * fix setup.py/MANIFEST.in

0.1.5
    * Warn if store is empty or does not exist (Issue #5)

0.1.4
    * Add j/k support for moving in the list (Issue #4)

0.1.3
    * Don’t show copied passwords (Issue #3)

0.1.2
    * Add mouse wheel support.

0.1.1
    * Fix search form
    * Fix top-level passwords appearing twice
    * Fix d/s/c for directory listings
    * Allow d/s/c keys in password display mode
    * Copy only the first line of multiline passwords

0.1.0
    Initial release.
