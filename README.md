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
it does not handle binary files well. also it does not care about
file attributes like ownership or timestamps.

license
-------

Copyright 2017 Lesmana Zimmer lesmana@gmx.de

This program is licensed under GNU GPL version 3 or later.
That means this program can be used, changed, shared (including changes)
provided that it is done under the same license.
For details see https://www.gnu.org/licenses/gpl-3.0.html
