import kmeans_trainer
import sparse_code
import cleanup_pregame
from sklearn.svm import SVC


def run ():

	filenames = ['m1.json', 'm2.json', 'm3.json']
	matches_matrix, winners_matrix = cleanup_pregame.data_cleanup(filenames)

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
	test_matrix, test_winners = cleanup_pregame.data_cleanup(testnames)
	# Some clean-up
	for i in xrange(len(test_matrix)):
		if len(test_matrix[i]) != 872:
			test_matrix[i] = test_matrix[i-1]

	test_codes = sparse_code.sparsify_omp(test_matrix, clusters, k)

	print clf.score(test_codes, test_winners)
	return

def run_pregame ():

	directory_prefix = 'data/'
	filenames = ['m1.json', 'm2.json', 'm3.json', 'm4.json', 'm6.json']
	full_filenames = []
	for fname in filenames:
		full_filenames.append((directory_prefix) + fname)

	matches_matrix, winners_matrix = cleanup_pregame.data_cleanup(full_filenames)

	expected_length = len(matches_matrix[0])
	num_unexpected = 0

	for i in xrange(len(matches_matrix)):
		if len(matches_matrix[i]) != expected_length:
			matches_matrix[i] = matches_matrix[i-1]
			num_unexpected += 1

	# print winners_matrix

	model = kmeans_trainer.KMeansCluster(matches_matrix)
	clusters = model[0]

	k = 15

	# Create sparse codes for original data based on clusters
	sparse_codes = sparse_code.sparsify_omp(matches_matrix, clusters, k)

	# print sparse_codes

	# Train SVC model for classification
	clf = SVC()
	clf.fit(sparse_codes, winners_matrix)

	print "Original training:", clf.score(sparse_codes, winners_matrix)

	# return

	# Test data
	testnames = ['m1.json', 'm2.json', 'm3.json', 'm4.json']
	full_testnames = []
	for fname in testnames:
		full_testnames.append((directory_prefix) + fname)

	for fname in full_testnames:
		fname_a = [fname]
		print fname
		test_matrix, test_winners = cleanup_pregame.data_cleanup(fname_a)

		test_unexpected = 0

		# Some clean-up
		# for i in xrange(len(test_matrix)):
		# 	if len(test_matrix[i]) != expected_length:
		# 		test_matrix[i] = test_matrix[i-1]
		# 		test_unexpected += 1

		test_codes = sparse_code.sparsify_omp(test_matrix, clusters, 15)

		print clf.score(test_codes, test_winners)

		wins = 0
		for i in xrange(len(test_winners)):
			if test_winners[i] != 0:
				wins += 1

		print float(wins) / len(test_winners)

	return

if __name__ == '__main__':
	run_pregame()


