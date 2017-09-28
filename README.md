# famafTextMining2017
Carpeta de trabajo para la materia de Textmining Famaf 2017

#Iinforme
Armado de un sistema para obtener clusters de palabras.

##Introduccion
La idea del proyecto es armar clusters de palabras por similaridad , entendiendo similaridad dependiendo de los features que nosotros elijamos. Esto puede ser mas semntico (significado de la palabra) o sintctico (lugar/funcin que ocupa en la oracin)

Para hacer estos clusters de palabras debemos hacer una serie de tareas
1 - primero conseguir el grupo de palabras de donde vamos a aprender estas caracteristicas
2 - preprocesar los datos (corpus)
3 - contar las palabras y sus contextos de uso
4 - normalizacion del diccionario
5 - crear matriz
6 - armar clusters
7 - visuaizar los lusters

##Trabajos anteriores
Vamos a estar atacando una de las aproximaciones de  Word-sense induction
Para esto el approach clsico es analizar las palabras del contexto para inferir el significado de la misma. El contexto puede ser representado como una bolsa de palabras o puede ser representado segun la posicin que ocupa con respecto a la palabra principal. Ademas esta informacin de contexto puede guardar informacin de POS o triplas de dependencias, adems de las palabras en si mismas.

##Metodo propuesto
Lo que ahremos sera tomar la informacin de las palabras del contexto guardando la posicin correspondientes, al mismo tiempo se probara variar diferentes parametros para ver como afecta esto la formacin de clusters.

1 - primero conseguir el grupo de palabras de donde vamos a aprender estas caracteristicas
	En este caso tomaremos el corpus de la voz del interior.
2 - preprocesar los datos (corpus)
	El preprocesamiento sera hacer lowercase todas las palabras, y el filtrado de stopwords del español (esto se aplica si o si para las palabras, pero puede o no ser usado para el contexto). Al mismo tiempo se lemmatizar el corpus. La lematizacin se hizo bsicamente utilinando un diccionario de lemmas, si bin no es la aprozimacin que mas me gusta es rapida de implementar y en algo mejora.
3 - contar las palabras y sus contextos de uso
	Se crean diccionarios contando las palabras con su contexto, por un lado y guardando el conteo de contextos por el otro. Ademas del contexto se puede o no guardar tambien el POS de cada palabra.
4 - normalizacion del diccionario
    Primero se eliminan todas las features que ocurran menos que un numero "Umbral" de veces, luego se eliminan las palabras que quedan con todas las features en 0 y se calcula tfidf sobre cada feature. 
5 - crear matriz
	Se convierte el diccionario en una matriz.
6 - armar clusters
	Para esto se usa el modulo de Kmeans de sklearn (uego se hizo tambien con MiniBatchKMeans, otra implementacin de kmeans.
7 - visuaizar los lusters
	Para visualizar se arma un diccionario nuevo usando como key el numero de cluster indicado y values las palabras de ese clusters.

##Desarrollo
Primero se redujo el corpus para desarrollar el pipeline. Pero esta version no cuenta.
###Primera iteracion
Corpus = primeras 1000 lineas de lavoz
Lowercase = True
lemmatize = False
context = 1 # Amplitud del contexto
stopWord = False #Si filtro las stopwords
contextStop = False #Si filtro las stopwords del contexto
umbral=2
Clustering = Kmeans
nClusters = 10

Anduvo, pero me daba 9 singletones (clusters de un elemento) y 1 mega cluster con todo el resto

###Segunda iteracion
Pruebo con las 10.000 primeras lineas de la voz. Tuve problemas de memoria

###Tercera iteracion
Para bajar la dimensionalidad implemento lo siguiente
Corpus = primeras 1000 lineas de lavoz
Lowercase = True
lemmatize = True
context = 1 # Amplitud del contexto
stopWord = True #Si filtro las stopwords
contextStop = False #Si filtro las stopwords del contexto
umbral=10
Clustering = Kmeans
nClusters = 10

Sigo con problemas de memoria

### Cuarta iteracin
Baje de nuevo el tamaño del corpus a 1000 lineas, pero por el problema de los singletones intente con 50 clusters, 100 clusters y 500 clusters. Sigue igual el comportamiento.

### Quinta iteracin
Cambie el algoritmo de cluster a MiniBatchKMeans. En este caso se conformaron clusters mas interesantes, (casi no singletones y con algun sentido)

### Sexta iteracion
Probamos de nuevo con todo
Para bajar la dimensionalidad implemento lo siguiente
Corpus = primeras completa de lavoz
Lowercase = True
lemmatize = True
context = 1 # Amplitud del contexto
stopWord = True #Si filtro las stopwords
contextStop = False #Si filtro las stopwords del contexto
umbral=10
Clustering = Kmeans
nClusters = 10


