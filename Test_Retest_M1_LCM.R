###############################################################################################################################################
library(irr)
###############################################################################################################################################
#1 set directory
setwd('/Users/Eoin/Documents/')
data <-read.csv("glx.csv", header = T)

#Glx
times <- cbind(data$Glx_1,data$Glx_2)

icc(times,model = "twoway",
    type = "consistency",
    unit = "single",
    r0 = 0,
    conf.level = 0.95) #0.275 - poor

icc(times,model = "twoway",
    type = "agreement",
    unit = "single",
    r0 = 0,
    conf.level = 0.95) #0.288 - poor

#Glu
times <- cbind(data$Glu_1,data$Glu_2)

icc(times,model = "twoway",
    type = "consistency",
    unit = "single",
    r0 = 0,
    conf.level = 0.95) #0.762 - excellent

icc(times,model = "twoway",
    type = "agreement",
    unit = "single",
    r0 = 0,
    conf.level = 0.95) #0.776 - excellent