package com.intel.c2;

import java.io.IOException;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;

import com.intel.c2.werater.WERater;
import com.intel.c2.werater.WERecord;
import com.intel.c2.werater.WERelation;

public class Example {
	
	public static void main(String[] args)  {
		
		String ref1 = "Welcome to the WERater demo";
		String ref2 = "Would you like some pizza with that?";
		

		String hyp11 = "Welcome the WERater to demo";
		String hyp12 = "Welcome to the WERater demonstration";
		String hyp13 = "welcome to the werater demo";

		String hyp21 = "Would you like pizza with that?";
		String hyp22 = "You like some pizza";

		Queue<String> refs = new LinkedList<String>();
		refs.add(ref1);
		refs.add(ref2);
		
		Queue<Queue<String>> hyps = new LinkedList<Queue<String>>();
		
		Queue<String> hyp1 = new LinkedList<String>();
		hyp1.add(hyp11);
		hyp1.add(hyp12);
		hyp1.add(hyp13);
		
		Queue<String> hyp2 = new LinkedList<String>();
		hyp2.add(hyp21);
		hyp2.add(hyp22);
		
		hyps.add(hyp1);
		hyps.add(hyp2);
	
		Queue<List<WERecord>> results;
		try {
			results = WERater.calculateHypBatches(hyps, refs, null);
			
			for(List<WERecord> queue : results) {
				for(WERecord rec : queue) {
					rec.print();
					for(WERelation rel : rec.relations) {
						System.out.println(rel.ref + "\t" + rel.type.name() + "\t" + rel.stt);
					}
				}
				System.out.println("--------------");
			}
		} catch (IOException | InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

}
