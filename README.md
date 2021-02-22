dumpdir
=======

`dumpdir` dumps directory trees including file contents to a text format.
the same text can in turn be used as input to `reversedumpdir` to recreate the
directory tree including files.

example

    $ mkdir dir1
    $ mkdir dir1/dir2
    $ echo hello > dir1/dir2/file

output

    $ dumpdir.py
    d dir1
    d dir1/dir2
    f dir1/dir2/file
    > hello

`dumpdir` works best in small directory trees with small text files.
at the moment it does not handle binary files.
it also does not care about file attributes and permissions
except the executable bit.
it handles symlinks but not tested thoroughly.

license
-------

Copyright Lesmana Zimmer lesmana@gmx.de

This program is free software.
It is licensed under the GNU GPL version 3 or later.
That means you are free to use this program for any purpose;
free to study and modify this program to suit your needs;
and free to share this program or your modifications with anyone.
If you share this program or your modifications
you must grant the recipients the same freedoms.
To be more specific: you must share the source code under the same license.
For details see https://www.gnu.org/licenses/gpl-3.0.html
