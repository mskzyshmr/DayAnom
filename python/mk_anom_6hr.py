#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This script constructs 6-hourly anomalies.
#
# Ref.: Barriopedro, D., García-Herrera, R. & Trigo, R.M.
#       Application of blocking diagnosis methods to General Circulation Models.
#       Part I: a novel detection scheme. Clim Dyn 35, 1373–1391 (2010).
#       https://doi.org/10.1007/s00382-010-0767-5
#       [Appendix]

import os
import subprocess

#-------------------
# user defined block
#-------------------

# C-shell script to be created by this Python script
fin = 'mk_anom_6hr.tcsh'

# specify the analysis period (+2 years data are needed)
year_start0 = 1980
year_end0 = 2013

# length of the running averages
nlen1 = 365*4+1
nlen2 = 31*4+1

# specify variables
inpdir = './inp'
outdir = './out'
var_list = ['z500']

#-----------------------
# do not edit below here
#-----------------------

# convert integer to 4-digit string
yyyys0 = str(year_start0).zfill(4)
yyyye0 = str(year_end0).zfill(4)

# +1 year for the running mean
year_start = year_start0 - 1
year_end = year_end0 + 1

# convert integer to 4-digit string
yyyys = str(year_start).zfill(4)
yyyye = str(year_end).zfill(4)

f = open(fin,'w')
f.write('#!/bin/tcsh\n')
f.write('\n')

for var in var_list:
    inp = inpdir
    out = outdir
    f.write('mkdir -p '+out+'\n')
    fout = out+'/'+var+'_y'+yyyys0+'-y'+yyyye0+'_anom.nc'

    # intermediate files
    fout0 = inp+'/'+var+'_y'+yyyys+'-y'+yyyye+'.nc'
    fout1 = out+'/'+var+'_y'+yyyys+'-y'+yyyye+'_runave_ann.nc'
    fout2 = out+'/'+var+'_y'+yyyys+'-y'+yyyye+'_runave_ann_anom.nc'
    fout3 = out+'/'+var+'_y'+yyyys0+'-y'+yyyye0+'_runave_ann_anom.nc'
    fout4 = out+'/'+var+'_y'+yyyys+'-y'+yyyye+'_runave_mon.nc'
    fout5 = out+'/'+var+'_y'+yyyys0+'-y'+yyyye0+'_runave_mon.nc'
    fout6 = out+'/'+var+'_y'+yyyys0+'-y'+yyyye0+'_runave_mon_clm.nc'

    # construct 365-day running mean
    f.write('# Compute the annual mean\n')
    f.write('cdo runmean,'+str(nlen1)+' '+fout0+' '+fout1+'\n')
    f.write('#\n')

    # compute the sub-annual component by subtracting the annual means (detrend)
    f.write('# Subtract the annual means\n')
    f.write('cdo select,startdate='+yyyys+'-08-01,enddate='+yyyye+'-05-31 ' \
              +fout0+' '+out+'/tmp0.nc\n')
    f.write('cdo select,startdate='+yyyys+'-08-01,enddate='+yyyye+'-05-31 ' \
              +fout1+' '+out+'/tmp1.nc\n')
    f.write('cdo sub '+out+'/tmp0.nc '+out+'/tmp1.nc '+fout2+'\n')
    f.write('cdo select,startdate='+yyyys0+'-01-01,enddate='+yyyye0+'-12-31 ' \
              +fout2+' '+fout3+'\n')
    f.write('/bin/rm '+out+'/tmp?.nc '+fout1+'\n')
    f.write('#\n')

    # construct 31-day running mean and daily climatology
    f.write('# Compute the daily climatology\n')
    f.write('cdo runmean,'+str(nlen2)+' '+fout2+' '+fout4+'\n')
    f.write('cdo select,startdate='+yyyys0+'-01-01,enddate='+yyyye0+'-12-31 ' \
              +fout4+' '+fout5+'\n')
    f.write('cdo yhourmean '+fout5+' '+fout6+'\n')
    f.write('/bin/rm '+fout2+' '+fout4+' '+fout5+'\n')
    f.write('#\n')

    # compute the sub-monthly component by subtracting the daily climatology
    f.write('# Subtract the daily climatology\n')
    f.write('cdo yhoursub '+fout3+' '+fout6+' '+fout+'\n')
    f.write('/bin/rm '+fout3+' '+fout6+'\n')
    f.write('#\n')

f.write('exit\n')

os.chmod(fin, 0o755)
