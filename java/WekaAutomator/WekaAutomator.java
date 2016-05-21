import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
//import java.util.Dictionary;
import java.util.HashMap;
//import java.util.HashSet;
import java.util.Map;
import java.util.Random;

import weka.classifiers.AbstractClassifier;
//import weka.classifiers.Classifier;
import weka.classifiers.Evaluation;
import weka.classifiers.bayes.NaiveBayes;
import weka.classifiers.functions.LibLINEAR;
import weka.classifiers.functions.LibSVM;
import weka.classifiers.functions.Logistic;
import weka.classifiers.functions.SMO;
//import weka.classifiers.functions.SMO.BinarySMO;
//import weka.classifiers.functions.supportVector.PolyKernel;
import weka.core.Instances;
//import weka.core.SelectedTag;
//import weka.core.Tag;
import weka.core.converters.ConverterUtils.DataSource;

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
		// "/Users/roeeaharoni/research_data/output/48914_sentences_exp/40k_function_words_non_reference_arff/");
		// "/Users/roeeaharoni/research_data/output/48914_sentences_exp/JHU_weights"
		// "/Users/roeeaharoni/research_data/output/48914_sentences_exp/function_words_pos_wmt13_non_ref_sentences_arff/"
		// "/Users/roeeaharoni/research_data/output/48914_sentences_exp/function_words_pos_wmt12_newstest_nonref_sentences_arff/");
		// "/Users/roeeaharoni/research_data/output/48914_sentences_exp/moses_function_words_pos_nonref_sentences_arff/"
		// "/Users/roeeaharoni/research_data/output/48914_sentences_exp/wmt13_pos_wmt12_newstest_nonref_sentences_arff/");
		// "/Users/roeeaharoni/research_data/output/48914_sentences_exp/wmt13_parse_both_wmt12_newstest_nonref_sentences_arff/");
		// "/Users/roeeaharoni/research_data/output/48914_sentences_exp/wmt13_parse_both_fixed_wmt12_newstest_nonref_sentences_arff/");
		// "/Users/roeeaharoni/research_data/output/48914_sentences_exp/wmt13_pos_fword_parse_both_fixed_wmt12_newstest_nonref_sentences_arff/");
		// "/Users/roeeaharoni/research_data/output/48914_sentences_exp/wmt13_parse_CFG_wmt12_newstest_nonref_sentences_arff/");
		// "/Users/roeeaharoni/research_data/output/48914_sentences_exp/wmt13_parse_nonter_fixed_wmt12_newstest_nonref_sentences_arff/");
		// //didn't finish with SMO
		// "/Users/roeeaharoni/research_data/output/48914_sentences_exp/wmt13_pos_fword_parse_t20_wmt12_newstest_nonref_sentences_arff/");
		// "/Users/roeeaharoni/research_data/output/48914_sentences_exp/wmt13_all_t30_wmt12_newstest_nonref_sentences_arff/");
		// "/Users/roeeaharoni/research_data/output/48914_sentences_exp/wmt13_pos_fword_CFG_t30_wmt12_newstest_nonref_sentences_arff/");
		// "/Users/roeeaharoni/research_data/post_ACL2014/classifier_comparison_exp/wmt13_pos_fword_t30_wmt12_newstest_nonref_sentences_arff");
				"/Users/roeeaharoni/research_data/post_ACL2014/feature_comparison_exp/wmt13_cfg_t30_wmt12_newstest_nonref_sentences_arff");
		// get the arff files from the directory
		File[] arff_files = arffFolder.listFiles();

		// create the classifier instances
		Map<String, AbstractClassifier> classifiers = CreateClassifiers();
		String[] classifierNames = new String[4];
		classifierNames = classifiers.keySet().toArray(classifierNames);

		// iterate throgh the classifiers
		for (int j = 0; j < classifiers.size(); j++) {

			// run classification using every classifier in the list
			for (int i = 0; i < arff_files.length; i++) {

				// get or create a new directory for each classifiers results
				String resultsDirPath = arffFolder.getPath() + "/"
						+ classifierNames[j];
				new File(resultsDirPath).mkdirs();
				if (arff_files[i].getPath().contains(".arff")) {
					String outputFilePath = resultsDirPath + "/"
							+ arff_files[i].getName() + ".result.txt";

					// run the actual classification
					Classify(arff_files[i].getPath(), outputFilePath,
							classifiers.get(classifierNames[j]));
				}
			}
		}
	}

	private static Map<String, AbstractClassifier> CreateClassifiers() {
		Map<String, AbstractClassifier> classifiers = new HashMap<String, AbstractClassifier>();

		classifiers.put("LogisticRegression", new Logistic());

		classifiers.put("NaiveBayes", new NaiveBayes());

		classifiers.put("LibLinear", new LibLINEAR());
		// PolyKernel kern = new PolyKernel(data, 250007, 2.0, false);
		// cls.setKernel(kern);

		// create the classifier
		classifiers.put("Libsvm", new LibSVM());
		// set the kernel to polynomial with degree 2
		// SelectedTag x = libsvm.getKernelType();
		// Tag[] y = x.getTags();
		// libsvm.setKernelType(new SelectedTag(1, y));
		// libsvm.setDegree(3);

		classifiers.put("SMO", new SMO());
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
}
