import json;
import glob;
import ntpath;
import numpy as np;
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans;
from scipy.cluster.vq import vq, kmeans, whiten
from scipy import spatial
from pprint import pprint
import sys;

entity2idx={};
idx2entity={};
def getEntityIdx(entity):
	if entity in entity2idx:
		#idx=entity2idx[entity];
		#idx2entity[idx]=entity;
		return entity2idx[entity];
	else:
		entity2idx[entity]=len(entity2idx);
		idx=entity2idx[entity];
		idx2entity[idx]=entity;
		return entity2idx[entity];
def getNumberOfUniqueEntity(totalRelations):
	for rel in totalRelations:
		getEntityIdx(rel[0]);
		getEntityIdx(rel[1]);
	return len(entity2idx);
	
def getMatrix(jsonDir):
	filePathList=glob.glob(jsonDir+"/*.json");
	totalRelations=[];
	for filepath in filePathList:
		#print filepath;
		try:
			relations=json.load(open(filepath))#[:20]; #get top 100 relations
		except:
			print filepath
			continue;
		totalRelations.extend(relations);
	n=getNumberOfUniqueEntity([x[1] for x in totalRelations]);
	print "#unique word: ",n;
	mat=np.zeros((n,n));
	# populate matrix;
	for x in totalRelations:
		p=x[0];
		rel=x[1];
		idx1=getEntityIdx(rel[0]);
		idx2=getEntityIdx(rel[1]);
		mat[idx1][idx2]+=1; #ignoring probability
		mat[idx2][idx1]+=1;
	return mat;
	
def getVector(mat,ncom):
	
	pca=PCA(n_components=ncom);
	matpca=pca.fit_transform(mat);
	return matpca;
	'''
	entity2vector={};
	for i in xrange(mat.shape[0]):
		entity2vector[idx2entity[i]]=mat[i,:];
	return entity2vector;
	'''

def getVecOfAWord(word):
	idx=entity2idx[word];
	return matpca[idx,:];
	
def getCosineSim(word1,word2):
	v1=getVecOfAWord(word1);
	v2=getVecOfAWord(word2);
	d=spatial.distance.cosine(v1, v2);
	#print d;
	return  1 - d;
	
def getTopNclosestWord(word,n):
	LST=[];
	for word2 in entity2idx:
		if word2!=word:
			d=getCosineSim(word,word2);
			LST.append( (word2,d) );
	sList=sorted(LST, key=lambda x: x[1],reverse=True);
	return sList[:n];
def storeAllVector(vectorPath):
	fout=open(vectorPath,"w");
	for entity in entity2idx:
		v=getVecOfAWord(entity);
		fout.write(entity+"\t"+"\t".join(str(a) for a in v)+"\n") ;
	fout.close();	
#main method
#param
import time;
import Constants;
startTime = time.time();   
dataDir="../sampleData1";
NCOM=20; #or vector dimension  
#end
jsonDir=dataDir+"/EntityRelationCommonKey3tf9main";

mat=getMatrix(jsonDir)
print mat
matpca=getVector(mat,NCOM);
#simWords=getTopNclosestWord("tripoli",10);
#pprint(simWords);
#open("temp.txt","w").write('\n'.join(entity2idx.keys()));
#print "sim: ",getCosineSim("united kingdom","london")
#print "sim: ",getCosineSim("china","beijing")

vectorPath = Constants.VECTOR_PATH_PCA
storeAllVector(vectorPath);

endTime = time.time();
print(endTime - startTime);
sys.exit();
'''
nCluster=50;
km=KMeans(n_clusters=nCluster);
labels=km.fit_predict(mat);
fout=open("cluster.txt","w");
for i in xrange(len(labels)):
	en=idx2entity[i];
	fout.write(str(en)+"\t"+str(labels[i])+"\n");
fout.close();
	
'''

