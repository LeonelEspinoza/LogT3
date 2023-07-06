import csv
import sys
import bitarray
import pandas as pd
import numpy as np
import random

#-----------------------------------------------------------------------------#

#VARIABLES GLOBALES
#arreglo para los arreglos de a's
A=[]
#arreglos de b's
B=[]
#cantidad de funciones de hash
k=1
#tamaño de tabla para hash
m=1
#primo para el hashing
#primo

#-----------------------------------------------------------------------------#

# Se lee el archivo csv
df = pd.read_csv('Popular-Baby-Names-Final.csv')

# Se obtiene el mayor largo de nombre, que es 15
max = df['Name'].str.len().max()
print('El mayor largo de nombre es: ', max)

#Se obtienen las caracteristicas del archivo csv
print(df.describe())
# Por lo tanto, el primo elegido para la función de hash será 17
primo = 17

# Se define el número de búsquedas que se harán
#N = 

def universal_hash(a_array, b, m, string):
    sum = int(0)
    for i in range(len(string)):
        #Se obtiene el número UNICODE de cada letra del string y se le resta 65 para que queden entre 0 y 25
        sum += int( (ord(string[i])-65) * a_array[i])
    res= ((sum + b) % primo) % m
    return res

# Hay que elegir b y el arreglo de a's al azar. b va entre 0 y 16, y el arreglo de a's va entre 1 y 16
# con eso se obtiene una función de hash universal

def initialize():
    #setear k arreglos de a's y b's   
    j=0
    while j<k:
        print("j=",j)
        a=np.arange(16)
        i=0
        while i<16:
            a[i]=random.randint(1,16)
            i+=1

        A.append(a)
        print("A=",a)

        B.append(random.randint(0,16))
        print("b=",B[j])
        j+=1
#initialize()

#def calculate_m(epsilon):
#    m = 1.44 * np.log2(epsilon)

def CrearFiltro(m,k,file):
    #crear un arreglo M de m bits
    M=bitarray(m)
    #inicializarlos en 0
    M.setall(0)

    #crear k funciones de hash

    #para cada elemento x del archivo PBN.csv calcular y_i=h_i(x) y modificar el arreglo M[y_i]=1
    #for element in file
    return 

#busca name en el CSV de PBNF.csv
def buscar(name):
    #read csv, and split on "," the line
    csv_file = csv.reader(open('Popular-Baby-Names-Final.csv', "r"), delimiter=",")

    #loop through the csv list
    for row in csv_file:
        #print(row[0])
        # Si el elemento existe, se imprime lo siguiente
        if name == row[0]:
            #exito
            print('Existe el elemento')
    #termino
    print(".")

def FunFiltro(valor):
    for _ in range(k): 
        universal_hash(A,b,m,valor)
    return

#Valores->valores que se buscarán
#Filtro->booleano indica si la busqueda es con o sin filtro
#N->Numero de busquedas (tamaño de Valores)
def BuscarValores(Valores,Filtro,N):
    #para cada valor de Valores O(N)
    for element in Valores:
        if Filtro:
            if FunFiltro(element):
                buscar(element)
        else:
            buscar(element)

    return