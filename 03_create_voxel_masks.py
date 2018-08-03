import os
from os import *
from utils.utils import *
from variables.variables import *
import shutil

def create_masks(population, workspace, days, voxels):

    print '============================================================================================'
    print '                             GluGABA -03_Create_Voxel_Masks                                '
    print '============================================================================================'

    count = 0
    for subject in population:
        count +=1
        
        for day in days:
            for voxel in voxels:
                    
                print '============================================================================================'
                print '     %s. Obtaining RDA Geometry and Creating Binarised Voxel Mask for %s, %s, %s' %(count, subject, day, voxel)
                print '============================================================================================'    
                
                if not os.path.isfile(os.path.join(workspace, 'DATA', subject, 'SVS', day, voxel, 'RDA', voxel)):
                
                    #work dir
                    sub_dir = os.path.join(workspace)
                    
                    #set paths & define files for RDA_TO_NIFTI MatLab script              
                    t1Path = os.path.join(sub_dir, 'DATA', subject, 'ANATOMICAL', day + '/')
                    t1File = "ANATOMICAL.nii"
                    RPath = os.path.join(sub_dir, 'DATA', subject, 'SVS', day, voxel, 'RDA', voxel + '/')
                    RFile = '%s.rda' %(voxel)
                    
                    #create new output_dir
                    mkdir_path(os.path.join(sub_dir, 'DATA', subject, 'SVS', day, voxel, 'voxel_masks'))
                    mask_dir = os.path.join(sub_dir, 'DATA', subject, 'SVS', day, voxel, 'voxel_masks')
                    
                    #MatLab/SPM in os.system
                    os.system("matlab -nodesktop -nosplash -softwareopengl -noFigureWindows -r \"RDA_TO_NIFTI_e(\'%s\', \'%s\', \'%s\', \'%s\') ; quit;\"" %(t1Path, t1File, RPath, RFile))
    
                    #move voxel masks from T1 path directory to voxel_mask dir
                    for file in os.listdir(t1Path):
                        if 'rda' in file and '%s' %voxel in file:
                            shutil.move(os.path.join(t1Path, file), mask_dir)
    
                        elif 'coord' in file:
                            shutil.move(os.path.join(t1Path, file), mask_dir)
                        
                else:
                    print 'Mask already exists - Check dir to see it'

create_masks(population, workspace, days, voxels)
