"""
Created on Mon Apr 16 16:33:53 2018

@author: molloy
"""

import os
from os import *
from utils.utils import *
from variables.variables import *
import shutil

def create_masks(population, workspace, days, voxels):

    print '============================================================================================'
    print '                             GluGABA_02 - Create Voxel Masks                                '
    print '============================================================================================'

    count = 0
    for subject in population:
        for day in days:
            for voxel in voxels:
                count +=1
            
                print '============================================================================================'
                print '                %s. Obtaining RDA Geometry and Creating Binarised Voxel Mask for %s, %s, %s' %(count, subject, day, voxel)
                print '============================================================================================'    
    
                #work dir
                sub_dir = os.path.join(workspace, 'population')
                #set paths & define files for RDA_TO_NIFTI MatLab script              
                t1Path = os.path.join(sub_dir, subject, 'ANATOMICAL', day + '/')
                t1File = "ANATOMICAL.nii"
                RPath = os.path.join(sub_dir, subject,'SVS', day, voxel, 'RDA', voxel + '/')
                RFile = '%s.rda' %(voxel)
                
                #create new output_dir
                mkdir_path(os.path.join(sub_dir, subject, 'SVS', day, voxel, 'voxel_masks'))
                mask_dir = os.path.join(sub_dir, subject, 'SVS', day, voxel, 'voxel_masks')

                
                #MatLab/SPM in os.system
                os.system("matlab -nodesktop -nosplash -r \"RDA_TO_NIFTI(\'%s\', \'%s\', \'%s\', \'%s\') ; quit;\"" %(t1Path, t1File, RPath, RFile))

                #move voxel masks from T1 path directory to voxel_mask dir
                for file in os.listdir(t1Path):
                    if 'rda' in file and '%s' %voxel in file:
                        shutil.move(os.path.join(t1Path, file), mask_dir)

                    elif 'coord' in file:
                        shutil.move(os.path.join(t1Path, file), mask_dir)

create_masks(test_population, workspace, days, voxels)
