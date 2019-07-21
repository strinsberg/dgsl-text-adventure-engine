import os

home = os.path.expanduser('~')
dgsl_dir = os.path.join(home, '.dgsl')
worlds = os.path.join(dgsl_dir, 'worlds')
saves = os.path.join(dgsl_dir, 'saves')

try:
    print('Creating', dgsl_dir)
    os.mkdir(dgsl_dir)
    print('Creating', worlds)
    os.mkdir(worlds)
    print('Creating', saves)
    os.mkdir(saves)
except FileExistsError:
    print("The .dgsl directories already exist")

# still need to copy worlds to the worlds directories
