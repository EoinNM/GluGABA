import os
from os import *
import dicom as dcm
import shutil
import glob
from utils.utils import *
from variables.variables import *

mkdir_path(workspace)

def pull_T1(population, zfs, workspace, days):

    print '========================================================================================'
    print '                                GluGABA - 00_Pull_T1                                    '
    print '========================================================================================'


    count = 0
    for subject in population:
        count += 1

        print '==================================='
        print ' %s. Getting data for subject %s' %(count,subject)
        print '==================================='
        for day in days:
            
            if not os.path.isfile(os.path.join(workspace, 'DATA', subject, 'ANATOMICAL', day, 'ANATOMICAL.nii')):
            
                #I/0
                zfs_dcm_dir = os.path.join(zfs, subject, day, 'DICOM')
                sub_dir = mkdir_path(os.path.join(workspace, 'DATA', subject))
                anat_dir = mkdir_path(os.path.join(sub_dir, 'ANATOMICAL', day))
                dcm_dir = mkdir_path(os.path.join(anat_dir, 'DCM'))
                nii_dir = mkdir_path(os.path.join(anat_dir, 'NII'))
    
                print '... Copying T1 data for day', day
    
                    # read all DICOM
                all_dicoms = [os.path.join(zfs_dcm_dir, img) for img in  os.listdir(zfs_dcm_dir)]

                # read T1 only
                mprage_dicoms = []
                for img in sorted(all_dicoms):
                    series_description = dcm.read_file(img).SeriesDescription
                    if "MPRAGE" in series_description:
                        mprage_dicoms.append(img)

                # copy MPRAGE dicoms to workspace
                print 'Now copying data for %s, %s'%(subject, day)
                for file in mprage_dicoms:
                    shutil.copy(file, dcm_dir)

                # convert dicoms to NIFTI
                print 'Converting now to .nii for %s, %s'%(subject, day)
                os.system('dcm2niix -o %s %s' % (nii_dir, dcm_dir))

                # rename .nii output
                print 'Renaming all T1 data for %s, %s'%(subject, day)
                for nifti in os.listdir(nii_dir):
                    if nifti.endswith('nii'):
                        os.rename(str(os.path.join(nii_dir, nifti)),
                            str(os.path.join(anat_dir, 'ANATOMICAL.nii')))

                # cleanup
                print 'Cleaning up unneeded DICOMS for %s, %s'%(subject, day)
                os.system('rm -rf %s %s' %(dcm_dir, nii_dir))

            else:
                print '...... MPRAGE already converted'

pull_T1(population, zfs, workspace, days)
