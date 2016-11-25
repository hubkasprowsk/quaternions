#!/usr/bin/env python

# Please use Python 2.7.x interpreter because of some used functions like xrange

# obviously for some methods, like matrix transposition and matrix
# multiplication I could use functions implemented in numpy
# however it is more fun to write own functions (perhaps not the most effective ones)

# some nomenclature used here is applied from article
# Karney C. F. F., 'Quaternions in molecular modeling'
# Journal of Molecular Graphics and Modelling
# 25 (2007) 595-604
# doi: 10.1016/j.jmgm.2006.04.002
# I had no better idea for some of the names

import numpy as np
from sys import argv, exit
from os.path import isfile

##### FUNCTIONS

def readInput(filename):
	if len(argv) < 4:
		print """Usage:
		./quaternions.py input1_to_fit_filename.xyz input_reference_filename.xyz output_filename.xyz
		"""
		exit()

	input_file = open(filename, "r").read().splitlines()[2:]

	coordinate_matrix = np.empty((0, 3), float)
	atom_list = []
	for element in input_file:
		line = element.split()
		coordinate_matrix = np.append(coordinate_matrix, np.array([line[1:]], float), axis = 0)
		atom_list.append(line[0])

	return atom_list, coordinate_matrix

def checksaveFile(atom_list, matrix, filename):

	if isfile(filename) == True:
		answer = raw_input("\nFile '%s' already exists. Overwrite? (y/n)\n" %filename).lower()
		# .lower() function called to avoid capital letter error raise
		if answer == "y":
			saveFile(atom_list, matrix, filename)
		elif answer == "n":
			filename = raw_input("\nProvide a new name:\n")
			saveFile(atom_list, matrix, filename)
		else:
			print "\nOption unrecognized. Program will shut down.\n"
	else:
		saveFile(atom_list, matrix, filename)

def saveFile(atom_list, matrix, filename):
	output = open(filename, "w")

	print >> output, len(matrix)
	print >> output, "Aligned molecule."

	for element in range(len(matrix)):
		atom = atom_list[element]
		x = matrix[element][0]
		y = matrix[element][1]
		z = matrix[element][2]
		out_line = "%2s   %15.10f   %15.10f   %15.10f" %(atom, x, y, z) # or change it to 10.7f
		print >> output, out_line

	print "\nCoordinate file '%s' has been written.\n" % filename

def transpose(matrix):
	rows = np.shape(matrix)[0] # rows in primary matrix or columns in transposed matrix
	columns = np.shape(matrix)[1] # columns in primary matrix or rows in transposed matrix
	transposed = np.empty((0, rows))

	for row_nr in range(columns):
		transposed = np.append(transposed, np.array([matrix[:,row_nr]]), axis = 0)

	return transposed

def createAverage(matrix):
	# creates a vector of average values from a matrix
	x_average = np.average(matrix[:,0])
	y_average = np.average(matrix[:,1])
	z_average = np.average(matrix[:,2])
	average_matrix = np.array([x_average, y_average, z_average], float)

	return average_matrix

def multiply(matrix_A, matrix_B): # matrix A dimensions: n x m
	# matrix B dimensions: k x j
	# dimensions of produced matrix (matrix C): n x j
	n_dim = len(matrix_A)
	j_dim = len(matrix_B[0])

	matrix_C = np.empty((n_dim,j_dim), float) #creates an empty array of n x j dimension

	for row in range(0, n_dim):
		for column in range(0, j_dim):
			sum_ = 0
			for element in range(0, j_dim): #col is an abbreviation for column
				sum_ += matrix_A[row][element] * matrix_B[element][column]
			matrix_C[row][column] = sum_

	return matrix_C

def calculateBmatrix(r_prim, f_prim):
	# for more reference what B matrix is, please see articled mentioned at the beginning of the file
	B_multi = 0
	N_atoms = len(f_prim)  # number of atoms
	for iterator in range(0, N_atoms):
		a = f_prim[iterator] + r_prim[iterator]
		b = f_prim[iterator] - r_prim[iterator]

		A = np.array([[0, -b[0], -b[1], -b[2]],
		[b[0], 0, -a[2], a[1]],
		[b[1], a[2], 0, -a[0]],
		[b[2], -a[1], a[0], 0]], float)

		A_transposed = transpose(A)

		B_multi += multiply(A, A_transposed)

	B = B_multi / N_atoms

	return B

def solveEigenproblem(B_matrix):
	# because eigenproblem is a bit too complex to implement own one, I used numpy implemented function from linalg package
	return np.linalg.eigh(B_matrix)

def createRotationMatrix(eigenvector):
	# uses eigenvector solved for B matrix and based on that, creates
	# the most optimal rotation matrix
	w = eigenvector[0][0]
	x = eigenvector[1][0]
	y = eigenvector[2][0]
	z = eigenvector[3][0]

	rotationMatrix = np.array([[1 - 2*y*y - 2*z*z, 2*x*y - 2*z*w, 2*x*z + 2*y*w],
	[2*x*y + 2*z*w, 1 - 2*x*x - 2*z*z, 2*y*z - 2*x*w],
	[2*x*z - 2*y*w, 2*y*z + 2*x*w, 1 - 2*x*x - 2*y*y]], float)

	return rotationMatrix

def alignStructures(input_1_filename, input_2_filename, output_filename):
	# input 1 - structure to be fitted - fit_*
	# input 2 - reference structure - ref_*
	fit_atoms, fit_coords = readInput(input_1_filename) # coords - coordinates
	ref_atoms, ref_coords = readInput(input_2_filename)

	fit_average = createAverage(fit_coords)
	ref_average = createAverage(ref_coords)

	fit_prim = fit_coords - fit_average
	ref_prim = ref_coords - ref_average

	B_matrix = calculateBmatrix(ref_prim, fit_prim)

	_, eigenvector = solveEigenproblem(B_matrix)

	rotation_matrix = createRotationMatrix(eigenvector)

	rotated_coords = multiply(fit_coords, rotation_matrix)

	displacement = ref_average - createAverage(rotated_coords)

	aligned_coords = rotated_coords + displacement

	checksaveFile(fit_atoms, aligned_coords, output_filename)

##### SCRIPT

alignStructures(argv[1], argv[2], argv[3])
