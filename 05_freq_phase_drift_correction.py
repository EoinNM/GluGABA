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
                twxdata_dir = os.path.join(workspace, 'DATA', subject,'SVS', day, voxel, 'TWIX')
                
                #run FID-A preprocessing
                os.chdir(twxdata_dir)
                
                #Auto FID-A scripts called - "MATLAB --patch freetype" called as environment
                if voxel[-1] != 'm':
                    print 'Processing PRESS data'
                    os.system("matlab -softwareopengl -nodesktop -nosplash -noFigureWindows -r \"run_pressproc_auto(\'%s\');quit;\""%voxel)
                    
                else: 
                    print 'Processing MEGA-PRESS data'
                    os.system("matlab -softwareopengl -nodesktop -nosplash -noFigureWindows -r \"run_megapressproc_auto(\'M1m\');quit;\"")

spectral_registration(workspace, population, days, voxels)

                
                
