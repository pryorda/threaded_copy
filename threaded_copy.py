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

for file in os.listdir(src_dir):
   new_file = re.sub(r'^\d{5}', '', file)

   old_file_src = src_dir + "\\" + file
   new_file_dest = dest_dir + "\\" + new_file

   command1 = "copy \"" + old_file_src + "\" \"" + new_file_dest + "\" >nul"

   processes.add(subprocess.Popen(command1, shell=True))
   if len(processes) >= max_processes:
      time.sleep(.1)
      processes.difference_update([p for p in processes if p.poll() is not None])

for p in processes:
   if p.poll() is None:
      p.wait()
