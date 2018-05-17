import os
from os import *
from variables.variables import *
from utils.utils import *
import shutil
import glob

def check_svs(test_population, days, voxels, PRESS_voxels, MPRESS_voxels, workspace, zfs):
    
    print '========================================================================================'
    print '                                GluGABA - 01 Check_SVS                                 '
    print '========================================================================================'
    
    count = 0
    for subject in test_population:
        count += 1
        
        print "===================="
        print "%s. Working on %s" %(count, subject) 
        print "===================="
        
        for day in days:          
            print "Copying for all MRS.zip for %s" %(day)
            
            #data sources
            zfs_mrs = os.path.join(zfs, subject, day, 'SVS')
            sub_dir = mkdir_path(os.path.join(workspace, subject, 'SVS', day))
                
            #copy zipped files to workspace
            zip_svs = glob.iglob(os.path.join(zfs_mrs, "*.zip"))
            for file in zip_svs:
                if os.path.isfile(file):
                    shutil.copy(file, sub_dir)
                else:
                    print 'no mrs zip files here to copy...'

           #rename zips
            print "Renaming zipped MRS file for %s" %(day)
            for zip_file in os.listdir(sub_dir):
                    if zip_file.endswith('zip'):
                        os.rename(str(os.path.join(sub_dir, zip_file)),
                                  str(os.path.join(sub_dir, 'MRS.zip')))

            #unzip
            print "Inflating MRS files for %s:" %(day)
            os.chdir(sub_dir)
            os.system("unzip MRS.zip")
            
            print "Cleaning up unneeded zip files"
            os.remove("MRS.zip")
            
            #rename unzipped file
            print "Now renaming unzipped directory"
            for unzip_file in os.listdir(sub_dir):
                os.rename(str(os.path.join(sub_dir, unzip_file)),
                          str(os.path.join(sub_dir, 'unzipped_mrs')))
            
            #copy PRESS data
            for se_voxel in PRESS_voxels:
    
                print "Creating new Locations for MRS data"
            
                #RDA Files
                RDA_PRESS_met_dst = mkdir_path(os.path.join(sub_dir, se_voxel, 'RDA', se_voxel))
                RDA_PRESS_h20_dst = mkdir_path(os.path.join(sub_dir, se_voxel, 'RDA', '%s_w' % se_voxel))
                RDA_MPRESS_met_dst = mkdir_path(os.path.join(sub_dir, 'M1m', 'RDA', 'M1m'))
                RDA_MPRESS_h20_dst = mkdir_path(os.path.join(sub_dir, 'M1m', 'RDA', 'M1m_w'))
            
                #Twix Files
                twx_PRESS_met_dst = mkdir_path(os.path.join(sub_dir, se_voxel, 'TWIX', se_voxel))
                twx_PRESS_h20_dst = mkdir_path(os.path.join(sub_dir, se_voxel, 'TWIX', '%s_w' % se_voxel))
                twx_MPRESS_met_dst = mkdir_path(os.path.join(sub_dir, 'M1m', 'TWIX', 'M1m'))
                twx_MPRESS_h20_dst = mkdir_path(os.path.join(sub_dir, 'M1m', 'TWIX', 'M1m_w'))
                
                print "Moving PRESS data to correct location for %s, %s, %s:" %(subject, se_voxel, day)

                #RDA PRESS src
                RDA_PRESS_met_src = os.path.join(sub_dir, 'unzipped_mrs', 'se%s.rda' % se_voxel)
                RDA_PRESS_h20_src = os.path.join(sub_dir, 'unzipped_mrs', 'se%sref.rda' %(se_voxel))
                 
                #copy RDA PRESS
                os.system('cp %s %s/%s.rda' % (RDA_PRESS_met_src, RDA_PRESS_met_dst, se_voxel))
                os.system('cp %s %s/%s_w.rda' % (RDA_PRESS_h20_src, RDA_PRESS_h20_dst, se_voxel))
                
                #TWIX PRESS src
                for press_met_dat in glob.glob(os.path.join(sub_dir, 'unzipped_mrs', '*svs_se_%s_FID*' % (se_voxel))):
                    twx_PRESS_met_src = press_met_dat
                    os.system('cp %s %s/%s.dat' % (twx_PRESS_met_src, twx_PRESS_met_dst, se_voxel))
                    
                for press_h20_dat in glob.glob(os.path.join(sub_dir, 'unzipped_mrs', '*svs_se_%s_ref*' % (se_voxel))):
                    twx_PRESS_h20_src = press_h20_dat
                    os.system('cp %s %s/%s_w.dat' % (twx_PRESS_h20_src, twx_PRESS_h20_dst, se_voxel))

            for mp_voxel in MPRESS_voxels:
                print "Moving MEGA-PRESS data to correct location for %s, %s:" %(subject, day)

        	     #copy MPRESS data

                #RDA MPRESS src
                RDA_MPRESS_met_src = os.path.join(sub_dir, 'unzipped_mrs', 'mpM1.rda')
                RDA_MPRESS_h20_src = os.path.join(sub_dir, 'unzipped_mrs', 'mpM1ref.rda')

                #copy RDA MPRESS
                os.system('cp %s %s/%s.rda' % (RDA_MPRESS_met_src, RDA_MPRESS_met_dst, mp_voxel))
                os.system('cp %s %s/%s_w.rda' % (RDA_MPRESS_h20_src, RDA_MPRESS_h20_dst, mp_voxel))
            
                #TWIX MPRESS src
                for mpress_met_dat in glob.glob(os.path.join(sub_dir, 'unzipped_mrs', '*mpw529_M1_FID*')):
                    twx_MPRESS_met_src = mpress_met_dat
                    os.system('cp %s %s/%s.dat' % (twx_MPRESS_met_src, twx_MPRESS_met_dst, mp_voxel))
                
                for mpress_h20_dat in glob.glob(os.path.join(sub_dir, 'unzipped_mrs', '*mpw529_M1_ref*')):
                    twx_MPRESS_h20_src = mpress_h20_dat
                    os.system('cp %s %s/%s.dat' % (twx_MPRESS_h20_src, twx_MPRESS_h20_dst, mp_voxel))
            
                #clean up unneded duplicates
                print "Cleaning up unneeded duplicate files"
                os.chdir(sub_dir)
                os.system('rm -rf unzipped_mrs')

check_svs(test_population, days, voxels, PRESS_voxels, MPRESS_voxels, workspace, zfs)
