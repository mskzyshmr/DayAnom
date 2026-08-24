# DayAnom

## Status

Testing...

## Description

These scripts create tc-shell scripts that do the following for 6-hourly or daily netCDF time series:
1. Compute the 365-day running mean
2. Subtract the 365-day running mean to de-trend the 6-hourly or daily data
3. Compute the 31-day running mean
4. Construct the 6-hourly or daily climatology (average over multiple years)
5. Subtract the climatology to construct 6-hourly or daily anomalies

## Directories

python: Python3 scripts to create .tcsh scripts

## Getting started

- 6-hourly data

python3 mk_anom_6hr.py

- Daily data

python3 mk_anom_1dy.py
