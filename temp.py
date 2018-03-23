# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
from os import *
import dicom as dcm
import shutil
import glob
from utils.utils import *
from variables.variables import *

mkdir_path(workspace)

def check_T1_SVS(test_population, zfs, workspace, days):
    for subject in test_population:
        for day in days:
            #data source for copying
            zfs_dcm_dir = os.path.join(zfs, subject, day, 'DICOM')

            #data destinations for copying
            temp_MRI = mkdir_path(os.path.join(workspace, subject, day, 'ANATOMICAL'))
            NII_dir = mkdir(os.path.join(temp_MRI, 'NII'))
            DCM_dir = mkdir_path(os.path.join(temp_MRI, 'DICOM'))

            #read all DICOM

            if os.listdir(DCM_dir) is not None:
                all_dicoms = []
            for img in os.listdir(zfs_dcm_dir):
                img = os.path.join(zfs_dcm_dir, img)
            all_dicoms.append(img)

            #copy the T1 data to temp workspace
            mprage_dicoms = []
            for img in sorted(all_dicoms):
                series_description = dcm.read_file(img).SeriesDescription
                if "MPRAGE" in series_description:
                    mprage_dicoms.append(img)

                    # 2. copy MPRAGE dicoms to workspace
                    for img in mprage_dicoms:
                        shutil.copy(img, DCM_dir)

                        #convert dicoms to NIFTI
                        os.system('dcm2nii -0 %s %s' %(NII_dir, DCM_dir))
                        #rename .nii output
                        for nifti in os.listdir(NII_dir):
                            if nifti.endswith('nii'):
                                os.rename(str(os.path.join(NII_dir, nifti))),
                                str(os.path.join(NII_dir, 'Anatomical.nii'))

                                #copy MRS data
                                for subject in test_population:
                                    for day in days:
                                        for voxel in voxels:
                                            zfs_mrs_dir = os.path.join(zfs, subject, day, SVS)
                                            temp_MRS = mkdir_path(os.path.join(workspace, subject))

                                            #copy TWIX data
                                            twx_met_src = glob.glob(os.path.join(zfs_mrs_dir, voxel, 'TWIX', voxel, '*'))[0]
                                            twx_h20_src = glob.glob(os.path.join(zfs_mrs_dir, voxel, 'TWIX', '%s_w' % voxel, '*'))[0]

                                            twx_met_dst = mkdir_path(os.path.join(temp_MRS, 'SVS', day, voxel, 'TWIX', voxel))
                                            twx_h20_dst = mkdir_path(os.path.join(temp_MRS, 'SVS', day, voxel, 'TWIX', '%s_w' % voxel))

                                            os.system('cp %s %s/%s.dat' % (twx_met_src, twx_met_dst, voxel))
                                            os.system('cp %s %s/%s_w.dat ' % (twx_h20_src, twx_h20_dst, voxel))

                                            #copyRDA
                                            rda_met_src = glob.glob(os.path.join(zfs_dir, voxel, 'RDA', '*'))[0]
                                            rda_h20_src = glob.glob(os.path.join(zfs_dir, voxel, 'RDA', '*'))[0]

                                            rda_met_dst = mkdir_path(os.path.join(subject_dir, 'SVS', day, voxel, 'RDA', voxel))
                                            rda_h20_dst = mkdir_path(os.path.join(subject_dir, 'SVS', day, voxel, 'RDA', '%s_w' % voxel))

                                            os.system('cp %s %s/%s.rda' % (rda_met_src, rda_met_dst, voxel))
                                            os.system('cp %s %s/%s_w.rda' % (rda_h20_src, rda_h20_dst, voxel))

check_T1_SVS(test_population, zfs, workspace, days)