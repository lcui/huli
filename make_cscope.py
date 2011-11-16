#
#usage: python make_cscope.py <path>
#
import os, sys

try:
    rootdir = sys.argv.pop(1)
except:
    rootdir = "/work/jack"

rootdir = os.path.abspath(rootdir)

print "rootdir is: %s" % rootdir

find_cmd = 'find %s -type d -name ".git" -prune -o -type d -name "out" -prune -o -type d -name "_out" -prune -o -name "*.[ch]" -o -name "*.[ch]pp" -o -name "*.java" > /tmp/cscope.files' % rootdir

os.system(find_cmd)
print "cscope.files is done."
os.system("cd /tmp && cscope -b && cp cscope.out %s && rm -f cscope.out" % rootdir)
print "cscope.out is created at %s." % rootdir

