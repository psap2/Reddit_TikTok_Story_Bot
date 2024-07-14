import os

folder_path = 'videos'

# Using scandir() to list all files and directories
with os.scandir(folder_path) as entries:
    for entry in entries:
        if entry.is_file():
            print(entry.name) 