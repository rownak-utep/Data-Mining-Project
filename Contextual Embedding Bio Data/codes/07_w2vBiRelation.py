#from gensimLocal.models import Word2Vec;
from gensim.models import Word2Vec;
from pprint import pprint
import glob;
import ntpath;
import json;
import sys;
from pprint import pprint;

def readAllRelations(jsonDir):
    filePathList=glob.glob(jsonDir+"/*.json");
    
    totalRelations=[];
    for filepath in filePathList:
        #print filepath;
        try:
            relations=json.load(open(filepath))#[:50]; #get top 100 relations
        except:
            print filepath
            continue;
        totalRelations.extend(relations);
    
    return totalRelations;
def makeSentences(allRelations):
    sentences=[];
    for r in allRelations:
        entityPair=r[1];
        sentences.append(entityPair);
    return sentences;

def storeAllVector(model):
	fout=open(vectorPath,"w+");
	for entity in model.wv.vocab.keys():
		v=model[entity];
		fout.write(entity+"\t"+"\t".join(str(a) for a in v)+"\n") ;	
	fout.close();
   
def makeVector(sentences):
    model = Word2Vec(sentences, size=25 , window=1, min_count=1,iter=10,sg=0);
    storeAllVector(model);
    #sim=model.most_similar(positive=["qaddafi"], negative=[], topn=10);
    #print sim;
        
#main method
#params
import time;
import Constants;
startTime = time.time();  

dataDir = Constants.DATA_DIR;
#end
jsonDir = Constants.RELATION_DIR;

vectorPath = Constants.VECTOR_PATH;

allRelations=readAllRelations(jsonDir)
#print allRelations[:15];
sentences=makeSentences(allRelations);
makeVector(sentences);

endTime = time.time();
print(endTime - startTime);
sys.exit();


sentences=[["A","B"],["B","C"]];
#sentences=[["A","B"],["B","C"],["B","A"],["C","B"]];
model = Word2Vec(sentences, size=5, window=1, min_count=1,iter=100,sg=0)
A_close=model.most_similar(positive=["A"], negative=[], topn=10)
B_close=model.most_similar(positive=["B"], negative=[], topn=10)
C_close=model.most_similar(positive=["C"], negative=[], topn=10)

print "A: ",A_close
print "B: ",B_close
print "C: ",C_close
