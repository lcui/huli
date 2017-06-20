import os, sys, shutil, filecmp
#############################################################
# compare two directory trees for files which are different.
# and copy the different file in destination to copy_dir
# Usage: python cmptree.py source destination copy_dir
#############################################################

def dirwalk(dir, blacklist):
    "walk a directory tree, using a generator"
    for f in os.listdir(dir):
        fullpath = os.path.join(dir,f)
        if os.path.isdir(fullpath) and not os.path.islink(fullpath):
            if blacklist and os.path.split(fullpath)[-1] in blacklist:
                #print "ignore " + fullpath
                continue

            for x in dirwalk(fullpath, blacklist):  # recurse into subdir
                yield x
        else:
            fff, ext = os.path.splitext(fullpath)
            if blacklist and ext in blacklist:
                #print "ignore " + fullpath
                continue

            yield fullpath


def copy_files(flist, cpy_dir):
    for f in difflist:
        print "copying %s" % f
        to_file = f.replace(dst, cpy_dir)
        print "to %s" % to_file
        to_dir = os.path.dirname(to_file)
        try:
            os.makedirs(to_dir)
        except:
            pass

        shutil.copy(f, to_file)
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "usage: cmptree.py source destination copy_dir"
        exit()

    src = os.path.abspath(sys.argv[1])
    dst = os.path.abspath(sys.argv[2])
    blacklist = [".git", ".repo", ".swp", ".so"]

    difflist = []

    # find files different
    for f in dirwalk(src, blacklist):
        #print "processing %s" % f
        fff, ext = os.path.splitext(f)

        base_file = f.replace(src, dst, 1)
        if os.path.exists(base_file) :
            #cmd = "diff %s %s" % (f, base_file)
            #ll = os.popen(cmd).readlines()
            ll = filecmp.cmp(f, base_file)
            if not ll:
                #print "%s\n%s\n are different" % (f, base_file)
                difflist.append(base_file)

    # find files exist only in destination folder
    for f in dirwalk(dst, blacklist):
        #print "processing %s" % f

        fff, ext = os.path.splitext(f)

        src_file = f.replace(dst, src, 1)
        #print src_file
        if not os.path.exists(src_file) :
            print "%s does not exist in source" % f
            difflist.append(f)

    copy_files(difflist, os.path.abspath(sys.argv[3]))
    print "diff files are copied to %s" % sys.argv[3]

