#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 10:20:49 2018

@author: molloy
"""

import os, sys
from os import *
from variables.variables import *
from utils.utils import *
import glob

def GABA(zfs, population, days, MPRESS_voxels):
    
    count = 0
    for subject in population:
        count +=1
        for day in days:
            for voxel in MPRESS_voxels:
                
                print '======================================================================'
                print "      %s. Copying for all GABA for %s, %s" %(count, subject, day)
                print '======================================================================='
                
                #data src & dst
                zfs_GABA_met = os.path.join(zfs, subject, day, 'SVS', 'M1m', 'TWIX', 'M1m')
                zfs_GABA_h20 = os.path.join(zfs, subject, day, 'SVS', 'M1m', 'TWIX', 'M1m_w')
                new_dir = mkdir_path(os.path.join(godata, 'GABA', subject, day))

		#copy met                
                for GABA_met in glob.glob(os.path.join(zfs_GABA_met, '*mpw529_M1_FID*')):
                    GABA_met_src = GABA_met
                    os.system('cp %s %s' % (GABA_met, new_dir))
                
                #copy water
                for GABA_h20 in glob.glob(os.path.join(zfs_GABA_h20, '*mpw529_M1_ref*')):
                    GABA_h20_src = GABA_h20
                    os.system('cp %s %s' % (GABA_h20, new_dir))
                
                print '======================================================================'    
                print "     %s. Renaming all GABA in new location for %s, %s" %(count, subject, day)
                print '======================================================================'
                 
                for GABA_met in glob.glob(os.path.join(new_dir, '*mpw529_M1_FID*')):
                    os.rename(str(os.path.join(new_dir, GABA_met)),
                              str(os.path.join(new_dir, 'Sub_%s_%s_M1m.dat' % (count, day))))
                    
                for GABA_h20 in glob.glob(os.path.join(new_dir, '*mpw529_M1_ref*')):
                    os.rename(str(os.path.join(new_dir, GABA_h20)),
                              str(os.path.join(new_dir, 'Sub_%s_%s_M1m_w.dat' % (count, day))))
                
GABA(zfs, population, days, MPRESS_voxels)
            
            
