from os import walk
import re
import mmap
import struct
import plotly.express as px
import pandas as pd
from datetime import datetime



urlRegex = re.compile(b'(?<=\xFF\xFF\x75\x72\x6C[\x00-\xFF]{13})[\x00-\xFF]+?(?=\x09\x00)')
timestampRegex = re.compile(b'(?<=\xFF\xFF\x74\x69\x6D\x65\x53\x74\x61\x6D\x70\x00\x00\x00\x00\x00\x00\x00)[\x00-\xFF]{8}')
completeUrl = "http://7wcnwsu3oqzm7b4zgputusb4yxng5memwchkovasee4u2nwbfnuaieqd.onion/"
id = -1

def parseFile(filename):
    global id
    id += 1
    with open("data/"+filename, 'rb') as f:
        m = mmap.mmap(f.fileno(), 0, access = mmap.ACCESS_READ)
        itemsUrl = re.finditer(urlRegex, m)
        itemsTime = re.finditer(timestampRegex, m)

        foundUrl = False
        foundTime = False
        time = 0
        url = ""
        for item in itemsUrl:
            try:
                url = item.group(0).decode("utf-16").replace('\x00','')
            except:
                print(item.group(0))
                print("Parsing error " + filename)
            foundUrl = True
        
        for item in itemsTime:
            time = int(struct.unpack("<d", item.group(0))[0])
            foundTime = True

        if not foundUrl or not foundTime:
            print("Not found " + filename)
    resource = url.replace(completeUrl,"")
    start = datetime.fromtimestamp(time/1000)
    y = 0
    if ".png" in resource:
        y = int(resource.replace(".png",""))

    return (dict(Id=id, Time=start, Y=y, Resource=resource),dict(Time=time, Resource=resource))


_, _, filenames = next(walk("data/"))
data = []
dataCSV = []
for filename in filenames:
    val = parseFile(filename)
    data.append(val[0])
    dataCSV.append(val[1])

print(data)

df = pd.DataFrame(data)

dfCsv = pd.DataFrame(dataCSV)
dfCsv.to_csv("data_exported.csv")
fig = px.scatter(df, x="Time", y="Y", color="Resource")
fig.show()