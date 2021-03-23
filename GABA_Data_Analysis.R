###############################################################################################################################################
#0 Load necessary packages
library(magrittr)
library(dplyr)
library(lme4)
library(car)
library(lmerTest)
library(psych)
require(MuMIn)
library(ggpubr)
library(rmcorr)
###############################################################################################################################################
#1 set directory
setwd('/Users/Eoin/Dropbox/My_Stuff/4_MRS/DATA/')
###############################################################################################################################################
#2 Set factors:
mrs <-read.csv("M1_Twix_Full.csv", header = T)
mrs$day = factor(mrs$Day)
mrs$group = factor(mrs$Group)
str(mrs)

#GABA Model fitting (Gannet Estimates of MEGA-PRESS):
#A Intercept Only
GABA_Intercept <- lmer(GABA_CSFcorr ~  (1|Subject), data=mrs, REML = F)
summary(GABA_Intercept)
#B With Day
GABA_Time <- lmer(GABA_CSFcorr ~  day + (1|Subject), data=mrs, REML = F)
summary (GABA_Time)
#C Compare A and B
anova(GABA_Intercept, GABA_Time)
#D With both main effects of group and day
GABA_Both <- lmer(GABA_CSFcorr ~  day + group + (1|Subject), data=mrs, REML = F)
summary (GABA_Both)
#E Compare B and D
anova(GABA_Time, GABA_Both)
#F With both main effects in interaction
GABA_Interaction <- lmer(GABA_CSFcorr ~ group*day + (1|Subject), data = mrs, REML = F)
summary(GABA_Interaction)
#G Compare D with F
anova(GABA_Both, GABA_Interaction)
#H Anova on full model
anova(GABA_Interaction)
summary(GABA_Interaction)
Anova(GABA_Interaction)
#I Marginal R squared for fixed effects
GABA_Intercept <- lmer(GABA_CSFcorr ~  (1|Subject), data=mrs, REML = F)
GABA_null <- lmer(GABA_CSFcorr ~ day + (1|Subject), data = mrs, REML = F)
GABA_null1 <- lmer(GABA_CSFcorr ~ group + day + (1|Subject), data = mrs, REML = F)
GABA <- lmer(GABA_CSFcorr ~ group*day + (1|Subject), data = mrs, REML = F)
r.squaredGLMM(GABA_Intercept)
r.squaredGLMM(GABA_null)
r.squaredGLMM(GABA_null1) 
r.squaredGLMM(GABA)

#GABA Model fitting (Gannet Estimates of MEGA-PRESS):
#A Intercept Only
GABA_Intercept <- lmer(GABA_Cr ~  (1|Subject), data=mrs, REML = F)
summary(GABA_Intercept)
#B With Day
GABA_Time <- lmer(GABA_Cr ~  day + (1|Subject), data=mrs, REML = F)
summary (GABA_Time)
#C Compare A and B
anova(GABA_Intercept, GABA_Time)
#D With both main effects of group and day
GABA_Both <- lmer(GABA_Cr ~  day + group + (1|Subject), data=mrs, REML = F)
summary (GABA_Both)
#E Compare B and D
anova(GABA_Time, GABA_Both)
#F With both main effects in interaction
GABA_Interaction <- lmer(GABA_Cr ~ group*day + (1|Subject), data = mrs, REML = F)
summary(GABA_Interaction)
#G Compare D with F
anova(GABA_Both, GABA_Interaction)
#H Anova on full model
anova(GABA_Interaction)
summary(GABA_Interaction)
Anova(GABA_Interaction)
#I Marginal R squared for fixed effects
GABA_Intercept <- lmer(GABA_Cr ~  (1|Subject), data=mrs, REML = F)
GABA_null <- lmer(GABA_Cr ~ day + (1|Subject), data = mrs, REML = F)
GABA_null1 <- lmer(GABA_Cr ~ group + day + (1|Subject), data = mrs, REML = F)
GABA <- lmer(GABA_CSFcorr ~ group*day + (1|Subject), data = mrs, REML = F)
r.squaredGLMM(GABA_Intercept)
r.squaredGLMM(GABA_null)
r.squaredGLMM(GABA_null1) 
r.squaredGLMM(GABA)
###############################################################################################################################################
#Glu Model fitting (LCModel Processed PRESS):
#A Intercept Only
Glu_Intercept <- lmer(Glu ~  (1|Subject), data=mrs, REML = F)
summary(Glu_Intercept)
#B With Day
Glu_Time <- lmer(Glu ~  day + (1|Subject), data=mrs, REML = F)
summary (Glu_Time)
#C Compare A and B
anova(Glu_Intercept, Glu_Time)
#D With both main effects of group and day
Glu_Both <- lmer(Glu ~  day + group + (1|Subject), data=mrs, REML = F)
summary (Glu_Both)
#E Compare B and D
anova(Glu_Time, Glu_Both)
#F With both main effects in interaction
Glu_Interaction <- lmer(Glu ~ group*day + (1|Subject), data = mrs, REML = F)
summary(Glu_Interaction)
#G Compare D with F
anova(Glu_Both, Glu_Interaction)
#H Anova on full model
anova(Glu_Interaction)
summary(Glu_Interaction)
Anova(Glu_Interaction)
#I Marginal R squared for fixed effects
Glu_Intercept <- lmer(Glu ~  (1|Subject), data=mrs, REML = F)
Glu_null <- lmer(Glu ~ day + (1|Subject), data = mrs, REML = F)
Glu_null1 <- lmer(Glu ~ group + day + (1|Subject), data = mrs, REML = F)
Glu <- lmer(Glu ~ group*day + (1|Subject), data = mrs, REML = F)
r.squaredGLMM(Glu_Intercept)
r.squaredGLMM(Glu_null)
r.squaredGLMM(Glu_null1) 
r.squaredGLMM(Glu)
###############################################################################################################################################
#Glx Model fitting (LCModel Processed PRESS):
#A Intercept Only
Glx_Intercept <- lmer(Glx ~  (1|Subject), data=mrs, REML = F)
summary(Glx_Intercept)
#B With Day
Glx_Time <- lmer(Glx ~  day + (1|Subject), data=mrs, REML = F)
summary (Glx_Time)
#C Compare A and B
anova(Glx_Intercept, Glx_Time)
#D With both main effects of group and day
Glx_Both <- lmer(Glx ~  day + group + (1|Subject), data=mrs, REML = F)
summary (Glx_Both)
#E Compare B and D
anova(Glx_Time, Glx_Both)
#F With both main effects in interaction
Glx_Interaction <- lmer(Glx ~ group*day + (1|Subject), data = mrs, REML = F)
summary(Glx_Interaction)
#G Compare D with F
anova(Glx_Both, Glx_Interaction)
#H Anova on full model
anova(Glx_Interaction)
summary(Glx_Interaction)
Anova(Glx_Interaction)
#I Marginal R squared for fixed effects
Glx_Intercept <- lmer(Glx ~  (1|Subject), data=mrs, REML = F)
Glx_null <- lmer(Glx ~ day + (1|Subject), data = mrs, REML = F)
Glx_null1 <- lmer(Glx ~ group + day + (1|Subject), data = mrs, REML = F)
Glx <- lmer(Glx ~ group*day + (1|Subject), data = mrs, REML = F)
r.squaredGLMM(Glx_Intercept)
r.squaredGLMM(Glx_null)
r.squaredGLMM(Glx_null1) 
r.squaredGLMM(Glx)