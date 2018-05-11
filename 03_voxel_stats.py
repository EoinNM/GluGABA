"""
Created on Wed May  2 14:51:02 2018

@author: molloy
"""
import os
from variables.variables import *
from utils.utils import *
import nibabel as nb
import numpy as np

def calc_partial_vols(population, workspace, voxels, days):
    
    print '================================================================================='
    print '                      GluGABA_04 - Calculate Patial Volumes                  '
    print '================================================================================='
            
    count = 0
    for subject in population:
        count += 1
        print '================================================================================='
        print ' %s. Calculating Voxel Tissue Stats for subject %s' %(count, subject)

        for voxel in voxels:
            for day in days:

                print '.... %s -- %s' %(voxel, day)

                seg_dir = os.path.join(workspace, subject, 'ANATOMICAL', day)
                svs_dir = os.path.join(workspace, subject, 'SVS', day, voxel, 'voxel_masks')
                
                #Output
                mkdir_path(os.path.join(workspace, subject, 'SVS', day, voxel, 'voxel_stats'))
                percent_dir = os.path.join(workspace, subject, 'SVS', day, voxel, 'voxel_stats')
                
                #load binarised masks & SVS mask
                gm_mask = os.path.join(seg_dir, 'GM.nii.gz')
                wm_mask = os.path.join(seg_dir, 'WM.nii.gz')
                csf_mask = os.path.join(seg_dir, 'CSF.nii.gz')
                svs_mask = os.path.join(svs_dir, '%s.rda_Mask.nii' %(voxel))

                #import data
                gm_data = (nb.load(gm_mask).get_data())
                wm_data = (nb.load(wm_mask).get_data())
                csf_data = (nb.load(csf_mask).get_data())
                svs_data = (nb.load(svs_mask).get_data())

                #calculate tissue concentrations ---> multiply binary masks
                total_gm = gm_data * svs_data
                total_wm = wm_data * svs_data
                total_csf = csf_data * svs_data
                
                #sum of above multiplication is voxel concentration of GM, WM, CSF
                total_svs = np.sum(svs_data)
                total_gm_svs = np.sum(total_gm)
                total_wm_svs = np.sum(total_wm)
                total_csf_svs = np.sum(total_csf)
                
                #calculate percentages of tissue ---> divide by total svs voxel count and output percentage
                svs_gm_percentage = float(total_gm_svs) / float(total_svs)*100
                svs_wm_percentage = float(total_wm_svs) / float(total_svs)*100
                svs_csf_percentage = float(total_csf_svs) / float(total_svs)*100
                
                #create and save concentrations to numpy array
                compartmentation_perc = np.array([svs_gm_percentage, svs_wm_percentage, svs_csf_percentage])
                print compartmentation_perc
                np.save(os.path.join(percent_dir, 'stats.npy'), compartmentation_perc)

                #also write percentage to text file
                 os.chdir(percent_dir)
                 with open('SVS_Voxel_Tissue_Stats.txt', "ab") as file:
                    file.write(b"Grey_Matter_Percentage....."), file.write(b'%f\n' %svs_gm_percentage)
                    file.write(b"White_Matter_Percentage...."), file.write(b'%f\n' %svs_wm_percentage)
                    file.write(b"CSF_percentage............."), file.write(b'%f\n' %svs_csf_percentage)

calc_partial_vols(test_population, workspace, voxels, days)
