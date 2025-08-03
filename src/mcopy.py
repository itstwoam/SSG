import shutil
import os
import sys

def copy_directory(source, dest):
    # Write all the files in the source root directory to the dest directory
    wsource = os.path.abspath(source)
    wdest = os.path.abspath(dest)
    entries = os.listdir(wsource)
    directories = []
    # if the destination doesn't exist then make it.
    if not os.path.exists(wdest):
        os.mkdir(wdest)

    entries = os.listdir(wsource)
    try:
        for entry in entries:
            full_path = os.path.join(wsource, entry)
            if (os.path.isfile(full_path)):
                shutil.copy(full_path, wdest)
            else:
                directories.append(entry)
    except:
        return False

    # recursively call copy to the directories
    for dire in directories:
        copy_directory(os.path.join(wsource, dire), os.path.join(wdest, dire))
    return



def wipe_directory(directory):
    #Get a list of all files in the directory
    if "playground/" not in directory:
        print("Guardrails are off, I'm out")
        sys.exit(1)
    if not os.path.exists(directory):
        return True
    entries = os.listdir(os.path.abspath(directory))
    directories = []
    try:
        for entry in entries:
            #print("Leftover:", repr(entry), "| Full path:", os.path.join(directory, leftover))
            full_path = os.path.join(directory, entry)
            if os.path.isfile(full_path):
                os.remove(full_path)
                #files.append(entry)
                #print("Would delete: ",os.path.abspath(full_path))
            else:
                directories.append(full_path)
    except:
        return False
    
    if len(directories) == 0:
       return True

    #recursively call wipe_directory on all the subdirectories
    success=True
    for dire in directories:
        if not success:
            return False
        success = wipe_directory(dire)
        if success:
            os.rmdir(dire)

    if not success:
        return False

    return success

def copy(source, destination):
    if not os.path.exists(os.path.abspath(source)):
        return
    if os.path.exists(destination):
        wipe_directory(destination)
        os.rmdir(destination)
    
    copy_directory(source, destination)




def main():
    dguard = "playground/"
    l = len(sys.argv)
    if l != 3:
        return
    sdirectory = sys.argv[1]

    ddirectory = sys.argv[2]
    copy(sdirectory, ddirectory)

if __name__ == "__main__":
    main()
