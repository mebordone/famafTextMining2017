# famafTextMining2017
Carpeta de trabajo para la materia de Textmining Famaf 2017

# Iinforme
Armado de un sistema para obtener clusters de palabras.

## Introduccion
La idea del proyecto es armar clusters de palabras por similaridad , entendiendo similaridad dependiendo de los features que nosotros elijamos. Esto puede ser mas semntico (significado de la palabra) o sintctico (lugar/funcin que ocupa en la oracin)

Para hacer estos clusters de palabras debemos hacer una serie de tareas
1 - primero conseguir el grupo de palabras de donde vamos a aprender estas caracteristicas
2 - preprocesar los datos (corpus)
3 - contar las palabras y sus contextos de uso
4 - normalizacion del diccionario
5 - crear matriz
6 - armar clusters
7 - visuaizar los lusters

## Trabajos anteriores
Vamos a estar atacando una de las aproximaciones de  Word-sense induction
Para esto el approach clsico es analizar las palabras del contexto para inferir el significado de la misma. El contexto puede ser representado como una bolsa de palabras o puede ser representado segun la posicin que ocupa con respecto a la palabra principal. Ademas esta informacin de contexto puede guardar informacin de POS o triplas de dependencias, adems de las palabras en si mismas.

## Metodo propuesto
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

## Desarrollo
Primero se redujo el corpus para desarrollar el pipeline. Pero esta version no cuenta.
### Primera iteracion
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

### Segunda iteracion
Pruebo con las 10.000 primeras lineas de la voz. Tuve problemas de memoria

### Tercera iteracion
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
contextStop = True #Si filtro las stopwords del contexto
umbral = 10
Clustering = MiniBatchKMeans
nClusters = 50

Caso 1: 50clusterdump.txt
Son 50 clusters, utilizando el corpus completo de lavoz

Caso 2: 50clustersdump_context_no_stop.txt
Son 50 clusters usando el corpus completo, sin filtrar las stopwords del contexto

Caso 3: 50clustersdump_context_no_stop_context2.txt
Son 50 clusters usando el corpus completo, sin filtrar las stopwords del contexto y ampliando el contexto a (-2,+2)

###Algunos resultados
Caso 1
Esta interesante, se conforman clasers como este por ejemplo
47: [u'norte',
      u'mar\xeda',
      u'roja',
      u'urbana',
      u'rural',
      u'sur',
      u'central',
      u'c\xe9ntrica',
      u'euro',
      u'serrana',
      u'carlos'],
Donde se ven palabras que tiene que ver principalmente con la geografa.
45: [u'c\xf3rdoba',
      u'vez',
      u'ac\xe1',
      u'ahora',
      u'a\xfan',
      u'adem\xe1s',
      u'todav\xeda',
      u'ya',
      u's\xf3lo',
      u'tampoco',
      u'siempre',
      u'hoy',
      u'\u201c',
      u'tambi\xe9n',
      u'bien'],
Palabras que parece ser que tienen que ver con lo temporal.

Caso 2
cambia un poco las agrupaciones, por ejmplo aparecen clusters de entidades
45: [u'dnu',
      u'china',
      u'cuadrados',
      u'apta',
      u'unrc',
      u'brasil',
      u'onu',
      u'enero',
      u'estrat\xe9gico',
      u'setiembre',
      u'septiembre',
      u'ambiente',
      u'francia',
      u'ingl\xe9s',
      u'farc',
      u'auh',
      u'foto',
      u'omc',
      u'oms',
      u'agosto',
      u'stia',
      u'oea',
      u'anses',
      u'tsj',
      u'octubre',
      u'up1',
      u'fuego',
      u'crese',
      u'ciento',
      u'junio',
      u'ups',
      u'chile',
      u'fedecom',
      u'fadea',
      u'inadi',
      u'sep',
      u'indec',
      u'm\xe9xico',
      u'cc',
      u'tamse',
      u'oncca',
      u'lunes',
      u'd2',
      u'apross',
      u'suoem',
      u'uepc',
      u'ersep',
      u'cgt',
      u'uruguay',
      u'martes',
      u'hogar',
      u'b',
      u'botnia',
      u'\u2026',
      u'cepal',
      u'h1n1',
      u'pp',
      u'pv',
      u'pt',
      u'psdb',
      u'nacer',
      u'domingo',
      u'jury',
      u'fmi',
      u'cotbn',
      u'cra',
      u'euros',
      u'd',
      u'ue',
      u'ucr',
      u'ucc',
      u'uca',
      u's\xe1bado',
      u'cae',
      u'ojal\xe1',
      u'radicales',
      u'pib',
      u'bce',
      u'unc',
      u'noviembre',
      u'uocra',
      u'pyme',
      u'copec',
      u'epec',
      u'julio',
      u'eln',
      u'mi\xe9rcoles',
      u'colombia',
      u'febrero',
      u'sip',
      u'sic',
      u'aparte',
      u'*',
      u'ate',
      u'diciembre',
      u'famaf',
      u'uia',
      u'uic',
      u'cta',
      u'otan',
      u'marzo',
      u'resultados',
      u'unidos',
      u'aoita',
      u'utn',
      u'cartez',
      u'iaraf',
      u'd\xe9cadas',
      u'c',
      u'afip',
      u'abril',
      u'etc\xe9tera',
      u'aires',
      u'bolivia',
      u'jueves',
      u'unasur',
      u'bid',
      u'viernes',
      u'alberto',
      u'rac',
      u'mayo',
      u'faa',
      u'nbi',
      u'bcra'],
o clustes de grupos
46: [u'indocumentados',
      u't\xe9rmica',
      u'sanciones',
      u'urbanizaciones',
      u'railway',
      u'programas',
      u'leyes',
      u'railways',
      u'generaciones',
      u'ilegales',
      u'islas',
      u'detenidos',
      u'revelaciones',
      u'invitados',
      u'tecnolog\xedas',
      u'estaci\xf3n',
      u'tropez',
      u'dalonso@lavozdelinterior.com.ar'],

Caso 3
En este caso empieza a agarrar creo, cosas mas sutiles, como procedencia
 36: [u'hay',
      u'sudamericano',
      u'm\xe1s',
      u'caribe\xf1o',
      u'vasco',
      u'tiene',
      u'\u201d',
      u'vecino',
      u'\u201c',
      u'tambi\xe9n',
      u'latinoamericano',
      u'europeo',
      u'asi\xe1tico'],

## Conclusiones y trabajo futuro.
Lo principal fu poder armar el pipeline de trabajo y poder parametrizar opciones para tunear y comparar. Parece ser que comenz a funcionar mejor. Sera interesante comenzar a armar mas clusters, adems poder agregar tripas de dependencia y un lematizador de verdad.
Mas adelanta tambien seria bueno comenzar a buscar etiquetar los clusters y tomar algunas mtricas de evaluacin de clusters para jugar y comparar.




