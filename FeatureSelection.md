# Informe de Feature Selection
## Informe

## Introduccion
## Antecedentes
## Metodo propuesto
##descripción del sampleo del corpus anotado

(idealmente, el corpus usado para clustering, y pueden hacer cut&paste de lo que escribieron para clustering)
The Wikicorpus is a trilingual corpus (Catalan, Spanish, English) that contains large portions of the Wikipedia (based on a 2006 dump) and has been automatically enriched with linguistic information. In its present version, it contains over 750 million words.

The corpora have been annotated with lemma and part of speech information using the open source library FreeLing. Also, they have been sense annotated with the state of the art Word Sense Disambiguation algorithm UKB. As UKB assigns WordNet senses, and WordNet has been aligned across languages via the InterLingual Index, this sort of annotation opens the way to massive explorations in lexical semantics that were not possible before.
KNOWN ISSUES:
- documents end with a marker 'ENDOFARTICLE', which should be removed. This marker was included by us to facilitate processing.
- some documents are truncated (i.e., </doc> marker at the end of the document), in cases where the parser broke down. These are generally long documents with many embedded elements.
- Est guardado en iso-8859-1 y hubo que trasformarlo a utf-8

##descripción del corpus no anotado


##brevísima descripción de las librerías utilizadas 

### Scikit-learn 
(formerly scikits.learn) is a free software machine learning library for the Python programming language.[3] It features various classification, regression and clustering algorithms including support vector machines, random forests, gradient boosting, k-means and DBSCAN, and is designed to interoperate with the Python numerical and scientific libraries NumPy and SciPy.

```
from sklearn.feature_extraction import DictVectorizer
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.feature_selection import SelectKBestimport re
from sklearn.feature_selection import chi2
```

###Spacy
spaCy (/speɪˈsiː/ spay-SEE) is an open-source software library for advanced Natural Language Processing, written in the programming languages Python and Cython. It offers the fastest syntactic parser in the world.[2][3][4] The library is published under the MIT license and currently supports English, German, French and Spanish, as well as tokenization for several other languages.[5]

Unlike NLTK, which is mainly intended for teaching and research, spaCy focuses on providing software for production usage.[6] As of version 1.0, spaCy also supports deep learning workflows[7] that allow connecting statistical models trained by popular machine learning libraries like TensorFlow, Keras or Scikit-learn.[8] spaCy's machine learning library, Thinc, is also available as a separate open-source Python library.[9]

spacy.load to load and panipulate "La voz" corpus

##descripción de la técnica supervisada de feature selection
Estimacion de relevancia de features segun extremely randomized trees, aka 

###Univariate feature selection
Univariate feature selection works by selecting the best features based on univariate statistical tests. It can be seen as a preprocessing step to an estimator. Scikit-learn exposes feature selection routines as objects that implement the transform method:
SelectKBest removes all but the k highest scoring features
como estimador utilizamos chi2 y en cantidad de features seleccionamos aproz la misma cantidad de features que surgieron con ETreeClassifier

###ExtraTreesClassifier + SelectFromModel
This class implements a meta estimator that fits a number of randomized decision trees (a.k.a. extra-trees) on various sub-samples of the dataset and use averaging to improve the predictive accuracy and control over-fitting.

```
clf = ExtraTreesClassifier()
clf = clf.fit(posX, pos)
model = SelectFromModel(clf, prefit=True)
X_new = model.transform(posX)
```
##descripción de la técnica no supervisada de feature selection
- de stopwords
- lematizacion
- eliminar contextos con pocas ocurrencias (menos de x)

#Removing features with low variance¶
VarianceThreshold is a simple baseline approach to feature selection. It removes all features whose variance doesn’t meet some threshold. By default, it removes all zero-variance features, i.e. features that have the same value in all samples.
As an example, suppose that we have a dataset with boolean features, and we want to remove all features that are either one or zero (on or off) in more than 80% of the samples. Boolean features are Bernoulli random variables, and the variance of such variables is given by

##discusión de cómo los nuevos espacios afectan a las soluciones de clustering elegidas, en comparación con el espacio anterior. Discusión cualitativa.

Comprativa de uso de los metodos supervisados para usando como tarea de pretexto clasificacin de POS y Clasificacin de sinsets