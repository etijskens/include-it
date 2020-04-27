# -*- coding: utf-8 -*-

"""Tests for include_it package."""

import re
import include_it


def test_IncludeProject():
    """Test for include_it.hello()."""
    prj = include_it.IncludeProject(
        "/Users/etijskens/software/dev/workspace/ofpy/OpenFOAM/OpenFOAM-v1912/applications/solvers/incompressible/simpleFoam/simpleFoam.C",
        "/Users/etijskens/software/dev/workspace/ofpy/OpenFOAM/OpenFOAM-v1912"
    )
    prj.verbose = True
    count = prj.include()
    assert count == 15
    count = prj.include()
    assert count == 41


def test_iteration():
    """Test for include_it.hello()."""
    prj = include_it.IncludeProject(
        "/Users/etijskens/software/dev/workspace/ofpy/OpenFOAM/OpenFOAM-v1912/applications/solvers/incompressible/simpleFoam/simpleFoam.C",
        "/Users/etijskens/software/dev/workspace/ofpy/OpenFOAM/OpenFOAM-v1912",
        from_main=True,
    )
    prj.verbose = True
    prj.recursive_include()


def test_pattern():
    lines = [ '#include "fvCFD.H"/n',
          '\t#include "fvCFD.H"/n',
          '    #include  "fvCFD.H"/n',
          '    #include  "fvCFD.H"  /n',
          '  #include  "fvCFD.H" // comment/n',
          ]
    for l in lines:
        print(l[:-2])
        m = re.match(include_it.include_pattern,l)
        assert m[1]=="fvCFD.H"

# ==============================================================================
# The code below is for debugging a particular test in eclipse/pydev.
# (otherwise all tests are normally run with pytest)
# Make sure that you run this code with the project directory as CWD, and
# that the source directory is on the path
# ==============================================================================
if __name__ == "__main__":
    the_test_you_want_to_debug = test_iteration

    print("__main__ running", the_test_you_want_to_debug)
    the_test_you_want_to_debug()
    print('-*# finished #*-')
    
# eof