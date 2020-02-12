# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 09:58:07 2020

@author: jaman
"""

import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import date
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates

pd.plotting.register_matplotlib_converters()

simbolo='MSFT'
nome='MICROSOFT'
inizio=date(2019,6,1)
fine=date.today()
data=yf.download(simbolo,inizio,fine)

df=pd.DataFrame(data)
ritorno_giornaliero = df['Close'].pct_change().fillna(0.0)
ret_dat=pd.DataFrame(ritorno_giornaliero)
ret_dat.reset_index(level=0, inplace=True)
ret_dat['nday'] =ret_dat['Date'].dt.weekday_name.fillna(0.0)

def ritorna_segnale (df,nday):
      segnale=0.0
      pos=len(df[(df['nday']==nday) & (df['Close']>0)])/len(df[df['nday']==nday])*100
      neg=len(df[(df['nday']==nday) & (df['Close']<0)])/len(df[df['nday']==nday])*100
      if pos>=neg:
        segnale=1.0
      else : segnale=0.0  
      return segnale
  
sig = []
for index,row in ret_dat.iterrows() :
    segnale=ritorna_segnale (ret_dat,row.nday)
    sig.append(segnale)
df['segnale']=sig 
df['posizione']=df['segnale'].diff().fillna(0.0)

df.head()
df.reset_index(inplace=True)
df.head()
df['Date'] = df['Date'].map(mdates.date2num)
fig = plt.figure(figsize=(18, 12))
ax1 = fig.add_subplot(111)
ax2=ax1.twinx()
ax1.set_title(nome,size=30, color='white',style='italic')
ax1.set_facecolor('black')
ax1.figure.set_facecolor('black')
ax1.tick_params(axis='x', colors='white')
ax1.tick_params(axis='y', colors='white')
candlestick_ohlc(ax1, df.values, width=0.6, colorup='green', colordown='red', alpha=1)
ax1.grid()
ax2.plot(df.Date[df.posizione==1],df.loc[df.posizione==1].Close,'^',markersize=5,color='white')
ax2.plot(df.Date[df.posizione==-1],df.loc[df.posizione==-1].Close,'v',markersize=5,color='yellow')
plt.xlabel('Data',size=20, color='white',style='italic')
plt.ylabel('Prezzo',size=20, color='white',style='italic')
plt.show()

capitale_iniziale=10000
portfolio = pd.DataFrame(index=df.index).fillna(0.0)
portfolio['simbolo']=100*df['posizione']
portfolio['res']=(df['posizione'].multiply(df['Close'],axis=0))
differenza_posizione=df['posizione'].diff()
portfolio['cash']=capitale_iniziale-(differenza_posizione.multiply(df['Close'],axis=0)).cumsum()
portfolio['totale']=portfolio['cash']+portfolio['res']
portfolio['ritorno']=portfolio['totale'].pct_change()

fig = plt.figure(figsize=(18, 12))
ax1 = fig.add_subplot(111)
ax1.set_title(nome,size=30, color='white',style='italic')
ax1.set_facecolor('black')
portfolio.totale.plot()
ax1.plot(portfolio.loc[df.posizione==1].index,portfolio.totale[df.posizione==1],'^',markersize=10,color='green')
ax1.plot(portfolio.loc[df.posizione==-1].index,portfolio.totale[df.posizione==-1],'v',markersize=10,color='red')
plt.show()