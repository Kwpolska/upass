============================
upass.  Console UI for pass.
============================
:Info: This is the README file for upass.
:Author: Chris Warrick <chris@chriswarrick.com>
:Copyright: © 2015-2017, Chris Warrick.
:Date: 2017-03-20
:Version: 0.1.9

.. image:: https://chriswarrick.com/galleries/upass/directory-listing.png

INSTALLATION
------------

::

    pip install upass

There are also AUR packages available.

USAGE
-----

Run ``upass`` and use the friendly console interface.

CONFIGURATION
-------------

upass stores its config in ``~/.config/kwpolska/upass/upass.ini`` (but it
respects ``XDG_CONFIG_HOME`` if you changed it). Available options:

* keys — keybinding configuration.
  * help, display, copy, refresh, search, quit — set key bindings for commands,
    space-separated (eg. ``quit=q f10`` will make ``q`` and ``f10`` keybindings
    for ``quit``)
  * ``uplevel_h`` — on/off, use the ``h`` key as a back button, make sure to change
    your ``help`` key bindings
  * ``downlevel_l`` — on/off, use the ``l`` key to open directory/password

COPYRIGHT
---------

Copyright © 2015-2017, Chris Warrick.
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
