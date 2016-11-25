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
	
def multiply(A, B): #A dimensions nxm, B dimensions kxj, dimensions of produced matrix nxj
	n = len(A)
	j = len(B[0])
	
	C = np.empty((n,j), float) #creates an empty array of nxj dimension
	
	for row in range(0,n):
		for col in range(0,j):
			sum = 0
			for element in range(0,j): #col is an abbreviation for column
				sum += A[row][element] * B[element][col]
			C[row][col] = sum
			
	return C

x_angle = float(argv[3]) * pi / 180
y_angle = float(argv[4]) * pi / 180
z_angle = float(argv[5]) * pi / 180

#~ print x_angle
#~ print y_angle
#~ print z_angle

x_rotation = np.array([[1, 0, 0],
[0, cos(x_angle), -sin(x_angle)],
[0, sin(x_angle), cos(x_angle)]], float)

print x_rotation

y_rotation = np.array([[cos(y_angle), 0, sin(y_angle)],
[0, 1, 0],
[-sin(y_angle), 0, cos(y_angle)]], float)

print y_rotation

z_rotation = np.array([[cos(z_angle), -sin(z_angle), 0],
[sin(z_angle), cos(z_angle), 0],
[0, 0, 1]], float)

print z_rotation

inp_atoms, inp = readInput(argv[1])

out = multiply(inp, x_rotation)
out = multiply(out, y_rotation)
out = multiply(out, z_rotation)

checksaveFile(inp_atoms, out, argv[2])

