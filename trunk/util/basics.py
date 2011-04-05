from zope.interface import implements
from interfaces import ILine, IGameResult, IParser, IBettor, IResultsParser, IActiveBettor

class BasicLine(object):

    implements(ILine)

    def __init__(self, site, sport, league, game_part, line_type, team1, team2, team1_num, team2_num, odds,
                 side, spread, overunder, max_bet, min_bet, commission,
                 event_date, event_time, locked=False, expiration="",
                 extra_data=""):

        self.site = site
        self.sport = sport
        self.league = league
        self.game_part = game_part
        self.line_type = line_type
        self.team1 = team1
        self.team2 = team2
        self.team1_number = team1_num
        self.team2_number = team2_num
        self.odds = odds
        self.side = side
        self.spread = spread
        self.overunder = overunder
        self.max_bet = max_bet
        self.min_bet = min_bet
        self.commission = commission
        self.event_date = event_date
        self.event_time = event_time
        self.locked = locked
        self.expiration = expiration
        self.extra_data = extra_data
        if '/' in self.event_date:
            self.event_date = '-'.join(self.event_date.split('/'))
        
        parts = self.event_date.split('-')
        if len(parts) == 3:
            parts = tuple([int(v) for v in parts])
            self.event_date = '%02d-%02d-%d' % tuple(parts)
        
    
    @classmethod
    def from_dict(self, d):
        site = d.get('site')
        if not site:
            site = d.get('sitename')
        
        l = BasicLine(site, d['sport'], d['league'], d.get('game_part', 'full overtime'), d['line_type'],
            d['team1'], d['team2'], d.get('team1_number', '0'), d.get('team2_number', '0'),
            d['odds'], d['side'], d['spread'], d['overunder'], d.get('max_bet', 1000.0), d.get('min_bet', 10.0),
            d.get('commission', 0.0), d.get('event_date', ''), d.get('event_time', ''), 
            extra_data=d.get('extra_data'))
        return l
    
    def __str__(self):
        return "%s: %s - %s at %s %s - (%s) %s @ (%s) %s / %s / %s / %.1f / %.1f / %.1f / $%.2f / $%.2f" % (
            self.site, self.sport, self.league, self.event_date, self.event_time, self.team1_number, self.team1,
            self.team2_number, self.team2, self.line_type, self.side, self.spread, self.overunder, self.odds,
            self.max_bet, self.min_bet)
    
    def __repr__(self):
        return str(self)
    
    def as_dict(self):
        return dict(site=self.site, sport=self.sport, league=self.league, game_part=self.game_part, line_type=self.line_type, 
            team1=self.team1, team2=self.team2, team1_number=self.team1_number, team2_number=self.team2_number, odds=self.odds,
            side=self.side, spread=self.spread, overunder=self.overunder, max_bet=self.max_bet, min_bet=self.min_bet,
            commission=self.commission, event_date=self.event_date, event_time=self.event_time, locked=self.locked, 
            expiration=self.expiration, extra_data=self.extra_data)


class BasicResult(object):

    implements(IGameResult)

    def __init__(self, sport, league, event_date, team1, team2, team1_number, team2_number, final_score1, final_score2, status):
        self.sport = sport
        self.league = league
        self.event_date = event_date
        self.team1 = team1
        self.team2 = team2
        self.team1_number = team1_number
        self.team2_number = team2_number
        self.final_score1 = final_score1
        self.final_score2 = final_score2
        self.status = status
        if '/' in self.event_date:
            self.event_date = '-'.join(self.event_date.split('/'))

    def __str__(self):
        return "%s - %s %s: %s (%s) %d at %d %s (%s) - %s" % (self.sport, self.league, self.event_date, self.team1, self.team1_number, self.final_score1,
            self.final_score2, self.team2, self.team2_number, self.status)
    
    def __repr__(self):
        return str(self)
    
    def as_dict(self):
        return dict(sport=self.sport, league=self.league, event_date=self.event_date, team1=self.team1, team2=self.team2, 
            team1_number=self.team1_number, team2_number=self.team2_number, final_score1=self.final_score1, final_score2=self.final_score2, status=self.status)

class BasicParser(object):

    implements(IParser)

    def setup(self, user, password):
        return False


    def get_lines(self, sport):
        return []


class BasicBettor(object):

    implements(IBettor)

    def setup(self, user, password):
        return False

    def bet(self, line, amount):
        return False

    def confirm(self, line, amount):
        return (False, None, 0.0)


class BasicResultsParser(BasicParser):

    implements(IResultsParser)

    def get_results_past_24(self):
        return []


class BasicActiveBettor(BasicBettor):

    implements(IActiveBettor)

    def get_lines(self, sport, league, page):
        return []
