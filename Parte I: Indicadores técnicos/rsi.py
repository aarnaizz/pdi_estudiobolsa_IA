import matplotlib.pyplot as plt
import ta
import pandas as pd
import pandas_datareader.data as web
import datetime as dt

start=dt.datetime(2017,12,1)    # Periodo a estudiar
end=dt.datetime(2019,1,1)

df=web.DataReader('IBE.MC', 'yahoo', start, end)    # Extracción de los datos

close = df['Close']
RSI= ta.momentum.rsi(close, n=25, fillna=False)     # Definición del indicador

df['RSI']=RSI
df=df.drop(['High', 'Low', 'Open','Volume', 'Adj Close'],axis=1)

compra_= pd.DataFrame(columns=('Close','RSI'))      # Lista de compra
for i in df.index:
    if df.loc[i, 'RSI'] <= 30:      # Cuando RSI<30, se guarda el precio del día
            compra_.loc[i]=(df.loc[i,'Close'], df.loc[i,'RSI'])

print('Compra')
print(compra_)


venta_= pd.DataFrame(columns=('Close','RSI'))      # Lista de venta
for i in df.index:
    if df.loc[i, 'RSI'] >= 70:      # Cuando RSI>70, se guarda el precio del día
        venta_.loc[i]=(df.loc[i,'Close'], df.loc[i,'RSI'])

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

