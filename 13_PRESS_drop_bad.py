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

def drop(workspace, days, ACC_dropped, M1_dropped, data_type, metabolites):
    
    for day in days:
        for dtype in data_type:     
        
            print '============================================'
            print 'QCing and cleaning PRESS absolute dataframes'
            print '============================================'
            
            #path to files
            ACC = os.path.join(workspace, "RESULTS", "PRESS", "ABSOLUTE", 'ACC', day, 'ACC_%s_%s.csv' %(day, dtype))
            M1 = os.path.join(workspace, "RESULTS", "PRESS", "ABSOLUTE", 'M1', day, 'M1_%s_%s.csv' %(day, dtype))
            
            #read spreadsheets
            print "Reading DataFrames now for both M1 & ACC"
            df_ACC = pd.read_csv(ACC, index_col = 0)
            df_M1 = pd.read_csv(M1, index_col = 0)
            
            #dropping previously ID'd bad subjects
            print "Removing bad voxel location subjects"
            dfACCx = df_ACC.drop(ACC_dropped, axis = 0)
            dfM1x  = df_ACC.drop(ACC_dropped, axis = 0)
            dfx0.to_csv(os.path.join(workspace, "RESULTS", "PRESS", "ABSOLUTE", 'ACC', day, "ACC_%s_%s_Dropped.csv" %(day, dtype)))
            dfx1.to_csv(os.path.join(workspace, "RESULTS", "PRESS", "ABSOLUTE", 'ACC', day, "ACC_%s_%s_Dropped.csv" %(day, dtype)))
            
            #previously created dropped dataframes
            drop_ACC = os.path.join(workspace, "RESULTS", "PRESS", "ABSOLUTE", 'ACC', day, 'ACC_%s_%s_Dropped.csv' %(day, dtype))
            drop_M1 = os.path.join(workspace, "RESULTS", "PRESS", "ABSOLUTE", 'M1', day, 'M1_%s_%s_Dropped.csv' %(day, dtype))        
            #read spreadsheets
            print "Reading new DataFrames now for both M1 & ACC"
            drop2_ACC = pd.read_csv(drop_ACC_RDA, index_col = 0)
            drop2_M1 = pd.read_csv(drop_M1_RDA, index_col = 0)
    
            #Check Line Width and SNR
            print "Checking and removing bad FWHM and SNR"
            dfx_ACC = drop2_ACC[(drop2_ACC['FWHM'] < 10) & (drop2_ACC_RDA['SNR'] > 10)]
            dfx_M1 = drop2_M1[(drop2_ACC['FWHM'] < 10) & (drop2_ACC_TWX['SNR'] > 10)]
            
            #check Cramer Rao Lower Bound Values
            print 'Checking Crámer Rao Lower Bound'        
            for metabolite in metabolites:
                #Calc CRLB_abs
                for subject in population:
                    df.loc[subject]
                    Abs_value = df['{}'.format(metabolite)].astype(float)
                    CRLB_value = df['{}%'.format(metabolite)].astype(float).divide(100)
                    ABS = df['{}_AbsCRLB'.format(metabolite)] = Abs_value*CRLB_value
                #Calc CRLB_lim
                for control in group_A:
                    df.loc[control]
                    df['{}'.format(metabolite)] = df['{}'.format(metabolite)].astype(float)
                    lim_mean = df['{}'.format(metabolite)].mean()
                    LIM = df['{}_LimCRLB'.format(metabolite)] = lim_mean*0.5  
                #make nan for bad CRLB values across all metabolites
                df.loc[ABS > LIM, metabolite] = np.nan
                         
                print 'Creating cleaned data frames now'
                dfx_ACC.to_csv(os.path.join(workspace, "RESULTS", "PRESS", "ABSOLUTE", 'ACC', day, "ACC_%s_%s_Clean.csv" %(day, dtype)))
                dfx_M1.to_csv(os.path.join(workspace, "RESULTS", "PRESS", "ABSOLUTE", 'M1', day, "M1_%s_%s_Clean.csv"%(day, dtype)))
                
                #remove the stuff you don't need anymore
                ACC_filesdir = os.path.join(workspace, "RESULTS", "PRESS", "ABSOLUTE", 'ACC', day)
                M1_filesdir = os.path.join(workspace, "RESULTS", "PRESS", "ABSOLUTE", 'M1', day)
                
                print "Removing files you no longer need"
                os.chdir(ACC_filesdir)
                os.system("rm -rf ACC_%s_%s_Dropped.csv" %(day, dtype))
                os.chdir(M1_filesdir)
                os.system("rm -rf M1_%s_%sDropped.csv" %(day, dtype))    

drop(workspace, days, ACC_dropped, M1_dropped, data_type, metabolites)