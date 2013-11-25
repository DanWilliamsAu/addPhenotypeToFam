##############################################################################
#
# Program Name:
#
# addPhenotypeToFam
#
# This program takes a PLINK fam file which contains no phenotype information,
# a file with case IDs and a file with control IDs, and creates a new plink
# fam file, which is encoded with the phenotypes as per the case and control
# ID files.  The ID system is as per the default PLINK codes:
#   -9 missing
#   1 unaffected
#   2 affected
#
# The case and control ID files should contain the Individual IDs, one
# individual per line. The program additionally converts the ID numbers
# from DBgap IDs to NG IDs.
#
# Author:
#
# Daniel Williams (Department of Psychiatry, University of Melbourne)
#                 daniel.williams@unimelb.edu.au
#
# Date Created:
#
# 25 November 2013
#
##############################################################################

import csv
import sys

### CONSTANTS ###

# files
CASE_FILE = 'cases.IDs'
CONTROL_FILE = 'controls.IDs'
OUT_FILE = 'RENAMETHISNewBimFile'
MAPPING_FILE = 'dbGap2ngID.mapping'

# string constants
UNAFFECTED = '1'
AFFECTED = '2'
MISSING = '-9'


### FUNCTIONS ###

def get_filename():
    """ checks command line arguments and returns name of
    PLINK fam file which is to be converted
    if supplied or defualt file if not """

    if len(sys.argv) != 2:
        print "please provide a fam file name. Usage:"
        print "python addPhenotypeToFam.py <filename>"
        sys.exit()
    else:
        return sys.argv[1]

def create_dbGap2NG_map(dbGAP2NG):
    """ Creates a dictionary which is used to convert from dbGAP ID to ngID
    where the key is the dbGap ID and the value is the ng ID. Argument is the
    mapping file in csv reader format. """
    
    mapping = {}

    # skip header
    dbGAP2NG.next()

    # process rest of file
    for line in dbGAP2NG:
        mapping[line[0]] = line[1]
        
    return mapping

def add_phenotype(out, famFile, pheno_dict):
    """ write out the new fam file, which will be encoded with phenotype
    information

    out -- file object of the new fam file which will be created
    famFile -- the original fam file, which has no phenotype data
    pheno_dict -- dctionary containing ID -> phenotype info"""

    writer = csv.writer(out, delimiter = ' ')
    
    for line in famFile:
        line = line.split()
        currID = line[0]

        # add phenotype
        if currID in pheno_dict:
            line[5] = pheno_dict[currID]
        else:
            line[5] = MISSING
        
        # write line to file
        writer.writerow(line)
        


def create_pheno_dict(cases, controls, mapping):
    """ Create and retruns a dictionary, with individual ID as the key
    and the phenotype status as the value.

    cases -- file containing the case IDs in dbGAP format
    controls -- file contiang the control IDs in dbGAP format
    mapping -- dbGap -> ng ID mapping dictionary"""

    pheno_dict = {}

    # add cases to dictionary
    for line in cases:
        pheno_dict[mapping[line[0]]] = UNAFFECTED

    # add controls to dictionary
    for line in controls:
        pheno_dict[mapping[line[0]]] = AFFECTED

    return pheno_dict

def main():
    """ Open up the data, process it and output the new file!"""
    
    # open up data files in csv reader format
    dbGAP2NG = csv.reader(open(MAPPING_FILE), delimiter = '\t')
    cases = csv.reader(open(CASE_FILE))
    controls = csv.reader(open(CONTROL_FILE))
    famfileName = get_filename()
    famFile = open(famfileName)

    # create the new fam file which will be in the desired phenotype format
    out = open(OUT_FILE,"w")
    
    # create mapping
    mapping = create_dbGap2NG_map(dbGAP2NG)

    # create data structure for associating IDs with phenotype
    pheno_dict = create_pheno_dict(cases, controls, mapping)
    
    # write new fam file with phenotypes added
    add_phenotype(out, famFile, pheno_dict)

    out.close()

main()
    


