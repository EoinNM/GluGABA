import os
from os import *
from utils.utils import *
from variables.variables import *
import nipype.interfaces.fsl as fsl
import shutil
import glob

def anat_registration(workspace, population, days):
    
    print '====================================================='
    print '      GluGABA 03_Anatomical Registration'
    print '====================================================='
    
    count = 0
    for subject in population:
        count += 1
        for day in days:
            
            print '===================================================='        
            print '%s. Anatomical Registration Underway for %s %s' %(count, subject, day)
            print '===================================================='
            
            #I/O
            pres = os.path.join(workspace, 'DATA', subject, 'ANATOMICAL', 'pres', 'PRES.nii')
            anat_dir = os.path.join(workspace, 'DATA', subject, 'ANATOMICAL', day)
            anat_file = os.path.join(anat_dir, 'ANATOMICAL.nii')
            reg_dir = mkdir_path(os.path.join(workspace, 'DATA', subject, 'ANATOMICAL', 'Reg'))
            
            #go to registration directory
            os.chdir(reg_dir)
            
            #Register assessment T1 scans to scout coordinates via prescan T1
            print '1. Running prescan coregistration'
            os.system('flirt -in %s -ref %s -omat PRES_2_%s.mat -out PRES_2_%s.nii.gz '
                      '-dof 6 -cost mutualinfo -finesearch 18'
                      %(anat_file, pres, day, day))
            print'2. Inflating zipped data'
            os.system('gunzip -k PRES_2_%s.nii.gz'%(day))
            
            #copy inflated .nii & .mat files to correct days directory
            print '3. Now moving the data to the correct subdir'
            for reg_img in glob.glob(os.path.join(reg_dir, '*PRES_2_%s.nii'%(day))):
                shutil.move(reg_img, anat_dir)
            for reg_mat in glob.glob(os.path.join(reg_dir, '*PRES_2_%s.mat'%(day))):
                shutil.move(reg_mat, anat_dir)
        
            print '4. Apply coregistration transform to previously segmented tissue probability maps'
            os.chdir(anat_dir)
            #now appy registration parameters to segmented tissue probablility maps from step 2
            os.system('flirt -in c1ANATOMICAL -ref PRES_2_%s -applyxfm -init PRES_2_%s.mat -out CoregGM.nii.gz'%(day, day))
            os.system('flirt -in c2ANATOMICAL -ref PRES_2_%s -applyxfm -init PRES_2_%s.mat -out CoregWM.nii.gz'%(day, day))
            os.system('flirt -in c3ANATOMICAL -ref PRES_2_%s -applyxfm -init PRES_2_%s.mat -out CoregCSF.nii.gz'%(day, day))
            
            #binarise coregistered tissues maps
            gm_mask = os.path.join(anat_dir, 'CoregGM.nii')
            wm_mask = os.path.join(anat_dir, 'CoregWM.nii')
            csf_mask = os.path.join(anat_dir, 'CoregCSF.nii')
            
            print '5. Now-Thresholding & Binarising tissue classes & saving individual masks'
            # threshold/binarise tissue classes to create mask
            os.system('fslmaths %s -add %s -add %s -thr 0.5 -bin brain_mask' % (gm_mask, wm_mask, csf_mask))
            #binarise tissue masks for voxel stat calculations
            os.chdir(anat_dir)
            os.system('fslmaths %s -thr 0.5 -bin binGM' % (gm_mask))
            os.system('fslmaths %s -thr 0.5 -bin binWM' % (wm_mask))
            os.system('fslmaths %s -thr 0.5 -bin binCSF' % (csf_mask))
            
            #inflate coregistered binarised tissue probability maps
            print '6. Inflating zipped tissue maps'
            os.system('gunzip -k binGM.nii.gz')
            os.system('gunzip -k binWM.nii.gz')
            os.system('gunzip -k binCSF.nii.gz')
   
anat_registration(workspace, population, days)
            
            
