
zfs = '/data/pt_nro174_mri/MRI/Assessment/A_Steady_State/'
workspace = '/nobackup/roggen2/Molloy/GluGABA'
days = ['base', 'day1', 'day7']
voxels = ['ACC', 'M1', 'M1m']
svs_file = ["TWIX", "RDA"]
sequence = ["PRESS", "MEGA_PRESS"]

population= ["AL3T", "BTBT", "GAUT", "IN3T", "MCLT", "PAKT", "SICT", "UC2T", "ZL2T", "BCQT",
             "CE2T", "GCPT", "JG2T", "MCMT", "PAMT", "SJDX", "VA9T", "BDPT", "DF6T", "GJFT",
             "KA3X", "MCNT", "PJGT", "SLPT", "VL3T", "BKJT", "DF7T", "GJGT", "KA6X", "NAAT",
             "PMUT", "SM9Y", "VL4T", "BM4X", "FE5T", "GJHT", "KCST", "NG4T", "PV3T", "SSNX",
             "VM9T", "BMNX", "FL8T", "GJJT", "KSBX", "NL5T", "RKHT", "TCET", "VS7T", "BMQX",
             "FL9T", "HS8X", "KTIT", "NT6T", "RMAX", "TO3T", "WSKT", "BSVT", "FN3T", "IL2T",
             "KTKT", "OK7T", "SATX", "TSFT", "ZJ4T"]

group_A= ["BJKT" "BMQX" "BSVT" "CE2T" "DF6T" "FL8T" "FL9T" "GAUT" "GCPT" "GJHT" 
	  "GJJT" "HSBX" "JG2T" "KA3X" "KA6X" "KTKT" "KTIT" "NAAT" "NG4T" "PAKT" 
	  "PMUT" "PV3T" "RKHT" "SICT" "SJDX" "SLPT" "SM9Y" "SSNX" "TCET" "UC2T" 
	  "VA9T" "VL3T" "VM9T" "VS7T"]

group_B= ["AL3T" "BCQT" "BDPT" "BM4X" "BMNX" "BTBT" "DF7T" "FE5T" "FN3T" "GJFT" 
	  "GJGT" "IL2T" "IN3T" "KCST" "VL4T" "KSBX" "MCLT" "MCMT" "MCNT" "NL5T" 
	  "NT6T" "OK7T" "PAMT" "PJGT" "RMAY" "SATX" "TO3T" "TSFT" "WSKT" "ZJ4T" 
	  "ZL2T"]


test_population = ["KSBX", "HS8X", "ZJ4T"]
