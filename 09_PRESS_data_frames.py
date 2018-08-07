import os
from variables.variables import *
from utils.utils import *
import pandas as pd
import numpy as np

def concatenate(workspace, PRESS_voxels, population, data_type, days):
    
    print '========================================================================================'
    print '                            GluGABA - 09_PRESS_Create_DataFrame                         '
    print '========================================================================================'
    
    df_group = []
    
    count = 0
    for subject in population:
        count += 1
        
        #1. Get information
        
        #pull demographics from rda file header
        print '==================================================================='
        print '%s. Reading demographics from rda file header %s' %(count, subject)
        print' ==================================================================='
        
        rda  = open(os.path.join(workspace, 'DATA', subject, 'SVS', 'base', 'ACC', 'RDA', 'ACC', 'ACC.rda')).read().splitlines()
        age = [i[13:15] for i in rda if 'PatientAge' in i][0]
        kg   = [i[15:17] for i in rda if 'PatientWeight' in i][0]
        
        for day in days:
            for se_voxel in PRESS_voxels:
                    
                #grab voxel composition stats
                voxel_comp_file = open(os.path.join(workspace, 'DATA', subject, 'SVS', day, se_voxel, 'voxel_stats', 'SVS_Voxel_Tissue_Stats.txt')).read().splitlines()
                GM      = [i[27:35] for i in voxel_comp_file if 'Grey_Matter_Percentage' in i][0]
                WM      = [i[27:35] for i in voxel_comp_file if 'White_Matter_Percentage' in i][0]
                CSF     = [i[27:34] for i in voxel_comp_file if 'CSF_percentage' in i][0]
                
                for dtype in data_type:
                    #pull data quality measures
                    quality = np.genfromtxt(os.path.join(workspace, 'DATA', subject, 'LCMODEL', day, se_voxel, dtype, se_voxel, 'snr.txt'), delimiter = ',')
                    #get metabolites from LCModel output .csv spreadsheet
                    csv = pd.read_csv(os.path.join(workspace, 'DATA', subject, 'LCMODEL', day, se_voxel, dtype, se_voxel, 'spreadsheet.csv'))
                    print 'Finished reading demographics, tissue concentrations, data quality and LCModel .csv information for %s. %s, %s, %s, %s' %(count, subject, se_voxel, dtype, day)      
        
                    #2. Create DataFrame
                    
                    #define column headers
                    columns = ['Age' ,  'WeightKG', 'FWHM'  , 'SNR'  , 'Shift', 'Ph0', 'Ph1', 'GM', 'WM', 'CSF', 'Brain',
                                        'Cre'    ,  'Cre%'      ,
                                        'tCho'   , 'tCho%'      ,
                                        'NAA'    ,  'NAA%'      ,
                                        'NAAG'   ,  'NAAG%'     ,
                                        'tNAA'   ,  'tNAA%'     ,
                                        'mIno'   ,  'mIno%'     ,
                                        'Glu'    ,  'Glu%'      ,
                                        'Gln'    ,  'Gln%'      ,
                                        'Glx'    ,  'Glx%'      ,
                                        'Glu_Cre',  'Gln_Cre'   ,   'Glx_Cre'   ,
                                        'GABA'   ,  'GABA%'     ,
                                        'Asp'    ,  'Asp%'      ,
                                        'Tau'    ,  'Tau%'      ,
                                        'Lac'    ,  'Lac%'      ,
                                        'Ala'    ,  'Ala%'      ,
                                        'Asp'    ,  'Asp%'      ,
                                        'Scy'    ,  'Scy%'      ,]
                                
                    #fill columns with data
                    print 'Adding information to data frame for %s. %s, %s, %s, %s' %(count, subject, se_voxel, dtype, day)
                    df_subject = pd.DataFrame(columns = columns, index = ['%s'%subject])
                    df_subject.loc['%s'%subject] = pd.Series({'Age'         :age,
                                                             'Weight kg'    :kg,
                                                             'FWHM'         :quality[1],
                                                             'SNR'          :quality[2],
                                                             'Shift'        :quality[3],
                                                             'Ph0'          :quality[4],
                                                             'Ph1'          :quality[5],
                                                             'GM'           :GM,
                                                             'WM'           :WM,
                                                             'CSF'          :CSF,
                                                             'Cre'         : float(csv[' Cre']),         'Cre%'        : float(csv[' Cre %SD']),
                                                             'tCho'        : float(csv[' GPC+PCh']),     'tCho%'       : float(csv[' GPC+PCh %SD']),
                                                             'tNAA'        : float(csv[' NAA+NAAG']),    'tNAA%'       : float(csv[' NAA+NAAG %SD']),
                                                             'NAA'         : float(csv[' NAA']),         'NAA%'        : float(csv[' NAA %SD']),
                                                             'NAAG'        : float(csv[' NAAG']),        'NAAG%'       : float(csv[' NAAG %SD']),
                                                             'mIno'        : float(csv[' mI']),          'mIno%'       : float(csv[' mI %SD']),
                                                             'Glu'         : float(csv[' Glu']),         'Glu%'        : float(csv[' Glu %SD']),
                                                             'Gln'         : float(csv[' Gln']),         'Gln%'        : float(csv[' Gln %SD']),
                                                             'Glx'         : float(csv[' Glu+Gln']),     'Glx%'        : float(csv[' Glu+Gln %SD']),
                                                             'Glu_Cre'     : float(csv[' Glu/Cre']),
                                                             'Gln_Cre'     : float(csv[' Gln/Cre']),
                                                             'Glx_Cre'     : float(csv[' Glu+Gln/Cre']),
                                                             'GABA'        : float(csv[' GABA']),        'GABA%'       : float(csv[' GABA %SD']),
                                                             'Asp'         : float(csv[' Asp']),         'Asp%'        : float(csv[' Asp %SD']),
                                                             'Ala'         : float(csv[' Ala']),         'Ala%'        : float(csv[' Ala %SD']),
                                                             'Lac'         : float(csv[' Lac']),         'Lac%'        : float(csv[' Lac %SD']),
                                                             'Tau'         : float(csv[' Tau']),         'Tau%'        : float(csv[' Tau %SD']),
                                                             'Scy'         : float(csv[' Scyllo']),      'Scy%'        : float(csv[' Scyllo %SD']),                    
                                                            })

        df_group.append(df_subject)
        print 'Concatenating data frames.....'
        dataframe = pd.concat(df_group, ignore_index = False).sort(columns='Age')
                                     
        #3. Save new dataframe with all information in new location
        dataframe_dir = mkdir_path(os.path.join(workspace, 'Results', 'PRESS', 'LCMODEL', se_voxel, day))
        dataframe.to_csv(os.path.join(dataframe_dir, '%s_%s_%s.csv'%(se_voxel, day, dtype)))
        print '.....concatenation complete - go to Results dir to view'
                       
concatenate(workspace, ['M1'], population, ['RDA'], ['base'])
concatenate(workspace, ['M1'], population, ['RDA'], ['day1'])
concatenate(workspace, ['M1'], population, ['RDA'], ['day7'])

concatenate(workspace, ['M1'], population, ['TWIX'], ['base'])
concatenate(workspace, ['M1'], population, ['TWIX'], ['day1'])
concatenate(workspace, ['M1'], population, ['TWIX'], ['day7'])

concatenate(workspace, ['ACC'], population, ['RDA'], ['base'])
concatenate(workspace, ['ACC'], population, ['RDA'], ['day1'])
concatenate(workspace, ['ACC'], population, ['RDA'], ['day7'])

concatenate(workspace, ['ACC'], population, ['TWIX'], ['base'])
concatenate(workspace, ['ACC'], population, ['TWIX'], ['day1'])
concatenate(workspace, ['ACC'], population, ['TWIX'], ['day7'])
