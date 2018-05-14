import os;
import shutil;
import Constants;
#main method

#parameter settings 
dataDir= Constants.DATA_DIR;  
#end 




cwd="";
if dataDir[0]=='.':  #if relative path
	cwd=os.getcwd()+"/";

savecwd=os.getcwd();
os.chdir("./DocsToEntities/Runner_DocsToEntities");
#########--------------Ubuntu Command----------##########or/codes/02_generateTFandEntityFile.py', wdir='/home/rownak/UTEP/Research/Contexual Embeding/Coding/EntityVector/codes')

cmd="java -Xms2000m -cp ../libs/lingpipe-4.0.1.jar:../libs/opennlp-tools-1.3.0.jar:../libs/maxent-2.4.0.jar:../libs/trove.jar:../libs/jsoup-1.7.3.jar:../libs/LBJPOS.jar:../libs/LBJ2Library.jar:../libs/jwnl.jar:../libs/commons-logging-1.1.1.jar:TextModeler.jar edu.utep.cs.EntityGenerator.MemoryEfficientEntityExtractionFromAFolderOfDoc ../../../MelihaData/TextOnly";
#########--------------Windows Command----------##########
#cmd="java -Xms2000m -cp ../libs/lingpipe-4.0.1.jar;../libs/opennlp-tools-1.3.0.jar;../libs/maxent-2.4.0.jar;../libs/trove.jar;../libs/jsoup-1.7.3.jar;../libs/LBJPOS.jar;../libs/LBJ2Library.jar;../libs/jwnl.jar;../libs/commons-logging-1.1.1.jar;TextModeler.jar edu.utep.cs.EntityGenerator.MemoryEfficientEntityExtractionFromAFolderOfDoc ../../../sampleData/TextOnly";
os.system(cmd);

os.chdir(savecwd);
TextModelerOutputPath = Constants.TEXT_MODELER_OUTPUT_PATH;
if not os.path.isdir(TextModelerOutputPath):
	os.makedirs(TextModelerOutputPath);

shutil.copyfile("./DocsToEntities/Runner_DocsToEntities/tfFile.txt",TextModelerOutputPath+"/tfFile.txt");
shutil.copyfile("./DocsToEntities/Runner_DocsToEntities/entityInfo.txt",TextModelerOutputPath+"/entityInfo.txt");

