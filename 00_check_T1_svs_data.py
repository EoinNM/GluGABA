import os
from os import *
import shutil
import glob
import dicom as pydcm
from utils.utils import mkdir_path

zfs = '/data/pt_nro174_mri/DATA/MRI/DATA'
workspace = '/nobackup/roggen2/Molloy/GluGABA/'

mkdir_path(workspace)

population = ["AL3T", "UC2T", "BMNX"]
days = ['base', 'day1', 'day7']
voxels = ["ACC", "M1", "M1m"]
svs_file = ["TWIX", "RDA"]
sequence = ["PRESS", "MEGA_PRESS"]



#Read and copy all T1 MPRAGE and svs data from zfs to nobackup directory

def get_T1_svs(workspace, population, days, voxels, zfs):
    for subject in population:
        for day in days:
            subject_dir = mkdir_path(os.path.join(workspace, subject))
           #make anatomical dirs
            sub_T1_dcm_dir = mkdir_path(os.path.join(subject_dir, 'ANATOMICAL', day, 'ANATOMICAL_DCM'))
            sub_T1_nifti_dir = mkdir_path(os.path.join(subject_dir, 'ANATOMICAL', day, 'ANATOMICAL.nii'))
                    
            zfs_dcm_dir = os.path.join(zfs, subject, day, 'DICOM')

            #1. read all dicoms and append into list with full path, then read S.D. for T1

            if os.listdir(sub_T1_dcm_dir) is not None:
                 all_dicoms = []
            for img in os.listdir(zfs_dcm_dir):
                 img = os.path.join(zfs_dcm_dir, img)
                 all_dicoms.append(img)
                        
            mprage_dicoms = []
            for img in sorted(all_dicoms):
                series_description = pydcm.read_file(img).SeriesDescription
                if "MPRAGE" in series_description:
                    mprage_dicoms.append(img)

                    #2. copy MPRAGE dicoms to workspace
                    for img in mprage_dicoms:
                        shutil.copy(img, sub_T1_dcm_dir)
                    #3. convert to .nii
                    os.system('dcm2niix -o %s %s' %(sub_T1_nifti_dir, sub_T1_dcm_dir))
                   #4. rename all .nii output to "Anatomical.nii"
                    for nifti in os.listdir(sub_T1_nifti_dir):
                       if nifti.endswith('nii'):
                           os.rename(str(os.path.join(sub_T1_nifti_dir, nifti)),
                              str(os.path.join(sub_T1_nifti_dir, 'Anatomical.nii')))

                    #copy MRS data for these 3 subjects
                    #5. copy TWX
                    for subject in population:
                        for day in days:
                            for voxel in voxels:
                                zfs_dir = os.path.join(zfs, subject, day, 'SVS')
                                subject_dir = mkdir_path(os.path.join(workspace, subject))
                        
                                twx_met_src = glob.glob(os.path.join(zfs_dir, voxel, 'TWIX', voxel, '*'))[0]
                                twx_h20_src = glob.glob(os.path.join(zfs_dir, voxel, 'TWIX', '%s_w'%voxel, '*'))[0]
                    
                                twx_met_dst = mkdir_path(os.path.join(subject_dir, 'SVS', day, voxel, 'TWIX', voxel))
                                twx_h20_dst = mkdir_path(os.path.join(subject_dir, 'SVS', day, voxel, 'TWIX', '%s_w'%voxel))
                    
                                os.system('cp %s %s/%s.dat' % (twx_met_src, twx_met_dst, voxel))
                                os.system('cp %s %s/%s_w.dat ' % (twx_h20_src, twx_h20_dst, voxel))

                                #6. copy RDA
                                rda_met_src = glob.glob(os.path.join(zfs_dir, voxel, 'RDA', '*'))[0]
                                rda_h20_src = glob.glob(os.path.join(zfs_dir, voxel, 'RDA', '*'))[0]
                
                                rda_met_dst = mkdir_path(os.path.join(subject_dir,'SVS', day, voxel, 'RDA', voxel))
                                rda_h20_dst = mkdir_path(os.path.join(subject_dir,'SVS', day, voxel, 'RDA', '%s_w'%voxel))
                                
                                os.system('cp %s %s/%s.rda' % (rda_met_src, rda_met_dst, voxel))
                                os.system('cp %s %s/%s_w.rda' % (rda_h20_src, rda_h20_dst, voxel))
#                                
get_T1_svs(workspace, population, days, voxels, zfs)