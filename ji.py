"""
A simple wrapper for git commands.
usage: python ji.py options cmds
cmds should follow options
    options:
        -v                      > show git command to run
    cmds:
        cat file                > show file contents in the server
        backup outdir id1, id2  > backup modified files
        changelist              > list files you added/deleted/modified.
"""

import os, sys
import shutil   #for copy

verbose = False

def ji(cmdline) :
    if verbose:
        print ("\t-> Runing command: %s" % cmdline)

    return os.popen(cmdline).readlines()

def jicat(fin, fout):
    fin = os.path.abspath(fin)
    if not os.path.exists(fin) :
        print ("%s does not exist" % fin)
        return

    gitroot = get_gitroot(fin)
    fin = fin.replace(gitroot, "")[1:]

    fin = fin.replace('\\', '/')    # hack for DOS
    cmdline = "git show HEAD:%s > %s" % (fin, fout)
    ji(cmdline)

def get_gitroot(fin):
    rootdir = "/"
    fin = os.path.abspath(fin)
    if os.path.isdir(fin):
        fin_dir = fin
    else :
        fin_dir = os.path.dirname(os.path.abspath(fin))
    os.chdir(fin_dir)
    try:
        while fin_dir != rootdir:
            #print fin_dir
            if os.path.isdir(os.path.join(fin_dir, ".git")):
                break
            fin_dir = os.path.abspath(os.path.join(fin_dir, "../"))
    except:
        print ("not in a git repo")
        fin_dir = None
    else:
        fin_dir = os.path.abspath(fin_dir)
        #print "find git root dir: " + fin_dir

    return fin_dir

#args format is: outdir  [ID1]  [ID2]
def jibackup(argv, useless):
    outdir = None
    id1 = None
    id2 = None
    cmdline = "git diff --name-only "

    if len(argv) == 1:
        outdir = argv.pop(0)
    elif len(argv) == 2:
        outdir = argv.pop(0)
        cmdline = cmdline + argv.pop(0)
    elif len(argv) == 3:
        outdir = argv.pop(0)
        cmdline = cmdline + argv.pop(0) + " " + argv.pop(0)

    if outdir :
        outdir = os.path.abspath(outdir)
    else:
        outdir = "c:/tmp"

    print (outdir)
    print (cmdline)

    files = ji(cmdline)
    if not files:
        return

    gitroot = get_gitroot(".")

    for src in files:
        dirpart = os.path.join(outdir, os.path.dirname(src))
        if not os.path.exists(dirpart):
            os.makedirs(dirpart)
        src = os.path.abspath(os.path.join(gitroot, src)).rstrip()
        if os.path.exists(src) :
            shutil.copy2(src, dirpart)
            print ("copied %s to %s" % (src, dirpart))

def jichangelist(useless1, useless2) :
    cmdline = "git status -s"
    lines = ji(cmdline)
    result = []
    for line in lines:
        if line.startswith("??") or line in result:
            continue

        result.append(line)

    for line in result:
        print (line, end="")

def parse_cmdline(argv):
    cmdline = None
    fin = None
    fout = None
    while len(argv) > 0 :
        arg = argv.pop(0).lower()
        if arg == "-v":
            global verbose
            verbose = True
        elif arg == "cat" :
            cmdline = "cat"
            fin = argv.pop(0)
            fout = argv.pop(0)
            break
        elif arg == "backup" :
            cmdline = "backup"
            fin = argv
            break
        elif arg == "changelist" :
            cmdline = "changelist"
            break

    return cmdline, fin, fout

if __name__ == '__main__':
    sys.argv.pop(0)
    cmdfuncs = {
            "cat"       : jicat,
            "backup"    : jibackup,
            "changelist": jichangelist,
            }
    cmd, fin, fout = parse_cmdline(sys.argv)
    #print cmd, fin, fout

    func = cmdfuncs.get(cmd, None)

    if func:
        func(fin, fout)
    else:
        print ("Invalid command" + __doc__)

