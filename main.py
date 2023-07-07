import csv
import sys
import bitarray
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
from timeit import default_timer as timer

#-----------------------------------------------------------------------------#
#VARIABLES GLOBALES
#arreglo para los arreglos de a's
A=[]
#arreglos de b's
B=[]
# Se define el número de elementos que se meten al filtro
df = pd.read_csv('Popular-Baby-Names-Final.csv')
df = df.dropna()
n = df['Name'].count()
#epsilon: probabilidad de falsos positivos
epsilon=0.1
#cantidad de funciones de hash
k=int((-1)*np.log2(epsilon))
#tamaño de tabla para hash
m = int(1.44 * k * n)
#Tabla de Hash
M=bitarray.bitarray(m)
#primo para el hashing
primo = 1000000007


# Maximo largo de nombre
df2 = pd.read_csv('Film-Names.csv')
max_len = df2['0'].str.len().max()


#Tamaños de las busquedas
listN = []
#K's
listK = []
#M's
listM = []

# Error o Busquedas Infructuosas
Errores = []
FalsosPositivos = []
PromError = []
DSError = []

# Tiempos de ejecución sin filtro
Tiempos = []
PromTiempo = []
DSTiempo = []

#Tiempos de ejecucion con Filtro
TiemposConFiltro = []
PromTiempoFiltro = []
DSTiempoFiltro = []

#Porcentaje de busquedas exitosas
PExito = 0.7
#-----------------------------------------------------------------------------#

def clearEverything():
    listN.clear()
    listK.clear()
    listM.clear()

    Errores.clear()
    FalsosPositivos.clear()
    PromError.clear()
    DSError.clear()

    Tiempos.clear()
    PromTiempo.clear()
    DSTiempo.clear()
    
    TiemposConFiltro.clear()
    PromTiempoFiltro.clear()
    DSTiempoFiltro.clear()

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
def initialize_hash():  #O(k*csv_len)
    global M
    global A
    global B

    M=bitarray.bitarray(m)
    #inicializarlos en 0
    M.setall(0)

    #vaciar A y B
    A.clear()
    B.clear()

    #setear k funciones de hash
    #setear k arreglos de a's y b's   
    j=0
    while j<k: #O(k * max_len)
        a=np.arange(max_len)
        i=0
        #Se llena el arreglo de a's con valores aleatorios entre 1 y primo-1
        while i<max_len: #O(max_len)
            a[i]=random.randint(1,primo-1)
            i+=1
        A.append(a)
        B.append(random.randint(0,primo-1))
        j+=1

    #leer el csv
    csv_file = csv.reader(open('Popular-Baby-Names-Final.csv', "r"), delimiter=",")
    #para cada nombre en el csv
    for row in csv_file: #O(csv_len * k)
        #aplicar las k funciones de hash y marcar M adecuadamente
        i=0
        while i<k: #O(k)
            j=universal_hash(A[i],B[i],row[0])
            M[j]=1
            i+=1

#Setea los valores de k y m según la probabilidad de falsos positivos buscada y la cantidad de elementos en el filtro basado en la teoría
def set_m_k_teorico(epsilon,n):
    global k
    global m
    k=(-1)*np.log2(epsilon)
    m = 1.44 * k * n

def set_k(i):
    global k
    k=i

def set_m(i):
    global m
    m=i

def set_theoric():
    global m
    global k
    k=int((-1)*np.log2(epsilon))
    m=int(1.44 * k * n)

#busca name en el .csv con PANDAS True si el valor existe, False ~
def buscarPANDAS(name): #O(csv_len)
    csv_file = pd.read_csv('Popular-Baby-Names-Final.csv')
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

#busca name en el .csv con CSV True si el valor existe, False ~
def buscarCSV(name):    #O(csv_len)
    csv_file = csv.reader(open('Popular-Baby-Names-Final.csv', "r"), delimiter=",")
    #loop through the csv list
    for row in csv_file:
        if name == row[0]:
            return True
    return False

#Verifica que el hash del valor calze con algun hash de la tabla
def Filtro(valor):  #O(k)
    i=0
    while i<k:
        j=universal_hash(A[i],B[i],valor)
        if M[j]==0:
            return False
        i+=1
    return True

#ArrValores->valores que se buscarán
#conFiltro->booleano indica si la busqueda es con o sin filtro
def BuscarValores(ArrValores,conFiltro):    #O(Ntotal)
    #iniciar temporizador
    start = timer()
    #para cada valor del arreglo de Valores O(N)
    error=0
    for element in ArrValores:
        if conFiltro:
            if Filtro(element):
                if not buscarCSV(element):
                    error+=1
        else:
            buscarCSV(element)
        
    #finalizar temporizador
    end = timer()
    #guardar datos
    if conFiltro:
        FalsosPositivos.append(error)
        TiemposConFiltro.append(end-start)
    else:
        Tiempos.append(end-start)
    return

#genera un csv con titulo nombre con los campos: 
# 'Tiempo sin filtro','Tasa de error','Tiempo con filtro','Tasa de error con filtro'
def generarCSV(nombre):
    #guardar tiempo ejecución en un csv
    data={
        #'Número exp':Nexp,
        'Tiempo sin filtro':Tiempos,
        'Cantidad de errores':Errores,
        'Tiempo con filtro':TiemposConFiltro,
        'Cantidad de Falsos Positivos':FalsosPositivos,
    }
    df=pd.DataFrame(data, columns = ['Tiempo sin filtro','Cantidad de errores','Tiempo con filtro','Cantidad de Falsos Positivos'])
    df.to_csv(nombre+'.csv')

# 'N', 'Promedio Tiempo sin Filtro', 'DS Tiempo sin Flitro', 'Promedio Tiempo con Filtro', 'DS Tiempo con Flitro', 'Promedio Cantidad de Errores', 'DS Cantidad de Errores'
def generarCSV2(nombre):
    data={
        'N':listN,
        'Promedio Tiempo sin Filtro' : PromTiempo,
        'DS Tiempo sin Flitro' : DSTiempo,
        'Promedio Tiempo con Filtro' : PromTiempoFiltro,
        'DS Tiempo con Flitro' : DSTiempoFiltro,
        'Promedio Cantidad de Errores' : PromError,
        'DS Cantidad de Errores' : DSError,
    }
    df=pd.DataFrame(data, columns = ['N',
                                    'Promedio Tiempo sin Filtro',
                                    'DS Tiempo sin Flitro',
                                    'Promedio Tiempo con Filtro',
                                    'DS Tiempo con Flitro',
                                    'Promedio Cantidad de Errores',
                                    'DS Cantidad de Errores'
                                    ])
    df.to_csv(nombre+'.csv')

# 'K','Promedio Tasa de Falsos Positivos/Infructuosas','Desviación estandar Tasa de Falsos Positivos/Infructuosas'
def generarCSV2_k(nombre):
    data={
        'K' : listK,
        'Promedio Tasa de Falsos Positivos/Infructuosas' : PromError,
        'Desviación estandar Tasa de Falsos Positivos/Infructuosas' : DSError,
    }

    df=pd.DataFrame(data, columns=['K','Promedio Tasa de Falsos Positivos/Infructuosas','Desviación estandar Tasa de Falsos Positivos/Infructuosas'])
    df.to_csv(nombre+'.csv')

#'m','Promedio Tasa de Falsos Positivos/Infructuosas','Desviación estandar Tasa de Falsos Positivos/Infructuosas'
def generarCSV2_m(nombre):
    data={
        'm' : listM,
        'Promedio Tasa de Falsos Positivos/Infructuosas' : PromError,
        'Desviación estandar Tasa de Falsos Positivos/Infructuosas' : DSError,
    }

    df=pd.DataFrame(data, columns=['m','Promedio Tasa de Falsos Positivos/Infructuosas','Desviación estandar Tasa de Falsos Positivos/Infructuosas'])
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
    if nFracasos<=len_fracaso_total:
        Arreglo_Fracaso = random.sample(range(0, len_fracaso_total), nFracasos)
        for i in range(nFracasos):
            ArrValoresSearch.append(csv_file_fracaso.iloc[Arreglo_Fracaso[i]]['0'])
    else:
        Arreglo_Fracaso=[]
        for _ in range(nFracasos):
            i=random.choice(range(0, len_fracaso_total))
            ArrValoresSearch.append(csv_file_fracaso.iloc[i]['0']) 

    ArrValoresSearch = random.sample(ArrValoresSearch, len(ArrValoresSearch))
    return ArrValoresSearch

# Ejecuta un experimento con Ntotal elementos a buscar con y sin filtro
def experimentoBase(N):
    Ntotal=N
    NExito=int(Ntotal*PExito)
    NFracaso=Ntotal-NExito
    
    #guardo el total de fracasos
    Errores.append(NFracaso)

    #Crear un arreglo de valores con PExito porcentaje existente
    ArrValoresSearch = create_Arreglo_Search(NExito , NFracaso)

    #Inicializar el hash y marcar M
    initialize_hash()
    print('-',end='',flush=True)


    #Hacemos la busqueda sin filtro
    BuscarValores(ArrValoresSearch,False)
    print(',',end='',flush=True)
    #Hacemos la busqueda con filtro
    BuscarValores(ArrValoresSearch,True)
    print('.',end='',flush=True)

    return

def experimentoBase2(N):
    Ntotal=N
    NExito=int(Ntotal*PExito)
    NFracaso=Ntotal-NExito

    #guardo el total de fracasos
    Errores.append(NFracaso)
    
    #Crear un arreglo de valores con PExito porcentaje existente
    ArrValoresSearch = create_Arreglo_Search(NExito , NFracaso)
    #Inicializar el hash y marcar M
    initialize_hash()
    print('-',end='',flush=True)
    #Hacemos la busqueda con filtro
    BuscarValores(ArrValoresSearch,True)
    print('.',end='',flush=True)
    return

def experimentoFiltro():
    clearEverything()
    #se corre el experimento para N=2^10 hasta 2^16
    for i in range(10,16):
        #Seteamos N y lo guardamos en la lista
        N=2**i
        listN.append(N)
        print('\nN =',N)
        #Repetimos el experimento 3 veces
        for i in range(0,3):
            experimentoBase(N)
        #generamos un CSV para cada N
        #generarCSV("Experimentos N="+str(N))

        #Guardamos los Promedios y descviaciones estandar
        PromTiempoFiltro.append(round(np.mean(TiemposConFiltro),4))
        DSTiempoFiltro.append(round(np.std(TiemposConFiltro),4))

        PromTiempo.append(round(np.mean(Tiempos),4))
        DSTiempo.append(round(np.std(Tiempos),4))

        PromError.append(round(np.mean(FalsosPositivos),4))
        DSError.append(round(np.std(FalsosPositivos),4))
    #Una vez terminado creamos un 
    generarCSV2('Resultados Filtro')

def experimentoK(N):
    clearEverything()
    set_theoric()

    #se corre el experimento para k=1 hasta 10
    for i in range(1,10+1):
        set_k(i)
        print("\nk =",k)
        listK.append(k)
        #repetimos el experimento 3 veces
        for i in range(0,5):
            experimentoBase2(N)
        
        TasaError=[]
        i=0
        while i<len(FalsosPositivos):
            TasaError.append(FalsosPositivos[i]/Errores[i])
            i+=1

        #guardamos el promedio y desviaciones estandar de las cantidades de errores
        PromError.append(round(np.mean(TasaError),4))
        DSError.append(round(np.std(TasaError),4))
    generarCSV2_k("Resultados K")

def experimentoM(N):
    clearEverything()
    set_theoric()
    
    #se corre el experimento para m=3*10^5 hasta 6*10^5 en saltos de 0.5*10^5
    for i in np.linspace(3,6, num=7):
        i=int(i*(10**5))
        set_m(i)
        print("\nm =",m)
        listM.append(m)

        #repetimos el experimento 3 veces
        for i in range(0,5):
            experimentoBase2(N)
        
        TasaError=[]
        i=0
        while i<len(FalsosPositivos):
            TasaError.append(FalsosPositivos[i]/Errores[i])
            i+=1

        #guardamos el promedio y desviaciones estandar de las cantidades de errores
        PromError.append(round(np.mean(TasaError),4))
        DSError.append(round(np.std(TasaError),4))
    generarCSV2_m("Resultados M")

#########################################################################
#---------------------------MAIN----------------------------------------#

#start = timer()
#experimentoFiltro()
experimentoK(2**12)
experimentoM(2**12)
#end = timer()
#print(end-start)

#########################################################################

#Acordarse de reiniciar arreglos A y B después de cada corrida
#A.clear() debería servir
#el 70% seran busquedas exitosas y las demas seran busquedas fallidas

# Se lee el archivo csv
#df = pd.read_csv('Popular-Baby-Names-Final.csv')
#Se quitan los valores nulos del dataset
#df = df.dropna()
#Se obtiene el largo del nombre más largo
#df2 = pd.read_csv('Film-Names.csv')

#max_len = df2['0'].str.len().max()
#Se obtiene el número de elementos en el dataset
#N = df['Name'].count()
#2^10-2^15
#