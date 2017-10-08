#!/usr/bin/python
# -*- coding: <utf8> -*-
import spacy
from pprint import pprint
from sklearn.feature_extraction import DictVectorizer
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.feature_selection import SelectKBestimport re
from sklearn.feature_selection import chi2

##################################~ Aprender features Con POS

f = open("./corpus/spanishEtiquetado_480000_485000_utf8",'r')
text = f.read()
f.close()
text = unicode(text,'utf-8').split(u'\n')

#Preprocessing - Limpiar etiquetas extras del corpus

text=text[:-1] #el ultimo quizas este roto por el chunk que hago
corpus =[]
patron1 = re.compile(r'<[^>]*>')
patron2 = re.compile(r'ENDOFARTICLE+') 
for line in text:
	if patron1.match(line): continue
	if patron1.match(line): continue
	append = line.split(' ')
	if len(append) == 4:
		corpus.append(line.split(' '))

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

#~ Armar diccionario de palabras y contexto para aprender features de Corpus anotado
stopWord = True #Si filtro las stopwords
context = 2 # Amplitud del contexto
contextStop = True #Si filtro las stopwords del contexto
wposDict ={} #diccionario de contextos por palabra wordDic -> {{}}
contextDict={} #diccionario de contextos absolutos {}
stopwords = set(unicode(open('./palabrasvacias1.txt', 
'r').read(),'utf-8').split())
for i in range(context,len(corpus)-context):
	if len(corpus[i]) <> 4: continue
	if isfloat(corpus[i][1]): corpus[i][1]= u"#DIGIT"
	word_pos= (u'{} {:.2}'.format(corpus[i][1],corpus[i][2])) #toma el pos truncado a los dos primeros caracteresexi
	if not (word_pos in wposDict): wposDict[word_pos]={}
	for j in range (-(context),(context+1)):
		if (j != 0):
			contextWord= corpus[i+j][0].lower()
			if contextStop and contextWord in stopwords: continue
			key = u'{}_{}'.format(contextWord,j)
			if not (key in wposDict[word_pos]): wposDict[word_pos][key]=0
			wposDict[word_pos][key]+=1
			if not (key in contextDict): contextDict[key]=0
			contextDict[key]+=1

# Eliminar features con menos de "umbral" repeticiones
# se eliminan las palabras que quedan sin features
umbral=10 # Repeticiones minimas para considerar una feature
wposDict_a = {}
for pos in wposDict:
	wposDict_a[pos]={}
	for context in wposDict[pos]:
		if wposDict[pos][context]>= umbral:
			wposDict_a[pos][context]= wposDict[pos][context]
wposDict = {clave: valor for clave, valor in wposDict_a.items() if valor}

# normalizar features (tfidf)
for pos in wposDict:
	for context in wposDict[pos]:
		wposDict[pos][context]/=float(contextDict[context])

# Convertir diccionarios en matriz
	
pos = []
dictlist = []
for key, value in wposDict.iteritems():
    dictlist.append(value)
    pos.append(key.split(' ')[1])
v = DictVectorizer(sparse=True)
posX = v.fit_transform(dictlist)

#Supervised "selectkfeatures" Feature selection 
pprint (posX.shape)
clf = ExtraTreesClassifier()
nfeatures=1500 #para seleccionar un numero similar a erandtree
X_new = SelectKBest(chi2, k=nfeatures).fit_transform(posX, pos)
pprint(X_new.shape)

wPosFeatures=[]
#~ Recuperar los features de entrenados con POS
filteredPosX = v.inverse_transform(posX)
posFeatures = []
for i in filteredPosX[:2]:
	for j in i:
		posFeatures.append(j)

posFeatures = set(posFeatures)
#~ pprint(wPosFeatures)


################################ Clustering con las features de POS
		

f = open("./corpus/lavoztextodump.txt",'r')
text = f.read()
f.close()

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

#Preprocessing
lowercase = True
lemmatize = True
if lowercase == True:
	text = text.lower()
if lemmatize == True:
	lemmas_lines=unicode(open('./lemmatization-es.txt', 
'r').read(),'utf-8').split(u'\n')
	lemmasDict={}
	for line in lemmas_lines[:-1]:
		a=line.split(u'	')
		lemmasDict[a[1]]=a[0]
#~ pprint(lemmasDict)

#Armar diccionarios de palabras y contextos
stopWord = True #Si filtro las stopwords
context = 2 # Amplitud del contexto
contextStop = True #Si filtro las stopwords del contexto
wordDict ={} #diccionario de contextos por palabra wordDic -> {{}}
contextDict={} #diccionario de contextos absolutos {}
stopwords = set(unicode(open('./palabrasvacias1.txt', 
'r').read(),'utf-8').split())
nlp = spacy.load('es')        
doc = nlp(unicode(text,'utf-8'))
for i in range(context,len(doc)-context):
	word= unicode(doc[i].text.lower())
	if lemmatize == True and word in lemmasDict: word = lemmasDict[word]
	if stopWord and word in stopwords: continue
	if isfloat(word): word= u"#DIGIT"
	if not (word in wordDict): wordDict[word]={}
	key = u'{}'.format(doc[i].pos_)
	if not (key in wordDict[word]): wordDict[word][key]=0
	wordDict[word][key]+=1
	if not (key in contextDict): contextDict[key]=0
	contextDict[key]+=1
	for j in range (-(context),(context+1)):
		if (j != 0):
			contextWord= unicode(doc[i+j].text.lower())
			if contextStop and contextWord in stopwords: continue
			key = u'{}_{}'.format(contextWord,j)
			if key not in posFeatures: continue
			if not (key in wordDict[word]): wordDict[word][key]=0
			wordDict[word][key]+=1
			if not (key in contextDict): contextDict[key]=0
			contextDict[key]+=1

# Eliminar features con menos de "umbral" repeticiones
# se eliminan las palabras que quedan sin features
umbral=10 # Repeticiones minimas para considerar una feature
wordDict_a = {}
for word in wordDict:
	wordDict_a[word]={}
	for context in wordDict[word]:
		if wordDict[word][context]>= umbral:
			wordDict_a[word][context]= wordDict[word][context]
wordDict = {clave: valor for clave, valor in wordDict_a.items() if valor}

# normalizar features (tfidf)
for word in wordDict:
	for context in wordDict[word]:
		wordDict[word][context]/=float(contextDict[context])
		
# Convertir diccionarios en matriz
v = DictVectorizer(sparse=False)
D = []
wordIndex = []
for word in wordDict:
	wordIndex.append(word)
	D.append(wordDict[word])
X = v.fit_transform(D)

#Armar Clusters
true_k =50 # Cantidad de clusters
Verbose=False #modo verboso de clustering
km = MiniBatchKMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1,
                verbose=Verbose)
km.fit(X)

# Mostrar los clusters -> armo un diccionario agrupando las palabras por 
# cluster
clusters = km.predict(X) # Devuelve una lista ipalabra->ncluster
clusterDict = {}
for i in range(len(wordIndex)):
	key = clusters[i]
	if not (key in clusterDict): clusterDict[key]=[]
	clusterDict[key].append(wordIndex[i])
f = open("./corpus/clustersPOS.txt",'w')
pprint (clusterDict)
