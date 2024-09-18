#! /usr/bin/env python3    
from sys import argv
from create import inBandCreate, outBandCreate
from extract import inBandExtract, outBandExtract


tarCommand = argv[1:]                                       # Takes TAR command input 
    
command = tarCommand[0].lower()                             # c or x

if(command == 'co'):                                        # Check if command valid "ci" in bound
    outBandCreate(tarCommand[1:])                           # create and store in .tar

elif(command == 'xo'):                                      # Check if command valid "xi" in bound                
    tar = tarCommand[1]
    outBandExtract(tar)                                     # Extract files from .tar

elif(command == 'ci'):                                      #  Check if command is valid 'co' out bound
    inBandCreate(tarCommand[1:])

elif(command == 'xi'):                                      # Check if command is valid 'xo' out bound
    tar = tarCommand[1]
    inBandExtract(tar)