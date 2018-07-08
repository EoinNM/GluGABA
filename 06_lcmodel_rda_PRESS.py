import os
from utils.utils import *
from variables.variables import  *

#You must ssh compute-lcmodel-1 before running

def run_lcmodel_rda(population, workspace, PRESS_voxels, days):

    print '========================================================================================'
    print '                                GluGABA - 06 LCModel_RDA_PRESS                                 '
    print '========================================================================================'

    count = 0
    for subject in population:
        count += 1
        for day in days:
            for se_voxel in PRESS_voxels:
                
                print '================================================================================'
                print ' Running LCMODEL quantitation for PRESS RDA file subject %s, %s, %s' % (subject, se_voxel, day)
                print '================================================================================'

                subject_dir = os.path.join(workspace, subject)
                #I/O
                svs_dir = os.path.join(subject_dir, 'SVS', day, se_voxel, 'RDA')
                rda_met = os.path.join(svs_dir, '%s' % se_voxel, '%s.rda' % se_voxel)
                rda_h2o = os.path.join(svs_dir, '%s_w' % se_voxel, '%s_w.rda' % se_voxel)
                lcm_dir = mkdir_path(os.path.join(subject_dir, 'LCMODEL', day, se_voxel, 'RDA', se_voxel))

                # bin2raw
                mkdir_path(os.path.join(lcm_dir, 'met'))
                mkdir_path(os.path.join(lcm_dir, 'h2o'))

                os.system('~/lcmodel/6.3-1L/siemens/bin2raw %s %s/ met' %(rda_met, lcm_dir))
                os.system('~/lcmodel/6.3-1L/siemens/bin2raw %s %s/ h2o' %(rda_h2o, lcm_dir))

                # build control file

                file = open(os.path.join(lcm_dir, 'control'), "w")
                file.write(" $LCMODL\n")
                file.write(" srcraw= '%s' \n" % rda_met)
                file.write(" srch2o= '%s' \n" % rda_h2o)
                file.write(" savdir= '%s' \n" % lcm_dir)
                file.write(" ppmst= 4.0 \n")
                file.write(" ppmend= 0.3\n")
                file.write(" nunfil= 2048\n")
                file.write(" ltable= 7\n")
                file.write(" lps= 8\n")
                file.write(" lcsv= 11\n")
                file.write(" lcoraw= 10\n")
                file.write(" lcoord= 9\n")
                file.write(" hzpppm= 1.2328e+02\n")
                file.write(" filtab= '%s/table'\n" % lcm_dir)
                file.write(" filraw= '%s/met/RAW'\n" % lcm_dir)
                file.write(" filps= '%s/ps'\n" % lcm_dir)
                file.write(" filh2o= '%s/h2o/RAW'\n" % lcm_dir)
                file.write(" filcsv= '%s/spreadsheet.csv'\n" % lcm_dir)
                file.write(" filcor= '%s/coraw'\n" % lcm_dir)
                file.write(" filcoo= '%s/coord'\n" % lcm_dir)
                file.write(" filbas= '/a/software/.lcmodel/6.3-1L/basis-sets/press_te30_3t_01a.basis'\n")
                file.write(" echot= 30.00 \n")
                file.write(" dows= T \n")
                file.write(" doecc= T\n")
                file.write(" deltat= 8.330e-04\n")
                file.write(" $END\n")
                file.close()
                
                #run lcmodel
                print 'Running LCModel on RDA Files'
                os.system('sh /home/raid2/molloy/lcmodel/6.3-1L/execution-scripts/standard %s 30 %s %s' % (lcm_dir, lcm_dir, lcm_dir))

                #create PDF
                os.chdir(lcm_dir)
                print "Converting ps to .pdf for %s, %s, %s" % (subject, se_voxel, day)
                os.system("ps2pdf ps")

run_lcmodel_rda(test_population, workspace, PRESS_voxels, days)

