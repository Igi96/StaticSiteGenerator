
import os
import shutil


def clear_and_copy(src, dest):
    # Check if the destination directory exists, and if so, remove it
    if os.path.exists(dest):
        print(f"Deleting all contents of {dest}")
        shutil.rmtree(dest)
    
    # Recreate the destination directory
    os.makedirs(dest, exist_ok=True)

    # Recursively copy the source directory to the destination
    recursive_copy(src, dest)

def recursive_copy(src, dest):
    # List all files and directories in the source directory
    for item in os.listdir(src):
        src_item = os.path.join(src, item)
        dest_item = os.path.join(dest, item)

        # If the item is a file, copy it
        if os.path.isfile(src_item):
            print(f"Copying file: {src_item} -> {dest_item}")
            shutil.copy(src_item, dest_item)
        
        # If the item is a directory, create the directory in the destination and recurse
        elif os.path.isdir(src_item):
            print(f"Creating directory: {dest_item}")
            os.makedirs(dest_item, exist_ok=True)
            recursive_copy(src_item, dest_item)





