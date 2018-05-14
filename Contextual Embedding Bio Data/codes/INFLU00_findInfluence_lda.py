import collections;
from collections import defaultdict;
from scipy.stats import entropy;
import numpy as np;
import math;
import json;
import sys;
import csv;
import ast;

def getDocID2Dist(docid2EventDistPath):
	docid2dist={}
	for line in open(docid2EventDistPath):
		words=line.strip().split("\t");
	
		docid=words[0];
		dist={}
		sum=0.0;
		for i in xrange(1,len(words),2):
			className=words[i];
			p=float(words[i+1]);
			sum+=p;
			dist[className]=p;
		for actor in dist:#convert to dist
			dist[actor]=dist[actor]/sum;
		docid2dist[docid]=dist;
	
	return docid2dist;

		

def distOf2Dist(dist1,dist2):
	p=dist1.values();
	q=dist2.values();
	d1=entropy(p,q);
	d2=entropy(q,p);
	return (d1+d2)/2;
def distanceOf2SparseDist(d1,d2):
	r=0;
	for entity in d1:
		if entity in d2:
			r+=d1[entity]*math.log(d1[entity]/d2[entity]);
		else:
			r+=d1[entity]*math.log(d1[entity]/1e-10);
	return r;
def distanceOf2SparseDistSymetric(d1,d2):
	return (distanceOf2SparseDist(d1,d2)+distanceOf2SparseDist(d2,d1))/2.0;
	
def findKN(targetDocID,docid2dist,K):
	
	tupleList=[];
	neighborDocIDList=[]
	for docid in docid2dist:
		if targetDocID not in docid2dist:
			return neighborDocIDList;
		if docid !=targetDocID:
			#d=distOf2Dist(docid2dist[docid],docid2dist[targetDocID]);
			d1=distanceOf2SparseDist(docid2dist[docid],docid2dist[targetDocID]);
			d2=distanceOf2SparseDist(docid2dist[targetDocID],docid2dist[docid]);
			d=(d1+d2)/2.0;
			#if (d<17.6):
			tupleList.append((d,docid));

	#print tupleList[:5];
	tupleList.sort(key=lambda x: x[0]);	
	#print tupleList[:5];	
	neighborDocIDList=[x[1] for x in  tupleList];
	return neighborDocIDList[:K];
	#return neighborDocIDList;
 

#==============================================================================
# def getDocID2KeywordListOld(entityInfoPath):
# 	docid2LocationList=defaultdict(list);
# 	for line in open(entityInfoPath):
# 		
# 		words=line.strip().split("\t");
# 		docid=words[0][:-4];
# 		if words[2]=="LOCATION":
# 			docid2LocationList[docid].append(words[1].lower());
# 	
# 	return docid2LocationList
#==============================================================================
def getDocid2TopicDist(docid2TopicPath):
	
	docid2topicDist=json.load(open(docid2TopicPath));
	'''
	i=0;
	for docid in docid2topicDist:
		

     
     docid,docid2topicDist[docid];
		i+=1;
		if i>10:
			break;
	'''		
	#docid=docid2topicDist.keys()[0];
	#print "mak",docid2topicDist[docid]
	return docid2topicDist;
def klForFixedLength(dist1,dist2):
	eps=1e-10;
	s=0;
	for i in xrange(len(dist1)):
		p=dist1[i];
		q=dist2[i];
		#print p,q;
		if q<eps:
			q=eps;
		if p<eps:
			p=eps;
		s+=p*math.log(p/q);
	return s;
def symmetric_klForFixedLength(dist1,dist2):
	d1=klForFixedLength(dist1,dist2);
	d2=klForFixedLength(dist2,dist1);
	return (d1+d2)/2.0;
#constrain 	
def TopicalDivergence(docid,docid2): #has threshold
	
	
	topicDist1=docid2topicDist[docid];
	topicDist2=docid2topicDist[docid2];
	
	
	#return np.argsort(topicDist1)[-1]==np.argsort(topicDist2)[-1]; # exactly same topic
	
	d=symmetric_klForFixedLength(topicDist1,topicDist2);
	return d;
	
def getCandidateCausalDocList(docid,docid2KeywordList, docid2dateKeyList):
    
    #print "docid :", docid
    
    dayTH = Constants.DAY_THRESHOLD; # for month multiply by 30;
    nCommonKeyword = Constants.COMMON_KEYWORD;
    
    TD=60; #Topical Divergence Threshold
    top=5;
    #all the neighbor docsid
      # not foun
    if(docid not in docid2dateKeyList): #We are using not in because we don't have the same trained data for text and date_keyword
        
        print "Not Found: ", docid
        return []
    #print "dateList", docid2dateKeyList[docid]
    docDate = str(docid2dateKeyList[docid]['date'])
    #print docDate

    docidDay=int(docDate[1:5])*12*30+int(docDate[5:7])*30+int(docDate[7:9]);
    docidMonth=int(docDate[1:7]);
    #docLocSet=set(docid2LocationList[docid]);
    docKeySet=set(docid2KeywordList[docid]); # for keyword 
    candidateList=[];
      
        # docid2dist: personOnlyTfFile where all the documents entities and weighted tf-idf is stored
        # So here in this for loop we are going through all of the documents date to see which doc are in the range of threshold with the 
        # 
    #redo
    TD5 = 5;
    TD10 = 10;
    TD15 = 15;
    TD20 = 20;
    TD25 = 25;
    
    for docidDist in docid2dist:
        #print "DocidDist :", docidDist
        if docidDist not in docid2dateKeyList:
            continue;
        distDate = str(docid2dateKeyList[docidDist]['date'])
        distDay=int(distDate[1:5])*12*30+int(distDate[5:7])*30+int(distDate[7:9]);
        distMonth=int(distDate[1:7]);
        
        #didLocSet=set(docid2LocationList[did]);
        distKeySet = set(docid2KeywordList[docidDist]);

        #redo
        if ( int(docDate[1:9])>int(distDate[1:9]) and docidDay-distDay<dayTH and len(distKeySet & docKeySet)>= nCommonKeyword): #and len(didLocSet & docLocSet)>=nCommonLocation):
        #if  int(docDate[1:9])>int(distDate[1:9]):
            div=TopicalDivergence(docid,docidDist);
        #redo
            if div<TD:
                #print "C: ",docid, "<>", docidDist, " len: ", len(distKeySet & docKeySet) , "set: ", distKeySet & docKeySet
                candidateList.append( (div,docidDist));
                candidateList.append( (div,docidDist));
                candidateList.append( (div,docidDist));
        sTupList=sorted(candidateList,key=lambda x: x[0])[:top];
    return [x[1] for x in sTupList];

def getCandidateCausalDocid4AllNeighbors(neighborDocIDList,docid2KeywordList, docid2dateKeyList):
	
	docid2CandidateList=collections.OrderedDict();
	allNei=neighborDocIDList;
	for docid in allNei:
		candidateList=getCandidateCausalDocList(docid,docid2KeywordList, docid2dateKeyList);
            # Here if any neighbor's candidate number is less then 2 then continue
		if len(candidateList)<2:
			#print "NN: ", docid, " Candidiate: ", candidateList
			continue;
		docid2CandidateList[docid]=candidateList;
		#print docid, len(candidateList),candidateList[0:5];
	
	return docid2CandidateList;

#To  find the common causal docs
def numberOfCommonDi(d0i,docid2CandidateList):
	
	count=0;
	for docid in docid2CandidateList:
		
		for canDocid in docid2CandidateList[docid]:
			if distanceOf2SparseDist(docid2dist[d0i],docid2dist[canDocid])<EPS:
				count+=1;
				break;
	return count;
	
def getCommonDki(d0i,docid2CandidateList):
	
	rlist=[]
	for docid in docid2CandidateList:
		tupList=[];
		for canDocid in docid2CandidateList[docid]:
			d=distanceOf2SparseDist(docid2dist[d0i],docid2dist[canDocid]);
			if d<EPS:
				tupList.append( (d,canDocid));
		
		tupList.sort(key=lambda x: x[0]);	
		
		DocIDList=[x[1] for x in  tupList];
		if len(DocIDList)>0:
			rlist.append(DocIDList[0]); # taking top
				
	return rlist;

def findCommonEventDoc(docid2CandidateList):
	
	D0CandidateList=docid2CandidateList[targetDocID];
	graph=defaultdict(int);
	
	print "id max"
	for d0i in D0CandidateList:
		ncom=numberOfCommonDi(d0i,docid2CandidateList);
		#print d0i,ncom;
		#if ncom==5 or ncom==3:
		if ncom>2:
			commondDocidList=getCommonDki(d0i,docid2CandidateList);
			showTitles(commondDocidList);
		graph[ncom]+=1;
	print graph;
def writeDocid2CandidateList2File(docid2CandidateList,targetDocID):
	fout=open("C:\Users\mkader\Desktop/kddData/NYData/data4OrangeBox/"+targetDocID+".txt","w");
	for docid in docid2CandidateList:
		line=docid;
		for d2id in docid2CandidateList[docid]:
			line+="\t"+d2id;
		fout.write(line+"\n");
			
def showTitles(docidList):
	docid2titlePath="C:\Users\mkader\Desktop/NYArchive/storyDiv/NYImageOnly2000-2015_docid2title.json";
	docid2title=json.load(open(docid2titlePath));
	print "---------------------------"
	for docid in docidList:
		print docid,docid2title[docid].encode('ascii','ignore');
	print "---------------------------"

def call(targetDocID):
    print "inside call :", targetDocID
    docid2CandidateList = []
    if targetDocID not in docid2dist:
        return docid2CandidateList;
    neighborDocIDList=findKN(targetDocID,docid2dist,K);
    #showTitles(neighborDocIDList);
    #print "\n Neighbor List: ", neighborDocIDList;
    allNeighbor=[targetDocID]+neighborDocIDList;
   # print "---------------------------"
   #redo
    docid2CandidateList=getCandidateCausalDocid4AllNeighbors(allNeighbor,docid2KeywordList, docid2dateKeyList);
    
    #print "docid2CandidateList: ", docid2CandidateList
    #print "Seed: ",targetDocID ,"Neighbor: ",allNeighbor, "Candidate: ", docid2CandidateList
    #print "DocIdCandidateList: ", docid2CandidateList
    return docid2CandidateList;
	#writeDocid2CandidateList2File(docid2CandidateList,targetDocID);

def getDatePMID(path):
    pmIdList = [];
    with open(path) as File:
        reader = csv.DictReader(File)
        for row in reader:
            pmid = row['PMID']
            date = row['Year']
            if int(date) >= 2014 and pmid not in pmIdList:
                pmIdList.append(pmid)
    print pmIdList
    return pmIdList;



def getDateKeyword(path):
    chemlist = [];
    keyword = [];
    dateKeywordList = {}
    docid2KeywordList=defaultdict(list);
    with open(path) as File:
        reader = csv.DictReader(File)
        for row in reader:
            dateKeywordDict = {}
            pmid = row['PMID']
            chemlist = ast.literal_eval(row['Chemical List'])
            keyword = ast.literal_eval(row['keywords'])
            date = row['Year'].zfill(2) + row['Month'].zfill(2) + row['Day'].zfill(2);
            dateKeywordDict['date'] = date
            #print "Error Line: ", row['PMID']
            for item in keyword:
                if item not in chemlist:
                    chemlist.append(item)
            #dateKeywordDict['keyword'] = chemlist
            docid2KeywordList[pmid] = chemlist
            dateKeywordList[pmid] = dateKeywordDict
            #results[row['PMID']]['Chemical List'].append(results[row['PMID']]['keywords']);
            #print "keyword: ", keyword
            #print "Chemlist: ", chemlist
        #print docid2KeywordList
    return dateKeywordList, docid2KeywordList
    
def getCommonKeyword(docid,docid2KeywordList):
	nCommonLocation = 2
	docLocSet=set(docid2KeywordList[docid]);
	for did in docid2dist:
		
		didLocSet=set(docid2KeywordList[did]);
		if (len(didLocSet & docLocSet)>=nCommonLocation):
			print did, " common: ", len(didLocSet & docLocSet)
def getTestTargetIDList():
    #getDatePMID(Constants.DATE_KEYWORD_FILE)
    return ['28617852'];
    #return getFileContainTerm(Constants.TEXT_ONLY_DIR, Constants.SEED_DOC_QUERY);   
	
    
#main method
import Constants;
from FileContainTerm import getFileContainTerm
K= Constants.KMEANS_K; # for findKN
EPS=17.6; # for naive orange box finder
dataDir = Constants.DATA_DIR;

#end param


docid2TopicPath = Constants.OUT_DOC_ID2_TOPIC;
docid2topicDist=getDocid2TopicDist(docid2TopicPath); #read json file of LDA output
print "getDocid2TopicDist"
docid2DistPath = Constants.OUT_WEIGHTED_TF_FILE_PATH;
print "EntityS"
entityInfoPath = Constants.ENTITY_INFO_PATH;
print "entityEnd"
docid2dist=getDocID2Dist(docid2DistPath);
print "getDocID2Dist"
docid2dateKeyList, docid2KeywordList = getDateKeyword(Constants.DATE_KEYWORD_FILE)

popKey = []
for key in docid2dist.keys():
    if (key not in docid2dateKeyList):
        popKey.append(key)
        popedItem = docid2dist.pop(key)
        
print "Poped key: ", popKey

seedDocId=getTestTargetIDList();

for docId in seedDocId:
    call(docId);


#print docid2dateKeyList
# =============================================================================
# docid2dist = {'A2016010205': {'love': 0.0566815972856374, 'angel': 0.008358839968471879, 'nat coles': 0.011336319457127481, 'marvin yancy': 0.011336319457127481, 'cbs': 0.008358839968471879, 'natalie cole story': 0.011336319457127481, 'stardust': 0.011336319457127481 }, 
#  'A2016010304': {'michael loman': 0.060219105063233885, 'squib': 0.030109552531616943, 'harlee santos': 0.030109552531616943, 'jennifer lawrence': 0.030109552531616943, 'nbc': 0.022201292083584234, 'ray': 0.060219105063233885, 'blue': 0.09032865286397318}}
# 
# =============================================================================
#-------I have changed here the docid2LocationList to docid2KeywordList
#docid2LocationList = getDocID2LocationList(entityInfoPath)


# =============================================================================
#  docid2LocationList = defaultdict(<type 'list'>, {'A2016010205': [u'robert yancy', u'aretha franklin', u'love', u'natalie', u'rolling stone', u'love brought me back', u'holly & ivy', u'cole', u'heritage', u'university'], 
#                                                 'A2016010201': [u'eileen myles', u'cherry jones', u'julie harris', u'smith', u'arc', u'frances sternhagen', u'gaby hoffmann', u'dublin', u'lee harvey oswalds', u'darling', u'iconic', u'stephen kings']}) 
#     
# =============================================================================

#targetDocID="u2006092504" #e coli
#targetDocID="u2006091600" # e coli 2
#targetDocID="u2006091500" # ecoli 3;
#targetDocID="u2015051609" # boston bombing
#targetDocID="w2010102306"; # cholera
#targetDocID="w2010071504"; # cholera 2

#targetDocID="u2013052308" #tsarnaev
#print docid2dist[targetDocID];
#print "Target doc Title"
#showTitles([targetDocID])

#call("28741686");

#getCommonKeyword("11121076", docid2KeywordList)

#testing
#print "test"
#print distanceOf2SparseDistSymetric(docid2dist["u2006091600"],docid2dist["u2009111306"])
