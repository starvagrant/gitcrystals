#!/usr/bin/env python3

import subprocess

def run_process(full_command):
    if repr(type(full_command))=="<class 'list'>":
        process=subprocess.run(full_command, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process
