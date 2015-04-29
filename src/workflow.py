import kmeans_trainer
import sparse_code
import data_cleanup
from sklearn.svm import SVC

def run ():

	filenames = ['matches_1.json']
	matches_matrix, winners_matrix = data_cleanup.data_cleanup(filenames)

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
	print clf.score(sparse_codes, winners_matrix)
	return

run()


