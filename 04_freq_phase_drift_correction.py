"""
Created on Tue Apr May 1 2018

@author: eoin
"""
import os
from os import *
from variables.variables import *
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
                twxdata_dir = os.path.join(workspace, subject,'SVS', day, voxel, 'TWIX',)
                
                #run Jamie Near SVS processing tools in MatLab for each voxel/sequence
                #change to correct sub dir!
                os.chdir(twxdata_dir)
                
                #MatLab through bash - auto script called
                if voxel[-1] != 'm':
                    print 'PRESS'
                    os.system("matlab -nodesktop -nosplash -r \"run_pressproc_auto(\'%s\');quit;\""%voxel)
                    
                else: 
                    print 'MEGAPRESS'
                    os.system("matlab -nodesktop -nosplash -r \"run_megapressproc_auto(\'M1m\');quit;\"")
                


spectral_registration(workspace, test_population, days, voxels)
                
                
