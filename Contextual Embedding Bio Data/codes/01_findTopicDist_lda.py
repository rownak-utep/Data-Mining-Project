from gensim import corpora
from gensim.models.ldamodel import LdaModel
import re;
import numpy as np
import glob;
import ntpath;
from nltk.corpus import stopwords
import time;
import sys;
from collections import defaultdict
import json;

def getPageID2TopicDist(docs,n_topics):
	"""
	:docs=[(docID,[word1,word2,..]),...]
	:param n_topics: Number of topics to generate from the data
	:return: [docid]=[0.9,0.1] # sequential topic probability
	"""
	# prepare the corpus in Gensim format
	texts = [doc[1] for doc in docs]

	
	dictionary = corpora.Dictionary(texts)
	
	
	corpus = [dictionary.doc2bow(text) for text in texts]
	#print corpus;
	# apply LDA on the corpus
	lda = LdaModel(corpus, id2word=dictionary, num_topics=n_topics,passes=4);

	# print top terms from each topic
	for i in range(lda.num_topics):
		topic = lda.print_topic(i, topn=8)
		print [tup[1] for tup in lda.show_topic(topicid=i,topn=8)]
		
	
	# get the topic distribution in each document
	pageID2TopicDist=dict();
	doc_topic = []
	for index, doc in enumerate(docs):
		
		doc_bow = dictionary.doc2bow(doc[1])
		topic_distri = lda[doc_bow]
		dlist=[0.0]*n_topics;
		for tup in topic_distri:
			dlist[tup[0]]=tup[1];
	
		#print topic_distri;
		#top_topic = sorted(topic_distri, key=lambda x: x[1], reverse=True)[0][0]
		#doc_topic.append(top_topic)
		
		pageid=doc[0];
		pageID2TopicDist[pageid]=dlist;

	# topic of each document
	#print doc_topic;
	return pageID2TopicDist;


def makeDocsForNaim(TextOnlyDir):
	StopWordsList = stopwords.words("english")+["he","said","said.","would","one","two","mr.","ms.","dr.","new","also","next","said,","skip","told"];
	nf=0;
	#print StopWordsList
	docs=[];
	docList=glob.glob(TextOnlyDir+"/*.txt");
	for docPath in docList:
		pageID=ntpath.basename(docPath).split(".")[0];
          
		print "page ID: ", pageID
		text=open(docPath).read().lower();
		text=''.join([i if ord(i) < 128 else "" for i in text]); # remove unicode
		#textS=' '.join([word for word in text.split() if word not in StopWordsList]);
		textS=[word for word in text.split() if word not in StopWordsList];
		#print textS;
		docs.append((pageID,textS));
		nf+=1;
		#if nf>100:#remove *****************************************************************
		#	break;
		sys.stdout.write("\b\b\b\b\b\b\b\b"+str(nf));
	print "";
	return docs;
	

	
#main method
#parameters settings
import Constants;

docs=makeDocsForNaim(Constants.TEXT_ONLY_DIR)
print "docs are ready for lda modeling"
pageID2Topic=getPageID2TopicDist(docs,Constants.N_TOPICS); #LDA 
json.dump(pageID2Topic,open(Constants.OUT_DOC_ID2_TOPIC,'w'));

