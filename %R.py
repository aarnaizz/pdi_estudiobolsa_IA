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
estado_c = False
for i in df.index:
    if df.loc[i, '%R'] <= -81:
        if estado_c == False:
            compra_.loc[i]=(df.loc[i,'Close'], df.loc[i,'%R'])
            estado_c = True
    else:
        estado_c = False

print('Compra')
print(compra_)

venta_= pd.DataFrame(columns=('Close','%R'))
estado_v = False
for i in df.index:
    if df.loc[i, '%R'] >= -20:
        if estado_v == False:
            venta_.loc[i]=(df.loc[i,'Close'], df.loc[i,'%R'])
            estado_v = True
    else:
        estado_v = False

print('Venta')       
print(venta_)

suma_c = compra_['Close'].sum()
suma_v = venta_['Close'].sum()

print(suma_c)

n_operaciones = compra_['Close'].count()
print('\n' + 'El nº de compras y ventas es de ' + str(n_operaciones))
benXacc = (suma_v - suma_c) / n_operaciones
rent = (suma_v - suma_c)/suma_c *100
print('\n' + 'La rentabilidad total con la estrategia %R es: ' + str(round(rent,2)) + ' %')

acciones = int(input('¿Cúantas acciones operó por movimiento?: '))
print('\n' + 'El beneficio por acción es de: ' + str(round(benXacc,2)))
print('Su beneficio total es de: ' + str(round(benXacc * acciones,2)))


