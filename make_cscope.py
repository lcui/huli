import os, sys
#################################
#Usage: python generate.py dir
#################################

def dirwalk(dir):
    "walk a directory tree, using a generator"
    for f in os.listdir(dir):
        fullpath = os.path.join(dir,f)
        if os.path.isdir(fullpath) and not os.path.islink(fullpath):
            for x in dirwalk(fullpath):  # recurse into subdir
                yield x
        else:
            yield fullpath

def make_filelist(dir):
    if not dir:
        dir = "."
    dir = os.path.normpath(os.path.abspath(dir))
    print (dir)
    fout = open("cscope.files", "w")
    extlist = [".c", ".cpp", ".h", ".cxx", ".hxx", ".java"]
    for ff in dirwalk(dir):
        root, ext = os.path.splitext(ff)
        ext = ext.lower()
        if ext in extlist:
            fout.write(ff+"\n")
            
if __name__ == "__main__":
    dir = sys.argv[1]
    make_filelist(dir)
    os.system("cscope -b")
