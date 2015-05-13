import json
import csv

##############################
# Summoner spells dict
##############################
summoner_spells = {
    1 : "cleanse",
    7 : "heal",
    10: "revive",
    11: "smite",
    3: "exhaust",
    12: "teleport",
    13: "clarity",
    2: "clairvoyance",
    21: "barrier",
    4: "flash",
    6: "haste",
    14: "ignite",
    17: "garrison"
}

##############################
# Champions dict
##############################
champions = {
    "Aatrox"  : 266,
    "Ahri"    : 103,
    "Akali"   : 84,
    "Alistar" : 12,
    "Amumu"   : 32,
    "Anivia"  : 34,
    "Annie"   : 1,
    "Ashe"    : 22,
    "Azir"    : 268,
    "Bard"    : 432,
    "Blitzcrank" : 53,
    "Brand"   : 63,
    "Braum"   : 201,
    "Caitlyn" : 51,
    "Cassiopeia" : 69,
    "Cho'Gath": 31,
    "Corki"   : 42,
    "Darius"  : 122,
    "Diana"   : 131,
    "Dr. Mundo" :  36,
    "Draven"  : 119,
    "Elise"   : 60,
    "Evelynn" : 28,
    "Ezreal"  : 81,
    "Fiddlesticks" : 9,
    "Fiora"   : 114,
    "Fizz"    : 105,
    "Galio"   : 3,
    "Gangplank" : 41,
    "Garen"   : 86,
    "Gnar"    : 150,
    "Gragas"  : 79,
    "Graves"  : 104,
    "Hecarim" : 120,
    "Heimerdinger" : 74,
    "Irelia"  : 39,
    "Janna"   : 40,
    "Jarvan IV" :  59,
    "Jax"     : 24,
    "Jayce"   : 126,
    "Jinx"    : 222,
    "Kalista" : 429,
    "Karma"   : 43,
    "Karthus" : 30,
    "Kassadin": 38,
    "Katarina": 55,
    "Kayle"   : 10,
    "Kennen"  : 85,
    "Kha'Zix" : 121,
    "Kog'Maw" : 96,
    "LeBlanc" : 7,
    "Lee Sin" : 64,
    "Leona"   : 89,
    "Lissandra" : 127,
    "Lucian"  : 236,
    "Lulu"    : 117,
    "Lux"     : 99,
    "Malphite": 54,
    "Malzahar": 90,
    "Maokai"  : 57,
    "Master Yi": 11,
    "Miss Fortune" : 21,
    "Mordekaiser" : 82,
    "Morgana" : 25,
    "Nami"    : 267,
    "Nasus"   : 75,
    "Nautilus": 111,
    "Nidalee" : 76,
    "Nocturne": 56,
    "Nunu"    : 20,
    "Olaf"    : 2,
    "Orianna" : 61,
    "Pantheon": 80,
    "Poppy"   : 78,
    "Quinn"   : 133,
    "Rammus"  : 33,
    "Rek'Sai" : 421,
    "Renekton": 58,
    "Rengar"  : 107,
    "Riven"   : 92,
    "Rumble"  : 68,
    "Ryze"    : 13,
    "Sejuani" :113,
    "Shaco"   :35,
    "Shen"    :98,
    "Shyvana" :102,
    "Singed"  :27,
    "Sion"    : 14,
    "Sivir"   : 15,
    "Skarner" : 72,
    "Sona"    : 37,
    "Soraka"  : 16,
    "Swain"   : 50,
    "Syndra"  : 134,
    "Talon"   : 91,
    "Taric"   : 44,
    "Teemo"   : 17,
    "Thresh"  : 412,
    "Tristana": 18,
    "Trundle" : 48,
    "Tryndamere" : 23,
    "Twisted Fate" : 4,
    "Twitch"  : 29,
    "Udyr"    : 77,
    "Urgot"   : 6,
    "Varus"   : 110,
    "Vayne"   : 67,
    "Veigar"  : 45,
    "Vel'Koz" : 161,
    "Vi"      : 254,
    "Viktor"  : 112,
    "Vladimir": 8,
    "Volibear": 106,
    "Warwick" : 19,
    "Wukong"  : 62,
    "Xerath"  : 101,
    "Xin Zhao": 5,
    "Yasuo"   : 157,
    "Yorick"  :  83,
    "Zac"     : 154,
    "Zed"     : 238,
    "Ziggs"   : 115,
    "Zilean"  : 26,
    "Zyra"    : 143
}

##############################
# Tiers dict
##############################
season_tiers = {
    "BRONZE"     : 1,
    "SILVER"     : 2,
    "GOLD"       : 3,
    "PLATINUM"   : 4,
    "DIAMOND"    : 5,
    "MASTER"     : 6,
    "CHALLENGER" : 7,
    "UNRANKED"   : 0
}

def find_fill (players):
    print "Guessing with heuristic..."
    if len(players) == 4:
        for x in xrange(5):
            if x + 1 not in players:
                players.append(x + 1)
                return x + 1
    return 0

def cleanup_pregame(match):

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

    # Pre-load all the summoner spells, champions, etc
    for k in summoner_spells:
        d[summoner_spells[k]] = [0] * NUM_PLAYERS

    champs = {}
    for k in champions:
        championId = champions[k]
        champKey = "c" + str(championId)
        d[champKey] = [0] * NUM_PLAYERS
        champs[championId] = k

    for k in season_tiers:
        d[k] = [0] * NUM_PLAYERS

    d['winner'] = [0] * NUM_PLAYERS

    playersBlue = []
    playersRed = []

    for participant in participants:

        # Grab the participant id
        participantId = participant["participantId"]
        role = participant['timeline']['role']
        lane = participant['timeline']['lane']
        if participantId <= 5:
            players = playersBlue
        else:
            players = playersRed

        #########################################
        # This section is to determine which position each player is
        # currently there is BAD meta-data (overlapping roles) on this, so
        # we have a heuristic on how to solve this
        #########################################
        if role == 'SOLO':
            if (lane == 'MID' or lane == 'MIDDLE'):
                playerId = 1
                if playerId in players:
                    x = find_fill(players)
                    if x == 0:
                        print players
                        print role, lane, champs[participant['championId']]
                        assert False
                players.append(playerId)
            elif (lane == 'TOP'):
                playerId = 2
                if playerId in players:
                    playerId = 3
                    if playerId in players:
                        playerId = 1
                        if playerId in players:
                            playerId = 4
                            if playerId in players:
                                x = find_fill(players)
                                if x == 0:
                                    print players
                                    print role, lane, champs[participant['championId']]
                                    assert False
                players.append(playerId)
            elif (lane == 'BOTTOM' or lane == 'BOT'):
                playerId = 3
                if playerId in players:
                    x = find_fill(players)
                    if x == 0:
                        print players
                        print role, lane, champs[participant['championId']]
                        assert False
                players.append(playerId)
            else:
                x = find_fill(players)
                if x == 0:
                    print "Found (lane, role):", lane, role, participant['championId']
                    assert False
        elif lane == 'TOP':
            playerId = 2
            if playerId in players:
                if role == 'DUO_SUPPORT':
                    playerId = 4
                else:
                    playerId = 3
                if playerId in players:
                    x = find_fill(players)
                    if x == 0:
                        print participantId, role, lane, champs[participant['championId']]
                        print playersBlue, playersRed
                        assert False
            else:
                players.append(playerId)
        elif role == 'DUO_CARRY' or role == 'DUO':
            if lane == 'MIDDLE' or lane == 'MID':
                playerId = 1
            else:
                playerId = 3
                if playerId in players:
                    playerId = 4
                    if playerId in players:
                        playerId = 1
                        if playerId in players:
                            x = find_fill(players)
                            if x == 0:
                                print participantId, role, lane, participant['championId']
                                print playersBlue, playersRed
                                assert False
            players.append(playerId)
        elif role == 'DUO_SUPPORT':
            playerId = 4
            if playerId in players:
                playerId = 5
                if playerId in players:
                    playerId = 2 
                    if playerId in players:
                        x = find_fill(players)
                        if x == 0:
                            print participantId, role, lane, champs[participant['championId']]
                            print playersBlue, playersRed
                            assert False
            players.append(playerId)
        elif role == 'NONE':
            playerId = 5
            if playerId in players:
                if lane == 'BOTTOM' or lane == 'BOT':
                    playerId = 4
                    if playerId in players:
                        playerId = 3
                        if playerId in players:
                            print participantId, role, lane, champs[participant['championId']]
                            print playersBlue, playersRed
                            assert False
                else:
                    playerId = 2
                    if playerId in players:
                        playerId = 3
                        if playerId in players:
                            playerId = 1
                            if playerId in players:
                                playerId = 4
                                if playerId in players:
                                    print participantId, role, lane, champs[participant['championId']]
                                    print playersBlue, playersRed
                                    assert False
            players.append(playerId)
        else:
            x = find_fill(players)
            if x == 0:
                print participantId, role, lane, participant['championId']
                print playersBlue, playersRed
                assert False

        ###############################
        # END HEURISTIC
        ###############################

        d['winner'][playerId - 1] = participant['stats']['winner']


        for k in participant:

            # Skip post-game stats
            if k == "timeline" or k == "stats":
                continue

            # Skip these keys (noise):
            if k == "teamId" or k == "masteries" or k == "runes" or k == "participantId":
                continue

            # Spell1Id and spell2Id are special categorical variables
            if k == "spell1Id":
                spell1Id = participant[k]
                spellName = summoner_spells[spell1Id]
                d[spellName][playerId - 1] = 1
                continue

            if k == "spell2Id":
                spell2Id = participant[k]
                spellName = summoner_spells[spell2Id]
                d[spellName][playerId - 1] = 1
                continue

            if k == 'championId':
                championId = participant[k]
                champKey = "c" + str(championId)
                d[champKey][playerId - 1] = 1
                continue

            if k == "highestAchievedSeasonTier":
                tier = participant["highestAchievedSeasonTier"]
                d[tier][playerId - 1] = 1
                continue

    # Get number of keys:
    num_keys = len(d.keys())
    row = []

    # Create a flatten row based on this dictionary
    for i in xrange(10):
        for k in d:
            if k == 'winner':
                continue
            if not d[k][i]:
                row.append(0)
                # row.append(k)
            elif d[k][i] == True:
                row.append(1.)
                # row.append(k)
            else:
                row.append(float(d[k][i]))
                # row.append(k)

    blue_win = 0
    if d['winner'][0] == True:
        blue_win = 1.
    return row, blue_win


def data_cleanup(filenames):
    
    matches_matrix = []
    winners_matrix = []
    for fname in filenames:

        with open(fname) as json_data:

            # data is { 'matches' : [...]}
            data = json.load(json_data)
            matches = data['matches']
            # Clean up some of the data, i.e. delete unnecessary key-value pairs
            for i in xrange(len(matches)):
                match = matches[i]
                clean_match, winner = cleanup_pregame(match)
                matches_matrix.append(clean_match)
                winners_matrix.append(winner)
    
            # Dump the file after updating it
            # with open (("clean_" + str(i) + ".csv"), "wb") as outfile:
            #   wr = csv.writer(outfile, quoting=csv.QUOTE_ALL)
            #   for row in matches_matrix:
            #       wr.writerow(row)

    return matches_matrix, winners_matrix

if __name__ == '__main__':

    matches_matrix = data_cleanup()
                
