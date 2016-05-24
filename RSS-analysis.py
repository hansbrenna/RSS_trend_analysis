from __future__ import print_function
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
import wget
import os

download_data=True
"""Download updatet input data"""
if download_data:
    try:    
        os.remove('RSS_TS_channel_TLT_Global_Land_And_Sea_v03_3.txt')
        url='http://data.remss.com/msu/graphics/TLT/time_series/RSS_TS_channel_TLT_Global_Land_And_Sea_v03_3.txt'
        f = wget.download(url)
    except:
        url='http://data.remss.com/msu/graphics/TLT/time_series/RSS_TS_channel_TLT_Global_Land_And_Sea_v03_3.txt'
        f = wget.download(url)

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

data=pd.DataFrame(data={'temp':temp},index=time)

for i in xrange(len(temp)):
    if data.temp.iloc[i] == -99.900:
        data.iloc[i].temp = None

data = data.dropna()

fig1 = plt.figure(num=1,figsize=(10,5))
fig1.hold()

plot_yrs=['1979-01-31','1997-01-31','1997-06-30','1998-01-31','1998-06-30','1999-01-31','1999-06-30']

df = pd.DataFrame(data={'trend':np.zeros(len(data.temp))},index=data.index)

for start in data.index:
    data = data.loc[start:]
    Y = pd.Series(data.temp)
    X = pd.Series(range(1, len(data) + 1), index=data.index)

    model = pd.ols(y=Y, x=X, intercept=True)
    
    if str(start).split()[0] == plot_yrs[0]:
        plt.plot(data,label='RSS global mean TLT ')
    
    if str(start).split()[0] in plot_yrs:
        plt.plot(data.index,model.y_fitted,label='{0}: slope={1:3f}'.format(start,model.beta[0]*12*10))
    
    df.loc[start]=model.beta[0]*12*10

print('Minimum trend {0}'.format(df.min()))

plt.legend(loc='upper left')

#plt.show()

fig1.savefig('trendlines.png',bbox_inches='tight')

fig2 = plt.figure(num=2,figsize=(10,5))

plt.semilogy(df.loc['1979-01-31':'2010-01-31'],label='monthly trend in K/decade')
plt.legend(loc = 'upper left')
#plt.show()

fig2.savefig('trends.png',bbox_inches='tight')
