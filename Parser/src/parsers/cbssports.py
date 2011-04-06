#!/usr/bin/env python

from util.basics import BasicResult
from util import equity

import mechanize
from BeautifulSoup import BeautifulSoup as Soup
import datetime
import time
import re

urls = {
    'basketball': {
        'ncaa':'http://www.cbssports.com/collegebasketball/scoreboard/',
    },
    'baseball': {
        'mlb':'http://www.cbssports.com/mlb/scoreboard',
    }
}

class CbsParser(object):

    def get_mech(self, proxies=None):
        self.mech = mechanize.Browser()
        self.mech.set_handle_robots(None)
        
        if proxies is not None:
            self.mech.set_proxies(proxies)
        self.mech.addheaders = [('User-agent', "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)")]
        return self.mech

    def get_scores(self, sport, date=None):
        mech = self.get_mech()
        for league in urls.get(sport, []):
            url = urls[sport][league]
            if date:
                if league == 'ncaa':
                    url += 'div1/' + date
                else:
                    url += date
            
            html = mech.open(url).read()
            
            yield self.parse_scores(sport, league, html)


    def parse_scores(self, sport, league, html):
        scores = []
        soup = Soup(html)
        score_divs = soup('div', 'scoreBox')
        date_link = soup('a', 'optsel')[-1]
        date = self.get_date_from_string(date_link.text)
        
        for score_div in score_divs:
            trs = score_div('tr')
            headers = trs[0]('td')
            status = headers[0].text
            last = headers[-1].text
            if (sport == 'basketball') & (last != 'T'):
                # no scores yet, skip this one
                continue
            
            tds1 = trs[1]('td')
            team1 = tds1[0].text
            
            tds2 = trs[2]('td')
            team2 = tds2[0].text
            
            score1, score2 = self.get_points(tds1, tds2, sport, league)
            
            scores.append(self.make_score_from_info(sport, league, date, [team1, team2], ['0', '0'], [score1, score2], status))
        return scores
    
    
    def get_points(self, tds1, tds2, sport, league):
        if sport == 'baseball':
            return int(tds1[10].text) , int(tds2[10].text)
        else:
            return int(tds1[-1].text), int(tds2[-1].text)
    
    
    
    def make_score_from_info(self, sport, league, date, teams, team_numbers, game_scores, status):
        def get_team_name(name):
            name = name.replace('&nbsp;', ' ').strip()
            name = name.replace('&laquo;', '').replace('(', ' (').replace('&#039;', "'")
            if '(' in name:
                parts = name.split()
                good_parts = [p for p in parts if not re.match(r'\(\d+\-\d+\)', p)]
                good_parts = [p for p in good_parts if not p.startswith('#')]
                name = ' '.join(good_parts).strip()
            #if '#' in name:
            #    name = name.split('#')[0].strip()
            
            return name
        team1 = get_team_name(teams[0])
        team2 = get_team_name(teams[1])
        
        team1_number = team_numbers[0].strip()
        team2_number = team_numbers[1].strip()
        score1 = int(game_scores[0])
        score2 = int(game_scores[1])
        if status.upper() == 'FINAL':
            status = status.upper()
        
        # HACK - mercer is getting swapped for some reason
        #if team2 == 'Mercer':
        #    team1, team2 = team2, team1
        #    score1, score2 = score2, score1
        
        score = BasicResult(sport, league, date, team1, team2, team1_number,
                            team2_number, score1, score2, status)
        return score
        
    def get_date_from_string(self, text):
        months = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
                  'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}
        date_parts = text.split()
        
        day = int(date_parts[-1])
        month = months[date_parts[-2]]
        year = datetime.datetime.now().year
        date = '%02d-%02d-%d' % (day, month, year)
        return date

def get_results():
    #from parsers.donbest import send
    parser = CbsParser()
    for results in parser.get_scores('baseball'):
        if not results:
            continue
        data = repr([v.as_dict() for v in results])
        #send(data)

if __name__ == '__main__':
    import sys
    #from parsers.donbest import send
    parser = CbsParser()
    date = None
    if len(sys.argv) >= 2:
        date = sys.argv[-1]
    for scores in parser.get_scores('baseball', date):
        print '-' * 100
        for score in scores:
            print score
        
        if not scores:
            continue
        if '-s' in sys.argv:
            data = repr([v.as_dict() for v in scores])
            #send(data)

