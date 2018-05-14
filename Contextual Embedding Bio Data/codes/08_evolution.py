# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 23:27:13 2018

@author: Rownak
"""
import os;

import numpy as np
from collections import defaultdict;
from sklearn.metrics.pairwise import cosine_similarity

def cosineSimilarityEntity(w2vBiRelVectors):
    entitySimilarityList={};
    for key in w2vBiRelVectors:

        for key2 in w2vBiRelVectors:
            if key!=key2:
                x = w2vBiRelVectors.get(key).reshape(1,-1);
                y = w2vBiRelVectors.get(key2).reshape(1,-1);
                entitySimilarity = cosine_similarity(x, y);
                #print entitySimilarity[0][0];
                if entitySimilarity[0][0]> 0.0:
                    continue;
                keyConcate = key + "\t" + key2;
                keyConcate2 = key2 + "\t" + key; 
                if keyConcate2 not in entitySimilarityList:
                    entitySimilarityList[keyConcate] = entitySimilarity[0][0];
 
    return entitySimilarityList;

def getVector(w2vBiRelVectorsPath):
    entity2vec=defaultdict(list);
    for line in open(w2vBiRelVectorsPath):
        
        words=line.strip().split("\t");
        #print words;	
        entity=words[0];
        #print entity
        vec = np.arange(1, 0, dtype=np.float);
        for i in xrange(1,len(words),2):
            #print words[i];
            p=float(words[i]);
            vec = np.append(vec, p);
        entity2vec[entity] = vec;
    return entity2vec;

###---------Main Method-------###
dataDir="../sampleData1";

w2vBiRelVectorsPath =dataDir+"/word2vectorCommonKey3tf9/w2vBiRelVectors.txt"
#pcaVectorsPath =dataDir+"/word2Vector/PCAVectors.txt"
#docid2titlePath="C:\Users\mkader\Desktop/NYArchive/storyDiv/NYImageOnly2000-2015_docid2title.json";
w2vBiRelVectors= getVector(w2vBiRelVectorsPath);
print "vector read complete";
cosineSimilarVector = cosineSimilarityEntity(w2vBiRelVectors);
dataDir="../sampleData1";  
evolutionPath=dataDir+"/evolution.txt";
if not os.path.isdir(dataDir):
	os.makedirs(dataDir);
file = open(evolutionPath, "w");
print "File Write Start:"
for key, value in sorted(cosineSimilarVector.iteritems(), key=lambda (k,v): (v,k), reverse = True ):
    #print "%s: %s" % (key, value)
    file.write("%s: %s" % (key, value));
    
    file.write("\n");
file.close();
print "File Write finish:"
#print cosineSimilarVector;
#print w2vBiRelVectors;