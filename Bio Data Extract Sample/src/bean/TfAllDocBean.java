package bean;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class TfAllDocBean {
	
	private String fileName = "";
	private Map<String, Integer> tf = null;
	private Map<String, Integer> tfIdf = null;
	
	public TfAllDocBean(String fileName, Map<String, Integer> tf) {
		super();
		this.fileName = fileName;
		this.tf = new HashMap<String, Integer>(tf);
	}

	public String getFileName() {
		return fileName;
	}

	public void setFileName(String fileName) {
		this.fileName = fileName;
	}

	public Map<String, Integer> getTf() {
		return tf;
	}

	public void setTf(Map<String, Integer> tfIdf) {
		this.tfIdf = tfIdf;
	}
	public Map<String, Integer> getTfIdf() {
		return tf;
	}

	public void setTfIdf(Map<String, Integer> tfIdf) {
		this.tfIdf = tfIdf;
	}
	
	

}
