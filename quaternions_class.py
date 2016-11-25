#!/usr/bin/env python

# because of several elements used in this class (like xrange) it may not work properly or may not work at all with Python 3

import numpy as np
from sys import argv, exit
from os.path import isfile

class Quaternions(object):
    """This class is able to take two sets of atomic coordinates and based on these two sets create the best transformation matrix to align the coordinates.

    Very important condition is that both structures (one to be fitted and the one serving as a reference) should have the same number of atoms, otherwise it quaternion aligning won't work.
    A solution to this issue would be aligning only to the fragment of reference structure and then evaluate the alignment based on some arbitrary scoring (to be implemented)

    Class and methods built based on:
    Karney C. F. F., 'Quaternions in molecular modeling', Journal of Molecular Graphics and Modelling, 25 (2007) 595-604
    doi: 10.1016/j.jmgm.2006.04.002"""

    # obviously for some methods, like matrix transposition and matrix
    # multiplication I could use functions implemented in numpy
    # however it is more fun to write own functions (perhaps not the most effective ones)

    # some nomenclature used here is applied from article
    # I had no better idea for some of the names

    def __init__(self, input_filename):
        input_file = open(input_filename, "r").read().splitlines() #
        self.input_header = input_file[:2]
        self.atom_list = []
        self.coordinate_matrix = np.empty((0,3), float)
        self.transposeMatrix()

        for element in input_file[2:]:
            line = element.split()
            self.atom_list.append(line[0])
            self.coordinate_matrix = np.append(self.coordinate_matrix, np.array([line[1:]], float), axis = 0)
            # this probably can be done a bit easier

    def rotateMatrix():
        pass

    def translateMatrix():
        pass

    def transposeMatrix(self):
        n_rows = np.shape(self.coordinate_matrix)[0]
        n_columns = np.shape(self.coordinate_matrix)[1]
        self.transposed_matrix = np.empty((0, n_rows))

        for row_nr in xrange(n_columns):
            self.transposed_matrix = np.append(self.transposed_matrix, np.array([self.coordinate_matrix[:, row_nr]]), axis = 0)

        # return transposed_matrix

    def transpose(matrix):
        n_rows = np.shape(matrix)[0]
        n_columns = np.shape(matrix)[1] #columns in primary matrix or columns in transposed matrix
        transposed_matrix = np.empty((0, n_rows))

        for row_nr in range(n_columns):
            transposed_matrix = np.append(transposed_matrix, np.array([matrix[:,row_nr]]), axis = 0)

        return transposed_matrix

    def createAverageMatrix(self):
        """Returns a vector consisting of average values calculated from columns of coordinate matrix"""

        x_avg = np.average(self.coordinate_matrix[:,0])
        y_avg = np.average(self.coordinate_matrix[:,1])
        z_avg = np.average(self.coordinate_matrix[:,2])

        self.average_matrix = np.array([x_avg, y_avg, z_avg], float)

        print self.average_matrix

    def multiplyMatrices(matrix_A, matrix_B):
        n_dim = len(matrix_A) # matrix A dimensions: n x m
        j_dim = len(matrix_B[0]) # matrix B dimensions: k x j

        matrix_C = np.empty((n_dim, j_dim), float) # creates an empty array with n x j dimension
        # because after multiplication dimensions of produced matrix are n x j
        for row_nr in xrange(n_dim):
            for column_nr in range(j_dim):
                sum_ = 0
                for element in range(j_dim):
                    sum_ += matrix_A[row_nr][element] * matrix_B[element][column_nr]
                matrixC[row_nr][col_nr] = sum_

        return matrix_C

    def caclculateBmatrix(r_prim, f_prim):
        B_multi = 0 # B_multi because later on it will be divided by number of atoms
        N_atoms = len(f_prim) # number of atoms

        for i in range(N_atoms):
            a = f_prim[iterator] + r_prim[iterator]
            b = f_prim[iterator] - r_prim[iterator]

            A = np.array([[0, -b[0], -b[1], -b[2]],
            [b[0], 0, -a[2], a[1]],
            [b[1], a[2], 0, -a[0]],
            [b[2], -a[1], a[0], 0]], float)

            A_transposed = transpose(A) # % this should be quite different
            # % i specified transpose function for self as input
            B = B_multi / N_atoms

            return B

    def solveEigenproblem(X):
        # eigenproblem is bit to complex to implement own
        # thus here numpy function is used
        # perhaps own function will be implemented
        return np.linalg.eigh(X)

    def createRotationMatrix():
        w = eigenvector[0][0]
        x = eigenvector[1][0]
        y = eigenvector[2][0]
        z = eigenvector[3][0]

        rotation_matrix = np.array([[1 - 2*y*y - 2*z*z, 2*x*y - 2*z*w, 2*x*z + 2*y*w],
    	[2*x*y + 2*z*w, 1 - 2*x*x - 2*z*z, 2*y*z - 2*x*w],
    	[2*x*z - 2*y*w, 2*y*z + 2*x*w, 1 - 2*x*x - 2*y*y]], float)

        return rotation_matrix

    def alignStructures():
        pass

a = Quaternions("crown.xyz")
print a.input_header
print a.coordinate_matrix
print a.atom_list
print a.transposed_matrix
