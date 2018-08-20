import os
from utils.utils import *
from variables.variables import *
import nipype.interfaces.fsl as fsl

def dice(workspace, PRESS_voxels, population, days):
    
   
    print '========================================================================================='
    print '                      GluGABA_05 Dice Metrics for PRESS Voxels                      '
    print '=========================================================================================' 
    
    count = 0
    for subject in population:
        count += 1
        
        print '===================================================='        
        print '%s. Dice Calculations are now Underway for %s' %(count, subject)
        print '===================================================='
        
        for voxel in voxels:
            for day in days:
            
                #path to voxel masks
                acc  = (os.path.join(workspace, 'DATA', subject, 'SVS', day, 'ACC', 'voxel_masks', 'ACC.rda_Mask.nii'))
                m1   = (os.path.join(workspace, 'DATA', subject, 'SVS', day, 'M1', 'voxel_masks', 'M1.rda_Mask.nii'))
                m1m  = (os.path.join(workspace, 'DATA', subject, 'SVS', day, 'M1m', 'voxel_masks', 'M1m.rda_Mask.nii'))
                
                #path to previously coregistered anatomical images 
                anat_path = os.path.join(workspace, 'DATA', subject, 'ANATOMICAL', day)
                anat = os.path.join(anat_path, 'Pres_2_%s.nii' %(day))
                
                #new dir for metrics
                dice_dir = mkdir_path(os.path.join(workspace, 'Results', 'PRESS', 'DICE', subject))
                os.chdir(dice_dir)
                
                #apply the coregistration parameters to the voxel masks
                print 'Applying %s coregistration to SVS' %(voxel)
                if not os.path.isfile('overlap_ACC_reg1.nii.gz'):
                    os.system('flirt -in %s -ref %s -applyxfm -init svs_reg1.mat -out overlap_ACC.nii.gz' %(acc, anat))
                    os.system('flirt -in %s -ref %s -applyxfm -init svs_reg1.mat -out overlap_M1.nii.gz' %(m1, anat))
                    os.system('flirt -in %s -ref %s -applyxfm -init svs_reg1.mat -out overlap_M1m.nii.gz' %(m1, anat))
                    
                dice1 = os.path.join(dice_dir, 'overlap_ACC.nii.gz')
                dice2 = os.path.join(dice_dir, 'overlap_M1.nii.gz')
                dice2 = os.path.join(dice_dir, 'overlap_M1m.nii.gz')
                
                print 'Calculating Dice Metric for %s' %(voxel)
                if not os.path.isfile('dice_metric_ACC.txt'):
                    calc_dice_metric(acc, anat, 'ACC')
                    calc_dice_metric(m1, anat, 'M1')
                    calc_dice_metric(m1m, anat, 'M1m')
                    
dice(workspace, PRESS_voxels, population, days)
            
