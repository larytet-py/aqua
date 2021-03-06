#!/usr/bin/env python3

'''
Find a signature in files in a folder recursively

Requires two arguments: a folder and a file containing a signature
1TB disk will take ~10 minutes

Cutting corners: single thread, single core
Cutting corners: I assume SSD, this script will run slow on HDD 

For HDD I need to map the block device, read sequentially, search, 
link the found blocks to the filepaths
'''

import os
import sys
import pathlib
import mmap
import time

import magic

def is_executable(filepath):
    '''
    returns (Is ELF file type, error) tuple
    '''
    if not os.path.isfile(filepath):
        return False, None
    try:
        resp = magic.from_file(filepath)
    except Exception as exc:
        return False, exc

    return resp.startswith("ELF"), None

def find_match(filepath, signature):
    '''
    mmap the file 
    Search the memory mapped file for the signature
    returns (found, size, error) tuple
    The upside is that I can use regex and the search is quite fast with 
    sustainable rate around 2GBytes/s and toping around 10Gbytes/s
    '''
    try:
        with open(filepath, "rb") as f:
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as memmory_maped_file:
                return memmory_maped_file.find(signature) >= 0, memmory_maped_file.size(), None
    except Exception as exc:
        return -1, 0, exc


def grep(root, signature):
    '''
    Look for the signature in the ELF files in the directory root
    '''
    # Cutting corners:Is rglob returning an iterator or list?
    # iglob() will make sense for large file systems
    # Cutting corners: what if the file system changes while 
    # I am walking the walk?
    pathlist = pathlib.Path(root).rglob('*')
    print("Scanning started...")
    for path in pathlist:
        filepath = str(path)

        executable_file, error = is_executable(filepath)
        if error:
            print(f"Failed to discover the filetype for {filepath}: {error}")
            continue
        if not executable_file:
            continue

        match, file_size, error = find_match(filepath, signature)
        if error:
            print(f"Failed to grep the file {filepath}: {error}")
            continue
        if match:
            #print(f"Binary file {filepath} matches")
            print(f"File {filepath} is infected!")

def main():
    root = sys.argv[1]
    if not os.path.exists(root):
        print(f"Path {root} not found")
        sys.exit(1)

    # load the signature from a file
    # Cutting corners: I assume that the signature fits in the RAM
    signature_filename = sys.argv[2]
    try:
        with open(signature_filename, mode='rb') as file:
            signature = file.read()
    except Exception as exc:
        print(f"Failed to load signature from the file {signature_filename}: {exc}")
        sys.exit(1)

    grep(root, signature)
    
if __name__ == "__main__":
    main()
