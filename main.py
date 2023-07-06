import csv
import sys
import bitarray
import pandas as pd
import numpy as np
import random
from timeit import default_timer as timer

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
N = 0
# Maximo largo de nombre
max_len = 0
# Tasas de error
TasasDeError=[]
#-----------------------------------------------------------------------------#

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

#inicializar A[], B[] y marcar M 
def initialize_hash():
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


#busca name en el CSV de PBNF.csv True si el valor existe, False ~
def buscar(name):
    #read csv, and split on "," the line
    csv_file = csv.reader(open('Popular-Baby-Names-Final.csv', "r"), delimiter=",")

    #loop through the csv list
    for row in csv_file:
        # Si el elemento existe, retorna True
        if name == row[0]:
            #Existe el elemento
            return True
        else:
            #No existe el elemento
            return False

def Filtro(valor):
    i=0
    while i<k:
        j=universal_hash(A[i],B[i],valor)
        if M[j]==0:
            return False
    return True

#Valores->valores que se buscarán
#conFiltro->booleano indica si la busqueda es con o sin filtro
#N->Numero de busquedas (tamaño de Valores)
def BuscarValores(ArrValores,conFiltro):
    #iniciar temporizdor
    #para cada valor del arreglo de Valores O(N)
    error=0
    total=0
    for element in ArrValores:
        if conFiltro:
            if Filtro(element):
                if not buscar(element):
                    error+=1
                total+=1
        else:
            buscar(element)
    #finalizar temporizador
    #guardar tiempo de ejecución

    #guardar tasa de error
    TasasDeError.append(error/total) 

    return


def generarCSV(nombre):
    #guardar tiempo ejecución en un csv
    data={
        'Número exp':[],
        'Tiempo sin filtro':[],
        'Tiempo con filtro':[],
        'Tasa de error':[],
    }
    df=pd.DataFrame(data, columns = ['col1','col2','col3','col4'])
    df.to_csv(nombre+'.csv')


#########################################################################
#---------------------------MAIN----------------------------------------#
#Acordarse de reiniciar arreglos A y B después de cada corrida
#A.clear() debería servir
#el 50% seran busquedas exitosas y las demas seran busquedas fallidas

# Se lee el archivo csv
df = pd.read_csv('Popular-Baby-Names-Final.csv')
#Se quitan los valores nulos del dataset
df = df.dropna()
#Se obtiene el largo del nombre más largo
max_len = df['Name'].str.len().max()
#Se obtiene el número de elementos en el dataset
N = df['Name'].count()

start = timer()

print(23*2.3)

end = timer()
print(end - start)
#########################################################################

