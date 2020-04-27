# -*- coding: utf-8 -*-
"""
Package include_it
==================

A 'hello world' example.
"""
__version__ = "0.0.0"

from pathlib import Path
from shutil import copyfile
import re
import os

include_pattern = re.compile(r"^\s*#include\s+\"([a-zA-Z0-9._\-]*)\"")

class IncludeProject:
    """
    
    """
    def __init__(self, file_path, search_path, from_main=False):
        """

        :param file_path: path to file on which recursive includes are to be performed
        :param search_path: path to a directory where to search for include files
        :param bool from_main: only treate include files appearing after the line with "int main(...)"
        """
        self.file_path = Path(file_path)
        self.search_paths = [self.file_path.parent, Path(search_path)]
        self.verbose = False
        self.from_main = from_main

        self.create_output_file()

    def create_output_file(self):
        prefix = "main-include-it." if self.from_main else "full-include-it."
        result_name =  prefix + self.file_path.name
        self.result_path = self.file_path.parent / result_name
        copyfile(self.file_path, self.result_path) # destination will be replaced if it exists.

        with self.result_path.open() as f:
            self.result = f.readlines()

        self.include_files = {}


    def include(self):
        """

        :return: the number of inclusions performed.
        """
        count = 0
        new_result = []
        if self.from_main:
            main_found = False
        else:
            main_found = True
        for l,line in enumerate(self.result):
            if not main_found:
                if line.startswith("int main"):
                    main_found = True
                else:
                    new_result.append(line)
                    continue
            m = re.match(include_pattern,line)
            if m:
                if m[1] in self.include_files:
                    if self.verbose:
                        print(f"repeated: {line}",end='')
                    if line.endswith("/* repeated */\n"):
                        new_result.append(line)
                    else:
                        new_result.append(f"{line.strip()} /* repeated */\n")
                else:
                    file = self.find(m[1])
                    self.include_files[m[1]] = file
                    if file:
                        count += 1
                        if self.verbose:
                            print(f"{count} : found {m[0].strip()} -> {file}")
                        with file.open() as fh:
                            lines = fh.readlines()
                            new_result.append(f"//! {line[:-2]} /* {m[1]} -> {file} */\n")
                            new_result.extend(lines)
                    else:
                        new_result.append(f"{line[:-2]} /* not found */\n")
            else:
                new_result.append(line)

        # print()
        # for line in new_result:
        #     print(line,end='')

        self.result = new_result
        with self.result_path.open(mode="w") as f:
            for line in self.result:
                f.write(line)

        return count


    def recursive_include(self):
        iter_count = 0
        print(f"\nIteration {iter_count} ...")
        count = self.include()
        print(f"Iteration {iter_count}: {count} new include files")
        while count:
            iter_count += 1
            print(f"\nIteration {iter_count} ...")
            count = self.include()
            print(f"iteration {iter_count}: {count} new include files, totalling {len(self.include_files)}")


    def find(self, file):
        for p in self.search_paths:
            for root, dirs, files in os.walk(p):
                r = Path(root)
                for d in dirs:
                    f = r / d / file
                    if f.exists():
                        return f



# eof
