
import numpy as np
import matplotlib.pyplot as plt
import ta
import pandas as pd
import talib
import pandas_datareader.data as web
import datetime as dt

start=dt.datetime(2017,11,11)
end=dt.datetime(2019,1,1)

df=web.DataReader('IBE.MC', 'yahoo', start, end)

close = df['Close']
MACD = ta.trend.macd_diff(close, n_fast=12, n_slow=26, n_sign=9, fillna=False)

df['MACD']=MACD
df=df.drop(['High', 'Low', 'Open','Volume', 'Adj Close'],axis=1)

if MACD.loc[dt.datetime(2018,1,2)] > 0:
    estdo_ant = True
else:
    estado_ant = False

registro= pd.DataFrame(columns=('Close','MACD'))
for i in df.index:
    if MACD.loc[i] > 0:
        estado = True
    else:
        estado = False
    if estado != estado_ant:
        registro.loc[i]=(df.loc[i,'Close'], df.loc[i,'MACD'])
        estado_ant = estado

compra = registro.loc[df.MACD > 0]
venta = registro.loc[df.MACD < 0]

compra.reset_index(level=0, inplace=True)
venta.reset_index(level=0, inplace=True)
compra=compra.drop(['MACD'],axis=1)
venta=venta.drop(['MACD'],axis=1)
compra.columns = ['Fecha_c','Compra']
venta.columns = ['Fecha_v','Venta']

operaciones = compra.join(venta)
print(operaciones)

suma_c = operaciones['Compra'].sum()
suma_v = operaciones['Venta'].sum()

rent = (suma_v - suma_c)/suma_c *100
print('\n' + 'La rentabilidad total con el MACD es: ' + str(round(rent,2)) + ' %')
