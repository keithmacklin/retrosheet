import re
import csv

class RetroSheet:
    def __init__(self):
        self.seasons = {}
        self.players = {}

    def parse_game_file(self, filename, year, team):
        game = Game('')
        if year not in self.seasons:
            self.seasons[year] = Season()

        if team not in self.seasons[year].teams:
            games = {}
            self.seasons[year].teams[team] = games

        with open(filename, 'r') as csvfile:
            datareader = csv.reader(csvfile)
            for row in datareader:
                match row[0]:
                    case "id":
                        id = row[1]
                        game = Game(id)
                        games[id] = game
                    case "com":
                        game.plays.append(Com(row[1]))
                    case "data":
                        game.data.append(Data(row[1], row[2], row[3]))
                    case "info":
                        game.info[row[1]] = row[2]
                    case "play":
                        game.plays.append(Play(row[1], row[2], row[3], row[4], row[5], row[6]))
                    case "radj":
                        game.plays.append(Radj(row[1], row[2]))
                    case "start":
                        game.start.append(StartSub(row[0], row[1], row[2], row[3], row[4], row[5]))
                    case "sub":
                        game.plays.append(StartSub(row[0], row[1], row[2], row[3], row[4], row[5]))

        for key in games:
            games[key].compute_score()

    def link_away_games(self, year):
        for team in self.seasons[year].teams:
            for game in self.seasons[year].teams[team]:
                visteam = self.seasons[year].teams[team][game].info['visteam']
                self.seasons[year].teams[visteam][game] = self.seasons[year].teams[team][game]

    def parse_roster_file(self, filename, year):
        with open(filename, 'r') as csvfile:
            datareader = csv.reader(csvfile)
            for row in datareader:
                id = row[0]
                if id not in self.players:
                    self.players[id] = Player(id, f"{row[2]} {row[1]}", row[3], row[4], row[5], row[6], year)
                elif year not in self.players[id].teams:
                    self.players[id].teams[year] = [row[3]]
                else:
                    self.players[id].teams[year].append(row[3])


class Player:
    def __init__(self, id, name, throws, bats, team, position, year):
        self.id = id
        self.name = name
        self.throws = throws
        self.bats = bats
        self.teams = {year: [team]}
        self.position = position


class Season:
    def __init__(self):
        self.teams = {}


class Game:
    def __init__(self, game_id):
        self.game_id = game_id
        self.plays = []
        self.start = []
        self.info = {}
        self.data = []
        self.score = [0, 0]

    def compute_score(self):
        for play in self.plays:
            if type(play) is Play:
                runs = len(re.findall("[H]", play.event.replace("TH", "").replace("SH", "").replace("HP", "")))
                if runs > 0:
                    self.score[int(play.home_visitor)] += runs


class Com:
    def __init__(self, comment):
        self.comment = comment


class Data:
    def __init__(self, type, player_id, runs):
        self.type = type
        self.player_id = player_id
        self.runs = runs


class Id:
    def __init__(self, game_id):
        self.game_id = game_id


class Play:
    def __init__(self, inning, home_visitor, player_id, count, pitches, event):
        self.inning = inning
        self.home_visitor = home_visitor
        self.player_id = player_id
        self.count = count
        self.pitches = pitches
        self.event = event

    def pitch_count(self):
        pat = "[A-Z,a-z]"
        return len(re.findall(pat, self.pitches))


class Radj:
    def __init__(self, player_id, base):
        self.player_id = player_id
        self.base = base


class StartSub:
    def __init__(self, type, player_id, player_name, home_visitor, batting_position, fielding_position):
        self.type = type
        self.player_id = player_id
        self.player_name = player_name
        self.home_visitor = home_visitor,
        self.batting_position = batting_position
        self.fielding_position = fielding_position
