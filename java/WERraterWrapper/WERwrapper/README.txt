|--------------|
| WERater v1.0 |
|--------------|

A benchmarking tool for measuring word error rate.

Maintainer:  Alexander Sivak, for issues / suggestions, contact at: alexander.sivak@intel.com

NOTICE: For large enough files, the tool requires more than Java's default heap size.
		Usually around 1.5gb is recommended. Run the tool with the -Xmx1500m flag.

		
Methods:
--------

Each method can also output to a file - pass null as a parameter to avoid that.

calculateRecords: 			The input is a hypothesis queue and a reference queues.
							Calculates the WER for each pair in order. Returns the output in order.

calculateHypBatches:		The input is a reference queue, and a queue consisting of hypothesis queues.
							For each element in the reference queue, a matching (in order) queue of hypothesis will be tested.
							Returns the output as a queue consisting of lists, each list matches a (ref., hyp. queue) pair.
						
calculateOracleBatches:		The input is a reference queue, and a queue consisting of hypothesis queues.
							For each element in the reference queue, a matching (in order) queue of hypothesis will be tested.
							The output will consist of the best hyp. only by WER matched to the correct reference, in order.

