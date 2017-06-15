#############################################################
# copy trees for files to dest
# Usage: python cpfiles.py files_list copy_dir
#############################################################


import os, sys, shutil

def find_common_dir(files):
    paths = []
    for f in files:
        drive, fn = os.path.split(f)

        paths.append(drive.split(os.sep))

    result = paths[0]
    size = len(result)
    for s in paths[1:]:
        ns = 0
        for k in range(size):
            if s[k] == result[k]:
                ns += 1

        size = ns

    dirs = result[0]
    print result
    for k in range(1,size):
        dirs += os.sep + result[k]

    return dirs


def copy_files(flist, cmn_dir, cpy_dir):
    for f in flist:
        print "copying %s" % f
        to_file = f.replace(cmn_dir, cpy_dir+os.sep)
        print "to %s" % to_file
        to_dir = os.path.dirname(to_file)
        try:
            os.makedirs(to_dir)
        except:
            pass

        shutil.copy(f, to_file)

if __name__ == "__main__":
    files = open(os.path.abspath(sys.argv[1])).read().splitlines()
    cmn_dir = find_common_dir(files)
    print cmn_dir
    copy_files(files, cmn_dir, os.path.abspath(sys.argv[2]))
    print "diff files are copied to %s" % sys.argv[2]

