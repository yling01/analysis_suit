#Aidan Fike
#June 28, 2019

#Program to go through measured omega angle trajectories and find all cis peptide bonds

import os

cisFound = False
currFile = open("struct_omega.xvg", "r")
for line in currFile:
    words = line.split()
    if words[0] != "#" and words[0] != "@":
	frame = words[0]
        for index, word in enumerate(words):
            if index > 1 and abs(float(word)) < 90:
                print("Cis bond found at frame %d at %d omega bond" % (frame, index)
                cisFound = True
if not cisFound:
	print("No cis angles found")
