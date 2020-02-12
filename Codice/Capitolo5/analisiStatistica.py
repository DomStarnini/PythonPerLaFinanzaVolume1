# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 11:48:41 2020

@author: jaman
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import date
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
from matplotlib.gridspec import GridSpec

pd.plotting.register_matplotlib_converters()

simbolo='TSLA'
nome='TESLA INC'
inizio=date(2014,1,1)
fine=date.today()
data=yf.download(simbolo,inizio,fine)
df=pd.DataFrame(data)
df.head()
df.reset_index(inplace=True)
df['Date'] = df['Date'].map(mdates.date2num)
fig = plt.figure(figsize=(18, 12))
ax1 = fig.add_subplot(111)
ax1.set_title(nome,size=30, color='white',style='italic')
ax1.set_facecolor('black')
ax1.figure.set_facecolor('black')
ax1.tick_params(axis='x', colors='white')
ax1.tick_params(axis='y', colors='white')
ax1.xaxis_date()
candlestick_ohlc(ax1, df.values, width=0.6, colorup='green', colordown='red', alpha=1)
ax1.grid()
df['SMA50'] = df['Close'].rolling(50).mean()
df['SMA100'] = df['Close'].rolling(100).mean()
ax1.plot(df['Date'], df['SMA50'], color='white', label='SMA50')
ax1.plot(df['Date'], df['SMA100'], color='red', label='SMA100')
plt.xlabel('Data',size=20, color='white',style='italic')
plt.ylabel('Prezzo',size=20, color='white',style='italic')
plt.legend(bbox_to_anchor=(0.3, 1.05))
plt.show()

data=yf.download(simbolo,inizio,fine)
df=pd.DataFrame(data)
ritorno_giornaliero = df['Close'].pct_change()
print(ritorno_giornaliero.head())
print(ritorno_giornaliero.describe())

fig = plt.figure(figsize=(18, 12))
ax1 = fig.add_subplot(111)
ax1.plot(ritorno_giornaliero)
ax1.set_xlabel("Data")
ax1.set_ylabel("Percentuale")
ax1.set_title("{} Ritorno Giornaliero".format(nome))
plt.show()

fig = plt.figure(figsize=(18, 12))
ax1 = fig.add_subplot(111)
ax1.plot((ritorno_giornaliero + 1).cumprod())
ax1.set_xlabel("Data")
ax1.set_ylabel("Percentuale")
ax1.set_title("{} Ritorno Cumulativo Giornaliero".format(nome))
plt.show()

data=yf.download(simbolo,inizio,fine)
df=pd.DataFrame(data)
ritorno_giornaliero = df['Close'].pct_change()
ret_dat=pd.DataFrame(ritorno_giornaliero)
ret_dat.reset_index(level=0, inplace=True)
ret_dat['nday'] =ret_dat['Date'].dt.weekday_name
ret_dat.head()

lunpos=len(ret_dat[(ret_dat['nday']=='Monday') & 
                                         (ret_dat['Close']>0)])/len(ret_dat[ret_dat['nday']=='Monday'])*100
lunneg=len(ret_dat[(ret_dat['nday']=='Monday') & 
                                         (ret_dat['Close']<0)])/len(ret_dat[ret_dat['nday']=='Monday'])*100
marpos=len(ret_dat[(ret_dat['nday']=='Tuesday') & 
                                         (ret_dat['Close']>0)])/len(ret_dat[ret_dat['nday']=='Tuesday'])*100
marneg=len(ret_dat[(ret_dat['nday']=='Tuesday') & 
                                         (ret_dat['Close']<0)])/len(ret_dat[ret_dat['nday']=='Tuesday'])*100
merpos=len(ret_dat[(ret_dat['nday']=='Wednesday') & 
                                         (ret_dat['Close']>0)])/len(ret_dat[ret_dat['nday']=='Wednesday'])*100
merneg=len(ret_dat[(ret_dat['nday']=='Wednesday') & 
                                         (ret_dat['Close']<0)])/len(ret_dat[ret_dat['nday']=='Wednesday'])*100
giopos=len(ret_dat[(ret_dat['nday']=='Thursday') & 
                                         (ret_dat['Close']>0)])/len(ret_dat[ret_dat['nday']=='Thursday'])*100
gioneg=len(ret_dat[(ret_dat['nday']=='Thursday') & 
                                         (ret_dat['Close']<0)])/len(ret_dat[ret_dat['nday']=='Thursday'])*100
venpos=len(ret_dat[(ret_dat['nday']=='Friday') & 
                                         (ret_dat['Close']>0)])/len(ret_dat[ret_dat['nday']=='Friday'])*100
venneg=len(ret_dat[(ret_dat['nday']=='Friday') & 
                                         (ret_dat['Close']<0)])/len(ret_dat[ret_dat['nday']=='Friday'])*100        

dataday = {'GIORNO DELLA SETTIMANA': ['LUN','MAR','MER','GIO','VEN'], 
         'UP': [lunpos,marpos,merpos,giopos,venpos],
         'DOWN': [lunneg,marneg,merneg,gioneg,venneg]}
dfday=pd.DataFrame(dataday)
fig = plt.figure(figsize=(18, 12))
dfday.plot(x="GIORNO DELLA SETTIMANA", y=["UP", "DOWN"], 
                  kind="bar",color=["Green","Red"],
                  title='FREQUENZA PERCENTUALE RIALZI/RIBASSI \nPER GIORNO DELLA SETTIMANA',figsize=(18, 12))
plt.grid(color='black')
plt.ylabel('FREQUENZA %')
plt.xlabel('GIORNO DELLA SETTIMANA')
plt.legend(loc='upper right')
plt.show()

data=yf.download(simbolo,inizio,fine)
df=pd.DataFrame(data)
ritorno_mensile = df['Close'].resample('M').ffill().pct_change()
print(ritorno_mensile.head())
print(ritorno_mensile.describe())

fig = plt.figure(figsize=(18, 12))
ax1 = fig.add_subplot(111)
ax1.plot(ritorno_mensile)
ax1.set_xlabel("Data")
ax1.set_ylabel("Percentuale")
ax1.set_title("{} Ritorno Mensile".format(nome))
plt.show()

fig = plt.figure(figsize=(18, 12))
ax1 = fig.add_subplot(111)
ax1.plot((ritorno_mensile + 1).cumprod())
ax1.set_xlabel("Data")
ax1.set_ylabel("Percentuale")
ax1.set_title("{} Ritorno Cumulativo Mensile".format(nome))
plt.show()

data=yf.download(simbolo,inizio,fine)
df=pd.DataFrame(data)
ritorno_mensile = df['Close'].resample('M').ffill().pct_change()
ret_dat=pd.DataFrame(ritorno_mensile)
ret_dat.reset_index(level=0, inplace=True)
ret_dat['nday'] =ret_dat['Date'].dt.month_name()
ret_dat.head()

genpos=len(ret_dat[(ret_dat['nday']=='January') & 
                                         (ret_dat['Close']>0)])/len(ret_dat[ret_dat['nday']=='January'])*100
genneg=len(ret_dat[(ret_dat['nday']=='January') & 
                                         (ret_dat['Close']<0)])/len(ret_dat[ret_dat['nday']=='January'])*100
febpos=len(ret_dat[(ret_dat['nday']=='February') & 
                                         (ret_dat['Close']>0)])/len(ret_dat[ret_dat['nday']=='February'])*100
febneg=len(ret_dat[(ret_dat['nday']=='February') & 
                                         (ret_dat['Close']<0)])/len(ret_dat[ret_dat['nday']=='February'])*100
marpos=len(ret_dat[(ret_dat['nday']=='March') & 
                                         (ret_dat['Close']>0)])/len(ret_dat[ret_dat['nday']=='March'])*100
marneg=len(ret_dat[(ret_dat['nday']=='March') & 
                                         (ret_dat['Close']<0)])/len(ret_dat[ret_dat['nday']=='March'])*100
aprpos=len(ret_dat[(ret_dat['nday']=='April') & 
                                         (ret_dat['Close']>0)])/len(ret_dat[ret_dat['nday']=='April'])*100
aprneg=len(ret_dat[(ret_dat['nday']=='April') & 
                                         (ret_dat['Close']<0)])/len(ret_dat[ret_dat['nday']=='April'])*100
magpos=len(ret_dat[(ret_dat['nday']=='May') & 
                                         (ret_dat['Close']>0)])/len(ret_dat[ret_dat['nday']=='May'])*100
magneg=len(ret_dat[(ret_dat['nday']=='May') & 
                                         (ret_dat['Close']<0)])/len(ret_dat[ret_dat['nday']=='May'])*100  
giupos=len(ret_dat[(ret_dat['nday']=='June') & 
                                         (ret_dat['Close']>0)])/len(ret_dat[ret_dat['nday']=='June'])*100
giuneg=len(ret_dat[(ret_dat['nday']=='June') & 
                                         (ret_dat['Close']<0)])/len(ret_dat[ret_dat['nday']=='June'])*100
lugpos=len(ret_dat[(ret_dat['nday']=='July') & 
                                         (ret_dat['Close']>0)])/len(ret_dat[ret_dat['nday']=='July'])*100
lugneg=len(ret_dat[(ret_dat['nday']=='July') & 
                                         (ret_dat['Close']<0)])/len(ret_dat[ret_dat['nday']=='July'])*100
agopos=len(ret_dat[(ret_dat['nday']=='August') & 
                                         (ret_dat['Close']>0)])/len(ret_dat[ret_dat['nday']=='August'])*100
agoneg=len(ret_dat[(ret_dat['nday']=='August') & 
                                         (ret_dat['Close']<0)])/len(ret_dat[ret_dat['nday']=='August'])*100
settpos=len(ret_dat[(ret_dat['nday']=='September') & 
                                         (ret_dat['Close']>0)])/len(ret_dat[ret_dat['nday']=='September'])*100
settneg=len(ret_dat[(ret_dat['nday']=='September') & 
                                         (ret_dat['Close']<0)])/len(ret_dat[ret_dat['nday']=='September'])*100
ottpos=len(ret_dat[(ret_dat['nday']=='October') & 
                                         (ret_dat['Close']>0)])/len(ret_dat[ret_dat['nday']=='October'])*100
ottneg=len(ret_dat[(ret_dat['nday']=='October') & 
                                         (ret_dat['Close']<0)])/len(ret_dat[ret_dat['nday']=='October'])*100
novpos=len(ret_dat[(ret_dat['nday']=='November') & 
                                         (ret_dat['Close']>0)])/len(ret_dat[ret_dat['nday']=='November'])*100
novneg=len(ret_dat[(ret_dat['nday']=='November') & 
                                         (ret_dat['Close']<0)])/len(ret_dat[ret_dat['nday']=='November'])*100
dicpos=len(ret_dat[(ret_dat['nday']=='December') & 
                                         (ret_dat['Close']>0)])/len(ret_dat[ret_dat['nday']=='December'])*100
dicneg=len(ret_dat[(ret_dat['nday']=='December') & 
                                         (ret_dat['Close']<0)])/len(ret_dat[ret_dat['nday']=='December'])*100
            

datamonth = {'MESI': ['GEN','FEB','MAR','APR','MAG','GIU','LUG','AGO','SET','OTT','NOV','DIC'], 
         'UP': [genpos,febpos,marpos,aprpos,magpos,giupos,lugpos,agopos,settpos,ottpos,novpos,dicpos],
         'DOWN': [genneg,febneg,marneg,aprneg,magneg,giuneg,lugneg,agoneg,settneg,ottneg,novneg,dicneg]}
dfmonth=pd.DataFrame(datamonth)
plt.figure(figsize=(18, 12))  
dfmonth.plot(x="MESI", y=["UP", "DOWN"], 
                  kind="bar",color=["Green","Red"],
                  title='FREQUENZA PERCENTUALE RIALZI/RIBASSI PER MESE',figsize=(18, 12))
plt.grid(color='black')
plt.ylabel('FREQUENZA %')
plt.xlabel('MESE')
plt.legend(loc='upper right')
plt.show()

ritorno_annuale = df['Close'].resample('Y').ffill().pct_change()
print(ritorno_annuale.head())
print(ritorno_annuale.describe())

fig = plt.figure(figsize=(18, 12))
ax1 = fig.add_subplot(111)
ax1.plot(ritorno_annuale)
ax1.set_xlabel("Data")
ax1.set_ylabel("Percentuale")
ax1.set_title("{} Ritorno Annuale".format(nome))
plt.show()

fig = plt.figure(figsize=(18, 12))
ax1 = fig.add_subplot(111)
ax1.plot((ritorno_annuale + 1).cumprod())
ax1.set_xlabel("Data")
ax1.set_ylabel("Percentuale")
ax1.set_title("{} Ritorno Cumulativo Annuale".format(nome))
plt.show()