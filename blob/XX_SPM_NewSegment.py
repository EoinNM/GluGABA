#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 11:14:50 2018

@author: molloy
"""

import os
import nipype.interfaces.spm as spm
import nipype.interfaces.fsl as fsl
from utils.utils import mkdir_path
from distutils.dir_util import copy_tree

#be inside fsl and spm environments
src = ('/NOBACKUP2/Molloy/GluGABA/')
temp = ('/NOBACKUP2/Molloy/temp/')

mkdir_path(temp)

population = ['AL3T', 'BMNX', 'UC2T']
days = ['base', 'day1', 'day7']

#make target directories
for subject in population:
    for day in days:
        sub_dir = mkdir_path(os.path.join(temp, subject, day, 'SPM_Anatomical_Segment'))
        src_dir = os.path.join(src, subject, 'ANATOMICAL', day)
        
        #copy the data over from the original workspace :)
        copy_tree (src_dir, sub_dir)
        
        #Segment using SPM NewSegment - code from github
        anatomical_file = os.path.join(sub_dir, 'Anatomical.nii')
        seg                      = spm.NewSegment()
        seg.inputs.channel_files = anatomical_file
        seg.inputs.channel_info  = (0.0001, 60, (True, True))
        seg.run()
        
        #create dirs for masks
        gm_mask = str(os.path.join(sub_dir, 'c1Anatomical.nii'))
        wm_mask = str(os.path.join(sub_dir, 'c2Anatomical.nii'))
        csf_mask = str(os.path.join(sub_dir, 'c3Anatomical.nii'))
        
        #threshold/binarise masks - code from github
        thr_hbin_GM1                          = fsl.Threshold()
        thr_hbin_GM1.inputs.in_file           = gm_mask
        thr_hbin_GM1.inputs.thresh            = 0.5
        thr_hbin_GM1.inputs.args              = '-bin'
        thr_hbin_GM1.inputs.ignore_exception  = True
        thr_hbin_GM1.inputs.out_file          = str(os.path.join(sub_dir, 'c1Anatomical.nii'))
        thr_hbin_GM1.run()

        thr_hbin_WM1                          = fsl.Threshold()
        thr_hbin_WM1.inputs.in_file           = wm_mask
        thr_hbin_WM1.inputs.thresh            = 0.5
        thr_hbin_WM1.inputs.args              = '-bin'
        thr_hbin_WM1.inputs.ignore_exception  = True
        thr_hbin_WM1.inputs.out_file          = str(os.path.join(sub_dir, 'c2Anatomical.nii'))
        thr_hbin_WM1.run()

        thr_hbin_CSF1                         = fsl.Threshold()
        thr_hbin_CSF1.inputs.in_file          = csf_mask
        thr_hbin_CSF1.inputs.thresh           = 0.5
        thr_hbin_CSF1.inputs.args             = '-bin'
        thr_hbin_CSF1.inputs.ignore_exception = True
        thr_hbin_CSF1.inputs.out_file         = str(os.path.join(sub_dir, 'c3Anatomical.nii'))
        thr_hbin_CSF1.run()
        
        # create brain mask for GM, WM, CSF - code from github
        gm_bin = os.path.join(sub_dir, 'c1Anatomical.nii')
        wm_bin = os.path.join(sub_dir, 'c2Anatomical.nii')
        cm_bin = os.path.join(sub_dir, 'c3Anatomical.nii')
        brain_mask = os.path.join(sub_dir, 'ANATOMICAL_brain_mask.nii')
        os.system('fslmaths %s -add %s -add %s -fillh -dilM %s'%(gm_bin,wm_bin, cm_bin, brain_mask))
        
        