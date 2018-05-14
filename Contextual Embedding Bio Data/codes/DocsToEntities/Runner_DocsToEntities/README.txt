Description: Generates entities and frequencies of terms from a directory of documents.

//change word net dict path in file_properties.xml

java -Xms1000m -cp ../libs/lingpipe-4.0.1.jar:../libs/opennlp-tools-1.3.0.jar:../libs/maxent-2.4.0.jar:../libs/trove.jar:../libs/jsoup-1.7.3.jar:../libs/LBJPOS.jar:../libs/LBJ2Library.jar:../libs/jwnl.jar:../libs/commons-logging-1.1.1.jar:TextModeler.jar edu.utep.cs.EntityGenerator.MemoryEfficientEntityExtractionFromAFolderOfDoc Documents

Input: A directory of text documents. In the command above, the input directory is stated by "Document" in the command line. 

Output Files
------------
entityVsDocs.txt : This file contains entities, entity type, the number of documents containing this entity, and the list of documents containing an entity.

entityinfo.txt : Lists entity type vs entity

tfFile.txt : Frequency of all detected entities and noun phases for each document. Each line contains the record for a document

	




M. Shahriar Hossain
CS@UTEP