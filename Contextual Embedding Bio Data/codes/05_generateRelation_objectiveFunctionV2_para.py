from scipy.optimize import minimize
import collections;
from collections import defaultdict;
import sys;
import math;
import json;
import random;
import numpy as np;
import scipy.stats;
from sklearn.decomposition import PCA
import os.path;
from multiprocessing import Pool
from FileContainTerm import getFileContainTerm

#1
def getSeedDocID(seedDocIdPath):
    seedDocID = [];
    count = 0;
    for line in open(seedDocIdPath):
        words=line.strip().split("\t");
        seedDocID.append(words[0]);
        count = count+1;
        sys.stdout.write("\b\b\b\b\b\b\b\b"+str(count));
    return seedDocID;

#2
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


#3
def readdocid2CandidateList(docid2CandidateListPath):
	docid2CandidateList=collections.OrderedDict();
	for line in open(docid2CandidateListPath):
		words=line.strip().split("\t");
		docid=words[0];
		if len(words[1:])<=1:
			continue;
		docid2CandidateList[docid]=words[1:];
	return docid2CandidateList;



#4
def diffAndNorm(x,y):
	#y["mak"]=0.5;
	s=0.0;
	for i in xrange(len(xLabel)):
		actor=xLabel[i];
		if actor not in y:
			s+=x[i]*x[i];
		else :
			s+=(x[i]-y[actor])*(x[i]-y[actor]);
	return math.sqrt(s);

#5
def distanceOf2SparseDist(d1,d2):
	eps=1e-7;
	r=0;
	for entity in d1:
		p=d1[entity]+eps;
		q=eps;
		if entity  in d2:
			q=d2[entity]+eps;
		try:
			r+=p*math.log(p/q);
		except:
			print " domain err ",p,q;
			sys.exit();
	return r;
#6
def convertToDistribution(x):
	s=sum(x);
	rx=[];
	for xi in x:
		rx.append(xi/s);
	return rx;
#7	
def symKL(x,y):
	rx=convertToDistribution(x);
	xDic=dict(zip(xLabel, rx));
	d1=distanceOf2SparseDist(xDic,y);
	d2=distanceOf2SparseDist(y,xDic);
	d=(d1+d2)/2.0;
	#print d;
	return d;
#8
def getVX(x):
	docid2vx=defaultdict(list);
	
	for docid in docid2CandidateList:
		if len(docid2CandidateList[docid])==0:
			continue;
		deno=0.0;
		for dij in docid2CandidateList[docid]:
			deno+=math.exp(-symKL(x,docid2dist[dij])) ;
			
		for dij in docid2CandidateList[docid]:
			docid2vx[docid].append(math.exp(-symKL(x,docid2dist[dij]))/deno);
	return docid2vx;
#9	
def getVX_PCA(x):
	#docid2vx=defaultdict(list);
	docid2vx=collections.OrderedDict();
	
	for docid in docid2CandidateList:
		if len(docid2CandidateList[docid])==0:
			continue;
		deno=0.0+1e-8;
		for dij in docid2CandidateList[docid]:
			deno+=math.exp(-np.linalg.norm(x-docid2xpca[dij])) ;
		vx=[];	
		for dij in docid2CandidateList[docid]:
			#try:
				vx.append(math.exp(-np.linalg.norm(x-docid2xpca[dij]))/deno);
			#except:
			#	print "mak Len: ",len(docid2CandidateList[docid]);
		docid2vx[docid]=vx;
	return docid2vx;	
#10
def uniform(n):
	return [1.0/n]*n;
#11	
def absDiffOfVector(x,y):# return another vector
	z=[];
	for i in xrange(len(x)):
		z.append(abs(x[i]-y[i]));
	return z;
#12	
def dotProduct(x,y):
	s=0.0;
	for i in xrange(len(x)):
		s+=x[i]*y[i];
	return s;
#13
#def 	
def profObjectFunction(xAndw):	
	#print "mak"
	n=len(xLabel);
	x=xAndw[:n];
	w=xAndw[n:];
	docid2vx=getVX(x);
	s=0.0;
	i=0;
	for docid in docid2vx:
		n=len(docid2vx[docid]);
		s+= w[i]*dotProduct(docid2vx[docid] , absDiffOfVector(uniform(n),docid2vx[docid]));
		i+=1;
	return -s;
#14
def profObjectFunction_pca(xAndw):	
	#print "mak"
	n=len(docid2xpca[docid2xpca.keys()[0]]);
	x=xAndw[:n];
	w=xAndw[n:];
	docid2vx=getVX_PCA(x);
	s=0.0;
	i=0;
	for docid in docid2vx:
		n=len(docid2vx[docid]);
		s+= w[i]*dotProduct(docid2vx[docid] , absDiffOfVector(uniform(n),docid2vx[docid]));
		i+=1;
	return -s;
 #15
#objective function v2
def getTFdata(TFFilePath):
	docid2entityList=defaultdict(list);
	docid2entity2fre={}

	for line in open(TFFilePath):
		words=line.strip().split("\t");
		docid=words[0];

		for i in xrange(1,len(words),2):
			words[i]=unicode(words[i], errors='ignore');
			docid2entityList[docid].append(words[i]);
			if i==1:
				docid2entity2fre[docid]=defaultdict(int);
			docid2entity2fre[docid][words[i]]=int(words[i+1]); #if the next word is not a int??
		#docid2entityList[docid]=docid2entityList[docid][:10];# remove *******
	return docid2entityList,docid2entity2fre;
 #16
def crispness(vxi):
	
	ni=len(vxi);
	#print ni;
	u=uniform(ni);
	diffV=absDiffOfVector(u,vxi);
	if ni==1:
		return 1;
	
	nu=np.linalg.norm(diffV,1);# L1 norm;
	
	return nu/(2-2.0/ni);
precomputeRelations={}

#17
def getRelationSet(di,aij):
	# return list of aij~di
	if (di,aij)  in precomputeRelations:
		return precomputeRelations[(di,aij)];
	rs=[]; # list of entity pair;
#==============================================================================
# 	print "\ndi: ", di, " aij: ", aij
# 	print "\n\ndocid2entityList[aij]: \n", docid2entityList[aij]
# 	print "\n\ndocid2entityList[di]: \n", docid2entityList[di]
#==============================================================================

	fileEntityToDoc = open(Constants.WORD2VECTOR_PATH + "/fileEntityToDoc.txt", "a");
    
	for e1 in docid2entityList[aij]:
		for e2 in docid2entityList[di]:
			#if e1!=e2: #dont allow same entity to be in the relation
				rs.append( (e1,e2));

				if aij not in entityToDoc[e1]:
				    entityToDoc[e1].append(aij);
				    fileEntityToDoc.write("%s\t%s\t%s\n" %(e1, aij, di))

				if di not in entityToDoc[e2]:
				    entityToDoc[e2].append(di);
				    fileEntityToDoc.write("%s\t%s\t%s\n" %(e2, di, aij))
				    
#==============================================================================
# 				print "\nentity1 : " , e1 , " doc: ", aij
# 				print "\nentity2 : " , e2 , " doc: ", di
#==============================================================================
	#print len(rs)," r";
	precomputeRelations[(di,aij)]=rs;
	fileEntityToDoc.close();
                     
	return rs;
 #18
def uniques(l, f = lambda x: x):
    return [x for i, x in enumerate(l) if f(x) not in [f(y) for y in l[:i]]]

precomputePi_den={};
#19	
def prGivenRij(r,aij,di,Rij):
	r1=r[0];
	r2=r[1];
	nu=docid2entity2fre[aij][r1]*docid2entity2fre[di][r2]+1.0;
	if (aij,di) in precomputePi_den:
		return nu/precomputePi_den[(aij,di)];
	de=0.0;
	for rprime in Rij:
		de+=docid2entity2fre[aij][rprime[0]]*docid2entity2fre[di][rprime[1]]+1;
	precomputePi_den[(aij,di)]=de;	
	return nu/de;
	
precomputePij_den={};	
#20
def prGivenRijRlk(r,aij,di,alk,dl,Runion):
	r1=r[0];
	r2=r[1];
	nu=min(docid2entity2fre[aij][r1]*docid2entity2fre[di][r2],docid2entity2fre[alk][r1]*docid2entity2fre[dl][r2])+1.0;
	if (aij,di,alk,dl) in precomputePij_den:
		return nu/precomputePij_den[(aij,di,alk,dl)];
	de=0.0;
	for rprime in Runion:
		de+=max(docid2entity2fre[aij][rprime[0]]*docid2entity2fre[di][rprime[1]],docid2entity2fre[alk][rprime[0]]*docid2entity2fre[dl][rprime[1]])+1;
	precomputePij_den[(aij,di,alk,dl)]=de;
	return nu/de;

precomputedNRS={};	
#21
def NRS(di,aij,diplus1,alk):
	if (di,aij,diplus1,alk) in precomputedNRS:
		return precomputedNRS[(di,aij,diplus1,alk)];
	Rij=getRelationSet(di,aij);
	Rlk=getRelationSet(diplus1,alk);



	Runion=uniques(Rij+Rlk);
	#print len(Rij),"runi";
	nrs=0.0;
	for r in Runion:
		pij=prGivenRijRlk(r,aij,di,diplus1,alk,Runion);
		pi=prGivenRij(r,aij,di,Rij)
		pj=prGivenRij(r,alk,diplus1,Rlk);
		#print "pij",pij," pi",pi,"pj ",pj ;
		nrs+=pij*math.log(pij/(pi*pj));
	
	precomputedNRS[(di,aij,diplus1,alk)]=nrs;	
	return nrs;
#22
def forBoxPair(i,docid2vx):
	docidList=docid2vx.keys();
	di=docidList[i];
	diplus1=docidList[i+1];
	ni=len(docid2vx[di]);
	niplus1=len(docid2vx[diplus1]);
	
	candidateDocidList4di=docid2CandidateList[di];
	candidateDocidList4diplus1=docid2CandidateList[diplus1];
	r=0.0;
	for j in xrange(ni):
		aij=candidateDocidList4di[j];
		vxaij=docid2vx[di][j];
		for k in xrange(niplus1):
			alk=candidateDocidList4diplus1[k];
			vxalk=docid2vx[diplus1][k];
			nrs=NRS(di,aij,diplus1,alk);
			r+=vxaij*vxalk*nrs;
			#print nrs;
	
	return r;
#23
def objectiveFunctionV2(xAndw):
	n=len(docid2xpca[docid2xpca.keys()[0]]);
	x=xAndw[:n];
	w=xAndw[n:];
	docid2vx=getVX_PCA(x);
	s=0.0;
	docidList=docid2vx.keys();
	K=len(docid2vx);

	for i in xrange(K-1): 
		di=docidList[i];
		diplus1=docidList[i+1];
		ni=len(docid2vx[di]);
		
		lastPart=forBoxPair(i,docid2vx);
		#lastPart=1;
		s+=crispness(docid2vx[di])*crispness(docid2vx[diplus1])*w[i]*w[i+1]*lastPart;
		
	#print -s;	
	return -s;
#end of objective function v2	
#24
def getXLabel(docid2CandidateList,docid2dist):
	d=defaultdict(int);
	label=[]
	for docid in docid2CandidateList:
		for dij in docid2CandidateList[docid]:
			for k in docid2dist[dij]:
				d[k]+=1;
	
	for k in d:
		if d[k]>3:# to reduce size of x; 3 is used
			label.append(k);
	return label;
#25
def write2File(resx,xLabel,filename):
	fout=open(filename,"w");
	for i in xrange(len(xLabel)):
		fout.write(xLabel[i]+"\t"+str(resx[i])+"\n");
	fout.close();
#26	
def findTheClosestInABox(x,docidList,docid2dist):
	docid=None;
	md=1e+12;
	for dij in docidList:
		#d=diffAndNorm(x,docid2dist[dij]);
		d=symKL(x,docid2dist[dij]);
		if md>d:
			md=d;
			docid=dij;
	return docid;
#27		
def findClosestDocFromEachBox(x,docid2CandidateList,docid2dist):
	orangeBox={};
	for docid in docid2CandidateList:
		#docid is the nn
		orangeBox[docid]=findTheClosestInABox(x,docid2CandidateList[docid],docid2dist);
	return orangeBox;
#28
def findTheClosestInABox_PCA(x,docidList,docid2xpca):
	docid=None;
	md=1e+12;
	for dij in docidList:
		#d=diffAndNorm(x,docid2dist[dij]);
		
		d=np.linalg.norm(x-docid2xpca[dij]);
			
		if md>d:
			md=d;
			docid=dij;
	return docid;
#29		
def findClosestDocFromEachBox_PCA(x,docid2CandidateList,docid2xpca):
	orangeBox=collections.OrderedDict();
	#print "orange MAKE: ", docid2CandidateList
	for docid in docid2CandidateList:
		#docid is the nn
		orangeBox[docid]=findTheClosestInABox_PCA(x,docid2CandidateList[docid],docid2xpca);
		#print "docid ", docid, " orange; ", orangeBox[docid]
	#print "orangeBox : \n", orangeBox;
	return orangeBox;
#30
def showTitles(docidList):
	
	print "---------------------------"
	for docid in docidList:
		print docid,docid2title[docid].encode('ascii','ignore');
	print "---------------------------"	
#31
def getRandomList(n):
	bounds=[];
	xx=[];
	for i in xrange(n):
		xx.append(random.random());
		bounds.append((0,1));
	return xx,tuple(bounds);
#32
def getRandomList_PCA(n):
	bounds=[];
	xx=[];
	for i in xrange(n):
		xx.append(random.random());
		if i<NCOM:
			bounds.append((None,None));
		else:
			bounds.append((0,1));
	return xx,tuple(bounds);
#33
def getTopNRelations(di,aij,n):
	Rij=getRelationSet(di,aij);
	LST=[];
	for r in Rij:
		pi=prGivenRij(r,aij,di,Rij);
		LST.append((pi,r));
	sList=sorted(LST, key=lambda x: x[0],reverse=True);
	return sList[:n];
#34
def getTopCommonRelations(aij,di,alk,dl,n, pijList):
    
#==============================================================================
#     aij = previous doc orange val candidate
#     di = previous doc orange key neighbor/seed
#     alk = current val candidate
#     dl = current key neighbor/seed
#==============================================================================
    
	Rij=getRelationSet(di,aij);
# aij, di == [(u'autism spectrum disorder', u'pdac'), (u'autism spectrum disorder', u'pkm1') 
	Rlk=getRelationSet(dl,alk);
# alk, dl = [(u'autism spectrum disorder', u'enzyme assay'), (u'autism spectrum disorder',

#==============================================================================
# 	print "\n\naij: ", aij , "\t di: ", di
# 	print "\nRij: ", Rij
# 	print "\n\naij: ", alk , "\t di: ", dl
# 	print "\n\nRlk: ", Rlk
#==============================================================================
 
	Runion=uniques(Rij+Rlk);
 	#print "\n\nRunion", Runion ;
	pij=0;
	LST=[];
	for r in Runion:
		pij=prGivenRijRlk(r,aij,di,dl,alk,Runion);
		#print "pij: ", pij, "r :", r;
		
            
		LST.append((pij,r));

	pijList.append(pij);

	sList =sorted(LST, key=lambda x: x[0],reverse=True);
	#print sList;

	#return [x[1] for x in sList[:n] ];
	return  sList[:n], pijList; # including probability (0.56,(e1,e2))
#35
def getPValueForRelations(relations):
	docidList=docid2dist.keys();
	n=len(docidList);
	sampleSize=50000;
	relationsWithPvalue=[];
	for rel in relations:
		c=0.0;
		for i in xrange(sampleSize):
			docid1=docidList[random.randint(0,n-1)];
			docid2=docidList[random.randint(0,n-1)];
			#getRelationSet(di,aij)# return aij~di
			#print rel[0]," ~ ",rel[1];
			if rel[0] in docid2entityList[docid1] and rel[1] in docid2entityList[docid2]:
				c+=1.0;
				#print rel,docid1,docid2;
		relationsWithPvalue.append((rel[0],rel[1],c/sampleSize));
	return relationsWithPvalue;
#36
def writeRelations(targetDocID,relations):
	outfile=open(relationDir+"/"+targetDocID+".json","w");
	

	json.dump(relations,outfile);
#37
def writeEntityToDoc(entityToDoc):
	outfile=open(Constants.ENTITY_TO_DOC,"w");
	json.dump(entityToDoc,outfile);
#38	
def printOrangeBoxForPresentation(orangeBox,w,targetDocID):
	table="<tr><td>wi</td><td>di (NN row)</td><td>aij (orange article)</td><td>Top10ProbableRelations(aij ~ di)</td></tr>";
	#print "\nTarget Doc ID: ", targetDocID;
     
	docidList=orangeBox.keys();
        #['2018010500010', '2018011500012', '2018012600003']
        
	#print "NN || doc in orangeBox "
	#print "\nDoc in OrangeBox: " , docidList;
     # Orange Box: ([('2018010500010', '2018010100069'), ('2018011500012', '2018010100072'), ('2018012600003', '2018011500012')])
     # docidList = ['2018010500010', '2018011500012', '2018012600003']
	combinedRelations=[];
	pijList = [];

	for i in xrange(len(docidList)):
        
		di=docidList[i];
		aij=orangeBox[di];
		#topRelations=getTopNRelations(di,aij,10);
		topRelations=[];
		relationsWithPvalue=[];
		if (i>0):
			topRelations, pijList = getTopCommonRelations(orangeBox[docidList[i-1]],docidList[i-1],aij,di,100, pijList);
      
       
			#relationsWithPvalue=getPValueForRelations(topRelations);
		combinedRelations.extend(topRelations);
		#print "Top Relations: ", (topRelations);
            
		#print "%.2f"%w[i],di,docid2title[di]," || ",aij,docid2title[aij];
		#table+="<tr style=\"outline: thin solid\"><td>"+"%.2f"%w[i]+"</td><td>"+docid2title[di]+"</td><td>"+docid2title[aij]+"</td><td>"+str(["%s ~ %s:%f"%x for x in relationsWithPvalue]).strip("[]")+"</td></tr>";
		table="";# remove**
  
	sPijList =sorted(pijList, key=lambda x: x,reverse=True);
	#print "list: ",sPijList;
 	#mid = sPijList[len(sPijList)/2]
	mid = 0.0;
 	#print "Mid: ", mid;
 	filteredCombineRelations = []; 

 	#print "Relations: ", combinedRelations
	for topRelations in combinedRelations:

		#print "Top Relation: ", topRelations

		if topRelations[0]>= mid:    
			#print "Top Rel: ", topRelations[0]
			filteredCombineRelations.append(topRelations)

	#print filteredCombineRelations;
#==============================================================================
#  	print "Comb: ";
#  	print combinedRelations;
#==============================================================================



	table="<table>"+table+"</table>";
	#html="<html><body><h2>Given Article: "+docid2title[targetDocID]+"</h2>"+table+"</body></html>";
	#open("C:\Users\mkader\Desktop/kddData/NYData/experimentsData/sampleResultInHTML/1000Articles/"+targetDocID+".html","w").write(html);
 
	
	writeRelations(targetDocID,filteredCombineRelations);
	#entityToDocList=json.load(open(relationDir+"/entityToDoc.json"));
	#print "entityToDoc: ", entityToDocList

#39
def getdocid2title(docid2titlePath):
	docid2title=json.load(open(docid2titlePath));	
	for docid in docid2title:
		docid2title[docid]=docid2title[docid].encode('ascii','ignore');
	return docid2title;


	
def getXandW(targetDocID):
	

	
	xLabel=getXLabel(docid2CandidateList,docid2dist);
	
	#print "Source Title:"
	#showTitles([targetDocID]);
	xAndW0,bnds=getRandomList(len(xLabel)+len(docid2CandidateList));
	#write2File(x0,xLabel,"x0.txt")
	#res = minimize(profObjectFunction, xAndW0, method='Nelder-Mead',options={'disp': True,'maxiter':100,'xtol':0.005});
	res = minimize(profObjectFunction, xAndW0, method='TNC',jac=False,bounds=bnds,options={'disp': True,'maxiter':25,'eps':0.0005});
	#print res.x;
	n=len(xLabel);
	xAndW=list(res.x);
	x=xAndW[:n];
	w=convertToDistribution(xAndW[n:]);


	xdist=convertToDistribution(x);
	orangeBox=findClosestDocFromEachBox(xdist,docid2CandidateList,docid2dist);
	#showTitles(orangeBox.values());
	printOrangeBoxForPresentation(orangeBox,w,targetDocID);
	return xdist, w;
def getActor2IDXMapping(docid2CandidateList):
	actor2idx={}
	idx=0;
	#print "Docid2", docid2dist
 
	for docid in docid2CandidateList:
		for candidateDocid in docid2CandidateList[docid]:
		
      
			#print "candidateDocid", candidateDocid
      
			for actor in docid2dist[candidateDocid]:
				if actor not in actor2idx:
					actor2idx[actor]=idx;
					idx+=1;	
      
			#print  candidateDocid, " Complete"
                 
	return actor2idx;
	
def getDocid2PCA(docid2CandidateList):
	actor2idx=getActor2IDXMapping(docid2CandidateList);
	
	docid2x=collections.OrderedDict();
	for docid in docid2CandidateList:
		for candidateDocid in docid2CandidateList[docid]:
			if candidateDocid in docid2x:
				continue;
			x=[0]*len(actor2idx);	
			for actor in docid2dist[candidateDocid]:
				idx=actor2idx[actor];
				x[idx]=docid2dist[candidateDocid][actor];
			docid2x[candidateDocid]=x;
	X=[];
	for docid in docid2x:
		X.append(docid2x[docid]);
	
	pca=PCA(n_components=NCOM);
	#pca.fit(X);
	xpca=pca.fit_transform(X);
	
	i=0;
	docid2xpca={};
	for docid in docid2x:
		docid2xpca[docid]=xpca[i,:];
		#print "pca:   ",type(docid2xpca[docid]),len(docid2xpca[docid]);
		i+=1;
	return 	docid2xpca;
def getXandW_PCA(targetDocID):
	
	
	global docid2xpca;
	docid2xpca=getDocid2PCA(docid2CandidateList);
	NCOM=len(docid2xpca[docid2xpca.keys()[0]]);
	print NCOM;
	
	
	#print "Source Title:"
	#showTitles([targetDocID]);
 
	xAndW0,bnds=getRandomList_PCA(NCOM+len(docid2CandidateList));
	#write2File(x0,xLabel,"x0.txt")
	#res = minimize(profObjectFunction_pca, xAndW0, method='TNC',jac=False,bounds=bnds,options={'disp': True,'maxiter':100,'eps':1e-06});
	res = minimize(objectiveFunctionV2, xAndW0, method='TNC',jac=False,bounds=bnds,options={'disp': True,'maxiter':100,'eps':1e-06});
	#print res.x;
	n=NCOM;
	xAndW=list(res.x);
	x=xAndW[:n];
	w=convertToDistribution(xAndW[n:]);


	xdist=convertToDistribution(x);
	orangeBox=findClosestDocFromEachBox_PCA(xdist,docid2CandidateList,docid2xpca);
	print "orange len: ", len(orangeBox);
	if len(orangeBox)<=0:
		return;
     
	#showTitles(orangeBox.values());
	printOrangeBoxForPresentation(orangeBox,w,targetDocID);
	return xdist, w;
	

def getTargetID2WandX(targetIDList):
	targetID2W={};
	targetID2X={};
	for docid in targetIDList:
		x,w=getXandW(docid);	
		targetID2W[docid]=w;
		targetID2X[docid]=x;
	return targetID2W,targetID2X;
def getDocid2kurt4VX(targetID2X):
	docid2kurt={};
	for docid in targetID2X:
		docid2vx=getVX(targetID2X[docid]);
		tot_kurt=0.0;
		for did in docid2vx:
			tot_kurt+=scipy.stats.kurtosis(docid2vx[did],fisher=False);
		avg_kurt=tot_kurt/len(docid2vx);
		docid2kurt[docid]=avg_kurt;
	return docid2kurt;

def printdocid2kurt(docid2kurt):
	print "---\ndocid\tavg_kurt";
	for docid in docid2kurt:
		print docid, docid2kurt[docid];
	print "end docid2kurt for vx"
def experiment():
	#scipy.stats.kurtosis
	
	targetIDList=getTestTargetIDList();
	targetID2W,targetID2X=getTargetID2WandX(targetIDList);
	
	docid2kurt=getDocid2kurt4VX(targetID2X);
	printdocid2kurt(docid2kurt);
	tot_ku=0.0;
	for docid in targetID2W:
		t=scipy.stats.kurtosis(targetID2W[docid],fisher=False);
		tot_ku+=t;
		#print docid,t;
	
	print "avg kurt for W: ", tot_ku/len(targetIDList);


def forEachStartingDoc(docid):
	path=relationDir+"/"+docid+".json";
#==============================================================================
# 	if os.path.isfile(path):
#  		return;
#==============================================================================
	global docid2CandidateList;	
	docid2CandidateList=INFLU00_findInfluence_lda.call(docid);	
	#print "docid2CandidateList", docid2CandidateList
    
#==============================================================================
#     docid : 2018010500010
#     DocIdCandidateList:  OrderedDict([
#     ('2018010500010', ['2018010100073', '2018010100064', '2018010400005', '2018010100078', '2018010100069']), 
#     ('2018011500012', ['2018010500012', '2018011000007', '2018010100066', '2018010100072', '2018010100074']), 
#     ('2018012600003', ['2018010400005', '2018010500010', '2018011800005', '2018011500012', '2018011100008'])])
#==============================================================================

#     DocIdCandidateList:  OrderedDict([
#     ('2018010500010', []) in this case
	if docid not in docid2CandidateList or len(docid2CandidateList[docid])<2 :
		print docid,"does not have sufficient documents in box0"
		return;
    
	elif len(docid2CandidateList.keys())<2:
		print docid," No Neighbour with candidate-----"
		return;
	print docid,"have sufficient documents in box0====", len(docid2CandidateList[docid])
    
	print docid,"have sufficient documents :", (docid2CandidateList[docid])
 
	x,w=getXandW_PCA(docid);
		
def relationsForAllDocuments():
    #print "seedDoc:", seedDocId 
    
    p = Pool(10);
    p.map(forEachStartingDoc, seedDocId); #it is a thread that run the function "forEachStartingDoc" with parameter "docid2dist.keys()"

#	#print "seedDoc:", seedDocId
#==============================================================================
#     for docid in seedDocId:	
#         forEachStartingDoc(docid);
#==============================================================================

#for experiments
def getTestTargetIDList():
     
    #return ['28617852'];
    return getFileContainTerm(TextOnlyDir, Constants.SEED_DOC_QUERY);   
	
		

#main method
#parameters
import time;
import Constants;

startTime = time.time();    
dataDir = Constants.DATA_DIR;
#

import INFLU00_findInfluence_lda;

#targetDocID="u2006092504" #e coli
#targetDocID="w2010102306"; #cholera
#targetDocID="w2010071504" #cholera 2
#targetDocID="u2013052308" #tsarnaev
print "tf file read"
TFFilePath = Constants.PERSON_ONLY_TF_FILE_PATH;
docid2DistPath = Constants.OUT_WEIGHTED_TF_FILE_PATH;
TextOnlyDir = Constants.TEXT_ONLY_DIR;

#docid2titlePath="C:\Users\mkader\Desktop/NYArchive/storyDiv/NYImageOnly2000-2015_docid2title.json";

docid2entityList,docid2entity2fre=getTFdata(Constants.PERSON_ONLY_TF_FILE_PATH);
#print docid2entityList
#==============================================================================
# print "\n\ndocid2entityList: \n"
# print docid2entityList
# print "\n\ndocid2entity2fre: \n"
# print docid2entity2fre
#==============================================================================

 
# =============================================================================
#  docid2entityList = defaultdict(<type 'list'>, {'A2016010205': [u'robert yancy', u'aretha franklin', u'love', u'natalie', u'rolling stone', u'love brought me back', u'holly & ivy', u'cole', u'heritage', u'university'], 
#                                                 'A2016010201': [u'eileen myles', u'cherry jones', u'julie harris', u'smith', u'arc', u'frances sternhagen', u'gaby hoffmann', u'dublin', u'lee harvey oswalds', u'darling', u'iconic', u'stephen kings']}) 
#     
# =============================================================================
 
# =============================================================================
#  docid2entity2fre =  {'A2016010205': defaultdict(<type 'int'>, {u'van halen': 1, u'love': 5, u'angel': 1, u'hepatitis c': 1, u'nat coles': 1, u'this will be': 2}),
#                       'A2016010201': defaultdict(<type 'int'>, {u'kelly': 1, u'scott': 1, u'stewart': 1, u'bradley cooper': 1, u'mary steenburgen': 1})}
# 
# 
# =============================================================================


#print "mak ",len(docid2entity2fre)
#print docid2entity2fre["n199305190039"];
#sys.exit();
NCOM=10;
#==============================================================================
# docid2titlePath = Constants.TEXT_ONLY_DIR;
# docid2title=getdocid2title(docid2titlePath)	; #docid to title map file
#==============================================================================

entityToDoc = defaultdict(list)
docid2dist=getDocID2Dist(docid2DistPath);
#seedDocId=getSeedDocID(seedDocIdPath);
seedDocId=getTestTargetIDList();

#==============================================================================
# 
# print "\n\docid2dist: \n"
# print docid2dist
#==============================================================================

# =============================================================================
# docid2dist = {'A2016010205': {' ve': 0.0566815972856374, 'angel': 0.008358839968471879, 'nat coles': 0.011336319457127481, 'marvin yancy': 0.011336319457127481, 'cbs': 0.008358839968471879, 'natalie cole story': 0.011336319457127481, 'stardust': 0.011336319457127481 }, 
#  'A2016010304': {'michael loman': 0.060219105063233885, 'squib': 0.030109552531616943, 'harlee santos': 0.030109552531616943, 'jennifer lawrence': 0.030109552531616943, 'nbc': 0.022201292083584234, 'ray': 0.060219105063233885, 'blue': 0.09032865286397318}}
# 
# =============================================================================


#experiment();

#find good sample
#tId="u2006092504" #e coli
#tId="w2010102306"; #cholera
#tId="u2014050404" #iphone
#tId="u2013060902" #data 
#tId="w2014082509" # bengazhi
#tId="w2009050500"; # trump
#tId="u2015031408" #tsarnaev;
#tId="w2015031106";
relationDir = Constants.RELATION_DIR;

  
if __name__ == '__main__':
    if os.path.isdir(relationDir)==False:
        os.makedirs(relationDir);
    relationsForAllDocuments();


#writeEntityToDoc(entityToDoc);
endTime = time.time();
print "Time in minitue: ", (endTime - startTime)/60.0;
'''
print "Source Title:"
showTitles([tId]);
docid2CandidateList=INFLU00_findInfluence_lda.call(tId);
if len(docid2CandidateList[tId])<2:
	print "It does not have sufficient documents in box0"
x,w=getXandW_PCA(tId);

'''