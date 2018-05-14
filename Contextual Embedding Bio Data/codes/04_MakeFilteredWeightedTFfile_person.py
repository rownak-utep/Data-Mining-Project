from subprocess import call
import os;
import time
def makeFilteredTFFile(TextModelerDir,TFFilePath,WeightedTFFilePath,Threshold,outFilteredTFFilePath):
	#generate outFilteredTFFile;

	cmd="java -Xms1g -cp "+TextModelerDir+"/TextModeler.jar -Xms2g edu.vt.cs.shahriar.Modeller.TFIDFFiltration "+TFFilePath+" "+WeightedTFFilePath+" "+outFilteredTFFilePath+" "+ str(Threshold);
	call(cmd,shell=True);	
	
	
def makeWeightedTermFileFromTFFile(TextModelerDir,TFFilePath,outputWeightedTFPath):

	cmd="java -Xms1000m -cp "+TextModelerDir+"/TextModeler.jar edu.vt.cs.shahriar.Modeller.Process ntc "+TFFilePath+" "+outputWeightedTFPath;
	call(cmd,shell=True);
	#os.remove("df_Log_Object_file");
#main method

import Constants;

#parameter setting 

startTime = time.time()
dataDir = Constants.DATA_DIR;
TextModelerDir = Constants.TEXT_MODELER_DIR;
#end 


#make person only weighted term file

personOnlyTFFilePath = Constants.PERSON_ONLY_TF_FILE_PATH;


outWeightedTFFilePath = Constants.OUT_WEIGHTED_TF_FILE_PATH;

makeWeightedTermFileFromTFFile(TextModelerDir,personOnlyTFFilePath,outWeightedTFFilePath);
endTime = time.time();
print(endTime - startTime);
'''
#make filtered Term file;
WeightedTFFilePath=outWeightedTFFilePath;
Threshold=0.00;
outFilteredTFFilePath=dataDir+"/personOnlyTF/personOnlyFilteredTFFile_0.00.txt";
makeFilteredTFFile(TextModelerDir,personOnlyTFFilePath,WeightedTFFilePath,Threshold,outFilteredTFFilePath);


#make person only filtered weighted term file
	#final output file
outPersonOnlyFilteredWeightedTFPath=dataDir+"/TextModelerOutput/personOnlyFilteredWeightedTFile.txt";
makeWeightedTermFileFromTFFile(TextModelerDir,outFilteredTFFilePath,outPersonOnlyFilteredWeightedTFPath);
'''







