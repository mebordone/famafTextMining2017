#!/usr/bin/python
# -*- coding: <utf8> -*-
import spacy
from pprint import pprint
from sklearn.feature_extraction import DictVectorizer
from sklearn.cluster import KMeans, MiniBatchKMeans
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
			if not (key in wordDict[word]): wordDict[word][key]=0
			wordDict[word][key]+=1
			if not (key in contextDict): contextDict[key]=0
			contextDict[key]+=1
			#~ key = "{}_{}".format(word.pos_,j)
			#~ if not (wordDic[word].has_key(key)): wordDic[word][key]=0
			#~ wordDic[word][key]+=1


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
#~ ppprint (wordDict)



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
Verbose=True #modo verboso de clustering
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
f = open("clusters.txt",'w')
pprint (clusterDict)

