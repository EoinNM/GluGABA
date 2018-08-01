import os
from variables.variables import *
from utils.utils import *
import pandas as pd
import math

print '========================================================================================'
print '                            GluGABA - 10_PRESS_Absolute_Quantitation                    '
print '========================================================================================'

def calc_concentrations(LCM, GM, WM, CSF):
    
    
    #Define equation for absolute quantitation
    #Relaxation related signal attenuation water factor 
    h20_factor = (55.55 / (35.88 * 0.7))

    #Relative h20 concentrations per tissue type - determined by Ahmad & Harald
    GM_h2o  = 0.81
    WM_h20  = 0.71
    CSF_h20 = 1.00
    
    #H2O attenuation via differential h20 relaxation times for T1 & T2 with sequence TR & TE and Euler's constant as input variables
    r_h20_GM  = (1.0 - math.e**(- 3000.0/1820.0)) * math.e**(- 30.0/99.0)
    r_h20_WM  = (1.0 - math.e**(- 3000.0/1084.0)) * math.e**(- 30.0/69.0)
    r_h20_CSF = (1.0 - math.e**(- 3000.0/4163.0)) * math.e**(- 30.0/503.0)
    
    #Gussew compartmentation equation to calculate metabolite concentration via consideration of heterogenous tissue composition
    chet = (LCM) * (((GM * GM_h2o * r_h20_GM +
                                       WM * WM_h20 * r_h20_WM +
                                       CSF * CSF_h20 + r_h20_CSF) /
                                      (GM *1.0 + WM +1.0))) * h20_factor
    
    return chet
    
##################################################################################################################################
    
#make a dataframe for absolute metabolite quantities
    
def make_frame(PRESS_voxels, data_type, days):
    
    print 'Creating absolute data frames'
    for se_voxel in PRESS_voxels:
        for day in days:
            for dtype in data_type:
                
                csv = os.path.join(workspace, '00Results', 'PRESS', se_voxel, day, '%s_%s_%s.csv'%(se_voxel, day, dtype))
                df = pd.read_csv(csv, index_col = 0)
                
                df.Cre      = calc_concentrations(df.Cre, df.GM, df.WM, df.CSF)
                df.tCho     = calc_concentrations(df.tCho, df.GM, df.WM, df.CSF)
                df.tNAA     = calc_concentrations(df.tNAA, df.GM, df.WM, df.CSF)
                df.mIno     = calc_concentrations(df.mIno, df.GM, df.WM, df.CSF)
                df.Glu      = calc_concentrations(df.Glu, df.GM, df.WM, df.CSF)
                df.Glu_Cre  = calc_concentrations(df.Glu_Cre, df.GM, df.WM, df.CSF)
                df.Gln      = calc_concentrations(df.Gln, df.GM, df.WM, df.CSF)
                df.Gln_Cre  = calc_concentrations(df.Gln_Cre, df.GM, df.WM, df.CSF)
                df.Glx      = calc_concentrations(df.Glx, df.GM, df.WM, df.CSF)
                df.Glx_Cre  = calc_concentrations(df.Glx_Cre, df.GM, df.WM, df.CSF)
                df.GABA     = calc_concentrations(df.GABA, df.GM, df.WM, df.CSF)
                df.Asp      = calc_concentrations(df.Asp, df.GM, df.WM, df.CSF)
                df.Tau      = calc_concentrations(df.Tau, df.GM, df.WM, df.CSF)
                df.Lac      = calc_concentrations(df.Lac, df.GM, df.WM, df.CSF)
                df.NAA      = calc_concentrations(df.NAA, df.GM, df.WM, df.CSF)
                df.NAAG     = calc_concentrations(df.NAAG, df.GM, df.WM, df.CSF)
                df.Ala      = calc_concentrations(df.Ala, df.GM, df.WM, df.CSF)
                df.Scy      = calc_concentrations(df.Scy, df.GM, df.WM, df.CSF)
                
                absolute_dir = mkdir_path(os.path.join(workspace, '00Results', 'PRESS', 'Absolute', se_voxel, day))
                df.to_csv(os.path.join(absolute_dir, '%s_%s_%s.csv'%(se_voxel, day, dtype)))
                print 'Absolute DataFrame created for %s_%s_%s'%(se_voxel, day, dtype)

make_frame(['M1'], ['RDA'], ['base'])
make_frame(['M1'], ['RDA'], ['day1'])
make_frame(['M1'], ['RDA'], ['day7'])

make_frame(['M1'], ['TWIX'], ['base'])
make_frame(['M1'], ['TWIX'], ['day1'])
make_frame(['M1'], ['TWIX'], ['day7'])

make_frame(['ACC'], ['RDA'], ['base'])
make_frame(['ACC'], ['RDA'], ['day1'])
make_frame(['ACC'], ['RDA'], ['day7'])

make_frame(['ACC'], ['TWIX'], ['base'])
make_frame(['ACC'], ['TWIX'], ['day1'])
make_frame(['ACC'], ['TWIX'], ['day7'])