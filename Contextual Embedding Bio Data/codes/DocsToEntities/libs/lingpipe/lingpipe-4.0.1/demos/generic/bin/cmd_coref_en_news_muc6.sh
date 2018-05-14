CLASS=com.aliasi.demo.demos.CorefDemo
ARGS="com.aliasi.tokenizer.IndoEuropeanTokenizerFactory,com.aliasi.sentences.MedlineSentenceModel,/models/ne-en-news-muc6.AbstractCharLmRescoringChunker,Newswire English trained on the MUC 6 Corpus"

CMD=com.aliasi.demo.framework.DemoCommand

CP=../../:../lingpipe-demos.jar:../../../lingpipe-4.0.1.jar:../../lib/nekohtml-1.9.14.jar:../../lib/xercesImpl-2.9.1.jar:../../lib/xml-apis-2.9.1.jar
java -cp $CP $CMD -demoConstructor=$CLASS -demoConstructorArgs=$ARGS $1 $2 $3 $4 $5 $6 $7 $8 $9
