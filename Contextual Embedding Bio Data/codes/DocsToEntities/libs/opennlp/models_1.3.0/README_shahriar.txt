http://sites.morganclaypool.com/wilcock/Home/chapter-3-using-statistical-nlp-tools

Below are the files mentioned in Chapter 3. The scripts for OpenNLP tools differ slightly from the book.

Installing OpenNLP Tools: Download OpenNLP Tools version 1.3.0 and unzip it, giving a directory opennlp-tools-1.3.0. In the scripts, OPENNLP_HOME must be set to location of this directory. Build the tools using Ant as described in the README file. This produces opennlp-tools-1.3.0.jar in a subdirectory opennlp-tools-1.3.0/output. The other jar files are in a subdirectory opennlp-tools-1.3.0/lib. 

Installing OpenNLP Models: The OpenNLP tools require statistical models for English. Create a subdirectory tree models/english in the opennlp-tools-1.3.0 directory. Download the models for version 1.3.0  into subdirectories in this tree, preserving the directory structure. For example, download the sentence detector model to models/english/sentdetect/EnglishSD.bin.gz, the tokenizer model to models/english/tokenize/EnglishTok.bin.gz, and so on.









http://uima.lti.cs.cmu.edu:8080/UCR/pages/static/osnlp/OpenNLPReadme.html


