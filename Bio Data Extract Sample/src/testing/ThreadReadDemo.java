package testing;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import constants.Constants;
public class ThreadReadDemo {

	/**Java multithreaded reading large files
	 * @param args
	 */
	public static void main(String[] args) {
		long lStartTime = System.nanoTime();
		Thread t1=new Thread(new MultiThread(),"A");
		Thread t2=new Thread(new MultiThread(),"B");
		t1.start();
		t2.start();
		long lEndTime = System.nanoTime();
		long output = lEndTime - lStartTime;
		System.out.println("Elapsed time in seconds: " + output / 1000000000);
	}

}


 class MultiThread implements Runnable{	
	private static BufferedReader br = null;
	private List<String> list;
	
	static{
		try {
			br = new BufferedReader(new FileReader("glutamine.txt"),10);
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	public void run() {
		String line = null;
		int count = 0;
		while(true) {
			System.out.println(Thread.currentThread().getName());
			this.list = new ArrayList<String>();
			synchronized(br) {
				try {
					while((line = br.readLine()) != null) {
						if(count<15) {
							list.add(line);
							count++;
						}else {
							list.add(line);
							count = 0;
							break;
						}
					}
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
			try {
				Thread.sleep(1);
				//display(this.list);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			if(line == null)
				break;
		}
		
		
	}
	
	public void display(List<String> list) {
		for(String str:list) {
			System.out.println(str);
		}
		System.out.println(list.size());
	}
	
}