package bean;

public class DocSetBean {
	
	private String fileName = "";
	private String docText = "";
	
	
	
	public DocSetBean(String fileName, String docText) {
		super();
		this.fileName = fileName;
		this.docText = docText;
	}
	
	public String getFileName() {
		return fileName;
	}
	public void setFileName(String fileName) {
		this.fileName = fileName;
	}
	public String getDocText() {
		return docText;
	}
	public void setDocText(String docText) {
		this.docText = docText;
	}
	
	

}
