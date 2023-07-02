# LogT3
Tarea 3 Diseño y análisis de algoritmos (CC4102-1)  semestre otoño 2023. Nicolás Calbucura, Felipe Olivares, Leonel Espinoza.

Implementar un **Filtro Bloom**:  
    Indica si el elemento que buscamos está dentro de la base de datos o no con una probabilidad de error al decir que el elemento si está.  

El filtro utiliza un arreglo *M* de *m* bits inicializado en 0 y *k* funciones de hash distintas (digamos que el arreglo *H* las contiene). Al aplicar *H[i]\(x)* retorna un valor entre *[1,m]*, para cualquier elemento *x*.  
Cuando se inserta un nuevo elemento a nuestro universo U, se aplica cada una de las *k* funciones de hash, lo que devolverá distintas posiciones *j* en el arreglo *M*. Luejo modificamos *M[j]* para cada *j* retornado por cada funcion de hash.  

Luego, cuando buscamos un elemento *y*, aplicamos el **filtro de Bloom**: calculamos *H[i]\(y)* con *i* en *[1,k]*. Si cada una de las funciones de hash retorna 1, entonces buscamos el elemento en la base de datos. Si al menos una de las funciones de hash retorna 0, entonces podemos decir con seguridad que el elemento no se encuentra en la base de datos.  


