import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('dataset1.csv')

planeta=['Mercurio','Venus','Tierra','Marte','Júpiter','Saturno','Urano','Neptuno','Plutón']
lugar=[1,2,3,4,5,6,7,8,9]
masa=[0.06,0.82,1.00,0.11,318,95.1,14.6,17.2,0.002]
datos={'Planeta':planeta,'Posición':lugar,'Masa':masa}
planetas_ss=pd.DataFrame(datos)
planetas_ss
print(planetas_ss)

for etiqueta, fila in planetas_ss.iterrows():
    print(etiqueta)
    print(fila)

nombre=['Paco','Juan','Andrés','Natalia','Vanesa','Miriam','Juan']
color=['rojo','verde','amarillo','verde','verde','rojo','amarillo']
edad=[24,30,41,22,31,35,22]
altura=[182,170,169,183,178,172,164]
peso=[74.8,70.1,60.0,75.0,83.9,76.2,68.0]
puntuacion=[83,500,20,865,221,413,902]
datos={'Nombres':nombre,'Color':color,'Edad':edad,'Peso':peso,'Puntuación':puntuacion}
registro=pd.DataFrame(datos)
registro

plt.plot(registro.iloc[:,2])
plt.title('Edad')
plt.show()

plt.scatter(registro['Edad'],registro['Peso'])
plt.title('Edad vs Peso')
plt.show()

paises=['China','India','Estados Unidos','Indonesia','Brasil']
poblaciones=[1.36,1.29,0.33,0.26,0.2]
datos={'Países':paises,'Población':poblaciones}
poblacion=pd.DataFrame(datos)
poblacion.index=['CH','IN','USA','ID','BR']
poblacion

for etiqueta, fila in poblacion.iterrows():
    print(etiqueta)
    print(fila)

for etiqueta, fila in poblacion.iterrows():
    print(etiqueta+':'+fila['Países'])

