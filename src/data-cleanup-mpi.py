import json
from mpi4py import MPI

def cleanup(match):
	"""
	cleanup(match)
	@Brief: Cleans up unncessary fields.  Converts fields of interest to quantitative values
	"""

	# Validator to make sure it's the kind of match we want
	if match['matchMode'] != "CLASSIC" or match['queueType'] != 'RANKED_SOLO_5x5':
		return -1

	# At the first level, we should delete some unncessary attributes
	delkeys = ['platformId', 'matchMode', 'matchCreation', 'mapId', 'season', 'matchVersion']
	for k in delkeys:
		if k in match:
			del match[k]

	### Update data to numerical:
	## Region:
	if match['region'] == 'NA':
		match['NA'] = 1
		match['EU'] = 0
		match['KR'] = 0
	elif match['region'] == 'EU':
		match['NA'] = 0
		match['EU'] = 1
		match['KR'] = 0
	elif match['region'] == 'KR':
		match['NA'] = 0
		match['EU'] = 0
		match['KR'] = 0

	# Now we should delete these fields
	if 'region' in match:
		del match['region']

	return 0


if __name__ == '__main__':
	"""
	Our main goal is to minimize IO and communication between processors.
	Trade-off: Less IO vs Better load balancing
	Master-slave implementation of data-cleanup using MPI
	"""

	# setup communications metadata for MPI
	comm = MPI.COMM_WORD
	rank = comm.Get_rank()
	size = comm.Get_size()

	if rank == 0:
		#filenames = ['matches1.json', 'matches2.json', 'matches3.json', 'matches4.json', 'matches5.json', 
		#	'matches6.json', 'matches7.json', 'matches8.json', 'matches9.json', 'matches10.json']
		filenames = ['matches_1.json']

		# Pass one filename to each processor to handle cleanup
		for i in xrange(len(filenames)):
			filename = filenames[i]

			# Distribute the first few tasks without listening
			if i < size - 1:
				comm.send(filename, i + 1, tag = (i+1))
				continue


			# Listen for responses before sending new processes
			res_val, res_rank = self.comm.recv(source=MPI.ANY_SOURCE)

			comm.send(filename, res_rank, tag=res_rank)

		# Tell the slaves to stop
		for i in xrange(size - 1):
			comm.send(None, i + 1, tag = i + 1)


	else:

		while (True):
			fname = comm.recv(source=0, tag=rank)
			
			# Stop working if there is nothing left...
			if fname == None:
				break

			with open(fname) as json_data:

				# data is { 'matches' : [...]}
				data = json.load(json_data)
				matches = data['matches']
				
				# Clean up some of the data, i.e. delete unnecessary key-value pairs
				for i in xrange(len(matches)):
					match = matches[i]
					clean_status = cleanup(match)

					if clean_status < 0:
						print "Game", i, "invalid."
						# XXX: Delete game here
				
				# Dump the file after updating it
				with open(("clean_" + fname), "w") as outfile:
					outfile.write(json.dumps(data))


