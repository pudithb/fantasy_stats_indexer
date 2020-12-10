import requests
import json

def main():
    #this is hard coding the position codes, used for creating the lineups
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
    
    #loading/ creating all the necessary info
    try:
        #load cached info
        with open('cached_creds.json') as j:
            creds = json.load(j)
    except:
        #no cached file found? Do things...
        print("You need a creds file first lets make that for next time! \nConsult README.md for what these are and the formats")
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

    

main()


