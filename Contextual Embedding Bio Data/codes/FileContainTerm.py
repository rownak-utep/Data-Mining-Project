#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import glob;
import ntpath;


import sys;

def getFileContainTerm(TextOnlyDir, query):
    nf=0;
    docName=[];
    docList=glob.glob(TextOnlyDir+"/*.txt");
    #print docList
    for docPath in docList:
        pageID=ntpath.basename(docPath)[:-4];
        text=open(docPath).read().lower();
        text=''.join([i if ord(i) < 128 else "" for i in text]); # remove unicode
        textS=[word for word in text.split() ];
        if query in textS: 
            docName.append(pageID);
            nf+=1;
		#if nf>100:#remove *****************************************************************
		#	break;
        sys.stdout.write("\b\b\b\b\b\b\b\b"+str(nf));
    print "";
    return docName;
	

	
#main method
#parameters settings


#docName=getFileContainTerm(TextOnlyDir, "warburg")
