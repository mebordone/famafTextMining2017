#!/usr/bin/python
# -*- coding: <utf8> -*-
import spacy                           # See "Installing spaCy"
from pprint import pprint
from sklearn.feature_extraction import DictVectorizer
from sklearn.cluster import KMeans

f = open("./corpus/lavoztextodump.txt",'r')
text = f.read()
nlp = spacy.load('es')                 # You are here.
context=1
wordDict ={} #diccionario de contextos por palabra wordDic -> {{}}
contextDict={} #diccionario de contextos absolutos {}
stopwords = set(unicode(open('./palabrasvacias1.txt', 
'r').read(),'utf-8').split())
doc = nlp(unicode(text,'utf-8'))
for i in range(context,len(doc)-context):
	word= unicode(doc[i].text.lower())
	if word in stopwords: continue
	if not (word in wordDict): wordDict[word]={}
	for j in range (-(context),(context+1)):
		if (j != 0):
			contextWord= unicode(doc[i+j].text.lower())
			key = u'{}_{}'.format(contextWord,j)
			if not (key in wordDict[word]): wordDict[word][key]=0
			wordDict[word][key]+=1
			if not (key in contextDict): contextDict[key]=0
			contextDict[key]+=1
			#~ key = "{}_{}".format(word.pos_,j)
			#~ if not (wordDic[word].has_key(key)): wordDic[word][key]=0
			#~ wordDic[word][key]+=1
for word in wordDict:
	for context in wordDict[word]:
		wordDict[word][context]/=float(contextDict[context])
#~ pprint (wordDict)
#~ pprint (contextDict)

v = DictVectorizer(sparse=False)
D = []
wordIndex = []
for word in wordDict:
	wordIndex.append(word)
	D.append(wordDict[word])
X = v.fit_transform(D)
true_k =10
Verbose=True
km = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1,
                verbose=Verbose)
km.fit(X)
clusters = km.predict(X) # Devuelve una lista ipalabra->ncluster
clusterDict = {}
for i in range(len(wordIndex)):
	key = clusters[i]
	if not (key in clusterDict): clusterDict[key]=[]
	clusterDict[key].append(wordIndex[i])
#~ pprint (clusterDict)
