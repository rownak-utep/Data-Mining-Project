#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 00:17:28 2018

@author: afarhan
"""

"""
Constants.py
"""
DATA_DIR="../sampleData1";
#01_findTopicDist_lda
TEXT_ONLY_DIR= DATA_DIR + "/pwTextOnly";
OUT_DOC_ID2_TOPIC= DATA_DIR + "/Topic/docid2topic.json";
N_TOPICS=30;

#02_generateTFandEntityFile

TEXT_MODELER_OUTPUT_PATH = DATA_DIR+"/TextModelerOutput";

#03
TF_PATH = TEXT_MODELER_OUTPUT_PATH + "/tfFile.txt";
ENTITY_INFO_PATH = TEXT_MODELER_OUTPUT_PATH+"/entityInfo.txt";
UNIQUE_ENTITY_PATH = TEXT_MODELER_OUTPUT_PATH+"/uniqueEntity.txt";
PERSON_ONLY_TF_FILE_PATH = TEXT_MODELER_OUTPUT_PATH+"/entityTfFile.txt";

#04
OUT_WEIGHTED_TF_FILE_PATH = TEXT_MODELER_OUTPUT_PATH + "/entityWeightTfFile.txt";
TEXT_MODELER_DIR = "./DocsToEntities/Runner_DocsToEntities";

#05
RELATION_DIR = DATA_DIR +"/EntityRelationCommonKey3tf9main"; #EntityRelationWithoutKey

SEED_DOC_QUERY = "warburg";


#INFLU
DAY_THRESHOLD = 10*365; # for month multiply by 30;
DATE_KEYWORD_FILE =DATA_DIR + "/csv/pyruvateKinase_warburg.csv"

#07
WORD2VECTOR_PATH = DATA_DIR + "/word2vectorCommonKey3tf9";  #word2vectorWithoutKey
VECTOR_PATH = WORD2VECTOR_PATH + "/w2vBiRelVectors.txt";
VECTOR_PATH_PCA = WORD2VECTOR_PATH + "/PCAVectors.txt";
COMMON_KEYWORD =3;

#clustering
CLUSTER_PATH = WORD2VECTOR_PATH + "/KMeansClusterOutput.txt"
CLUSTER_PATH_HIERARCHICAL = WORD2VECTOR_PATH + "/HClusterOutput.txt"
CLUSTER_PATH_DBSCAN = WORD2VECTOR_PATH + "/DBClusterOutput.txt"
CLUSTER_PATH_COS_SIM = WORD2VECTOR_PATH + "/CosSimOutput.txt"
KMEANS_K = 1;
ENTITY_TO_DOC = WORD2VECTOR_PATH+"/fileEntityToDoc.txt"

CLUSTER_ENTITY_ALL_DOC_PATH = WORD2VECTOR_PATH + "/ClusterDoc"
CLUSTER_ENTITY_ORANGE_DOC_PATH = WORD2VECTOR_PATH + "/ClusterOrangeDoc"