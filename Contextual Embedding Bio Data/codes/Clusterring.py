
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 09:47:40 2018

@author: rownak
"""
import numpy as np

from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
from collections import defaultdict
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from sklearn import metrics
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import pairwise_distances
import json;

def getVectorForCosine(w2vBiRelVectorsPath):
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



def kmeans(values, entity2Doc, entity2Doc2, n_clusters):
    fileKmeans = open(Constants.CLUSTER_PATH, "w");
    count =0;
    label2VectorList = []
    for i in range(len(values)):
        label2VectorList.append([terms[i]] + values[i].tolist())
    kmeansModel = KMeans(n_clusters, random_state=0)
    cluster_labels = kmeansModel.fit_predict(values)
    silhouette_avg = silhouette_score(values, cluster_labels)
    print "For Cluster Size: ", n_clusters
    print "silhouette_avg", silhouette_avg
    kmeansClusterTerm = defaultdict(list)
    print "Sum of square distance:", kmeansModel.inertia_;
    print "Number of iteration:", kmeansModel.n_iter_;
    fileClusterEntityDoc = open(Constants.WORD2VECTOR_PATH + "/" + "KmeansEntity2Doc"+ ".txt", "w");
    for x in kmeansModel.labels_:
        kmeansClusterTerm[x].append(terms[count]);
        count = count +1
    for cluster in kmeansClusterTerm:
        #print cluster
        #print kmeansClusterTerm[cluster]
        fileKmeans.write("%s : %s : %s" % (cluster, kmeansClusterTerm[cluster], len(kmeansClusterTerm[cluster])));
        fileKmeans.write("\n");
        fileClusterEntityDoc.write("Cluster No: " + str(cluster) + "\n")
        fileClusterEntityDoc.write("Cluster Items : %s" %( kmeansClusterTerm[cluster]) + "\n")
        
        for entity in kmeansClusterTerm[cluster]:
            fileClusterEntityDoc.write("Entity: " + entity + "\n")
            fileClusterEntityDoc.write("File That contain this entity: " + str(entity2Doc[entity]) + "\n\n")
            fileClusterEntityDoc.write("File that is related: " + str(entity2Doc2[entity]) + "\n\n")
    fileKmeans.close();
    return label2VectorList


def hierarchical(values):
    fileHierarchi = open(Constants.CLUSTER_PATH_HIERARCHICAL, "w");
    count =0;
    
    hierarchyModel = AgglomerativeClustering(n_clusters=50,linkage="average")
    hierarchyModel.fit(values)
    hierarchyClusteredTerm = defaultdict(list)
    for x in hierarchyModel.labels_:
        hierarchyClusteredTerm[x].append(terms[count]);
        count = count +1
    for cluster in hierarchyClusteredTerm:
        print cluster
        print hierarchyClusteredTerm[cluster]
        fileHierarchi.write("%s : %s : %s" % (cluster, hierarchyClusteredTerm[cluster], len(hierarchyClusteredTerm[cluster])));
        fileHierarchi.write("\n");
    fileHierarchi.close();
 
def dbScan(values, eps, min_samples):
    fileDBScan = open(Constants.CLUSTER_PATH_DBSCAN, "w");
    count =0;
    dbScanModel = DBSCAN(eps, min_samples).fit(values)
    dbScanClusteredTerm = defaultdict(list)
    labels = dbScanModel.labels_;
    print "Number Of Cluster: ", len(set(labels))
    
    # list of list for PCA
    label2VectorList = [];
    avgSilhotte = metrics.silhouette_score(values, labels, metric='euclidean');
    print avgSilhotte
    for x in dbScanModel.labels_:
        dbScanClusteredTerm[x].append(terms[count]);
        if x>0:
            label2VectorList.append([x] + values[count].tolist())
        count = count +1
    
    #print "label2VectorList: ", label2VectorList
    
    countTotalEntity =0
   
    for cluster in dbScanClusteredTerm:
       # print cluster
        #print dbScanClusteredTerm[cluster], " : Item Number: ", len(dbScanClusteredTerm[cluster]) 
        if(cluster>=0 and len(dbScanClusteredTerm[cluster])<50):
            countTotalEntity = countTotalEntity + len(dbScanClusteredTerm[cluster]);
        fileDBScan.write("%s\t%s\t%s" % (cluster, dbScanClusteredTerm[cluster], len(dbScanClusteredTerm[cluster])));
        fileDBScan.write("\n");
    fileDBScan.write("Total entity inside cluster: %s" %(countTotalEntity));
    fileDBScan.close();
    
    return dbScanClusteredTerm, label2VectorList;

 

 

def dbScanOptimal(values):
    
    x = np.arange(0.05, 1, 0.005);
    avgSilhotteList = [];
    for i in x:
        #fileOpt = open(Constants.WORD2VECTOR_PATH + "/OptimalDb25dim.txt", "a");
        
        for j in range(5, 10):
            dbScanModel = DBSCAN(eps=i, min_samples=j).fit(values)
            labels = dbScanModel.labels_;
            

            numCLuster = len(set(labels))
            if numCLuster>5:
                avgSilhotte = metrics.silhouette_score(values, labels, metric='euclidean');
                print "avgSilhotte:", avgSilhotte, "  Eps : ", i, " minS: ", j, "Number Of Cluster: ", len(set(labels))
                avgSilhotteList.append([avgSilhotte, i, j, numCLuster])
                #fileOpt.write("avgSilhotte: %s\tEps: %s\tMinS: %s\tClusterNo: %s\n" %(avgSilhotte, i, j, numCLuster))
        #fileOpt.close();
    storeDataCSV(Constants.WORD2VECTOR_PATH, avgSilhotteList)

def cosineSimilarityEntity(w2vBiRelVectorsPath):
    entitySimilarityList={};
    w2vBiRelVectors= getVectorForCosine(w2vBiRelVectorsPath);
    fileCosineSim = open(Constants.CLUSTER_PATH_COS_SIM, "w");
    csvVec = [];
    for key in w2vBiRelVectors:

        for key2 in w2vBiRelVectors:
            #if str(key) != "warburg" and  str(key2) != "glutamine":
                #continue;
                #'glycogen', 'phosphatase'
            if str(key) == "glycogen metabolism" and  str(key2) == "phosphatase 1":
                if key!=key2:
                    csvVec.append(w2vBiRelVectors.get(key))
                    csvVec.append(w2vBiRelVectors.get(key2))
                    
                    x = w2vBiRelVectors.get(key).reshape(1,-1);
                    y = w2vBiRelVectors.get(key2).reshape(1,-1);
                    entitySimilarity = cosine_similarity(x, y);
                    print key
                    print x
                    print key2
                    print y
                    print "cosine:"
                    print entitySimilarity;
                    #print entitySimilarity[0][0];
                    keyConcate = key + "\t" + key2;
                    keyConcate2 = key2 + "\t" + key; 
                    if keyConcate2 not in entitySimilarityList:
                        entitySimilarityList[keyConcate] = entitySimilarity[0][0];
            

    for key, value in sorted(entitySimilarityList.iteritems(), key=lambda (k,v): (v,k), reverse = True ):
        #print "%s: %s" % (key, value)
        fileCosineSim.write("%s: %s" % (key, value));
    
        fileCosineSim.write("\n");
    storeDataCSV(Constants.WORD2VECTOR_PATH, csvVec)
def getTFdata(TFFilePath):
	docid2entityList=defaultdict(list);

	for line in open(TFFilePath):
		words=line.strip().split("\t");
		docid=words[0];

		for i in xrange(1,len(words),2):
			words[i]=unicode(words[i], errors='ignore');
			docid2entityList[docid].append(words[i]);
			 #if the next word is not a int??
		#docid2entityList[docid]=docid2entityList[docid][:10];# remove *******
	return docid2entityList;    

def getEntityToDoc(entityToDocPath):
    entity2Doc = defaultdict(list);
    entity2Doc2 = defaultdict(list);

    for line in open(entityToDocPath):
        words=line.strip().split("\t");
	
        entity=words[0];
        if(words[1] not in entity2Doc[entity]):
            entity2Doc[entity].append(words[1])
            entity2Doc2[entity].append(words[2])
    return entity2Doc, entity2Doc2;
  
def getDocFromEntityList(dbScanClusteredTerm, docid2entityList):
    for cluster in dbScanClusteredTerm:
        if cluster < 1:
            continue;
        print str(dbScanClusteredTerm[cluster])
        
        fileClusterEntityDoc = open(Constants.CLUSTER_ENTITY_ALL_DOC_PATH + "/" + str(cluster)+ ".txt", "w");

        fileClusterEntityDoc.write("Clustered Size: \n" + str(len(dbScanClusteredTerm[cluster])) + "\n\n");
        fileClusterEntityDoc.write("Clustered Entity: \n" + str(dbScanClusteredTerm[cluster]) + "\n\n")
        
        for entity in dbScanClusteredTerm[cluster]:
            #print entity
            entityToDocId = []
            for k in docid2entityList.keys():
                if entity in docid2entityList[k]:
                    print str(k)
                    entityToDocId.append('' + str(k))
            
            fileClusterEntityDoc.write("Entity: " + entity + "\n")
            fileClusterEntityDoc.write("All FileNames: " + str(entityToDocId) + "\n")
        fileClusterEntityDoc.close();  

def getDocFromEntity2Doc(dbScanClusteredTerm, entity2Doc, entity2Doc2):
    for cluster in dbScanClusteredTerm:
        if cluster < 0:
            continue;
        fileClusterEntityDoc = open(Constants.CLUSTER_ENTITY_ORANGE_DOC_PATH + "/" + str(cluster)+ ".txt", "w");
        
        fileClusterEntityDoc.write("Clustered Size: \n" + str(len(dbScanClusteredTerm[cluster])) + "\n\n");
        fileClusterEntityDoc.write("Clustered Entity: \n" + str(dbScanClusteredTerm[cluster]) + "\n\n")
        for entity in dbScanClusteredTerm[cluster]:
            print entity
            if entity not in entity2Doc.keys():
                print "Not recognized\n"
                continue
            print entity2Doc[entity]
            fileClusterEntityDoc.write("Entity: " + entity + "\n")
            fileClusterEntityDoc.write("File That contain this entity: " + str(entity2Doc[entity]) + "\n\n")
            fileClusterEntityDoc.write("File that is related: " + str(entity2Doc2[entity]) + "\n\n")
            
#==============================================================================
#             for fileName in entityToDocList[entity]:
#                 fileContent = open(Constants.TEXT_ONLY_DIR + "/"+ fileName +".txt");
#                 fileClusterEntityDoc.write("FileName: " + fileName + "\n\n")
#                 for line in fileContent:
#                     fileClusterEntityDoc.write(line)
#                 fileClusterEntityDoc.write("\n\n")
#==============================================================================
        fileClusterEntityDoc.close();

def getDoc(dbScanClusteredTerm, entityToDocPath):
    for cluster in dbScanClusteredTerm:
        if cluster < 0:
            continue;
        fileClusterEntityDoc = open(Constants.CLUSTER_ENTITY_DOC_PATH + "/" + str(cluster)+ ".txt", "w");
        entityToDocList=json.load(open(entityToDocPath));
        fileClusterEntityDoc.write("Clustered Size: \n" + str(len(dbScanClusteredTerm[cluster])) + "\n\n");
        fileClusterEntityDoc.write("Clustered Entity: \n" + str(dbScanClusteredTerm[cluster]) + "\n\n")
        for entity in dbScanClusteredTerm[cluster]:
            print entity
            if entity not in entityToDocList:
                print "Not recognized\n"
                continue
            print entityToDocList[entity]
            fileClusterEntityDoc.write("Entity: " + entity + "\n")
            fileClusterEntityDoc.write("File/Files Containing the entity: " + str(entityToDocList[entity]) + "\n\n")
            
#==============================================================================
#             for fileName in entityToDocList[entity]:
#                 fileContent = open(Constants.TEXT_ONLY_DIR + "/"+ fileName +".txt");
#                 fileClusterEntityDoc.write("FileName: " + fileName + "\n\n")
#                 for line in fileContent:
#                     fileClusterEntityDoc.write(line)
#                 fileClusterEntityDoc.write("\n\n")
#==============================================================================
        fileClusterEntityDoc.close();

def storeDataCSV(path, label2VectorList):
    
    
    #Create a CSV File
    print path
    absolutePath = os.getcwd() +'/'+ path +'/'+ 'avgSilhotteData.csv'
    with open(absolutePath, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for r in label2VectorList:
            writer.writerow(r)

  ###---------Main Method-------###
import Constants
import os
import csv

terms = [];

values = [];

w2vBiRelVectorsPath = Constants.VECTOR_PATH

values= getVector(w2vBiRelVectorsPath);



entity2Doc, entity2Doc2 = getEntityToDoc(Constants.ENTITY_TO_DOC);

count = 0;
csvVec = [];
#==============================================================================
# for t in terms:
#     
#     if t == "glutamine" :
#         csvVec.append([3] + values[count].tolist())
#     if t == "warburg" :
#         csvVec.append([1] + values[count].tolist())
#     if t == "pyruvate kinase m1":
#         csvVec.append([2] + values[count].tolist())
#     count = count +1;
# storeDataCSV(Constants.WORD2VECTOR_PATH, csvVec)
#==============================================================================
#==============================================================================
# label2VectorList = kmeans(values,entity2Doc, entity2Doc2, 75);
# storeDataCSV(Constants.WORD2VECTOR_PATH, label2VectorList)
#==============================================================================

#dbScanOptimal(values)

#dbScanClusteredTerm, label2VectorList = dbScan(values, 0.08,5);

#storeDataCSV(Constants.WORD2VECTOR_PATH, label2VectorList)

#==============================================================================
#entity2Doc, entity2Doc2 = getEntityToDoc(Constants.ENTITY_TO_DOC);
#getDocFromEntity2Doc(dbScanClusteredTerm, entity2Doc, entity2Doc2)
#==============================================================================


#docid2entityList=getTFdata(Constants.PERSON_ONLY_TF_FILE_PATH);
#print docid2entityList;
#getDocFromEntityList(dbScanClusteredTerm, docid2entityList)

cosineSimilarityEntity(w2vBiRelVectorsPath);