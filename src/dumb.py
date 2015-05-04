import json

def dumbmoney(matches, param):
	total = 0
	correct = 0
	
	for match in matches:
		team1metric = 0
		team2metric= 0
		for player in match['participants']:
			if player["teamId"] == 100:
				team1metric += player['stats'][param]
			else:
				team2metric += player['stats'][param]
		
		speculatedwinner = -1
		if team1metric > team2metric:
			speculatedwinner = 100
		else:
			speculatedwinner = 200
		
		winner = -2
		for team in match['teams']:
			if team['winner']:
				winner = team['teamId']
		
		if speculatedwinner == winner:
			correct += 1
		
		total += 1
	print "Using naive with param:", param, correct, total

if __name__ == '__main__':
	filenames = ['m1.json', 'm2.json', 'm3.json', 'm4.json', 'm5.json']
	for file in filenames:
		with open(file) as json_data:
			matches = json.load(json_data)['matches']
			dumbmoney(matches, 'goldEarned')
			dumbmoney(matches, 'kills')