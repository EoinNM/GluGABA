import os
import shutil
import dicom as pydcm
from utils.utils import mkdir_path

zfs = '/data/pt_nro174_mri/DATA/MRI/DATA'
workspace = '/nobackup/roggen2/Molloy/GluGABA/'

mkdir_path(workspace)

population = ["AL3T", "UC2T", "BMNX"]
days = ['base', 'day1', 'day7']
voxels = ["ACC", "M1", "M1m"]

#Read and copy all T1 MPRAGE and svs data from zfs to nobackup directory

def get_T1_svs(dst, subjects, scan_day, src):
    for subject in population:
        for day in days:
            for voxel in voxels:
                subject_dir = mkdir_path(os.path.join(workspace, subject))
                #anatomical dirs
                sub_T1_dcm_dir = mkdir_path(os.path.join(subject_dir, 'ANATOMICAL', day, 'ANATOMICAL_DCM'))
                sub_T1_nifti_dir = mkdir_path(os.path.join(subject_dir, 'ANATOMICAL', day, 'ANATOMICAL.Nii'))
                #svs dirs
                sub_ACCMETRDA_svs_dir = mkdir_path(os.path.join(subject_dir, 'SVS', day, "RDA", "ACC", "MET"))
                sub_ACCH2ORDA_svs_dir = mkdir_path(os.path.join(subject_dir, 'SVS', day, "RDA", "ACC", "H20"))
                sub_ACCMETTWX_svs_dir = mkdir_path(os.path.join(subject_dir, 'SVS', day, "TWX", "ACC", "MET"))
                sub_ACCH20TWX_svs_dir = mkdir_path(os.path.join(subject_dir, 'SVS', day, "TWX", "ACC", "H20"))
                sub_M1METRDA_svs_dir = mkdir_path(os.path.join(subject_dir, 'SVS', day, "RDA", "M1", "MET"))
                sub_M1H20RDA_svs_dir = mkdir_path(os.path.join(subject_dir, 'SVS', day, "RDA", "M1", "H20"))
                sub_M1METTWX_svs_dir = mkdir_path(os.path.join(subject_dir, 'SVS', day, "TWX", "M1", "MET"))
                sub_M1H20RDA_svs_dir = mkdir_path(os.path.join(subject_dir, 'SVS', day, "TWX", "M1", "H20"))
                sub_M1mMETRDA_svs_dir = mkdir_path(os.path.join(subject_dir, 'SVS', day, "RDA", "M1m", "MET"))
                sub_M1mH20RDA_svs_dir = mkdir_path(os.path.join(subject_dir, 'SVS', day, "RDA", "M1m", "H20"))
                sub_M1mH20TWX_svs_dir = mkdir_path(os.path.join(subject_dir, 'SVS', day, "TWX", "M1m", "MET"))
                sub_M1mH20TWX_svs_dir = mkdir_path(os.path.join(subject_dir, 'SVS', day, "TWX", "M1m", "H20"))