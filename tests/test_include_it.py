# -*- coding: utf-8 -*-

"""Tests for include_it package."""

import re
import include_it
from pathlib import Path
from datetime import date

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


def test_main():
    """Test for include_it.hello()."""
    prj = include_it.IncludeProject(
        "/Users/etijskens/software/dev/workspace/ofpy/OpenFOAM/OpenFOAM-v1912/applications/solvers/incompressible/simpleFoam/simpleFoam.C",
        "/Users/etijskens/software/dev/workspace/ofpy/OpenFOAM/OpenFOAM-v1912",
        from_main=True,
    )
    prj.verbose = True
    prj.recursive_include()


def test_full():
    """Test for include_it.hello()."""
    prj = include_it.IncludeProject(
        "/Users/etijskens/software/dev/workspace/ofpy/OpenFOAM/OpenFOAM-v1912/applications/solvers/incompressible/simpleFoam/simpleFoam.C",
        "/Users/etijskens/software/dev/workspace/ofpy/OpenFOAM/OpenFOAM-v1912",
    )
    prj.verbose = True
    prj.recursive_include()


def test_include_pattern():
    lines = [ '#include "fvCFD.H"\n',
          '\t#include "fvCFD.H"\n',
          '    #include  "fvCFD.H"\n',
          '    #include  "fvCFD.H"  \n',
          '  #include  "fvCFD.H" // comment\n',
          ]
    for l in lines:
        print(l[:-1])
        m = re.match(include_it.include_pattern,l)
        assert m[1]=="fvCFD.H"

def test_include_pattern2():
    lines = ['#include INCLUDE_FILE(NAME)\n',
        '\t#include  INCLUDE_FILE(NAME) \n',
        ]
    for l in lines:
        print(l[:-1])
        m = re.match(include_it.include_pattern2,l)
        assert m[1]=="NAME"

def test_define_pattern():
    lines = ['#define NAME1 NAME2 \n',
        ]
    for l in lines:
        print(l[:-2])
        m = re.match(include_it.define_pattern,l)
        print(m)
        assert m[1]=="NAME1"
        assert m[2]=="NAME2"

def check_start_inserting_again(line):
    return line.endswith("<http://www.gnu.org/licenses/>.\n")

def test_split():
    p = Path("/Users/etijskens/software/dev/workspace/ofpy/OpenFOAM/OpenFOAM-v1912/applications/solvers/incompressible/simpleFoam")
    pin = p / "include-it-up-to-main.simpleFoam.C"
    # this file has almoast 200000 lines. it is too big for PyCharm to handle. therefor we split it here
    print(f"reading {pin}")
    with pin.open() as f:
        lines = f.readlines()
    lines2 = []
    myline = f"** ET:{date.today()}: removed non-informative part of the openfoam header **\n"
    inserting = True
    l = 0
    while l < len(lines):
        line = lines[l]
        if line.startswith("  =========                 |\n"):
            inserting = False
            lines2.append(myline)
        if not inserting and check_start_inserting_again(line):
            l += 2
            line = lines[l]
            print(line)
            inserting = True
        if inserting:
            lines2.append(line)
        print(l,inserting)
        l += 1

    lines = lines2
    pout = p / "include-it-up-to-main-1.simpleFoam.C"
    print(f"writing {pout}")
    with pout.open(mode="w") as f:
        f.writelines(lines[:60000])
    pout = p / "include-it-up-to-main-2.simpleFoam.C"
    print(f"writing {pout}")
    with pout.open(mode="w") as f:
        f.writelines(lines[60000:120000])
    pout = p / "include-it-up-to-main-3.simpleFoam.C"
    print(f"writing {pout}")
    with pout.open(mode="w") as f:
        f.writelines(lines[120000:])

# ==============================================================================
# The code below is for debugging a particular test in eclipse/pydev.
# (otherwise all tests are normally run with pytest)
# Make sure that you run this code with the project directory as CWD, and
# that the source directory is on the path
# ==============================================================================
if __name__ == "__main__":
    the_test_you_want_to_debug = test_main

    print("__main__ running", the_test_you_want_to_debug)
    the_test_you_want_to_debug()
    print('-*# finished #*-')
    
# eof