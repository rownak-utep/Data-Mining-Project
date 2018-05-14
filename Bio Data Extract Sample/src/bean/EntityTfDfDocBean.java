package bean;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

public class EntityTfDfDocBean  {
	
	private String fileName = "";
	private String term = "";
	private double tf_df = 0.0;
	private String type = "";
	
	public String getType() {
		return type;
	}
	public void setType(String type) {
		this.type = type;
	}
	public String getFileName() {
		return fileName;
	}
	public void setFileName(String fileName) {
		this.fileName = fileName;
	}
	public String getTerm() {
		return term;
	}
	public void setTerm(String term) {
		this.term = term;
	}
	public double getTf_df() {
		return tf_df;
	}
	public void setTf_df(double tf_df) {
		this.tf_df = tf_df;
	}
	public EntityTfDfDocBean(String fileName, String term, double tf_df, String type) {
		super();
		this.fileName = fileName;
		this.term = term;
		this.tf_df = tf_df;
		this.type = type;
	}
	
	public static void main(String args[]){
		
		
		EntityTfDfDocBean tf_DfDocBean = new EntityTfDfDocBean("A", "B", 1.5, "X");
		EntityTfDfDocBean tf_DfDocBean1 = new EntityTfDfDocBean("A", "B", .5, "X");
		EntityTfDfDocBean tf_DfDocBean2 = new EntityTfDfDocBean("A", "B", 6.5, "Z");
		
		List<EntityTfDfDocBean> docs = new ArrayList<EntityTfDfDocBean>();
		docs.add(tf_DfDocBean);
		docs.add(tf_DfDocBean1);
		docs.add(tf_DfDocBean2);
		
		Collections.sort(docs, new Comparator<EntityTfDfDocBean>(){
			@Override
			public int compare(EntityTfDfDocBean o1, EntityTfDfDocBean o2) {
				if (o1.getTf_df() < o2.getTf_df()) return 1;
		        if (o1.getTf_df() > o2.getTf_df()) return -1;
		        return 0;
			}
		});
		
		for(int i=0; i<docs.size(); i++){
			System.out.println("sorted" + docs.get(i).getTf_df());
		}
	}

}
