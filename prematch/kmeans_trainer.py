import numpy as np
from sklearn.cluster import KMeans
from sklearn.cluster import k_means
from sklearn.preprocessing import scale
from math import sqrt

def KMeansCluster(matrix):
    """
    Performs the K-Means cluster given a matrix of data
    @param[in]: matrix, List of List(s)
    """

    # Possibly need to scale the data first
    data = scale(matrix)

    # Approximate the number of clusters using c = root(n/2)
    # num_clusters = int(sqrt(len(matrix) / 2))
    num_clusters = 5
    number_init = 10 # Default
    number_iter = 300
    num_cpus = 2

    print "==================="
    print "Training KMeans with (num_clusters, num_init, num_iters, num_cpus)"
    print num_clusters, number_init, number_iter, num_cpus

    # estimator = KMeans(init='k-means++', n_clusters = num_clusters, n_init = number_init)
    # estimator.fit(data)
    # clusters = k_means(data, n_clusters = num_clusters, max_iter=number_iter, n_init = number_iter, 
    #     init='k-means++', n_jobs = num_cpus)
    clusters = k_means(data, n_clusters = num_clusters, max_iter=number_iter, n_init = number_iter, n_jobs = num_cpus)


    return clusters

if __name__ == '__main__':

    # Load the preliminary data set
    d = data_cleanup()
    clusters = KMeansCluster(d)
