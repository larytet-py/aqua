
#!/usr/bin/env python3

import os
import pathlib
import magic

def is_executable(filepath):


def grep(root, pattern):
    pathlist = Path(root).rglob('*')
    for path in pathlist:
        filepath = str(path)



def main():
    root = sys.argv[1]
    if not os.path.exists(root):
        print(f"Path {root} not found")
        exit(1)
    pattern = sys.argv[2]
    grep(root, pattern)
    
if __name__ == "__main__":
    main()
