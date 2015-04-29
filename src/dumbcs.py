import json

total = 0
correct = 0
with open('matches_1.json') as json_data:
    matches = json.load(json_data)['matches']
    for match in matches:
        team1gold = 0
        team2gold = 0
        for player in match['participants']:
            if player["teamId"] == 100:
                team1gold += player['stats']['goldEarned']
            else:
                team2gold += player['stats']['goldEarned']
        
        speculatedwinner = -1
        if team1gold > team2gold:
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

print correct, total