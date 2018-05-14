package extract_bio_entity;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;

import bean.DocSetBean;
import bean.TfAllDocBean;
import bean.EntityTfDfDocBean;

import com.aliasi.chunk.Chunk;
import com.aliasi.chunk.Chunker;
import com.aliasi.chunk.Chunking;
import com.aliasi.tokenizer.RegExTokenizerFactory;
import com.aliasi.tokenizer.TokenNGramTokenizerFactory;
import com.aliasi.tokenizer.Tokenizer;
import com.aliasi.tokenizer.TokenizerFactory;
import com.aliasi.util.AbstractExternalizable;

import constants.Constants;

public class ExtractBioEntity {
	
	
	
	public static Map<String, Integer> tf = new HashMap<>();
	public static Map<String, Integer> df = new HashMap<>();
	public static ArrayList<TfAllDocBean> tfAllFiles = new ArrayList<TfAllDocBean>();
	public static ArrayList<EntityTfDfDocBean> tf_DfDocBeans = new ArrayList<EntityTfDfDocBean>();
	public static Map<String, String> entityMap = new HashMap<>();
	public static Map<String, Map<String, String>> entityAllFiles = new HashMap<>();
	public static Chunker chunker;
	
	
	public static BufferedWriter tfWriter;
	public static BufferedWriter tf_idfWriter;
	
	static int numOfDoc = 0;
	
	void getTf_Idf() throws IOException{
		double sqrtTfIdf = 0.0;
		
		System.out.println("File Writing Start");
		BufferedWriter filterWriter = new BufferedWriter(new FileWriter(Constants.OUTPUT_PATH+"filterWriter.txt"));
		
		for(int i=0; i<tfAllFiles.size(); i++) {
			double sumOfTfIdfSqr = 0.0;
			Map<String,Double> tfIdfList = new HashMap<String, Double>();
			// Finding the summation of tfIdf of All terms in this doc
			// This program is for normalized TF-IDF
			/*for(String term: tfAllFiles.get(i).getTf().keySet()) {
				
				double idf =   Math.log(numOfDoc/df.get(term));
				double tf = 1 + Math.log(tfAllFiles.get(i).getTf().get(term));
				double tf_idf = tf * idf;
				tfIdfList.put(term,new Double(tf_idf));
				sumOfTfIdfSqr += Math.pow(tf_idf, 2);
				//System.out.println("\n\nTerm: " + term + "\ntf: " + tf + "\ndf: " + df.get(term) + "\nidf: " + idf + "\nsumOfTfIdf: " + sumOfTfIdfSqr);
			}
			sqrtTfIdf = Math.sqrt(sumOfTfIdfSqr);
			*/
			// For getting the information of number of entity before and after filtering using TF_IDF_THRESH
			filterWriter.write("\n "+tfAllFiles.get(i).getFileName()+" Total Entity: " + tfAllFiles.get(i).getTf().size());
			int countEntity=0;
			
			for(String term: tfAllFiles.get(i).getTf().keySet()) {
				
				double idf =   Math.log(numOfDoc/df.get(term));
				/* Changed the tf_idf to tf_df : experiment*/
				//double idf =   df.get(term)/(double)numOfDoc;
				double tf = 1 + Math.log(tfAllFiles.get(i).getTf().get(term));
				double tf_idf = tf * idf;
				
				
				
				//double weightedTfIdf = tfIdfList.get(term)/sqrtTfIdf;
				//System.out.println("\n\nTerm: " + term + "\nWeighted tf idf: " + weightedTfIdf);
				//double tf_idf = (tfAllFiles.get(i).getTf().get(term) * (double)df.get(term))/numOfDoc;
				
				//double tf_idf = tfAllFiles.get(fileName).get(term) * df.get(term);
				if(tf_idf>= Constants.TF_IDF_THRESH) {
					String fileName1 = tfAllFiles.get(i).getFileName();
					String type = entityAllFiles.get(fileName1).get(term);
					
					
					//System.out.println(fileName + "\t" + term );
					tf_DfDocBeans.add(new EntityTfDfDocBean(fileName1, term, tf_idf,type));
					countEntity++;
				}
				
			}
						
			filterWriter.write("\nEnitity after Filtering: " +countEntity);
		}
		System.out.println("File Writing Finish");
		
		tfWriter.close();
		
		filterWriter.close();
	}
	
	void getTfDfEntity(String fileName, String docText) throws IOException{
		
		Chunking chunking = chunker.chunk(docText);
		// System.out.println("Chunking=" + chunking);
		
		Set<Chunk> chunkSet = chunking.chunkSet();
		Iterator<Chunk> it = chunkSet.iterator();
		boolean termInDocFound = false;
		while (it.hasNext()) {
			Chunk chunk = it.next();
			int start = chunk.start();
			int end = chunk.end();
			
			String text = docText.substring(start, end).toLowerCase();
			
			if(text.split("\\s+").length>2) {
				TokenizerFactory tokenf
			    = new RegExTokenizerFactory("\\S+");
				TokenizerFactory ntf = new TokenNGramTokenizerFactory(tokenf,2, 3);
				
				Tokenizer y = ntf.tokenizer(text.toCharArray() , 0, text.length());
				String[] tokens = y.tokenize();
				for(String token: tokens) {
					
					//System.out.println("\nToken: " +token);
					if (tf.containsKey(token)) {
						tf.put(token, tf.get(token) + 1);
						
					} else {
						tf.put(token, 1);
						entityMap.put(token, chunk.type());
						String output = fileName + "\t" + token + "\t" + chunk.type();
					}
				}
			}
			else {
				if (tf.containsKey(text)) {
					tf.put(text, tf.get(text) + 1);
					
				} else {
					tf.put(text, 1);
					entityMap.put(text, chunk.type());
					String output = fileName + "\t" + text + "\t" + chunk.type();
					//System.out.println(output);
					
				}
			}
			

		}
		
		
		if(tf.keySet().isEmpty()) {
			System.out.println("No Content: " +fileName );
			entityMap.clear();
			tf.clear();
			return;
		}
		tfWriter.write(fileName);
		String outputTf = "";
		for (String term : tf.keySet()) {
			
			Integer theVal = tf.get(term);
			
			if(df.containsKey(term)) {
				df.put(term, df.get(term)+1);
				
			}
			else {
				df.put(term, 1);
			}
			outputTf = outputTf + "\t" + term + "\t" + theVal;
			//System.out.println(outputTf);
		}
		
		
		if(fileName.equalsIgnoreCase("28288137")) {
			System.out.println("No Content: " +outputTf + " Length: " + outputTf.length());
		}
		tfWriter.write(outputTf);
		tfWriter.write("\n");
		tfAllFiles.add(new TfAllDocBean(fileName, tf));
		entityAllFiles.put(fileName, new HashMap(entityMap));
		entityMap.clear();
		tf.clear();
	}
	
	void getBioEntity(String path) throws IOException {
		
		
		 tfWriter = new BufferedWriter(new FileWriter(Constants.OUTPUT_PATH + "entityTfFile.txt"));
		 tf_idfWriter = new BufferedWriter(new FileWriter(Constants.OUTPUT_PATH + "entityInfo.txt"));
		
		File folder = new File(path);
		File[] listOfFiles = folder.listFiles();
		numOfDoc = listOfFiles.length;
		
		long st = System.nanoTime();
		for (File file : listOfFiles) {
			if (file.isFile()) {

				try (BufferedReader br = new BufferedReader(new FileReader(file.getAbsolutePath()))) {

					String sCurrentLine = "";
					String fullText = "";
					while ((sCurrentLine = br.readLine()) != null) {
						fullText = fullText + " " + sCurrentLine.toLowerCase();

					}
					String fileNameWithExt = file.getName();
					String fileNameWithOutExt = fileNameWithExt.substring(0, fileNameWithExt.length()-4);
					
					getTfDfEntity(fileNameWithOutExt,fullText);
					
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
		}
		long et = System.nanoTime();
		long ot = et - st;

        System.out.println("Df time Elapsed time in seconds: " + ot / 1000000000);
	}

	public static void main(String args[]) throws ClassNotFoundException, IOException {

		long lStartTime = System.nanoTime();
		ExtractBioEntity eBioEntity = new ExtractBioEntity();

		File corpus = new File(Constants.CORPUS_PATH);

		System.out.println("Reading chunker from file=" + corpus);
		chunker = (Chunker) AbstractExternalizable.readObject(corpus);
		
		
		long readTfDfS = System.nanoTime();
		eBioEntity.getBioEntity(Constants.INPUT_PATH);
		long readTfDfE = System.nanoTime();
		System.out.println("read file tf df time Elapsed time in Micro_Seconds: " + (readTfDfE - readTfDfS) / 1000);
		
		long tf_dfS = System.nanoTime();
		eBioEntity.getTf_Idf();
		long tf_dfE = System.nanoTime();	
		
		System.out.println("tf*df time Elapsed time in Micro_Seconds: " + (tf_dfE - tf_dfS) / 1000);
		
		

        
        long sortTimeS = System.nanoTime();
		Collections.sort(tf_DfDocBeans, new Comparator<EntityTfDfDocBean>(){
			@Override
			public int compare(EntityTfDfDocBean o1, EntityTfDfDocBean o2) {
				if (o1.getTf_df() < o2.getTf_df()) return 1;
		        if (o1.getTf_df() > o2.getTf_df()) return -1;
		        return 0;
			}
		});
		
		for(int i=0; i<tf_DfDocBeans.size(); i++){
			tf_idfWriter.write(tf_DfDocBeans.get(i).getFileName()+ "\t" +tf_DfDocBeans.get(i).getTerm() + "\t" + tf_DfDocBeans.get(i).getType()  + "\t" + tf_DfDocBeans.get(i).getTf_df()+"\n");
		}
		long sortTimeE = System.nanoTime();
		System.out.println("Sorting and Writing Elapsed time in Micro_Seconds: " + (sortTimeE-sortTimeS) / 1000);
        tf_idfWriter.close();
        long lEndTime = System.nanoTime();
		long output = lEndTime - lStartTime;
		System.out.println("Elapsed time in miniute: " + output / (60.0*1000000000));
	}

}
