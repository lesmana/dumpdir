dumpdir
=======

`dumpdir` dumps directory trees including file contents to a text format.
the same text can in turn be used as input to `reversedumpdir` to recreate the
directory tree including files.

example in some git repository refs dir:

    $ cd .git/refs
    $ dumpdir
    d heads
    f heads/master
    > 4591bc27978a558e6b3904c8d3dbe9b7e688931f
    d remotes
    d remotes/origin
    f remotes/origin/HEAD
    > ref: refs/remotes/origin/master
    f remotes/origin/master
    > 4591bc27978a558e6b3904c8d3dbe9b7e688931f
    d tags

compare with `tree`:

    $ tree
    .
    ├── heads
    │   └── master
    ├── remotes
    │   └── origin
    │       ├── HEAD
    │       └── master
    └── tags

    4 directories, 3 files

`dumpdir` works best in small directory trees with small text files.
it does not handle binary files well. also it does not care about
file attributes like ownership or timestamps.
