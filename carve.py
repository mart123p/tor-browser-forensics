import sys
import re
import mmap
import os

if not os.path.exists('extracted'):
    os.makedirs('extracted')


if len(sys.argv) != 2:
    print("Usage python3 carve.py file.bin")

regex = re.compile(b'\xFF\xFFurl\x00[\x00-\xFF]{1,400}\.onion[\x00-\xFF]{1,800}connectionIsolationKey\x00')

filename = sys.argv[1]
with open(filename, 'rb') as dataBinary:
    m = mmap.mmap(dataBinary.fileno(), 0, access = mmap.ACCESS_READ)
    items = re.finditer(regex, m)
    for item in items:

        offset = item.start(0)
        data = item.group(0)
        length = len(data)
        if(length > 16384):
            print("Data over sized! {} bytes".format(length))
        else:
            print("Found data at {} of {} bytes".format(hex(offset),length))
            exportFile = open("extracted/"+hex(offset).upper()+".bin", "wb")
            exportFile.write(data)
            exportFile.close()