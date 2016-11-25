# quaternions
Scripts and class (unfinished) helpful in molecular modelling. It calculates optimal rotation/translation (transformation matrix to align two chemical/biological entities with the same number of atoms.

Very important condition is that both structures (one to be fitted and the one serving as a reference) should have the same number of atoms, otherwise it quaternion aligning won't work.

A solution to this issue would be aligning only to the fragment of reference structure and then evaluate the alignment based on some arbitrary scoring (to be implemented)

Class, methods and script is built based on:
Karney C. F. F., 'Quaternions in molecular modeling', Journal of Molecular Graphics and Modelling, 25 (2007) 595-604
doi: 10.1016/j.jmgm.2006.04.002

Usage:

To run the program user needs to provide a typical command for running python scripts from the shell and after that names of the files containing coordinates for reference molecule, molecule that needs to be fitted and for a new coordinate file with aligned molecule, respectively.

As an example, two files are provided: 'crown.xyz' and 'crown_fit.xyz' which is the same molecule as in 'crown.xyz' but translated by a vector [2,2,2].
Assuming that we want a new file 'crown_aligned.xyz' to be created we need to execute following command:

python quaternions.py crown.xyz crown_fit.xyz crown_aligned.xyz

where:  'crown_fit.xyz' is a molecule that needs to be fitted
        'crown.xyz' is a reference molecule
        'crown_aligned.xyz' is filename for an aligned molecule that will be produced and saved to the file

If a specified output file already exists, program will ask the user if an overwrite or changing the name of output file is desired.
