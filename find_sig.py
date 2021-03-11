#!/usr/bin/env python3

'''
Find a signature in files in a folder recursively
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
    The upside is that I can use regex and the search is very (~1GB/s) fast
    '''
    try:
        with open(filepath, "rb") as f:
            with mmap.mmap(f.fileno(), 0, flags=mmap.MAP_PRIVATE) as memmory_maped_file:
                return memmory_maped_file.find(signature) >= 0, memmory_maped_file.size(), None
    except Exception as exc:
        return -1, 0, exc


def grep(root, signature):
    '''
    Look for the signature in the ELF files in the directory root
    '''
    pathlist = pathlib.Path(root).rglob('*')
    processed_bytes = 0
    start_time = time.time()
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
        processed_bytes += file_size
    print(f"Processed {processed_bytes/(1000*1000)}MB, average rate {processed_bytes/(1000*1000*(time.time()-start_time))}MB/s")  # 600-700MB/s

def main():
    '''
    Requires two arguments: a folder and a file containing a signature
    '''
    root = sys.argv[1]
    if not os.path.exists(root):
        print(f"Path {root} not found")
        sys.exit(1)
    signature_filename = sys.argv[2]

    # load the signature from a file
    # Cutting corners: I assume that the signature fits in the RAM
    try:
        with open(signature_filename, mode='rb') as file:
            signature = file.read()
    except Exception as exc:
        print(f"Failed to load signature from the file {signature_filename}: {exc}")
        sys.exit(1)

    # Cutting corners: single thread, single core
    # 1TB disk will take ~10 minutes
    grep(root, signature)
    
if __name__ == "__main__":
    main()
