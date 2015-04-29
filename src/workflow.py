import kmeans_trainer
import sparse_code
import data_cleanup
from sklearn.svm import SVC

def run ():

	filenames = ['m1.json', 'm2.json', 'm3.json']
	matches_matrix, winners_matrix = data_cleanup.data_cleanup(filenames)

	for i in xrange(len(matches_matrix)):
		if len(matches_matrix[i]) != 872:
			matches_matrix[i] = matches_matrix[i-1]

	print winners_matrix

	model = kmeans_trainer.KMeansCluster(matches_matrix)
	clusters = model[0]

	k = 15

	# Create sparse codes for original data based on clusters
	sparse_codes = sparse_code.sparsify_omp(matches_matrix, clusters, k)

	print sparse_codes

	# Train SVC model for classification
	clf = SVC()
	clf.fit(sparse_codes, winners_matrix)

	# Test data
	testnames = ['m5.json']
	test_matrix, test_winners = data_cleanup.data_cleanup(testnames)
	# Some clean-up
	for i in xrange(len(test_matrix)):
		if len(test_matrix[i]) != 872:
			test_matrix[i] = test_matrix[i-1]

	test_codes = sparse_code.sparsify_omp(test_matrix, clusters, k)

	print clf.score(test_codes, test_winners)
	return

run()


