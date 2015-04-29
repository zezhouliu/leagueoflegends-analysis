import numpy as np

def matching_pursuit(xs, Dt, k, zs):
	"""
	Performs recursive matching pursuit 
	xs: [X_1, X_2, ... X_i]
	Dt: [d1, d2, d3, ..., d_j]
	k: iterations left
	zs: [[sparse1], [sparse2], ..., [sparse_i]]
	"""
	if k == 0:
		return zs

	num_xs = len(xs)
	num_ds = len(Dt)

	for x_index in xrange(num_xs):
		x = xs[x_index]

		max_inner_product = 0
		max_z_index = None

		for i in xrange(num_ds):
			di = Dt[i]
			ip = np.dot(di, x)
			if abs(ip) > abs(max_inner_product):
				max_inner_product = ip
				max_z_index = i

		if max_z_index != None:
			zs[x_index][max_z_index] += max_inner_product

		# Update the X-vector
		xs[x_index] -= (max_inner_product * np.transpose(Dt[max_z_index]))

	return matching_pursuit(xs, Dt, k-1, zs)


def orthogonal_matching_pursuit(xs, Dt, D, k, zs, selected):
	"""
	Performs recursive orthogonal matching pursuit 
	xs: [X_1, X_2, ... X_i]
	Dt: [d1, d2, d3, ..., d_j]
	k: iterations left
	zs: [[sparse1], [sparse2], ..., [sparse_i]]
	selected: [[selected1], [selected2], ..., [selected_i]]
	"""

	if k == 0:
		return zs

	num_xs = len(xs)
	num_ds = len(Dt)

	for x_index in xrange(num_xs):
		x = xs[x_index]

		max_inner_product = 0
		max_z_index = None

		for i in xrange(num_ds):
			di = Dt[i]
			ip = np.dot(di, x)
			if abs(ip) > abs(max_inner_product):
				max_inner_product = ip
				max_z_index = i

		if max_z_index != None:
			zs[x_index][max_z_index] += max_inner_product

			# Add selected dictionary atom to selected
			selected[x_index].append(max_z_index)

			# Update the X-vector based on OMP
			gamma, _, _, _  = np.linalg.lstsq(D[:,selected[x_index]], x)
			xs[x_index] = xs[x_index] - np.dot(D[:,selected[x_index]], gamma)

	return orthogonal_matching_pursuit(xs, Dt, D, k-1, zs, selected)