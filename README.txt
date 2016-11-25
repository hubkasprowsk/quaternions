Program aligning molecule using quaternions.

***How to use this program?

To run the program user needs to provide a typical command for running python scripts from the shell and after that names of the files containing coordinates for reference molecule, molecule that needs to be fitted and for a new coordinate file with aligned molecule, respectively.

As an example, two files are provided: 'crown.xyz' and 'crown_fit.xyz' which is the same molecule as in 'crown.xyz' but translated by a vector [2,2,2].
Assuming that we want a new file 'crown_aligned.xyz' to be created we need to execute following command:

python quaternions.py crown.xyz crown_fit.xyz crown_aligned.xyz

where:  'crown.xyz' is a reference molecule
	'crown_fit.xyz' is a molecule that needs to be fitted
	'crown_aligned.xyz' is an aligned molecule that will be produced and saved to the file
	
If a specified output file already exists, program will ask the user if an overwrite or changing the name of output file is desired.
