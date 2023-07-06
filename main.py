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
k=2
#tamaño de tabla para hash
m=10
#Tabla de Hash
M=bitarray.bitarray(m)
#primo para el hashing
primo = 1000000007
#epsilon: probabilidad de falsos positivos
epsilon=0.1
# Se define el número de elementos que se meten al filtro
N = 100
# Maximo largo de nombre
max_len = 0


# Parámetros para definir la cantidad de exitos y fracasos reales
NExito = 2
NFracaso = 8
#-----------------------------------------------------------------------------#


#Universal_hash: función de hash universal
def universal_hash(a_array, b, string):
    sum = int(0)
    for i in range(len(string)):
        
        # aqui hay un bug
        #if len(string) > len(a_array):
        #    print(len(string), len(a_array))


        #Se obtiene el número UNICODE de cada letra del string
        sum += int( (ord(string[i])) * a_array[i])
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
        #print("j=",j)
        a=np.arange(max_len)
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
    #print("A,B listo")

    #leer el csv
    csv_file = csv.reader(open('Popular-Baby-Names-Final.csv', "r"), delimiter=",")
    #para cada nombre en el csv
    for row in csv_file:
        #aplicar las k funciones de hash y marcar M adecuadamente
        i=0
        while i<k:
            #j=universal_hash(A[i],B[i],m,row[0])
            j=universal_hash(A[i],B[i],row[0])
            M[j]=1
            i+=1
    #print("M marcado")
    #print(M)

#initialize_hash()

#def calculate_m(epsilon):
#    m = -1.44 * np.log2(epsilon) * N


#busca name en el CSV de PBNF.csv True si el valor existe, False ~
def buscar(name):
    #read csv, and split on "," the line

    csv_file = pd.read_csv('Popular-Baby-Names-Final.csv')
    #Se quitan los valores nulos del dataset
    #csv_file = csv_file.dropna()
    csv_file_len = csv_file['Name'].count()
    i =0
    #loop through the csv list
    while i<csv_file_len:
        # Si el elemento existe, retorna True
        if name == csv_file['Name'][i]:
            #Existe el elemento
            return True
        i+=1
    return False

def Filtro(valor):
    i=0
    while i<k:
        j=universal_hash(A[i],B[i],valor)
        if M[j]==0:
            return False
        i+=1
    return True

#Valores->valores que se buscarán
#conFiltro->booleano indica si la busqueda es con o sin filtro
#N->Numero de busquedas (tamaño de Valores)
def BuscarValores(ArrValores,conFiltro):
    #iniciar temporizador
    start = timer()
    #para cada valor del arreglo de Valores O(N)
    error=0
    total=0
    for element in ArrValores:
        if conFiltro:
            if Filtro(element):
                if not buscar(element):
                    error+=1

        else:
            buscar(element)
        total+=1
    #finalizar temporizador
    end = timer()
    #guardar datos
    if conFiltro:
        TasasDeErrorConFiltro.append(error/total)
        TiemposConFiltro.append(end-start)
    else:
        TasasDeError.append(error/total)
        TiemposSinFiltro.append(end-start)
    return

# Tasas de error
TasasDeError=[]
TasasDeErrorConFiltro=[]
# Tiempos de ejecución
TiemposSinFiltro=[]
TiemposConFiltro=[]

def generarCSV(nombre):
    #guardar tiempo ejecución en un csv
    data={
        #'Número exp':[],
        'Tiempo sin filtro':[],
        'Tasa de error':[],
        'Tiempo con filtro':[],
        'Tasa de error con filtro':[],
    }
    data['Tiempo sin filtro']=TiemposSinFiltro
    data['Tasa de error']=TasasDeError
    data['Tiempo con filtro']=TiemposConFiltro
    data['Tasa de error con filtro']=TasasDeErrorConFiltro
    df=pd.DataFrame(data, columns = ['Tiempo sin filtro','Tasa de error','Tiempo con filtro','Tasa de error con filtro'])
    df.to_csv(nombre+'.csv')


# Crea un arreglo de nExito y nFracaso elementos 
def create_Arreglo_Search(nExito,nFracasos):
    
    ArrValoresSearch=[]
    #Se crean los valores de busqueda exitosa
    csv_file_exito = pd.read_csv('Popular-Baby-Names-Final.csv')
    #Se quitan los valores nulos del dataset
    csv_file_exito = csv_file_exito.dropna()

    len_exito_total = csv_file_exito['Name'].count()
    Arreglo_Exito = random.sample(range(0, len_exito_total), nExito)

    for i in range(nExito):
        ArrValoresSearch.append(csv_file_exito.iloc[Arreglo_Exito[i]]['Name'])

    #Se crean los valores de busqueda fracasada
    csv_file_fracaso = pd.read_csv('Film-Names.csv')
    #Se quitan los valores nulos del dataset
    csv_file_fracaso = csv_file_fracaso.dropna()

    len_fracaso_total = csv_file_fracaso['0'].count()
    Arreglo_Fracaso = random.sample(range(0, len_fracaso_total), nFracasos)
    for i in range(nFracasos):
        ArrValoresSearch.append(csv_file_fracaso.iloc[Arreglo_Fracaso[i]]['0'])

    ArrValoresSearch = random.sample(ArrValoresSearch, len(ArrValoresSearch))
    return ArrValoresSearch


    


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
df2 = pd.read_csv('Film-Names.csv')

max_len = df2['0'].str.len().max()
#Se obtiene el número de elementos en el dataset
N = df['Name'].count()



ArrValoresSearch = create_Arreglo_Search(NExito , NFracaso)

initialize_hash()


start = timer()
#Hacemos la busqueda sin filtro
BuscarValores(ArrValoresSearch,False)

#Hacemos la busqueda con filtro
BuscarValores(ArrValoresSearch,True)
generarCSV('Resultados')
end = timer()
print(end - start)
#########################################################################

