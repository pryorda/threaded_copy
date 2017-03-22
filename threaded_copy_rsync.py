#!/usr/bin/env python
import re
import os
from optparse import OptionParser
import sys
import subprocess
import time

processes = set()
max_processes = 20

# Usage
parser = OptionParser()

parser.add_option("-s", "--src", dest="src_dir",
                  help="Src Directory", metavar="src")

parser.add_option("-d", "--dest", dest="dest_dir",
                  help="Dest Directory", metavar="dest")

(options, args) = parser.parse_args()

if not options.src_dir or not options.dest_dir:
   parser.print_help()
   sys.exit()


#config
src_dir = options.src_dir
dest_dir = options.dest_dir

for folder in os.listdir(src_dir):
    for folder_lower in os.listdir(str(src_dir + "/" + folder)):
        old_file_src = src_dir + "/" + folder + "/" + folder_lower
        new_file_dest = dest_dir + "/" + folder + "/"
        try:
            os.stat(new_file_dest)
        except:
            print "Creating Directory for", new_file_dest
            os.makedirs(str(dest_dir + "/" + folder))

        command1 = "rsync -a \"" + old_file_src + "\" \"" + new_file_dest + "\""
#        command1 = "rsync --remove-source-files -a \"" + old_file_src + "\" \"" + new_file_dest + "\""
        processes.add(subprocess.Popen(command1, shell=True))
        print "Process ", len(processes), " started on folder", str(new_file_dest + folder_lower)
        while len(processes) >= max_processes:
            time.sleep(1)
            processes.difference_update([p for p in processes if p.poll() is not None])

for p in processes:
   if p.poll() is None:
      p.wait()

