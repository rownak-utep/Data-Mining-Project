from collections import defaultdict;

def getDocid2PersonEntityList(entityInfoPath):
    docid2PersonEntityList=defaultdict(list);
    uniqueEntity = []
    fout=open(uniqueEntityPath,"w");
    for line in open(entityInfoPath):
        words=line.strip().split("\t");
        docid=words[0].strip()[:-4];
        entity = words[1].strip().lower();
        docid2PersonEntityList[docid].append(entity);
        if entity not in uniqueEntity:
            uniqueEntity.append(entity)
            fout.write(entity + "\n");
    fout.close();
    return docid2PersonEntityList;
	
def makePersonOnlyTFFile(entityInfoPath,tfpath,personOnlyTFfilePath):
    docid2PersonEntityList=getDocid2PersonEntityList(entityInfoPath);
    print docid2PersonEntityList;
    fout=open(personOnlyTFfilePath,"w");
    for line in open(tfpath):
        words=line.strip().split("\t");

        docid=words[0].strip()[:-4];
        outline=docid;
        hasEntity=0;
        for i in xrange(1,len(words),2):
            print words[i]
            if words[i].strip().lower() in docid2PersonEntityList[docid]:
                outline+="\t"+words[i].strip()+"\t"+words[i+1];
                hasEntity=1;
        if hasEntity==0:
            continue;
        fout.write(outline+"\n");	
    fout.close();
	
#main method
import Constants;
#parameters
dataDir = Constants.DATA_DIR;
#end

tfpath = Constants.TF_PATH;
entityInfoPath = Constants.ENTITY_INFO_PATH;
uniqueEntityPath = Constants.UNIQUE_ENTITY_PATH;
#output
personOnlyTFfilePath = Constants.PERSON_ONLY_TF_FILE_PATH;

docid2PersonEntityList=getDocid2PersonEntityList(entityInfoPath);
#makePersonOnlyTFFile(entityInfoPath,tfpath,personOnlyTFfilePath)
