import os
from RetroSheet import Play, RetroSheet

event_dir = '../data/events/'
roster_dir = '../data/rosters/'

rs = RetroSheet()

dir_list = os.listdir(roster_dir)
for file in dir_list:
    team = file[0:3]
    year = file[3:7]
    if team not in ["ALS", "NLS"]:
        print(f"Parsing Players {year} season of {team}")
        rs.parse_roster_file(roster_dir + file, year)

dir_list = os.listdir(event_dir)
for file in dir_list:
    year = file[0:4]
    team = file[4:7]
    print(f"Parsing Events {year} season of {team}")
    rs.parse_game_file(event_dir + file, year, team)

rs.link_away_games('2023')

for year in rs.seasons:
    for team in rs.seasons[year].teams:
        print(f"{year} : {team} : game count: {len(rs.seasons[year].teams[team])}")

print(f"Yankee season was {len(rs.seasons['2023'].teams['NYA'])} games long")

longest_pitch_count = None
pitch_count = 0
game_id = ''
visteam = ''
hometeam = ''
for year in rs.seasons:
    for team in rs.seasons[year].teams:
        games = rs.seasons[year].teams[team]
        for key in games:
            game = games[key]
            if game.info['hometeam'] != team:
                continue
            for play in game.plays:
                if type(play) is Play:
                    pc = play.pitch_count()
                    if pc > pitch_count:
                        longest_pitch_count = play
                        pitch_count = pc
                        game_id = game.game_id
                        visteam = game.info['visteam']
                        hometeam = game.info['hometeam']
                    if pc > 10:
                        print(f"Game {game.game_id}: pitchcount: {pc}, Plays: {play.__dict__}")

print(f"Longest at bat was by {rs.players[longest_pitch_count.player_id].name}")
print(f"LONGEST: Game {game_id}: {visteam} vs {hometeam}: pitchcount: {pitch_count}, Plays: {longest_pitch_count.__dict__}")
