# Fantasy Stats Puller

Create a raw pull of json formatted information from ESPNs Fantasy API

# Initial Setup

```sh
$ git clone https://github.com/pudithb/fantasy_stats_indexer.git
$ cd fantasy_stats_indexer
$ pip3 install -r requirements.txt
```

# Credentials
ESPNs Fantasy API doesnt seem to have any real public interface to get a key, instead we will make the requests look like they are coming from a logged in device

### League ID
* Login to the ESPN Fantasy [webpage](https://fantasy.espn.com/football/)
* You should now see that your URL has changed to contain your league id
    * eg. https://fantasy.espn.com/football/team?leagueId=12345678&teamId=1&seasonId=2020

### SWID 
* Once Logged into ESPN Fantasy open developer console (<kbd>CTRL</kbd>+<kbd>SHIFT</kbd>+<kbd>I</kbd>)
* Go to the application tab and find SWID 
    * eg. A1B2C3D4-A1B2-A1B2-A1B2-A1B2C3D4E5F6

### ESPN_LONG
* Once Logged into ESPN Fantasy open developer console (<kbd>CTRL</kbd>+<kbd>SHIFT</kbd>+<kbd>I</kbd>)
* Go to the application tab and find espn_s2 
    * This is a long alphanumeric string

# Default Values
Some values are hardcoded just because they are common league formats. These can be changed if your league uses a different format
### Positions and Structures
Positions variable, defined on ln 106, looks like this:
```python
positions = ['QB', 'RB', 'WR', 'Flex', 'TE', 'D/ST', 'K']
```
Defines the positions that your league uses.

Structure variable, defined on ln 107, looks like this:
```python
structure = [1, 2, 2, 1, 1, 1, 1]
```
This denotes the number of players at each position, in this case:

| Position  | Count |
| ------------- | ------------- |
| QB  | 1  |
| RB  | 2  |
| WR  | 2  |
| Flex  | 1  |
| TE  | 1  |
| D/ST  | 1  |
| K  | 1  |

Edit these if that applies to your league, some functionality may need to be adjusted in the data_process() function

# Usage

```sh
$ python pull_data.py
```

If this is the first time running the script will run you through setting up your credentials (To Find where to get your credentials check in the Credentials sections)

A file will be output to the working directory with a EPOCH Timestamp as the name. 

# Whats the point?
Get some data analysis going with the data you pull on your league and players.

My implementation involves forwarding these logs to a Splunk Instance on my network while I learn to use some of the data analysis features better.
