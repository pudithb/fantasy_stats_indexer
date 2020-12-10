import requests
import json

def get_raw(league_id, season, week, swid, espn_long):
    url = 'https://fantasy.espn.com/apis/v3/games/ffl/seasons/{}/segments/0/leagues/{}?view=mMatchup&view=mMatchupScore'.format(str(season), str(league_id))
    raw = requests.get(
        url, 
        params={'scoringPeriodId': week, 'matchupPeriodId': week}, 
        cookies={"SWID": swid, "espn_s2": espn_long}
    )

    return raw.json()

def get_teamnames(league_id, season, week, swid, espn_long):
    url = 'https://fantasy.espn.com/apis/v3/games/ffl/seasons/{}/segments/0/leagues/{}?view=mTeam'.format(str(season), str(league_id))
    
    raw = requests.get(
        url,
        params={'scoringPeriodId': week},
        cookies={"SWID": swid, "espn_s2": espn_long}
    ).json()

    team_names = {tm['id']: tm['location'].strip() + ' ' + tm['nickname'].strip() for tm in raw['teams']}

    return team_names

#this feels like a really hacky implemetation im not happy with this :( note to sober be fix this
def process_teams(teams):
    list_of_teams = []

    for i, j in teams.items():
        list_of_teams.append(j)
    
    return list_of_teams

#another hacky bit of code gotta clean this later
def data_process(raw, teams, week, pos_codes):
    raw_data = []
    index = 0
    
    for team in raw['teams']:
        players = []
        for p in team['roster']['entries']:
            name = p['playerPoolEntry']['player']['fullName']

            slotid = p['lineupSlotId']
            slot = pos_codes[slotid]

            act, proj = 0, 0
            for stat in p['playerPoolEntry']['player']['stats']:
                if stat['scoringPeriodId'] != week:
                    continue
                if stat['statSourceId'] == 0:
                    act = stat['appliedTotal']
                elif stat['statSourceId'] == 1:
                    proj = stat['appliedTotal']
                else:
                    print('something happend idek, seek help from a higher power')

            pos = 'Unk'
            ess = p['playerPoolEntry']['player']['eligibleSlots']
            if 0 in ess: pos = 'QB'
            elif 2 in ess: pos = 'RB'
            elif 4 in ess: pos = 'WR'
            elif 6 in ess: pos = 'TE'
            elif 16 in ess: pos = 'D/ST'
            elif 17 in ess: pos = 'K'

            player_stats = {
                'name': name,
                'slotid': slotid,
                'slot': slot,
                'pos': pos,
                'act': act,
                'proj': proj
            }

            players.append(player_stats)
        
        team_name=teams[index]
        
        for i in players:
            i['team_name'] = team_name
            i['team_id'] = index
            i['week'] = week
            raw_data.append(i)

        index = index + 1

    return raw_data

def main():
    #this is hard coding the defaults change them here or in the creds setup further down
    pos_codes = {
        0 : 'QB', 1 : 'QB',
        2 : 'RB', 3 : 'RB',
        4 : 'WR', 5 : 'WR',
        6 : 'TE', 7 : 'TE',
        16: 'D/ST',
        17: 'K',
        20: 'Bench',
        21: 'IR',
        23: 'Flex'
    }  
    positions = ['QB', 'RB', 'WR', 'Flex', 'TE', 'D/ST', 'K']
    structure = [1, 2, 2, 1, 1, 1, 1]

    #loading/ creating all the necessary info
    try:
        #load cached info
        with open('cached_creds.json') as j:
            creds = json.load(j)
    except:
        #no cached file found? Do things...
        print("You need a creds file!!! Lets make that for next time. \nConsult README.md for what these are and the formats")
        league_id = input("League ID: ")
        positions = input('''Input your positions (default: '['QB', 'RB', 'WR', 'Flex', 'TE', 'D/ST', 'K']'): ''')
        structure = input('''Input your sturcture (default '[1, 2, 2, 1, 1, 1, 1]'): ''')
        swid = input("SWID: ")
        espn_long = input("ESPN_long: ")
        
        creds = {
            'league_id': league_id,
            'positions': positions,
            'structure': structure,
            'swid': swid,
            'espn_long': espn_long
        }
        
        with open('cached_creds.json', 'w') as j:
            json.dump(creds, j)
    
    #More essential info
    season = int(input("Season (year eg. 2020): "))
    week = int(input("Week (number eg. 11): "))

    for i in range(1, week+1):
        week = i
        raw_pull = get_raw(creds['league_id'], season, week, creds['swid'], creds['espn_long'])
        team_names = get_teamnames(creds['league_id'], season, week, creds['swid'], creds['espn_long'])
        teams = process_teams(team_names)
        #another hacky implement that i wanna fix this later
        process_results = data_process(raw_pull, teams, week, pos_codes)



main()


