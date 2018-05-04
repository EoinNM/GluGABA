import os
from variables.variables import *
import nipype.interfaces.spm as spm

def Segment_T1(workspace, population, days):

    print '========================================================================================'
    print ''
    print '                                GluGABA - 01.SEGMENT                                    '
    print ''
    print '========================================================================================'

    for subject in population:
        print '-Segmenting for subject %s' % subject

        for day in days:
            print '...  day', day
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
            
            print ' Now-Thresholding & Binarising tissue classes for subject %s' % subject
            # threshold/binarise tissue classes to create mask
            os.system('fslmaths %s -add %s -add %s -thr 0.5 -bin brain_mask' % (gm_mask, wm_mask, csf_mask))

	    # save outputs for individual binarised tissue classes
	    os.system('fslmaths gm_mask -thr 0.5 -bin GM')
	    os.system('fslmaths wm_mask -thr 0.5 -bin WM') 
	    os.system('fslmaths csf_mask -thr 0.5 -bin CSF')      

            print 'Now Making Mask for subject %s' % subject
            # create brain mask for GM, WM, CSF
            gm_bin = os.path.join(anatomical_dir, 'c1ANATOMICAL.nii')
            wm_bin = os.path.join(anatomical_dir, 'c2ANATOMICAL.nii')
            csf_bin = os.path.join(anatomical_dir, 'c3ANATOMICAL.nii')
            brain_mask = os.path.join(anatomical_dir, 'brain_mask.nii')
            os.system('fslmaths %s -add %s -add %s -fillh -dilM %s' % (gm_bin, wm_bin, csf_bin, brain_mask))


Segment_T1(workspace, population, days)
