# Tor Browser Memory Forensics
This is a small collection of scripts that attempt to recover session information of a user in the swap. It uses a 
JavaScript JSON structure that Firefox generates for every resource requested. It can be located with a simple regex.
This work was part of the final project in the class Computer and Forensics investigations 
[INF8430](https://www.polymtl.ca/programmes/cours/investigation-numerique-en-informatique) at Polytechnique Montreal.

## Usage
First we need to carve the structures from the page file. To do so you need to use the first script.
`python3 carve.py swapfile`

This will extract all the structures from the swap file. Once those are extracted, they can be analyzed with the other
script. This script will produce a CSV and open a scatter plot with Plot.ly. It was customized for one of my classes
experiments, but the code should be easy to adapt for your use case.
`python3 parse.py`

## Dependencies
To use the script you can use virtual environement and install the requirements.txt. You might also have the
requirements preinstalled on your system. It uses only pandas and plot.ly as external dependencies.