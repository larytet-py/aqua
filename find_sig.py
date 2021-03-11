
#!/usr/bin/env python3

import os
import pathlib
import magic
import mmap

def is_executable(filepath):
    try:
        resp = magic.from_file(filepath)
    except Exception as exc:
        return False, exc

    return resp.startswith("ELF"), None

def find_match(filepath, signature):
    try:
        with open(filepath, "r+b") as f:
            mm = mmap.mmap(f.fileno(), 0)
            return mm.find(signature) >= 0, None
    except Exception as exc:
            return -1, exc


def grep(root, signature):
    pathlist = Path(root).rglob('*')
    print("Scanning started...")
    for path in pathlist:
        filepath = str(path)
        executable_file, error = is_executable(filepath)
        if error:
            print(f"Failed to discover the filetype for {filepath}")
            continue
        if not executable_file:
            continue
        match, err = find_match(filepath, signature)
        if error:
            print(f"Failed to grep the file {filepath}")
            continue
        if match:
            print(f"File {filepath} is infected!")


def main():
    root = sys.argv[1]
    if not os.path.exists(root):
        print(f"Path {root} not found")
        exit(1)
    signature_filename = sys.argv[2]
    try:
        with open(signature_filename, mode='rb') as file: # b is important -> binary
            signature = file.read()
    except Exception as exc:
        print(f"Failed to load signature from the file {signature_filename}")
        exit(1)

    grep(root, signature)
    
if __name__ == "__main__":
    main()
