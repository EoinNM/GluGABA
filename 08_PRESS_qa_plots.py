import os
from os import *
import nibabel as nb
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from variables.variables import *
from utils.utils import *
import shutil
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm, mm, inch, pica

def plot_qa(population, workspace, PRESS_voxels, days, data_type):
    
    print '========================================================================================'
    print '                           GluGABA - 08 PRESS_Visual_Assessment                      '
    print '========================================================================================'
    
#    count = 0
#    for subject in population:
#        count +=1
#        for day in days:
#            for dtype in data_type:
#                for se_voxel in PRESS_voxels:
#                    
#                    print '==========================================================='
#                    print '%s. Creating Quality Assessment Images for %s, %s, %s, %s' % (count, subject, se_voxel, day, dtype)
#
#                    #######Step 1 - Create .png for the LCModel Spectra#######
#                    #I/O - Create Spectra and Twix output .png files
#                    lcm_dir = os.path.join(workspace, 'DATA', subject, 'LCMODEL', day, se_voxel, dtype)
#                    lcm_file = os.path.join(lcm_dir, se_voxel, '%s_%s_%s.pdf' %(subject, se_voxel, day))
#                    qa_dir = mkdir_path(os.path.join(workspace, 'DATA', subject, 'QA_Plots', day, se_voxel, dtype))
#                    twx_qa_dir = mkdir_path(os.path.join(workspace, 'DATA', subject, 'QA_Plots', day, se_voxel, 'TWIX'))
#                    twx_out_dir = os.path.join(workspace, 'DATA', subject, 'SVS', day, se_voxel, 'TWIX', se_voxel, 'report', 'figs')
#                    pre_post_file = os.path.join(twx_out_dir, 'alignAvgs_prePostFig.jpg')
#                    freq_drift_file = os.path.join(twx_out_dir, 'freqDriftFig.jpg')
#                    phase_drift_file = os.path.join(twx_out_dir, 'phaseDriftFig.jpg')
#                    
#                    #create LCM plots & Twix .png files
#                    shutil.copy(lcm_file, qa_dir)
#                    os.chdir(qa_dir)
#                    os.system('pdftk %s_%s_%s.pdf cat 1 output LCM_%s.pdf' %(subject, se_voxel, day, se_voxel))
#                    #convert split file to .png
#                    os.system('pdftoppm LCM_%s.pdf LCM_%s -png' %(se_voxel, se_voxel))
#                    #cleanup uneeded leftover files
#                    os.system('rm -rf %s_%s_%s.pdf LCM_%s.pdf ' %(subject, se_voxel, day, se_voxel))
#                    #convert freq & phase drift spectra to .png
#                    os.chdir(twx_out_dir)
#                    os.system('mogrify -format png *alignAvgs_prePostFig.jpg* *freqDriftFig.jpg* *phaseDriftFig.jpg*')
#                    shutil.copy('alignAvgs_prePostFig.png', twx_qa_dir)
#                    shutil.copy('freqDriftFig.png', twx_qa_dir)
#                    shutil.copy('phaseDriftFig.png', twx_qa_dir)
#                    print '.png file containing LCModel and Twix outputs created for %s, %s, %s, %s - Moving on to voxel plotting' % (subject, se_voxel, day, dtype)
#                    
#                #######Step 2 - Create .png with Voxel location images#######
#                #I/O grab T1 & voxel masks
#                T1 = os.path.join(workspace, 'DATA', subject, 'ANATOMICAL', day, 'ANATOMICAL.nii')
#                ACC = os.path.join(workspace, 'DATA', subject, 'SVS', day, 'ACC', 'voxel_masks', 'ACC.rda_Mask.nii')
#                M1 = os.path.join(workspace, 'DATA', subject, 'SVS', day, 'M1', 'voxel_masks', 'M1.rda_Mask.nii')
#                M1_qa_dir = os.path.join(workspace, 'DATA', subject, 'QA_Plots', day, 'M1', dtype)
#                ACC_qa_dir = os.path.join(workspace, 'DATA', subject, 'QA_Plots', day, 'ACC', dtype)
#
#                #load data
#                T1_load = nb.load(T1)
#                T1_data = T1_load.get_data()
#                acc_load  = nb.load(ACC)
#                m1_load = nb.load(M1)
#                acc_data = acc_load.get_data()
#                m1_data = m1_load.get_data()
#
#                #grab snr info from .txt created at steps 06/07
#                ACC_snr = np.genfromtxt(os.path.join(workspace, 'DATA', subject, 'LCMODEL', day, 'ACC', dtype, 'ACC', 'snr.txt'), delimiter = ',')
#                M1_snr = np.genfromtxt(os.path.join(workspace, 'DATA', subject, 'LCMODEL', day, 'M1', dtype, 'M1', 'snr.txt'), delimiter = ',')
#                #grab LCM .png
#                ACC_lcm_plot = os.path.join(workspace, 'DATA', subject, 'QA_Plots', day, 'ACC', dtype, 'LCM_ACC-1.png')
#                M1_lcm_plot = os.path.join(workspace, 'DATA', subject, 'QA_Plots', day, 'M1', dtype, 'LCM_M1-1.png')
#                
#                #pull cut coords to get center of voxel
#                M1_coords = find_cut_coords(m1_load)
#                ACC_coords = find_cut_coords(acc_load)
#                
#                #make svs mask zeros into nan
#                m1_data[m1_data==0]=np.nan
#                acc_data[acc_data==0]=np.nan
#                
#                fig =plt.figure()
#                fig.set_size_inches(6.5, 6.5)
#                fig.subplots_adjust(wspace=0.005)
#                
#                #plot M1 voxel on T1 & save to .png
#                print '1. Generating M1 Saggital Image for %s, %s, %s' % (subject, day, dtype)
#                #plot saggital
#                ax1 = plt.subplot2grid((1,3), (0,0), colspan = 1, rowspan =1)
#                ax1.imshow(np.rot90(T1_data[M1_coords[0], :, :]), cmap= 'bone', origin='lower')
#                ax1.imshow(np.rot90(m1_data[M1_coords[0], :, :]), cmap= 'rainbow', alpha = 0.7, origin='lower')
#                ax1.set_xlim(2, 170)
#                ax1.set_ylim(170, 2)
#                ax1.axes.get_yaxis().set_visible(False)
#                ax1.axes.get_xaxis().set_visible(False)
#                print '2. Generating M1 Coronal Image for %s, %s, %s' % (subject, day, dtype)
#                #plot coronal
#                ax2 = plt.subplot2grid((1,3), (0,1), colspan = 1, rowspan =1)
#                ax2.imshow(np.rot90(T1_data[:, M1_coords[1], :]), cmap= 'bone', origin='lower')
#                ax2.imshow(np.rot90(m1_data[:, M1_coords[1], :]), cmap= 'rainbow', alpha = 0.7, origin='lower')
#                ax2.set_xlim(2, 170)
#                ax2.set_ylim(170, 2)
#                ax2.axes.get_yaxis().set_visible(False)
#                ax2.axes.get_xaxis().set_visible(False)
#                print '3. Generating M1 Axial Image for %s, %s, %s' % (subject, day, dtype)
#                #plot axial
#                ax3 = plt.subplot2grid((1,3), (0,2),  colspan = 1, rowspan =1)
#                ax3.imshow(np.rot90(T1_data[:, : , M1_coords[2]]), cmap= 'bone', origin='lower')
#                ax3.imshow(np.rot90(m1_data[:, : , M1_coords[2]]) , cmap= 'rainbow', alpha = 0.7, origin='lower')
#                ax3.set_xlim(2, 170)
#                ax3.set_ylim(170, 2)
#                ax3.axes.get_yaxis().set_visible(False)
#                ax3.axes.get_xaxis().set_visible(False)
#                os.chdir(M1_qa_dir)
#                plt.tight_layout()
#                plt.savefig('Loc_M1.png', dpi=200, bbox_inches='tight')
#                        
#                #plot ACC voxel on T1 and save to .png
#                print '4. Generating ACC Saggital Image for %s, %s, %s' % (subject, day, dtype)
#                #plot saggital
#                ax1 = plt.subplot2grid((1,3), (0,0), colspan = 1, rowspan =1)
#                ax1.imshow(np.rot90(T1_data[ACC_coords[0], :, :]), cmap= 'bone', origin='lower')
#                ax1.imshow(np.rot90(acc_data[ACC_coords[0], :, :]), cmap= 'rainbow', alpha = 0.7, origin='lower')
#                ax1.set_xlim(10, 200)
#                ax1.set_ylim(200, 10)
#                ax1.axes.get_yaxis().set_visible(False)
#                ax1.axes.get_xaxis().set_visible(False)
#                print '5. Generating ACC Coronal Image for %s, %s, %s' % (subject, day, dtype)
#                #plot coronal
#                ax2 = plt.subplot2grid((1,3), (0,1), colspan = 1, rowspan =1)
#                ax2.imshow(np.rot90(T1_data[:, ACC_coords[1], :]), cmap= 'bone', origin='lower')
#                ax2.imshow(np.rot90(acc_data[:, ACC_coords[1], :]), cmap= 'rainbow', alpha = 0.7, origin='lower')
#                ax2.set_xlim(10, 200)
#                ax2.set_ylim(200, 10)
#                ax2.axes.get_yaxis().set_visible(False)
#                ax2.axes.get_xaxis().set_visible(False)
#                print '6. Generating ACC Axial Image for %s, %s, %s' % (subject, day, dtype)
#                #plot axial
#                ax3 = plt.subplot2grid((1,3), (0,2),  colspan = 1, rowspan =1)
#                ax3.imshow(np.rot90(T1_data[:, :, ACC_coords[2]]), cmap= 'bone', origin='lower')
#                ax3.imshow(np.rot90(acc_data[:, :, ACC_coords[2]]) , cmap= 'rainbow', alpha = 0.7, origin='lower')
#                ax3.set_xlim(39, 140)
#                ax3.set_ylim(160, 60)
#                ax3.axes.get_yaxis().set_visible(False)
#                ax3.axes.get_xaxis().set_visible(False)
#                os.chdir(ACC_qa_dir)
#                plt.tight_layout()
#                plt.savefig('Loc_ACC.png', dpi=200, bbox_inches='tight')
#                
#                #########Step 3 - Concatenate all create figures and plots in to a .pdf#################
#                #Create M1 PRESS .pdf
#                print 'Now concatenating into new .pdf for %s, %s, M1, %s' % (subject, day, dtype)
#                report = canvas.Canvas(os.path.join(M1_qa_dir,'QC_REPORT_%s_%s_M1_%s.pdf'%(subject, day, dtype)), pagesize=(1280, 1556))
#                report.setFont("Helvetica", 40)
#                report.drawImage(os.path.join(M1_qa_dir, 'Loc_M1.png'), 1, inch*13.5)
#                report.drawImage(M1_lcm_plot, 30, inch*1, width = 1200, height = 800)
#                report.drawString(230, inch*20, '%s_M1_%s_%s SNR=%s FWHM=%s' %(subject, day, dtype, M1_snr[2], M1_snr[1]))
#                report.showPage()
#                
#                M1_fig1 = os.path.join(workspace, 'DATA', subject, 'QA_Plots', day, 'M1', 'TWIX', 'alignAvgs_prePostFig.png')
#                M1_fig2 = os.path.join(workspace, 'DATA', subject, 'QA_Plots', day, 'M1', 'TWIX', 'freqDriftFig.png')
#                M1_fig3 = os.path.join(workspace, 'DATA', subject, 'QA_Plots', day, 'M1', 'TWIX', 'phaseDriftFig.png')
#                
#                if dtype is 'TWIX':
#                    
#                    report.drawImage(M1_fig1, 1, inch*7.2)
#                    report.drawImage(M1_fig2, 90, inch*1, width = 540, height = 450)
#                    report.drawImage(M1_fig3, 590, inch*1, width = 540, height = 450)
#                    report.setFont("Helvetica", 40)
#                    report.drawString(350, inch*20, 'Results from FID-A Preprocessing')
#                    report.showPage()
#                    report.save()
#                else:
#                    report.save()
#                
#                #Create ACC PRESS .pdf
#                print 'Now concatenating into new .pdf for %s, %s, ACC, %s' % (subject, day, dtype)
#                report = canvas.Canvas(os.path.join(ACC_qa_dir,'QC_REPORT_%s_%s_ACC_%s.pdf'%(subject, day, dtype)), pagesize=(1280, 1556))
#                report.setFont("Helvetica", 40)
#                report.drawImage(os.path.join(ACC_qa_dir, 'Loc_ACC.png'), 1, inch*13.5)
#                report.drawImage(ACC_lcm_plot, 30, inch*1, width = 1200, height = 800)
#                report.drawString(230, inch*20, '%s_ACC_%s_%s SNR=%s FWHM=%s' %(subject, day, dtype, ACC_snr[2], ACC_snr[1]))
#                report.showPage()
#                
#                ACC_fig1 = os.path.join(workspace, 'DATA', subject, 'QA_Plots', day, 'ACC', 'TWIX', 'alignAvgs_prePostFig.png')
#                ACC_fig2 = os.path.join(workspace, 'DATA', subject, 'QA_Plots', day, 'ACC', 'TWIX', 'freqDriftFig.png')
#                ACC_fig3 = os.path.join(workspace, 'DATA', subject, 'QA_Plots', day, 'ACC', 'TWIX', 'phaseDriftFig.png')
#                
#                if dtype is 'TWIX':
#
#                    report.drawImage(ACC_fig1, 1, inch*7.2)
#                    report.drawImage(ACC_fig2, 90, inch*1, width = 540, height = 450)
#                    report.drawImage(ACC_fig3, 590, inch*1, width = 540, height = 450)
#                    report.setFont("Helvetica", 40)
#                    report.drawString(350, inch*20, 'Results from FID-A Preprocessing')
#                    report.showPage()
#                    report.save()
#                else:
#                    report.save()
                    
       
    for subject in population:
        for day in days:
            for dtype in data_type:
                for se_voxel in PRESS_voxels:              
    
                    print 'Now copying pdfs to plot directory'
                    plot_path = (os.path.join(workspace, 'DATA', subject, 'QA_Plots', day, se_voxel, dtype))
                    plot_file = (os.path.join(plot_path, 'QC_REPORT_%s_%s_%s_%s.pdf' %(subject, day, se_voxel, dtype)))
                    new_plot_path = mkdir_path(os.path.join(workspace, 'Plots'))
                    shutil.copy(plot_file, new_plot_path)
    
    print 'Now creating single .pdf file for your convienience'
    os.chdir(new_plot_path)    
    os.system('pdftk *.pdf output Full_PRESS_QA.pdf')

plot_qa(population, workspace, PRESS_voxels, days, data_type)
