# -*- encoding: utf-8 -*-
# upass v0.2.0
# Console UI for pass.
# Copyright © 2015-2017, Chris Warrick.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions, and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions, and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the author of this software nor the names of
#    contributors to this software may be used to endorse or promote
#    products derived from this software without specific prior written
#    consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Console UI for pass.

:Copyright: © 2015-2017, Chris Warrick.
:License: BSD (see /LICENSE).
"""

import os
import pkg_resources
import configparser

__title__ = 'upass'
__version__ = '0.2.0'
__author__ = 'Chris Warrick'
__license__ = '3-clause BSD'
__docformat__ = 'restructuredtext en'

__all__ = ('config',)


# Config directory setup
confhome = os.getenv('XDG_CONFIG_HOME')
if confhome is None:
    confhome = os.path.expanduser('~/.config/')

kwdir = os.path.join(confhome, 'kwpolska')
confdir = os.path.join(kwdir, 'upass')
confpath = os.path.join(confdir, 'upass.ini')

if not os.path.exists(confhome):
    os.mkdir(confhome)
if not os.path.exists(kwdir):
    os.mkdir(kwdir)
if not os.path.exists(confdir):
    os.mkdir(confdir)

if not os.path.exists(confpath):
    print("upass.ini does not exist, creating")
    with open(confpath, 'wb') as fh:
        fh.write(pkg_resources.resource_string(
            'upass', 'data/upass.ini.skel'))
    print("created " + confpath)

# Configuration file support
config = configparser.ConfigParser()
config.read_string(pkg_resources.resource_string(
            'upass', 'data/upass.ini.skel').decode('utf-8'))
config.read([confpath], encoding='utf-8')
