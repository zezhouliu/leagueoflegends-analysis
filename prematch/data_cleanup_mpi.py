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

    # Create dictionary for columns
    d = {}
    NUM_PLAYERS = 10
    participants = match['participants']
    for participant in participants:

        # Grab the participant id
        playerId = participant["participantId"]

        for k in participant:

            # Skip these keys:
            if k == "teamId" or k == "masteries" or k == "runes" or k == "participantId":
                continue

            # Spell1Id and spell2Id are special categorical variables
            if k == "spell1Id" or k == "spell2Id":
                continue

            if k == "highestAchievedSeasonTier":
                tier = participant["highestAchievedSeasonTier"]
                if tier == "BRONZE":
                    tier = 1
                elif tier == "SILVER":
                    tier = 2
                elif tier == "GOLD":
                    tier = 3
                elif tier == "PLATINUM":
                    tier = 4
                elif tier == "DIAMOND":
                    tier = 5
                elif tier == "MASTER":
                    tier = 6
                elif tier == "CHALLENGER":
                    tier = 7
                else:
                    tier = 0
                if "highestAchievedSeasonTier" not in d:
                    d["highestAchievedSeasonTier"] = [None] * NUM_PLAYERS
                d["highestAchievedSeasonTier"][playerId - 1] = tier
                continue

            # Timeline and stats are special nested dictionaries
            if k == 'timeline':
                timeline = participant[k]
                for k_deltas in timeline:

                    if k_deltas == "role":
                        role = timeline[k_deltas]
                        if role == 'SOLO':
                            role = 1
                        elif role == 'DUO':
                            role = 2
                        elif role == 'DUO_CARRY':
                            role = 3
                        elif role == 'DUO_SUPPORT':
                            role = 4
                        else:
                            role = 0
                        if 'role' not in d:
                            d['role'] = [None] * NUM_PLAYERS
                        d['role'][playerId - 1] = role
                        continue

                    if k_deltas == 'lane':
                        lane = timeline[k_deltas]
                        if lane == 'TOP':
                            lane = 1
                        elif lane == 'MID' or lane == 'MIDDLE':
                            lane = 2
                        elif lane == 'JUNGLE':
                            lane = 3
                        elif lane == 'BOT' or lane == 'BOTTOM':
                            lane = 4
                        else:
                            lane = 0
                        if 'lane' not d:
                            d['lane'] = [None] * NUM_PLAYERS
                        d['lane'][playerId - 1] = lane
                        continue

                    if k_deltas == "role" or k_deltas == "lane":
                        continue
                        if k_deltas not in d:
                            d[k_deltas] = [None] * NUM_PLAYERS
                        d[k_deltas][playerId - 1] = timeline[k_deltas]
                        continue
                    deltas = timeline[k_deltas]
                    for k_range in deltas:
                        if (k_deltas + k_range) not in d:
                            d[(k_deltas + k_range)] = [None] * NUM_PLAYERS
                        d[(k_deltas + k_range)][playerId - 1] = deltas[k_range]
                    if len(deltas.keys()) <= 2:
                        if (k_deltas + "twentyToThirty") not in d:
                            d[(k_deltas + "twentyToThirty")] = [None] * NUM_PLAYERS
                        d[(k_deltas + "twentyToThirty")][playerId - 1] = 0
                    if len(deltas.keys()) <= 3:
                        if (k_deltas + "thirtyToEnd") not in d:
                            d[(k_deltas + "thirtyToEnd")] = [None] * NUM_PLAYERS
                        d[(k_deltas + "thirtyToEnd")][playerId - 1] = 0
                continue

            if k == 'stats':
                stats = participant[k]
                for k_stat in stats:
                    # Ignore some of the keys like "winner"
                    if k_stat == 'winner':
                        continue
                    if k_stat not in d:
                        d[k_stat] = [None] * NUM_PLAYERS
                    d[k_stat][playerId - 1] = stats[k_stat]
                continue

            # If key not already in dictionary, then add it
            if k not in d:
                d[k] = [None] * NUM_PLAYERS
            d[k][playerId - 1] = participant[k]

    # Get number of keys:
    num_keys = len(d.keys())
    row = []

    # Add match ID and duration
    row.append(match['matchId'])
    row.append(match['matchDuration'])

    # Create a flatten row based on this dictionary
    for i in xrange(10):
        for k in d:
            row.append(d[k][i])

    return row


if __name__ == '__main__':
    """
    Our main goal is to minimize IO and communication between processors.
    Trade-off: Less IO vs Better load balancing
    Master-slave implementation of data-cleanup using MPI
    """

    # setup communications metadata for MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if rank == 0:
        #filenames = ['matches1.json', 'matches2.json', 'matches3.json', 'matches4.json', 'matches5.json', 
        #   'matches6.json', 'matches7.json', 'matches8.json', 'matches9.json', 'matches10.json']
        filenames = ['matches_1.json']

        # Pass one filename to each processor to handle cleanup
        for i in xrange(len(filenames)):
            filename = filenames[i]

            # Distribute the first few tasks without listening
            if i < size - 1:
                comm.send(filename, i + 1, tag = (i+1))
                continue

            # Listen for responses before sending new processes
            res_val, res_rank = comm.recv(source=MPI.ANY_SOURCE)

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
                
                matches_matrix = []
                # Clean up some of the data, i.e. delete unnecessary key-value pairs
                for i in xrange(len(matches)):
                    match = matches[i]
                    clean_row = cleanup(match)
                    matches_matrix.append(clean_row)
                
                # Dump the file after updating it
                with open (("clean_" + fname), "wb") as outfile:
                    wr = csv.writer(outfile, quoting=csv.QUOTE_ALL)
                    for row in matches_matrix:
                        wr.writerow(row)

