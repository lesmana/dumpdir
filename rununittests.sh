#! /bin/sh

export PYTHONPATH=$PWD:$PWD/unittests/helpers:$PYTHONPATH

cd unittests
./rununittests.py
