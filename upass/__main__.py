# -*- encoding: utf-8 -*-
# upass v0.1.1
# Console UI for pass.
# Copyright © 2015, Chris Warrick.
# See /LICENSE for licensing information.

"""
upass user interface.

:Copyright: © 2015, Chris Warrick.
:License: BSD (see /LICENSE).
"""

import os
import sys
import upass
import urwid
import pyperclip
import subprocess

__all__ = ('main', 'App')
HELP = """upass is an interface for pass, the standard unix password manager.
Use arrows and Enter to navigate the directory tree.
Available commands:
   d display
   s display
   c copy
   r refresh
   / search
   h help
   q quit
upass requires pass installed and in $PATH: http://www.passwordstore.org/"""


class PasswordButton(urwid.Button):

    """A password button."""

    def __init__(self, caption, callback):
        """Initialize a button."""
        super(PasswordButton, self).__init__("")
        self.caption = caption[:-len('.gpg')]
        urwid.connect_signal(self, 'click', callback, self.caption)
        self._w = urwid.AttrMap(urwid.SelectableIcon(
            [u'├ ', self.caption], 0), 'button', 'button_reversed')


class DirectoryButton(urwid.Button):

    """An password button."""

    def __init__(self, caption, callback):
        """Initialize a button."""
        super(DirectoryButton, self).__init__("")
        self.caption = caption
        urwid.connect_signal(self, 'click', callback, self.caption)
        self._w = urwid.AttrMap(urwid.SelectableIcon(
            [u'├ ', self.caption, '/'], 0), 'button', 'button_reversed')


class ActionButton(urwid.Button):

    """An action button."""

    def __init__(self, caption, callback, user_arg=None):
        """Initialize a button."""
        super(ActionButton, self).__init__("")
        self.caption = caption
        urwid.connect_signal(self, 'click', callback, user_arg)
        self._w = urwid.AttrMap(urwid.SelectableIcon(
            [u'> ', self.caption], 0), 'button', 'button_reversed')


class BackButton(urwid.Button):

    """An action button."""

    def __init__(self, caption, callback, user_arg=None):
        """Initialize a button."""
        super(BackButton, self).__init__("")
        self.caption = caption
        urwid.connect_signal(self, 'click', callback, user_arg)
        self._w = urwid.AttrMap(urwid.SelectableIcon(
            [u'< ', self.caption], 0), 'button', 'button_reversed')


class App(object):

    """The upass app object."""

    palette = [
        ('header', 'white', 'dark red'),
        ('footer', 'white', 'dark blue'),
        ('footer_reversed', 'standout', 'dark blue'),
        ('highlight', 'light cyan', ''),
        ('error', 'light red', ''),
        ('button', 'white', ''),
        ('button_reversed', 'standout', ''),
    ]

    def __init__(self):
        """Initialize the app."""
        self.header = urwid.AttrWrap(urwid.Text(
            "upass v{0}".format(upass.__version__)), 'header')

        listbox_content = [urwid.Text('LOADING')]
        self.box = urwid.ListBox(urwid.SimpleFocusListWalker(listbox_content))

        self.home = os.path.expanduser('~/.password-store')
        self.refresh()
        self.current = '.'
        self.dir_load(None, self.current)

        column_data = [
            urwid.Button('DiSplay', self.display_selected),
            urwid.Button('Copy', self.copy_selected),
            urwid.Button('Refresh', self.refresh_and_reload),
            urwid.Button('/search', self.search),
            urwid.Button('Help', self.help),
            urwid.Button('Quit', self.quit),
        ]
        column_data = [urwid.AttrWrap(i, 'footer', 'footer_reversed')
                       for i in column_data]

        self.footer = urwid.Columns(column_data)

        self.keys = {
            'd': self.display_selected,
            's': self.display_selected,
            'c': self.copy_selected,
            'r': self.refresh_and_reload,
            '/': self.search,
            'h': self.help,
            '?': self.help,
            'q': self.quit,
            'f10': self.quit,  # unadvertised backup
        }

        self.frame = urwid.Frame(self.box, header=self.header,
                                 footer=self.footer)
        self.loop = urwid.MainLoop(self.frame, self.palette,
                                   unhandled_input=self._unhandled)

    def _unhandled(self, key):
        """Handle unhandled input."""
        try:
            key = key.lower()
            # string == keyboard input
            if key in self.keys:
                self.keys[key]('unhandled')
            elif key == 'tab':
                if self.frame.focus_position == 'body':
                    self.frame.focus_position = 'footer'
                elif self.frame.focus_position == 'footer':
                    self.frame.focus_position = 'body'
            elif self.mode == 'search' and key == 'enter':
                self.search_results('unhandled')
        except AttributeError:
            # tuple == mouse event
            pass

    def refresh(self):
        """Refresh the passwords."""
        self.directories = []
        self.passwords = []
        self.recurse(self.home, '')
        self.topdir_passwords = [i for i in os.listdir(self.home)
                                 if not i.startswith('.') and
                                 i not in self.directories]

    def refresh_and_reload(self, originator):
        """Refresh the passwords and rebuild the directory listing."""
        self.refresh()
        self.load_dispatch(originator, self.current)

    def get_selected_password(self, originator):
        """Get the currently selected password."""
        if self.mode in ('dir_load', 'search_results'):
            path = self.box.focus.caption
        elif self.mode in ('pass_load', 'call_pass'):
            path = self.current
        else:
            return None, None
        pathg = path + '.gpg'
        return path, pathg

    def display_selected(self, originator):
        """Display the currently selected password."""
        path, pathg = self.get_selected_password(originator)
        if pathg in self.passwords:
            self.call_pass(originator, (path, False))

    def copy_selected(self, originator):
        """Copy the currently selected password."""
        path, pathg = self.get_selected_password(originator)
        if pathg in self.passwords:
            self.call_pass(originator, (path, True))

    def search(self, originator):
        """Display the search box."""
        if self.mode == 'search':
            self.load_dispatch(originator, self.current)
            return
        self.mode = 'search'
        self.set_header('SEARCH')
        self._clear_box()
        self.search_input = urwid.Edit(("highlight", "Keyword: "))
        self.box.body.append(self.search_input)
        self.box.body.append(ActionButton('SEARCH', self.search_results))

    def search_results(self, originator):
        """Display the search results."""
        query = self.search_input.text[len("Keyword: "):]
        self.mode = 'search_results'
        self.set_header('SEARCH RESULTS FOR "{0}"'.format(query))
        results = [i for i in self.passwords if query in i]
        self._clear_box()
        self.box.body.append(BackButton('BACK', self.load_dispatch,
                                        self.current))
        self._make_password_buttons(results)

    def help(self, originator):
        """Display help."""
        if self.mode == 'help':
            self.load_dispatch(originator, self.current)
            return
        self.mode = 'help'
        self.set_header('HELP')
        self._clear_box()
        self.box.body.append(urwid.Text(HELP))
        self.box.body.append(BackButton('BACK', self.load_dispatch,
                                        self.current))
        self.box.set_focus(1)
        self.frame.focus_position = 'body'

    def quit(self, originator):
        """Quit the program."""
        raise urwid.ExitMainLoop()

    def recurse(self, home, subdir):
        """Recurse into directories."""
        path = os.path.join(home, subdir)
        for i in os.listdir(path):
            name = os.path.join(subdir, i)
            if i.startswith('.'):
                continue
            elif os.path.isdir(os.path.join(path, i)):
                self.directories.append(name)
                self.recurse(home, name)
            else:
                self.passwords.append(name)

    def set_header(self, text):
        """Set the header (title bar) text."""
        self.header.base_widget.set_text('[upass v{1}] {0}'.format(
            text, upass.__version__))

    def load_dispatch(self, originator, name):
        """Intelligently load a directory or a password page."""
        if name == '.' or name in self.directories:
            self.dir_load(originator, name)
        else:
            self.pass_load(originator, name)

    def dir_load(self, originator, dirname):
        """Load a directory."""
        self.set_header(dirname)
        self.current = dirname
        self.mode = 'dir_load'

        if dirname == '.':
            new_directories = self.directories
            new_passwords = self.topdir_passwords
        else:
            dirnames = dirname + '/'
            new_directories = [i for i in self.directories
                               if i.startswith(dirnames)]
            new_passwords = [i for i in self.passwords
                             if i.startswith(dirnames)]
        self._clear_box()
        if dirname != '.':
            prevdir = os.path.normpath(dirname + '/..')
            self.box.body.append(BackButton('..', self.dir_load, prevdir))
        self._make_directory_buttons(new_directories)
        self._make_password_buttons(new_passwords)

    def pass_load(self, originator, path):
        """Load a password page."""
        self.set_header(path)
        self.current = path
        self.mode = 'pass_load'
        self._clear_box()
        prevdir = os.path.dirname(path) or '.'
        self.box.body.append(BackButton('BACK', self.dir_load, prevdir))
        self.box.body.append(ActionButton('DISPLAY', self.call_pass,
                                          (path, False)))
        self.box.body.append(ActionButton('COPY', self.call_pass,
                                          (path, True)))

    def call_pass(self, originator, args):
        """Call pass to get a password."""
        self.current, copy = args
        self.set_header(self.current)
        pargs = ['pass', self.current]
        copymsg = ' and copying output afterwards' if copy else ''
        self.mode = 'call_pass'
        self._clear_box()
        self.box.body.append(urwid.AttrMap(
            urwid.Text('Calling {0}{1}'.format(' '.join(pargs), copymsg)),
            'highlight'))
        self.loop.draw_screen()
        p = subprocess.Popen(pargs, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        if p.returncode == 0:
            self._clear_box()
            self.box.body.append(urwid.Text(stdout.strip()))
            if copy:
                try:
                    copytarget = stdout.decode('utf-8')
                except AttributeError:
                    copytarget = stdout
                copytarget = copytarget.split('\n', 1)[0]
                pyperclip.copy(copytarget)
                self.box.body.append(
                    urwid.AttrMap(
                        urwid.Text('Copied to clipboard.'), 'highlight'))
            else:
                self.box.body.append(ActionButton('COPY', self.call_pass,
                                                  (self.current, True)))
        else:
            self.box.body.append(urwid.Text(('error', 'ERROR')))
            self.box.body.append(
                urwid.Text(('error', stderr.strip())))
        self.box.body.append(BackButton(
            'BACK TO DIRECTORY', self.dir_load,
            os.path.dirname(self.current) or '.'))
        self.box.body.append(BackButton(
            'BACK TO PASSWORD', self.pass_load, self.current))
        if p.returncode != 0:
            self.box.set_focus(3)
        elif copy:
            self.box.set_focus(2)
        else:
            self.box.set_focus(1)

    def _make_directory_buttons(self, new_directories):
        """Add directory buttons to the box."""
        for i in new_directories:
            self.box.body.append(DirectoryButton(i, self.dir_load))

    def _make_password_buttons(self, new_passwords):
        """Add password buttons to the box."""
        for i in new_passwords:
            self.box.body.append(PasswordButton(i, self.pass_load))

    def _clear_box(self):
        del self.box.body[:]

    def run(self):
        """Run the loop."""
        self.loop.run()


def main():
    """The main function of upass."""
    App().run()

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("")
