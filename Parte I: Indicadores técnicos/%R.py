import matplotlib.pyplot as plt
import ta
import pandas as pd
import talib
import pandas_datareader.data as web
import datetime as dt

start=dt.datetime(2017,12,30)
end=dt.datetime(2019,1,1)

df=web.DataReader('IBE.MC', 'yahoo', start, end)

high = df['High']
low = df['Low']
close = df['Close']
WR = ta.momentum.wr(high, low, close, lbp=14, fillna=False)

df['%R']=WR
df=df.drop(['High', 'Low', 'Open','Volume', 'Adj Close'],axis=1)

compra_= pd.DataFrame(columns=('Close','%R'))
for i in df.index:
    if df.loc[i, '%R'] <= -81:
        compra_.loc[i]=(df.loc[i,'Close'], df.loc[i,'%R'])

print('Compra')
print(compra_)

venta_= pd.DataFrame(columns=('Close','%R'))
for i in df.index:
    if df.loc[i, '%R'] >= -20:
            venta_.loc[i]=(df.loc[i,'Close'], df.loc[i,'%R'])

print('Venta')       
print(venta_)

suma_c = compra_['Close'].sum()     # Suma precios de compra
suma_v = venta_['Close'].sum()      # Suma precios de venta
prom_c = suma_c/(compra_['Close'].count())
prom_v = suma_v/(venta_['Close'].count())

print('El precio medio de cada acción comprada es: '+ str(round(prom_c, 2)))
print('El precio medio de cada acción vendida es: '+ str(round(prom_v, 2)))

rent = (prom_v - prom_c)/prom_c *100        # Fórmula de la rentabilidad
print('\n' + 'La rentabilidad media total con la estrategia RSI es: ' + str(round(rent,2)) + ' %')

acciones = int(input('¿Cúantas acciones operó por movimiento?: '))
inicio = acciones*prom_c
print('Su beneficio total es de: ' + str(round(rent*inicio/100,2)))


