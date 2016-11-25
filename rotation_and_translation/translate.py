#!/usr/bin/env python
import numpy as np
from sys import argv
from math import pi, sin, cos
from os.path import isfile

def readInput(filename):
	input = open(filename, "r").read().splitlines()[2:]

	matrix = np.empty((0, 3), float)
	atom_list = []
	for element in input:
		line = element.split()
		matrix = np.append(matrix, np.array([line[1:]], float), axis = 0)
		atom_list.append(line[0])

	return atom_list, matrix
	
def checksaveFile(atom_list, matrix, filename):
	
	if isfile(filename) == True:
		print "\nFile '%s' already exists. Overwrite? (y/n)" %filename
		answer = raw_input()
		possibleAnswers = "yYnN"
		if answer not in possibleAnswers:
			"\nWrong answer. Program will shut down.\n"
		elif answer == "y" or answer == "Y":
			saveFile(atom_list, matrix, filename)
		elif answer == "n" or answer == "N":
			filename = raw_input("\nProvide a new name:\n")
			saveFile(atom_list, matrix, filename)
	else:
		saveFile(atom_list, matrix, filename)
	
def saveFile(atom_list, matrix, filename):
	output = open(filename, "w")
	
	print >> output, len(matrix)
	print >> output, "Rotated molecule."
	
	for element in range(len(matrix)):
		atom = atom_list[element]
		x = matrix[element][0]
		y = matrix[element][1]
		z = matrix[element][2]
		out = "%2s   %15.10f   %15.10f   %15.10f" %(atom, x, y, z) #or change it to 10.7f
		print >> output, out
	
	print "\nCoordinate file '%s' has been written.\n" % filename

def translate(matrix, x, y, z):
	vec = np.array([x,y,z], float)
	translated = matrix + vec
	
	return translated
	
x = int(argv[3])
y = int(argv[4])
z = int(argv[5])

inp_atoms, inp = readInput(argv[1])

out = translate(inp, x, y, z)
checksaveFile(inp_atoms, out, argv[2])
