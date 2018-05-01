"""
Created on Tue Apr May 1 2018

@author: eoin
"""
import os
from os import *
from variables.varaibles import *
from utils.utils import *


def spectral_registration(workspace, population, days, voxels):
    
    print '============================================================================================'
    print '                         GluGABA_03 - Frequency & Phase Drift Correction                    '
    print '============================================================================================'
    
    count = 0
    for subject in population:
        for day in days:
            for voxel in voxels:
                count +=1
                
                print '============================================================================================'
                print ' %s. Performing Spectral Registration for Frequency & Phase Drift Correction on %s, %s, %s'  %(count, subject, voxel, day)
                print '============================================================================================'
                
                #directory
                twxdata_dir = os.path.join(workspace, 'population', subject,'SVS', day, voxel, 'TWIX', voxel)
                
                #run Jamie Near SVS processing tools in MatLab for each voxel/sequence
                
                ACC_dir = os.path.join(twxdata_dir, 'ACC')
                #change to correct sub dir!
                os.chdir(ACC_dir)
                #MatLab through bash - auto press script called
                os.system("matlab -nodesktop -nosplash -r \"run_pressproc_auto(\'ACC\');quit;\"")
                
                M1_dir = os.path.join(twxdata_dir, 'M1')
                #change through correct sub dir!
                os.chdir(M1_dir)
                #MatLab in bash - auto press script called
                os.system("matlab -nodesktop -nosplash -r \"run_pressproc_auto(\'M1\');quit;\"")
                
                M1m_dir = os.path.join(twxdata_dir, 'M1m')
                #change to correct sub dir!
                os.chdir(M1m_dir)
                #MatLab through bash - auto megapress script called
                os.system("matlab -nodesktop -nosplash -r \"run_megapressproc_auto(\'M1m\');quit;\"")
                
spectral_registration(workspace, population, days, voxels)
                
                