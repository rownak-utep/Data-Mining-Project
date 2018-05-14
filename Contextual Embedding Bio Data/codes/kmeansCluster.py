#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 09:47:40 2018

@author: rownak
"""
import numpy as np
from sklearn.cluster import KMeans
from collections import defaultdict
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import pairwise_distances

def getVector(w2vBiRelVectorsPath):
    scores = [];
    count = 0;
    for line in open(w2vBiRelVectorsPath):
        
        words=line.strip().split("\t");
        #print words;	
        entity=words[0];
        #print entity
        terms.append(entity);
        vec = [];

        vec = words[1:]
        #print len(vec);
        scores.append(np.array(vec, dtype=float));
        count = count +1;
    return scores;

###---------Main Method-------###
import Constants
dataDir="../sampleData/word2vector/";
terms = [];

values = [];

w2vBiRelVectorsPath = Constants.VECTOR_PATH
clusterPath = Constants.CLUSTER_PATH
#docid2titlePath="C:\Users\mkader\Desktop/NYArchive/storyDiv/NYImageOnly2000-2015_docid2title.json";
values= getVector(w2vBiRelVectorsPath);
#print len(values);

kmeans = KMeans(n_clusters=50, random_state=0).fit(values)


file = open(clusterPath, "w");
count =0;

clusteredTerm = defaultdict(list)
for x in kmeans.labels_:
    clusteredTerm[x].append(terms[count]);
    count = count +1
for cluster in clusteredTerm:
    print cluster
    print clusteredTerm[cluster]
    file.write("%s : %s : %s" % (cluster, clusteredTerm[cluster], len(clusteredTerm[cluster])));
    file.write("\n");

labels = kmeans.labels_
c_e = metrics.calinski_harabaz_score(values, labels)
s_e = metrics.silhouette_score(values, labels, metric='euclidean')  
print "calinski_harabaz_score :", c_e
print "Sel :", s_e
print "Inertia: ", kmeans.inertia_

#==============================================================================
# file = open(Constants.CLUSTER_PATH_HIERARCHICAL, "w");
# count =0;
# hierarchyModel = AgglomerativeClustering(n_clusters=50,linkage="average")
# hierarchyModel.fit(values)
# clusteredTerm = defaultdict(list)
# for x in hierarchyModel.labels_:
#     clusteredTerm[x].append(terms[count]);
#     count = count +1
# for cluster in clusteredTerm:
#     print cluster
#     print clusteredTerm[cluster]
#     file.write("%s : %s : %s" % (cluster, clusteredTerm[cluster], len(clusteredTerm[cluster])));
#     file.write("\n");
#==============================================================================
file.close();
        