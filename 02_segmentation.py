import os
from os import *
from variables.variables import *
import nipype.interfaces.spm as spm

def Segment_T1(workspace, population, days):

    print '========================================================================================'
    print '                                GluGABA - 02_Segmentation                                    '
    print '========================================================================================'

    count = 0
    for subject in population:
        count += 1
        for day in days:    
            
            print '=============================================================================='
            print ' %s. Segmenting & Binarising Anatomical Images & Tissue Classes for %s, %s.'  %(count, subject, day)
            print '=============================================================================='
            
            anatomical_dir = os.path.join(workspace, 'DATA', subject, 'ANATOMICAL', day)
            anatomical_file = os.path.join(anatomical_dir, 'ANATOMICAL.nii')

            #SPM_NewSegment
            seg = spm.NewSegment()
            seg.inputs.channel_files = anatomical_file
            seg.inputs.channel_info = (0.0001, 60, (True, True))
            seg.run()

            print 'Now Making Whole Brain Mask for subject %s' % subject
            # create brain mask for GM, WM, CSF
            gm_bin = os.path.join(anatomical_dir, 'c1ANATOMICAL.nii')
            wm_bin = os.path.join(anatomical_dir, 'c2ANATOMICAL.nii')
            csf_bin = os.path.join(anatomical_dir, 'c3ANATOMICAL.nii')
            brain_mask = os.path.join(anatomical_dir, 'brain_mask.nii')
            #add binned masks with specific spatial resolution parameters in fslmaths
            os.system('fslmaths %s -add %s -add %s -fillh -dilM %s' % (gm_bin, wm_bin, csf_bin, brain_mask))

Segment_T1(workspace, population, days)
