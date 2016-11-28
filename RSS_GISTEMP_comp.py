# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 10:41:36 2016

@author: hanbre
"""
from __future__ import print_function
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import wget
import os

matplotlib.rcParams['xtick.labelsize']=14
matplotlib.rcParams['ytick.labelsize']=14
matplotlib.rcParams['axes.labelsize']=16

download_data=True
"""Download updatet input data"""
if download_data:
    try:    
        os.remove('GLB.Ts+dSST.txt')
        url = 'http://data.giss.nasa.gov/gistemp/tabledata_v3/GLB.Ts+dSST.txt'
        f = wget.download(url)
    except:
        url = 'http://data.giss.nasa.gov/gistemp/tabledata_v3/GLB.Ts+dSST.txt'
        f = wget.download(url)

giss = pd.read_table('GLB.Ts+dSST.txt',skiprows=7, index_col=0,skipfooter=7,delim_whitespace=True,usecols=range(0,13))
giss = giss.drop_duplicates(keep=False)  
giss = giss.stack()
giss = giss.convert_objects(convert_numeric=True)
gisvals = giss.values/100.0

time = pd.date_range('1880-1','2017-1',freq='M')

giss = pd.DataFrame(data = {'temp':gisvals},index=time)

with open('RSS_TS_channel_TLT_Global_Land_And_Sea_v03_3.txt') as file_in:
    d=0;i=0; y=[];m=[];T=[]
    for line in file_in:
       if d<5:
           print(line)
       else:
           a,b,c = line.split()
           y.append(int(a)); m.append(int(b)); T.append(float(c))
           i+=1
       d+=1 

temp = np.array(T)
year = np.array(y)
mon = np.array(m)

time = pd.date_range('1978-1','2017-1',freq='M')

RSS=pd.DataFrame(data={'temp':temp},index=time)
#data_bu = data.copy(deep=True)

#uncorrected
plt.plot(giss['1997':'2013'],label='GISTEMP')
plt.plot(RSS['1997':'2013'],label='RSS')
plt.xlabel('time')
plt.ylabel('temperature anomaly (K)')
plt.legend(loc='upper right')
plt.title('GISTEMP vs RSS raw')
plt.savefig('gistemp_rss_raw_1997-2013.png',dpi=100,bbox_inches='tight')

plt.figure()
#correct way
giss_c=giss-giss['1979':'2008'].mean()
RSS_c=RSS-RSS['1979':'2008'].mean()
plt.plot(giss_c['1997':'2013'],label='GISTEMP')
plt.plot(RSS_c['1997':'2013'],label='RSS')
plt.xlabel('time')
plt.ylabel('temperature anomaly (K)')
plt.legend(loc='upper right')
plt.title('GISTEMP vs RSS normalized by mean of 1979-2008')
plt.savefig('gistemp_rss_norm1979-2008_1997-2013.png',dpi=100,bbox_inches='tight')

plt.figure()
#wrong way
giss_w = giss-0.28
giss_w= giss_w.rolling(60,center=True).mean()
RSS_w = RSS.rolling(60,center=True).mean()
plt.plot(giss_w['1997':'2013'],label='GISTEMP')
plt.plot(RSS_w['1997':'2013'],label='RSS')
plt.xlabel('time')
plt.ylabel('temperature anomaly (K)')
plt.legend(loc='upper right')
plt.title('GISTEMP offset -0.28 vs RSS. Centered rolling mean (60)')
plt.savefig('gistemp_rss_offset0.28_rollingc60_1997-2013.png',dpi=100,bbox_inches='tight')

#from 1979
plt.figure()
#uncorrected
plt.plot(giss['1982':'2013'],label='GISTEMP')
plt.plot(RSS['1982':'2013'],label='RSS')
plt.xlabel('time')
plt.ylabel('temperature anomaly (K)')
plt.legend(loc='upper right')
plt.title('GISTEMP vs RSS raw')
plt.title('GISTEMP offset -0.28 vs RSS. Centered rolling mean (60)')
plt.savefig('gistemp_rss_raw_1979-2013.png',dpi=100,bbox_inches='tight')

plt.figure()
#correct way
giss_c=giss-giss['1979':'2008'].mean()
RSS_c=RSS-RSS['1979':'2008'].mean()
plt.plot(giss_c['1982':'2013'],label='GISTEMP')
plt.plot(RSS_c['1982':'2013'],label='RSS')
plt.xlabel('time')
plt.ylabel('temperature anomaly (K)')
plt.legend(loc='upper right')
plt.title('GISTEMP vs RSS normalized by mean of 1979-2008')
plt.title('GISTEMP offset -0.28 vs RSS. Centered rolling mean (60)')
plt.savefig('gistemp_rss_norm1979-2008_1979-2013.png',dpi=100,bbox_inches='tight')

plt.figure()
#wrong way
giss_w = giss-0.28
giss_w= giss_w.rolling(60,center=True).mean()
RSS_w = RSS.rolling(60,center=True).mean()
plt.plot(giss_w['1982':'2013'],label='GISTEMP')
plt.plot(RSS_w['1982':'2013'],label='RSS')
plt.xlabel('time')
plt.ylabel('temperature anomaly (K)')
plt.legend(loc='upper right')
plt.title('GISTEMP offset -0.28 vs RSS. Centered rolling mean (60)')
plt.savefig('gistemp_rss_offset0.28_rollingc60_1982-2013.png',dpi=100,bbox_inches='tight')