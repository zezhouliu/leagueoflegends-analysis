import kmeans_trainer
import sparse_code
import cleanup_pregame
from sklearn.svm import SVC

def run_pregame ():
	"""
	Driver for running the workflow.
	1. Pre-process the data to clean up formatting.
	2. Data cleanup into the layout we want
	3. Train kmeans clusters
	4. Generate sparse codes
	5. Repeat 1-4 for test data to evaluate
	"""

	# Read in input files
	directory_prefix = 'data/'
	filenames = ['m1.json', 'm2.json', 'm3.json', 'm4.json', 'm5.json']
	full_filenames = []
	for fname in filenames:
		full_filenames.append((directory_prefix) + fname)

	matches_matrix, winners_matrix = cleanup_pregame.data_cleanup(full_filenames)

	# Train K-means model
	model = kmeans_trainer.KMeansCluster(matches_matrix)
	clusters = model[0]

	# Create sparse codes for original data based on clusters
	k = 15
	sparse_codes = sparse_code.sparsify_omp(matches_matrix, clusters, k)

	# Train SVC model for classification
	clf = SVC()
	clf.fit(sparse_codes, winners_matrix)

	# print "Original training:", clf.score(sparse_codes, winners_matrix)

	# Test model using testing data 
	testnames = ['m6.json']
	full_testnames = []
	for fname in testnames:
		full_testnames.append((directory_prefix) + fname)

	for fname in full_testnames:
		fname_a = [fname]
		print "Testing on...", fname
		test_matrix, test_winners = cleanup_pregame.data_cleanup(fname_a)
		test_codes = sparse_code.sparsify_omp(test_matrix, clusters, 15)

		print "Accuracy", clf.score(test_codes, test_winners)

	return

if __name__ == '__main__':
	run_pregame()


