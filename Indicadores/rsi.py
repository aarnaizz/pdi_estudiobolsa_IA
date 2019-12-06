import matplotlib.pyplot as plt
import ta
import pandas as pd
import pandas_datareader.data as web
import datetime as dt

start=dt.datetime(2017,12,1)
end=dt.datetime(2019,1,1)

df=web.DataReader('IBE.MC', 'yahoo', start, end)

close = df['Close']
RSI= ta.momentum.rsi(close, n=25, fillna=False)

df['RSI']=RSI
df=df.drop(['High', 'Low', 'Open','Volume', 'Adj Close'],axis=1)

compra_= pd.DataFrame(columns=('Close','RSI'))
estado_c = False
for i in df.index:
    if df.loc[i, 'RSI'] <= 30:
        if estado_c == False:
            compra_.loc[i]=(df.loc[i,'Close'], df.loc[i,'RSI'])
            estado_c = True
    else:
        estado_c = False

print('Compra')
print(compra_)


venta_= pd.DataFrame(columns=('Close','RSI'))
estado_v = False
for i in df.index:
    if df.loc[i, 'RSI'] >= 70:
        if estado_v == False:
            venta_.loc[i]=(df.loc[i,'Close'], df.loc[i,'RSI'])
            estado_v = True
    else:
        estado_v = False

print('Venta')       
print(venta_)

suma_c = compra_['Close'].sum()
suma_v = venta_['Close'].sum()

n_operaciones = compra_['Close'].count() 
benXacc = (suma_v - suma_c)
rent = (suma_v - suma_c)/suma_c *100
print('\n' + 'La rentabilidad total con la estrategia RSI es: ' + str(round(rent,2)) + ' %')

acciones = int(input('¿Cúantas acciones operó por movimiento?: '))
print('\n' + 'El beneficio por acción es de: ' + str(round(benXacc,2)))
print('Su beneficio total es de: ' + str(round(benXacc * acciones,2)))

