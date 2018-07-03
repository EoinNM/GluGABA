"""
Created on Tue Apr May 1 2018

@author: eoin

MATLAB --patch freetype
"""
import os, sys
from os import *
from variables.variables import *
from utils.utils import *


def spectral_registration(workspace, population, days, voxels):
    
    print '========================================================================================='
    print '                      GluGABA - 05_Frequency & Phase Drift Correction                    '
    print '========================================================================================='
    
    count = 0
    for subject in population:
        count +=1
        for day in days:
            for voxel in voxels:
                
                print '======================================================================================================'
                print ' %s. Performing Spectral Registration for Frequency & Phase Drift Correction on %s, %s, %s'  %(count, subject, day, voxel)
                print '======================================================================================================'
                
                #directory
                twxdata_dir = os.path.join(workspace, subject,'SVS', day, voxel, 'TWIX')
                
                #run Jamie Near SVS processing tools in MatLab for each TWIX voxel/sequence
                #change to correct sub dir!
                os.chdir(twxdata_dir)
                
                #MATLAB through bash - auto scripts called
                #MATLAB --patch freetype as environment
                if voxel[-1] != 'm':
                    print 'PRESS'
                    os.system("matlab -softwareopengl -nodesktop -nosplash -noFigureWindows -r \"run_pressproc_auto(\'%s\');quit;\""%voxel)
                    
                else: 
                    print 'MEGA-PRESS'
                    os.system("matlab -softwareopengl -nodesktop -nosplash -noFigureWindows -r \"run_megapressproc_auto(\'M1m\');quit;\"")

spectral_registration(workspace, test_pop, days, voxels)

                
                
