# -*- encoding: utf-8 -*-
# upass v0.2.0
# Console UI for pass.
# Copyright © 2015-2017, Chris Warrick.
# See /LICENSE for licensing information.

"""
upass user interface.

:Copyright: © 2015-2017, Chris Warrick.
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
Use up/down arrows or jk (vim-style) and Enter to navigate the directory tree.
Available commands (with default key bindings):
   d display
   s display
   c copy
   r refresh
   / search
   h help
   q quit
upass requires pass installed and in $PATH: http://www.passwordstore.org/"""


# Case folding
if sys.version_info[0] == 2:
    try:
        from py2casefold import casefold
    except ImportError:
        casefold = str.lower  # workaround
else:
    casefold = str.casefold


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

    """A back button."""

    def __init__(self, caption, callback, user_arg, app):
        """Initialize a button."""
        super(BackButton, self).__init__("")
        self.caption = caption
        urwid.connect_signal(self, 'click', callback, user_arg)
        self._w = urwid.AttrMap(urwid.SelectableIcon(
            [u'< ', self.caption], 0), 'button', 'button_reversed')
        app.back_callback = callback
        app.back_arg = user_arg


# h/t Heiko Noordhof @hkoof
class FancyListBox(urwid.ListBox):

    """A list box you can scroll in fancy ways."""

    def keypress(self, size, key):
        """Handle keypresses."""
        currentfocus = self.focus_position
        maxindex = len(self.body) - 1
        newfocus = None
        if key == 'home':
            newfocus = 0
        elif key == 'end':
            newfocus = maxindex
        elif key == 'k' and self._app.mode != 'search':
            newfocus = currentfocus - 1
        elif key == 'j' and self._app.mode != 'search':
            newfocus = currentfocus + 1
        if newfocus is not None:
            if newfocus < 0:
                newfocus = 0
            elif newfocus > maxindex:
                newfocus = maxindex
            self.set_focus(newfocus)
        return super(FancyListBox, self).keypress(size, key)

    def mouse_event(self, size, event, button, col, row, focus):
        """Handle scroll events."""
        currentfocus = self.focus_position
        newfocus = None
        maxindex = len(self.body) - 1

        if button == 4:
            newfocus = currentfocus - 3
        elif button == 5:
            newfocus = currentfocus + 3

        if newfocus is not None:
            if newfocus < 0:
                newfocus = 0
            elif newfocus > maxindex:
                newfocus = maxindex

            self.set_focus(newfocus)

        # handle clicks
        return super(FancyListBox, self).mouse_event(
            size, event, button, col, row, focus)


class App(object):

    """The upass app object."""

    palette = [
        ('header', 'white', 'dark red'),
        ('footer', 'white', 'dark blue'),
        ('footer_reversed', 'dark blue', 'white'),
        ('highlight', 'light blue', ''),
        ('error', 'light red', ''),
        ('button', 'default', ''),
        ('button_reversed', 'standout', ''),
    ]
    back_callback = None
    back_arg = None

    def __init__(self):
        """Initialize the app."""
        self.header = urwid.AttrWrap(urwid.Text(
            "upass v{0}".format(upass.__version__)), 'header')

        listbox_content = [urwid.Text('LOADING')]
        self.box = FancyListBox(urwid.SimpleFocusListWalker(listbox_content))
        self.box._app = self

        self.home = os.environ.get('PASSWORD_STORE_DIR', os.path.expanduser('~/.password-store'))
        if os.path.exists(self.home) and os.listdir(self.home):
            self.refresh()
            self.current = '.'
            self.dir_load(None, self.current)
        else:
            self._clear_box()
            self.box.body.extend([
                urwid.Text(("error", 'Your Password Store is empty.')),
                urwid.Text('Please use the `pass` command to create passwords. upass is a read-only browser.'),
                urwid.Text('Press q to exit.')])

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

        # Load keys from ini file
        ini_commands = {
            'display': self.display_selected,
            'copy': self.copy_selected,
            'refresh': self.refresh_and_reload,
            'search': self.search,
            'help': self.help,
            'quit': self.quit
        }

        self.keys = {}
        for command, handler in ini_commands.items():
            bindkeys = upass.config.get('keys', command).strip().split()
            for k in bindkeys:
                self.keys[k] = handler

        if upass.config.getboolean('keys', 'uplevel_h'):
            self.keys['h'] = self.uplevel

        if upass.config.getboolean('keys', 'downlevel_l'):
            self.keys['l'] = self.downlevel

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
            self.call_pass(originator, (path, False, None))

    def copy_selected(self, originator):
        """Copy the currently selected password."""
        path, pathg = self.get_selected_password(originator)
        if pathg in self.passwords:
            self.call_pass(originator, (path, True, False))

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
        query_cf = casefold(query)
        self.mode = 'search_results'
        self.set_header('SEARCH RESULTS FOR "{0}"'.format(query))
        results = [i for i in self.passwords if query_cf in casefold(i)]
        self._clear_box()
        self.box.body.append(BackButton('BACK', self.load_dispatch,
                                        self.current, self))
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
                                        self.current, self))
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
            self.box.body.append(BackButton('..', self.dir_load, prevdir,
                                            self))
        else:
            self.back_callback = None
        self._make_directory_buttons(new_directories)
        self._make_password_buttons(new_passwords)

    def pass_load(self, originator, path):
        """Load a password page."""
        self.set_header(path)
        self.current = path
        self.mode = 'pass_load'
        self._clear_box()
        prevdir = os.path.dirname(path) or '.'
        self.box.body.append(BackButton('BACK', self.dir_load, prevdir, self))
        self.box.body.append(ActionButton('DISPLAY', self.call_pass,
                                          (path, False, None)))
        self.box.body.append(ActionButton('COPY FIRST LINE', self.call_pass,
                                          (path, True, False)))
        self.box.body.append(ActionButton('COPY EVERYTHING', self.call_pass,
                                          (path, True, True)))
        self.box.body.append(urwid.Text("More copy options are available after displaying the password."))

    def call_pass(self, originator, args):
        """Call pass to get a password."""
        self.current, copy, copy_key = args
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
            try:
                text = stdout.decode('utf-8')
            except AttributeError:
                text = stdout

            copiable_entries = {}
            copiable_keys = []

            for index, line in enumerate(text.split('\n')):
                entry = line.split(': ', 1)
                if len(entry) > 1:
                    copiable_entries[entry[0]] = entry[1]
                    copiable_keys.append(entry[0])

            if copy:
                if copy_key is False:  # False: copy first line
                    copytarget = text.split('\n', 1)[0]
                    copy_key = 'first line'
                elif copy_key is True:  # True: copy everything
                    copytarget = text
                    copy_key = 'everything'
                else:  # string: copy whatever is passed
                    copytarget = copiable_entries[copy_key]

                pyperclip.copy(copytarget)
                self.box.body.append(
                    urwid.AttrMap(
                        urwid.Text('Copied {0} to clipboard.'.format(copy_key)),
                        'highlight'))
            else:
                self.box.body.append(urwid.Text(text.strip()))

            self.box.body.append(ActionButton('COPY FIRST LINE', self.call_pass,
                                              (self.current, True, False)))
            self.box.body.append(ActionButton('COPY EVERYTHING', self.call_pass,
                                              (self.current, True, True)))

            for k in copiable_keys:
                self.box.body.append(ActionButton('COPY {0}'.format(k), self.call_pass,
                                                  (self.current, True, k)))
        else:
            self.box.body.append(urwid.Text(('error', 'ERROR')))
            self.box.body.append(
                urwid.Text(('error', stderr.strip())))
        self.box.body.append(BackButton(
            'BACK TO DIRECTORY', self.dir_load,
            os.path.dirname(self.current) or '.', self))
        self.box.body.append(BackButton(
            'BACK TO PASSWORD', self.pass_load, self.current, self))
        if p.returncode != 0:
            self.box.set_focus(3)
        else:
            self.box.set_focus(1)

    def uplevel(self, event=None):
        """Go up one level."""
        if self.back_callback is not None:
            self.back_callback('uplevel', self.back_arg)

    def downlevel(self, event=None):
        """Go down one level."""
        b = self.box.get_focus()[0]
        b._emit('click')

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
    return App().run()

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("")
