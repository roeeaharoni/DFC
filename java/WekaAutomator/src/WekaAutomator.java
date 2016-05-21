// NEEDS WITH WEKA 3.7, LibLINEAR (liblinear-1.92.jar, liblinear-1.9.0/libLINEAR.jar) and LibSVM (WERWrapper/LibSVM.jar) JARS!!!!!!!!!!!!

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
//import java.util.Dictionary;
import java.util.HashMap;
import java.util.Enumeration;
//import java.util.HashSet;
import java.util.Map;
import java.util.Random;

import weka.classifiers.AbstractClassifier;
import weka.classifiers.Classifier;
//import weka.classifiers.Classifier;
import weka.classifiers.Evaluation;
import weka.classifiers.bayes.NaiveBayes;
import weka.classifiers.functions.LibLINEAR;
import weka.classifiers.functions.LibSVM;
import weka.classifiers.functions.Logistic;
import weka.classifiers.functions.SMO;
import weka.core.Instance;
import weka.core.Attribute;
//import weka.classifiers.functions.SMO.BinarySMO;
//import weka.classifiers.functions.supportVector.PolyKernel;
import weka.core.Instances;
import weka.core.Utils;
import weka.core.converters.ConverterUtils.DataSink;
//import weka.core.SelectedTag;
//import weka.core.Tag;
import weka.core.converters.ConverterUtils.DataSource;
import weka.filters.Filter;
import weka.filters.supervised.attribute.AddClassification;

/**
 * 
 */

/**
 * @author roeeaharoni
 * 
 */
public class WekaAutomator {

	/**
	 * @param args
	 * @throws Exception
	 */
	public static void main(String[] args) throws Exception {

		File arffFolder = new File(
				//"/Users/roeeaharoni/research_data/icri-speech/extracted-data/arff/nbest_WER_clusters_merged_40000_vs_40000_trans_unigram_t30_arff");
				"/Users/roeeaharoni/research_data/icri-speech/extracted-data/arff/robot/wer_clusters_382_vs_rockin_only_382_trans_unigram_t30_arff");
		
		// get the arff files from the directory
		File[] arff_files = arffFolder.listFiles();

		// create the classifier instances
		Map<String, AbstractClassifier> classifiers = CreateClassifiers();
		String[] classifierNames = new String[4];
		classifierNames = classifiers.keySet().toArray(classifierNames);

		// iterate throgh the classifiers
		for (int j = 0; j < classifiers.size(); j++) {

			// run classification for each file using every classifier in the list
			for (int i = 0; i < arff_files.length; i++) {
				
				// get or create a new directory for each classifiers results
				String resultsDirPath = arffFolder.getPath() + "/"
						+ classifierNames[j];
				new File(resultsDirPath).mkdirs();
				if (arff_files[i].getPath().contains(".arff")) {
					String outputFilePath = resultsDirPath + "/"
							+ arff_files[i].getName() + ".result.txt";

					// run the actual classification
					//Classify(arff_files[i].getPath(), outputFilePath,
					//		classifiers.get(classifierNames[j]));
					
					ClassifyWithLables(arff_files[i].getPath(), outputFilePath,
							classifiers.get(classifierNames[j]));
				}
			}
		}
	}

	private static Map<String, AbstractClassifier> CreateClassifiers() {
		Map<String, AbstractClassifier> classifiers = new HashMap<String, AbstractClassifier>();

		//classifiers.put("LogisticRegression", new Logistic());

		//classifiers.put("NaiveBayes", new NaiveBayes());

		classifiers.put("LibLinear", new LibLINEAR());
		// PolyKernel kern = new PolyKernel(data, 250007, 2.0, false);
		// cls.setKernel(kern);

		// create the classifier
		// classifiers.put("Libsvm", new LibSVM());
		// set the kernel to polynomial with degree 2
		// SelectedTag x = libsvm.getKernelType();
		// Tag[] y = x.getTags();
		// libsvm.setKernelType(new SelectedTag(1, y));
		// libsvm.setDegree(3);

		//classifiers.put("SMO", new SMO());
		return classifiers;
	}

	/**
	 * Classifies the arff file using WEKA.
	 * 
	 * @param arff_file_path
	 * @param output_file_path
	 * @throws Exception
	 */
	public static void Classify(String arff_file_path, String output_file_path,
			AbstractClassifier cls) throws Exception {
		System.out.println("starting classification with file:");
		System.out.println(arff_file_path);

		// create the data source
		DataSource source = new DataSource(arff_file_path);
		Instances data = source.getDataSet();

		// setting class attribute if the data format does not provide this
		// information
		// For example, the XRFF format saves the class attribute information as
		// well
		if (data.classIndex() == -1)
			data.setClassIndex(data.numAttributes() - 1);

		// create the 10-folds evaluation instance
		Evaluation eval = new Evaluation(data);
		Random rand = new Random(1); // using seed = 1
		int folds = 10;
		eval.crossValidateModel(cls, data, folds, rand);
		
		System.out.println(eval.toMatrixString());
		System.out.println(eval.toSummaryString());

		/*
		 * // try to get the weights of the attributes after the training
		 * cls.buildClassifier(data); String attributes[] = cls.getAttributes();
		 * double weights[] = cls.getAttributeWeights(); for (int i = 0; i <
		 * weights.length; i++) System.out.println(attributes[i] + " " +
		 * weights[i]);
		 * 
		 * File w_file = new File(
		 * "/Users/roeeaharoni/research_data/output/48914_sentences_exp/JHU_weights/weights.txt"
		 * ); BufferedWriter w_output = new BufferedWriter(new
		 * FileWriter(w_file)); w_output.write(weights); w_output.close();
		 */

		// write the result to a file
		File file = new File(output_file_path);
		BufferedWriter output = new BufferedWriter(new FileWriter(file));
		output.write(eval.toMatrixString());
		output.write(eval.toSummaryString());
		output.write(eval.toString());
		output.close();

		// finished
		System.out.println("finished classification!");
		System.out.println("output file: ");
		System.out.println(output_file_path);
	}
	
	public static void ClassifyWithLables(String arff_file_path, String output_file_path,
			AbstractClassifier cls) throws Exception
	{
		int seed = 1;
		int folds = 10;
		Random rand = new Random(seed);
		DataSource source = new DataSource(arff_file_path);
	    Instances randData = source.getDataSet();
	    randData.randomize(rand);
	    randData.setClassIndex(randData.numAttributes()-1);
	    if (randData.classAttribute().isNominal())
	      randData.stratify(folds);

	    // perform cross-validation and add predictions
	    Instances predictedData = null;
	    Evaluation eval = new Evaluation(randData);
	    for (int n = 0; n < folds; n++) {
	      Instances train = randData.trainCV(folds, n);
	      Instances test = randData.testCV(folds, n);
	      // the above code is used by the StratifiedRemoveFolds filter, the
	      // code below by the Explorer/Experimenter:
	      // Instances train = randData.trainCV(folds, n, rand);

	      // build and evaluate classifier
	      Classifier clsCopy = AbstractClassifier.makeCopy((Classifier)cls);
	      clsCopy.buildClassifier(train);
	      eval.evaluateModel(clsCopy, test);

	      // add predictions
	      AddClassification filter = new AddClassification();
	      filter.setClassifier(cls);
	      filter.setOutputClassification(true);
	      //filter.setOutputDistribution(true);
	      filter.setOutputErrorFlag(true);
	      filter.setInputFormat(train);
	      Filter.useFilter(train, filter);  // trains the classifier
	      Instances pred = Filter.useFilter(test, filter);  // perform predictions on test set
	      if (predictedData == null)
	        predictedData = new Instances(pred, 0);
	      // go through predictions
	      for (int j = 0; j < pred.numInstances(); j++)
	      {
	    	System.out.println("instance no. " + j);
	        predictedData.add(pred.instance(j));
	      	Instance inst = pred.instance(j);
	      	Enumeration attrs = train.enumerateAttributes();
	      	
	      	// go through attributes 
	      	for (int k = 0; k < pred.numAttributes(); k++)
	      	{
	      		if (attrs.hasMoreElements())
	      		{
	      			Attribute a = (Attribute)attrs.nextElement();
		      		if (inst.value(k) == 1)
		      		{
		      			System.out.println(a.name());
		      		}
		      		attrs.toString();
	      		}
	      	}
	      	
	      	// get gold, prediction, is correct  
	    	System.out.println(inst.toString());

	      	
	      }
	      	
	    }

	    // output evaluation
	    System.out.println();
	    System.out.println("=== Setup ===");
	    System.out.println("Classifier: " + cls.getClass().getName() + " " + Utils.joinOptions(cls.getOptions()));
	    System.out.println("Dataset: " + arff_file_path);
	    System.out.println("Folds: " + folds);
	    System.out.println("Seed: " + seed);
	    System.out.println();
	    System.out.println(eval.toSummaryString("=== " + folds + "-fold Cross-validation ===", false));
	    
	    int x = seed;
	    return;
	    // output "enriched" dataset
	    //DataSink.write(Utils.getOption("o", args), predictedData);
	}
}
