import os
from os import *
from variables.variables import *
import nipype.interfaces.spm as spm
import nipype.interfaces.fsl as fsl

def Segment_T1(workspace, population, days):

    print '========================================================================================'
    print '                                GluGABA - 02_Segmentation                                    '
    print '========================================================================================'

    count = 0
    for subject in population:
        count += 1
        
        for day in days:    
            
            print '==========================================================================='
            print ' %s. Segmenting & Binarising Anatomical Images & Tissue Classes for %s, %s.'  %(count, subject, day)
            print '==========================================================================='
            
            anatomical_dir = os.path.join(workspace, subject, 'ANATOMICAL', day)
            anatomical_file = os.path.join(anatomical_dir, 'ANATOMICAL.nii')

            # SPM_NewSegment
            seg = spm.NewSegment()
            seg.inputs.channel_files = anatomical_file
            seg.inputs.channel_info = (0.0001, 60, (True, True))
            seg.run()
            
            #create paths for masks
            gm_mask = os.path.join(anatomical_dir, 'c1ANATOMICAL.nii')
            wm_mask = os.path.join(anatomical_dir, 'c2ANATOMICAL.nii')
            csf_mask = os.path.join(anatomical_dir, 'c3ANATOMICAL.nii')
            
            print ' Now-Thresholding & Binarising tissue classes & Saving individual Masks for subject %s' % subject
            # threshold/binarise tissue classes to create mask
            os.system('fslmaths %s -add %s -add %s -thr 0.5 -bin brain_mask' % (gm_mask, wm_mask, csf_mask))
            
            #binarise tissue masks for step 04_voxel_stats
            os.chdir(anatomical_dir)
            os.system('fslmaths %s -thr 0.5 -bin GM' % (gm_mask))
            os.system('fslmaths %s -thr 0.5 -bin WM' % (wm_mask))
            os.system('fslmaths %s -thr 0.5 -bin CSF' % (csf_mask))
   
            print 'Now Making Whole Brain Mask for subject %s' % subject
            # create brain mask for GM, WM, CSF
            gm_bin = os.path.join(anatomical_dir, 'c1ANATOMICAL.nii')
            wm_bin = os.path.join(anatomical_dir, 'c2ANATOMICAL.nii')
            csf_bin = os.path.join(anatomical_dir, 'c3ANATOMICAL.nii')
            brain_mask = os.path.join(anatomical_dir, 'brain_mask.nii')
            os.system('fslmaths %s -add %s -add %s -fillh -dilM %s' % (gm_bin, wm_bin, csf_bin, brain_mask))


Segment_T1(workspace, test_population, days)
