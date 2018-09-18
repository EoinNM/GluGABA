import os
import numpy as np
from variables.variables import *
import pandas as pd
from utils.utils import *
import math
import seaborn as sns
import matplotlib

print '============================================'
print '    GluGABA 13 - PRESS Drop Bad Data'
print '============================================'

def drop(workspace, days, ACC_dropped, M1_dropped, data_type, metabolites, ppmst):
    
    for day in days:
        for dtype in data_type:
            for width in ppmst:
                for se_voxel in PRESS_voxels:
        
                    print '==============================================================='
                    print 'QCing and cleaning PRESS absolute dataframes for %s, %s at %s' %(se_voxel, day, width)
                    print '==============================================================='
                    
                    #path to files
                    ACC = os.path.join(workspace, 'ACC', day, 'ABS_ACC_%s_%s.csv' %(day, width))
                    M1  = os.path.join(workspace, 'M1', day, 'ABS_M1_%s_%s.csv' %(day, width))
                    
                    #read spreadsheets
                    print "Reading DataFrames now for both M1 & ACC"
                    df_ACC = pd.read_csv(ACC, index_col = 0)
                    df_M1 = pd.read_csv(M1, index_col = 0)
                    
                    #drop exclusions, low SNR & high line width subjects
                    print "Removing ACC exclusions and saving new frame..."
                    df_ACC_exc = df_ACC.drop(ACC_dropped, axis = 0)
                    df_ACC_exc.to_csv(os.path.join(workspace, 'ACC', day, "ACC_ABS_%s_%s_clean.csv" %(day, width)))
                    print "Removing M1 exclusions and saving new frame..."
                    df_M1_exc = df_M1.drop(M1_dropped, axis = 0)
                    df_M1_exc.to_csv(os.path.join(workspace, 'M1', day, "M1_ABS_%s_%s_clean.csv" %(day, width)))
                    print "...and removing any bad SNR/FWHM also"
                    #reading above frames
                    saved_ACC = os.path.join(workspace, 'ACC', day, "ACC_ABS_%s_%s_clean.csv" %(day, width))
                    saved_M1 = os.path.join(workspace, 'M1', day, "M1_ABS_%s_%s_clean.csv" %(day, width))
                    df_ACC_QC = pd.read_csv(saved_ACC, index_col = 0)
                    df_M1_QC = pd.read_csv(saved_M1, index_col = 0)
                    #dropping bad SNR and FWHM
                    df_ACC_exc_b = df_ACC_QC[(df_ACC_QC['FWHM'] < 10) & (df_ACC_QC['SNR'] > 10)] #df_ACC_QC is anything that fits these criteria - this is not a statement of exclusion but of inclusion
                    df_M1_exc_b  = df_M1_QC[(df_M1_QC['FWHM'] < 10) & (df_M1_QC['SNR'] > 10)]
                    #updating cleaned framesnote
                    df_ACC_exc_b.to_csv(os.path.join(workspace, 'ACC', day, "ACC_ABS_%s_%s_clean.csv" %(day, width)))
                    df_M1_exc_b.to_csv(os.path.join(workspace, 'M1', day, "M1_ABS_%s_%s_clean.csv" %(day, width)))
                    
                    #CRLB check and exclusion
                    print 'Checking ACC dataframes Cramer Rao Lower Bound'
                    #1. Calc the Absolute metabolite value
                    print 'Calculating Absolute ACC values'
                    for metabolite in metabolites:
                        for ACC_sub in ACC_population:
                            ACC_CRLB = os.path.join(workspace, 'ACC', day, "ACC_ABS_%s_%s_clean.csv"%(day, width))
                            df_ACC_CRLB = pd.read_csv(ACC_CRLB, index_col = 0)
                            df_ACC_CRLB.loc[ACC_sub]
                            ACC_Abs_value = df_ACC_CRLB['{}'.format(metabolite)].astype(float)
                            ACC_CRLB_value = df_ACC_CRLB['{}%'.format(metabolite)].astype(float).divide(100)
                            ABS_ACC = df_ACC_CRLB['{}_AbsCRLB'.format(metabolite)] = ACC_Abs_value*ACC_CRLB_value
                        #2. Calc the CRLB value
                        print 'Calculating ACC CRLB values'
                        for ctrl in Group_A_ACC:
                            df_ACC_CRLB.loc[ctrl]
                            df_ACC_CRLB['{}'.format(metabolite)] = df_ACC_CRLB['{}'.format(metabolite)].astype(float)
                            lim_mean_ACC = df_ACC_CRLB['{}'.format(metabolite)].mean()
                            LIM_ACC = df_ACC_CRLB['{}_LimCRLB'.format(metabolite)] = lim_mean_ACC*0.5
                        #3. Make values above threshold as nan
                        df_ACC_CRLB.loc[ABS_ACC > LIM_ACC, metabolite] = np.nan
                        #4. Now update the cleaned ACC dataframes
                        df_ACC_CRLB.to_csv(os.path.join(workspace, 'ACC', day, "ACC_ABS_%s_%s_clean.csv"%(day, width)))
                        
                        print 'Checking M1 dataframes Cramer Rao Lower Bound'
                        #5. Calc the M1 Absolute metabolite value
                        print 'Calculating Absolute M1 values'
                        for M1_sub in M1_population:
                            M1_CRLB = os.path.join(workspace, 'M1', day, "M1_ABS_%s_%s_clean.csv"%(day, width))
                            df_M1_CRLB = pd.read_csv(M1_CRLB, index_col = 0)
                            df_M1_CRLB.loc[M1_sub]
                            M1_Abs_value = df_M1_CRLB['{}'.format(metabolite)].astype(float)
                            M1_CRLB_value = df_M1_CRLB['{}%'.format(metabolite)].astype(float).divide(100)
                            M1_ABS = df_M1_CRLB['{}_AbsCRLB'.format(metabolite)] = M1_Abs_value*M1_CRLB_value
                        #6. Calc the M1 CRLB value
                        print 'Calculating M1 CRLB values'
                        for ctrl in Group_A_M1:
                            df_M1_CRLB.loc[ctrl]
                            df_M1_CRLB['{}'.format(metabolite)] = df_ACC_CRLB['{}'.format(metabolite)].astype(float)
                            M1_lim_mean = df_M1_CRLB['{}'.format(metabolite)].mean()
                            M1_LIM = df_M1_CRLB['{}_LimCRLB'.format(metabolite)] = M1_lim_mean*0.5
                        #7. Make M1 values above threshold as nan
                        df_M1_CRLB.loc[M1_ABS > M1_LIM, metabolite] = np.nan
                        #8. Now update the cleaned M1 dataframes
                        df_M1_CRLB.to_csv(os.path.join(workspace, 'M1', day, "M1_ABS_%s_%s_clean.csv"%(day, width)))      

drop(workspace, days, ACC_dropped, M1_dropped, data_type, metabolites, ppmst)
