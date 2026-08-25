# DayAnom

## Status
Testing...

## Description
These scripts generate tcsh scripts to process 6-hourly or daily netCDF time series as follows:

1. Compute the 365-day running mean.
2. Subtract the 365-day running mean to remove low-frequency variability on timescales longer than about one year.
3. Compute the 31-day running mean.
4. Construct the 6-hourly or daily climatology by averaging over multiple years.
5. Subtract the climatology to obtain 6-hourly or daily anomalies.

## Directories
python: Python3 scripts to create tcsh scripts

## Getting started

- 6-hourly data

python3 mk_anom_6hr.py

- Daily data

python3 mk_anom_1dy.py
