import os
from utils.utils import *
from variables.variables import  *
import shutil

def run_lcmodel_twx(population, workspace, PRESS_voxels, days):

    print '========================================================================================'
    print '                               GluGABA - 09_LCModel_TWIX_PRESS                         '
    print '========================================================================================'

    count = 0
    for subject in population:
        count += 1
        for day in days:
            for se_voxel in PRESS_voxels:
                
                print '============================================================================='
                print ' %s. Running LCMODEL quantitation on PRESS TWIX data for %s, %s, %s' % (count, subject, se_voxel, day)
                print '============================================================================='
                
                subject_dir = os.path.join(workspace, 'DATA', subject)
                #I/O
                svs_dir = os.path.join(subject_dir, 'SVS', day, se_voxel, 'TWIX')
                twix_met = os.path.join(svs_dir, '%s' % se_voxel, '%s_lcm' % se_voxel)
                twix_h2o = os.path.join(svs_dir, '%s_w' % se_voxel, '%s_w_lcm' % se_voxel)
                lcm_dir = mkdir_path(os.path.join(subject_dir, 'LCMODEL', day, se_voxel, 'TWIX', se_voxel))
                
                #create RAW directories
                met = mkdir_path(os.path.join(lcm_dir, 'met'))
                h2o = mkdir_path(os.path.join(lcm_dir, 'h2o'))

                #copy files to RAW directories
                shutil.copy(os.path.join(twix_met),
                        os.path.join(met))

                shutil.copy(os.path.join(twix_h2o),
                            os.path.join(h2o))
                
                #rename to RAW
                print "Renaming met lcm_file for %s %s" %(subject, day)
                for lcm_file in os.listdir(met):
                    os.rename(str(os.path.join(met, '%s_lcm' %(se_voxel))),
                          str(os.path.join(met, 'RAW')))
                
                print "Renaming h2o lcm_file for %s %s" %(subject, day)
                for lcm_w_file in os.listdir(h2o):
                    os.rename(str(os.path.join(h2o, '%s_w_lcm' %(se_voxel))),
                          str(os.path.join(h2o, 'RAW')))
                
                #build TWIX control file
                file = open(os.path.join(lcm_dir, 'control'), "w")
                file.write(" $LCMODL\n")
                file.write(" title= 'TWIX %s, %s, %s' \n" %(subject, se_voxel, day))
                file.write(" srcraw= '%s' \n" %met)
                file.write(" srch2o= '%s' \n" %h2o)
                file.write(" savdir= '%s' \n" %lcm_dir)
                file.write(" ppmst= 4.0 \n")
                file.write(" ppmend= 0.2\n")
                file.write(" nunfil= 4096\n")
                file.write(" ltable= 7\n")
                file.write(" lps= 8\n")
                file.write(" lprint= 6\n")
                file.write(" lcsv= 11\n")
                file.write(" lcoraw= 10\n")
                file.write(" lcoord= 9\n")
                file.write(" hzpppm= 123.244438\n")
                file.write(" filtab= '%s/table'\n" %lcm_dir)
                file.write(" filraw= '%s/met/RAW'\n" %lcm_dir)
                file.write(" filps= '%s/ps'\n" %lcm_dir)
                file.write(" filpri= '%s/print'\n" %lcm_dir)
                file.write(" filh2o= '%s/h2o/RAW'\n" %lcm_dir)
                file.write(" filcsv= '%s/spreadsheet.csv'\n" %lcm_dir)
                file.write(" filcor= '%s/coraw'\n" %lcm_dir)
                file.write(" filcoo= '%s/coord'\n" %lcm_dir)
                file.write(" filbas= '/a/software/.lcmodel/6.3-1L/basis-sets/press_te30_3t_01a.basis'\n")
                file.write(" echot= 30.00 \n")
                file.write(" dows= T \n")
                file.write(" NEACH= 999 \n")
                file.write(" doecc= T\n")
                file.write(" deltat= 0.000417\n")
                file.write(" $END\n")
                file.close()
                
                #run lcmodel
                print 'Running LCModel Now'
                os.system('sh /home/raid2/molloy/lcmodel/6.3-1L/execution-scripts/standard %s 30 %s %s' % (lcm_dir, lcm_dir, lcm_dir))
                
                #create snr.txt file for QA.
                print 'Now creating .txt file with some useful information for later :)'
                reader = open(os.path.join(lcm_dir, 'table'), 'r')
                for line in reader:
                    if 'FWHM' in line:
                        fwhm = float(line[9:14])
                        snrx  = line[29:31]
                        fwhm_hz = fwhm * 123.24
                    if 'Data shift' in line:
                        shift = line[15:21]
                    if 'Ph:' in line:
                        ph0 = line[6:10]
                        ph1 = line[19:24]

                        filex = open(os.path.join(lcm_dir, 'snr.txt'), "w")
                        filex.write('%s, %s, %s, %s, %s, %s' %(fwhm,fwhm_hz, snrx, shift, ph0, ph1))
                        filex.close()
                        
                #create & rename PDF
                os.chdir(lcm_dir)
                print "Creating pdf output for %s, %s, %s" % (subject, se_voxel, day)
                os.system("ps2pdf ps")
                print "Renaming .pdf file output for %s, %s, %s" %(subject, se_voxel, day)
                for pdf_file in os.listdir(lcm_dir):
                    if pdf_file.endswith('pdf'):
                        os.rename(str(os.path.join(lcm_dir, pdf_file)),
                                  str(os.path.join(lcm_dir, '%s_%s_%s.pdf' %(subject, se_voxel, day))))
                        
run_lcmodel_twx(population, workspace, PRESS_voxels, days)
