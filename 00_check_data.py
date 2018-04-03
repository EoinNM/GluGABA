import os
from os import *
import dicom as dcm
import shutil
import glob
from utils.utils import *
from variables.variables import *

mkdir_path(workspace)

def check_T1_SVS(population, zfs, workspace, days):



    print '========================================================================================'
    print ''
    print '                                GluGABA - 00.Check Data                                 '
    print ''
    print '========================================================================================'


    count = 0
    for subject in population:
        count += 1

        print '========================================================================================'
        print '-%s. Checking data for subject %s' %(count,subject)

        for day in days:
            #### I/O
            #  make dirs & def src dir
            zfs_dcm_dir = os.path.join(zfs, subject, day, 'DICOM')
            sub_dir = mkdir_path(os.path.join(workspace, subject))
            anat_dir = mkdir_path(os.path.join(sub_dir, 'ANATOMICAL', day))
            dcm_dir = mkdir_path(os.path.join(anat_dir, 'DCM'))
            nii_dir = mkdir_path(os.path.join(anat_dir, 'NII'))

            print '... Copying T1 data for day', day

            if not os.path.isfile(os.path.join(anat_dir, 'ANATOMICAL.nii')):

                # read all DICOM
                all_dicoms = [os.path.join(zfs_dcm_dir, img) for img in  os.listdir(zfs_dcm_dir)]

                # read T1 only
                mprage_dicoms = []
                for img in sorted(all_dicoms):
                    series_description = dcm.read_file(img).SeriesDescription
                    if "MPRAGE" in series_description:
                        mprage_dicoms.append(img)

                # copy MPRAGE dicoms to workspace
                for file in mprage_dicoms:
                    shutil.copy(file, dcm_dir)

                # convert dicoms to NIFTI
                os.system('dcm2niix -o %s %s' % (nii_dir, dcm_dir))

                # rename .nii output
                for nifti in os.listdir(nii_dir):
                    if nifti.endswith('nii'):
                        os.rename(str(os.path.join(nii_dir, nifti)),
                            str(os.path.join(anat_dir, 'ANATOMICAL.nii')))

                # cleanup
                os.system('rm -rf %s %s' %(dcm_dir, nii_dir))

            else:
                print '...... MPRAGE already converted'

            print '... Copying SVS data for day', day

            # copy MRS data
            for voxel in voxels:

                print '...... Working on voxel', voxel

                zfs_mrs_dir = os.path.join(zfs, subject, day, 'SVS')
                sub_dir = mkdir_path(os.path.join(workspace, subject))


                # copy TWIX data
                twx_met_src = glob.glob(os.path.join(zfs_mrs_dir, voxel, 'TWIX', voxel, '*'))[0]
                twx_h20_src = glob.glob(os.path.join(zfs_mrs_dir, voxel, 'TWIX', '%s_w' % voxel, '*'))[0]

                twx_met_dst = mkdir_path(os.path.join(sub_dir, 'SVS', day, voxel, 'TWIX', voxel))
                twx_h20_dst = mkdir_path(os.path.join(sub_dir, 'SVS', day, voxel, 'TWIX', '%s_w' % voxel))

                os.system('cp %s %s/%s.dat' % (twx_met_src, twx_met_dst, voxel))
                os.system('cp %s %s/%s_w.dat' % (twx_h20_src, twx_h20_dst, voxel))

                # copyRDA
                rda_met_src = glob.glob(os.path.join(zfs_mrs_dir, voxel, 'RDA', '*'))[0]
                rda_h20_src = glob.glob(os.path.join(zfs_mrs_dir, voxel, 'RDA', '*'))[0]

                rda_met_dst = mkdir_path(os.path.join(sub_dir, 'SVS', day, voxel, 'RDA', voxel))
                rda_h20_dst = mkdir_path(os.path.join(sub_dir, 'SVS', day, voxel, 'RDA', '%s_w' % voxel))

                os.system('cp %s %s/%s.rda' % (rda_met_src, rda_met_dst, voxel))
                os.system('cp %s %s/%s_w.rda' % (rda_h20_src, rda_h20_dst, voxel))

check_T1_SVS(population, zfs, workspace, days)