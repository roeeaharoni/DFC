import java.io.File;
import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.util.LinkedList;
import java.util.Queue;

import com.intel.c2.werater.WERater;
import com.intel.c2.werater.WERecord;

public class WERwrapper {

	/**
	 * @param args
	 * @throws IOException 
	 */
	public static void main(String[] args) throws IOException {
		String referenceFilePath = args[0];
		String hypothesesFilePath = args[1];
		String outputFilePath = null;
		if(args.length>2)
			outputFilePath = args[2];
		
		
		// read reference file and hypotheses file from arguments
		// reference file 
		Queue<String> refs = new LinkedList<String>();
		for (String line : Files.readAllLines(Paths.get(referenceFilePath),Charset.defaultCharset() )) {
			refs.add(line);
		}
		
		// hypotheses file 
		Queue<String> hypos = new LinkedList<String>();
		for (String line : Files.readAllLines(Paths.get(hypothesesFilePath),Charset.defaultCharset() )) {
			hypos.add(line);
		}
		
		// use the WER jar to compute WER and output the WER results to a file
		Queue<WERecord> results;
		try {
			results = WERater.calculateRecords(hypos, refs, new File(outputFilePath));

			// calculate average WER and accuracy
			Double avearageWER = 0.0;
			Double avearageAccuracy = 0.0;
			for(WERecord result : results){
				avearageWER += result.getWordErrorRate();
				if(result.getAccuracyRate()!=Double.NaN){
					avearageAccuracy += result.getAccuracyRate();	
				}
				if(avearageAccuracy==Double.NaN){
					avearageAccuracy += result.getAccuracyRate();	
				}
			}
			
			avearageWER /= results.size();
			avearageAccuracy /= results.size();
			String avgWERStr = "avearageWER=" + avearageWER + "\n";
			String avgAccStr = "avearageAccuracy=" + avearageAccuracy + "\n";
			
			System.out.print("reference file:" + args[0]+'\n');
			System.out.print("input file:" + args[1]+'\n');
			System.out.print(avgWERStr);
			System.out.print(avgAccStr);
			
			//write to file
			try {
			    Files.write(Paths.get(outputFilePath), 
			    		(avgWERStr+avgAccStr).getBytes(), 
			    		StandardOpenOption.APPEND);
			}catch (IOException e) {
			    //exception handling left as an exercise for the reader
			}
			
		}
		catch  (IOException | InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
}
