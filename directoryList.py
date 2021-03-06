from pathlib import Path
from itertools import islice

space =  '    '
branch = '│   '
tee =    '├── '
last =   '└── '

def tree(dir_path: Path, level: int=-1, limit_to_directories: bool=False,
         length_limit: int=1000):
    """Given a directory Path object print a visual tree structure"""
    dir_path = Path(dir_path) # accept string coerceable to Path
    print(dir_path)
    files = 0
    directories = 0
    def inner(dir_path: Path, prefix: str='', level=-1):
        nonlocal files, directories
        if not level: 
            return # 0, stop iterating
        if limit_to_directories:
            contents = [d for d in dir_path.iterdir() if d.is_dir()]
        else: 
            contents = list(dir_path.iterdir())
        pointers = [tee] * (len(contents) - 1) + [last]
        for pointer, path in zip(pointers, contents):
            if path.is_dir():
                yield prefix + pointer + path.name
                directories += 1
                extension = branch if pointer == tee else space 
                yield from inner(path, prefix=prefix+extension, level=level-1)
            elif not limit_to_directories:
                yield prefix + pointer + path.name
                files += 1
    print(dir_path.name)
    iterator = inner(dir_path, level=level)
    for line in islice(iterator, length_limit):
        print(line)
    if next(iterator, None):
        print(f'... length_limit, {length_limit}, reached, counted:')
    print(f'\n{directories} directories' + (f', {files} files' if files else ''))


#tree(Path.home() / 'Documents', level=2, limit_to_directories=True, length_limit=100)
#you might not need to use all the parameters
#for folders in 'C:\Users\Koustav Sinha Ray\' we do not need to specify the full path, pass 'Documents' as parameter for 'C:\Users\Koustav Sinha Ray\Document'

def ui():
    print("DIRECTORY LIST VIEW v1.0")
    userPath = input("Enter path: ")
    userBoolean1 = input("Do you want to continue and list path with default settings? (y/n):")
    if (userBoolean1=="y"):
        tree(Path.home() / userPath)
    else:
        userlimit_to_directories=False
        userLevel = int(input("Restrict directory listing level to (e.g. 2, 3; default: -1, lists all subdirectories/files):"))
        userBoolean2 = input("Limit listing to directory names? (y/n; default:n):")
        if (userBoolean2=="y"):
            userlimit_to_directories=True
        
        userLengthLimit = int(input("Enter length limit (default: 1000):"))
        print("Displaying results as per user specified settings:")
        tree(userPath, level=userLevel, limit_to_directories=userlimit_to_directories, length_limit=userLengthLimit)
    input("Press any key to exit...")

ui()
