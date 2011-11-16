# Save files in a commit to another folder
# Usage: cmtfiles.py commit_id target_folder
import os, sys, shutil

def dirwalk(dir):
    "walk a directory tree, using a generator"
    for f in os.listdir(dir):
        fullpath = os.path.join(dir,f)
        if os.path.isdir(fullpath) and not os.path.islink(fullpath):
            for x in dirwalk(fullpath):  # recurse into subdir
                yield x
        else:
            yield fullpath


def get_commit_files(commit_id):
    git_cmd = "git show --pretty='format:' --name-only %s" % commit_id
    print git_cmd
    return [ff.strip() for ff in os.popen(git_cmd).readlines()]


def copy_files(files, dst_dir, commit_id):
    for ff in files:
        if len(ff) <= 0:
            continue

        dir_name = os.path.dirname(ff)
        dst_path = "%s/%s" % (dst_dir, dir_name)

        try:
            os.makedirs(dst_path)
        except:
            pass

        dst_file = "%s/%s" % (dst_dir, ff)
        #shutil.copy(ff, dst_path)
        git_cmd = "git show %s:%s > %s" % (commit_id, ff, dst_file)
        print git_cmd
        os.system(git_cmd)


if __name__=="__main__":
    commit_id = sys.argv[1]
    dst_dir = sys.argv[2]
    print commit_id
    files = get_commit_files(commit_id)
    copy_files(files, dst_dir, commit_id)
