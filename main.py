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
#Tabla de Hash
M=bitarray(m)
#primo para el hashing
primo = 1000000007
#epsilon: probabilidad de falsos positivos
epsilon=0.1
# Se define el número de elementos que se meten al filtro
N = 1
# Maximo largo de nombre
max_len = 0
#-----------------------------------------------------------------------------#

# Se lee el archivo csv
df = pd.read_csv('Popular-Baby-Names-Final.csv')

#Se quitan los valores nulos del dataset
df = df.dropna()

#Se obtiene el largo del nombre más largo
max_len = df['Name'].str.len().max()

#Universal_hash: función de hash universal
def universal_hash(a_array, b, string):
    sum = int(0)
    for i in range(len(string)):
        #Se obtiene el número UNICODE de cada letra del string y se le resta 65 para que queden entre 0 y 25
        sum += int( (ord(string[i])-65) * a_array[i])
    res= ((sum + b) % primo) % m
    return res

# Hay que elegir b y el arreglo de a's al azar. b va entre 0 y 16, y el arreglo de a's va entre 1 y 16
# con eso se obtiene una función de hash universal

#inicializar A[] y B[] 
def initialize_hash():
    #crear un arreglo M de m bits
    M=bitarray(m)

    #inicializarlos en 0
    M.setall(0)

    #setear k funciones de hash
    #setear k arreglos de a's y b's   
    j=0
    while j<k:
        print("j=",j)
        a=np.arange(max_len-1)
        i=0
        #Se llena el arreglo de a's con valores aleatorios entre 1 y primo-1
        while i<max_len:
            a[i]=random.randint(1,primo-1)
            i+=1
        A.append(a)
        #print("A=",a)
        B.append(random.randint(0,primo-1))
        #print("b=",B[j])
        j+=1
    print("A,B listo")

    #leer el csv
    csv_file = csv.reader(open('Popular-Baby-Names-Final.csv', "r"), delimiter=",")
    #para cada nombre en el csv
    for row in csv_file:
        #aplicar las k funciones de hash y marcar M adecuadamente
        i=0
        while i<k:
            j=universal_hash(A[i],B[i],m,row[0])
            M[j]=1
            i+=1
    print("M marcado")
    print(M)

#initialize_hash()

#def calculate_m(epsilon):
#    m = -1.44 * np.log2(epsilon) * N


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
        else:
            print('No existe el elemento')
    #termino
    print(".")

def Filtro(valor):
    i=0
    while i<k:
        j=universal_hash(A[i],B[i],valor)
        if M[j]==0:
            return False
    return True

#Valores->valores que se buscarán
#Filtro->booleano indica si la busqueda es con o sin filtro
#N->Numero de busquedas (tamaño de Valores)
def BuscarValores(ArrValores,bool):
    #iniciar temporizdor
    #para cada valor del arreglo de Valores O(N)
    for element in ArrValores:
        if not bool:
            if Filtro(element):
                buscar(element)
        else:
            buscar(element)
    #finalizar temporizador
    #guardar tiempo ejecución en un csv
    return