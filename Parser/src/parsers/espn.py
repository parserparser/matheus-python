#!/usr/bin/env python

'''
Created on 02/04/2011

@author: Matheus
'''

from util.basics import BasicResult
from util import equity

import mechanize
from BeautifulSoup import BeautifulSoup as Soup
from datetime import datetime
import time
import re


urls = {
    'basketball': {
        'nba':'http://scores.espn.go.com/nba/scoreboard',
        'ncaa':'http://scores.espn.go.com/ncb/scoreboard',
    },
    'baseball': {
        'mlb':'http://scores.espn.go.com/mlb/scoreboard'
    }
}


class EspnParser(object):
    
    def get_mech(self, proxies=None):
        self.mech = mechanize.Browser()
        self.mech.set_handle_robots(None)
        
        if proxies is not None:
            self.mech.set_proxies(proxies)
        self.mech.addheaders = [('User-agent', "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)")]
        return self.mech
    
    
    
    def get_scores(self, sport, date=None):
        self.mech = self.get_mech()
        
        if not date:
            date = datetime.today()
        
        date_url = date.strftime("%Y%m%d")
        date_formated = date.strftime("%d/%m/%Y")
        
        for league in urls.get(sport, []):
            url = urls[sport][league]
            if date:
                url = url + '?date=' + date_url
            html = self.mech.open(url).read()
            
            yield self.parser_scores(sport, league, date_formated, html)
    
           
    
    def parser_scores(self, sport, league, date, html):
        
        scores = []
        regex = re.compile(r'id="([0-9]+)-gameDetails', re.IGNORECASE)
        ids = re.findall(regex, html)
        soup = Soup(html)
        
        for id in ids:
            divs = soup('div', {'id':id+'-gamebox'})
            div = divs[0]
            
            a = div('a')
            team1 = a[0].contents[0]
            team2 = a[1].contents[0]
            
            status = self.get_status(div, sport, league)
            
            tables = div('table', {'class':'game-details'})
            table = tables[0]
                        
            tbodys = table('tbody')
            tbody = tbodys[0]
            
            trs = tbody('tr')
            
            point1, point2 = self.get_points(trs, sport, league)
                        
            scores.append( BasicResult(sport, league, date, team1, team2,
                           0, 0, point1, point2, status))
        return scores
    
    
    
    def get_status(self, div, sport, league):
        
        st1 = div('li')
        
        if len(st1[0].contents) == 0:
            st1[0].contents.append('')
        
        st2 = div('span')
        
        if len(st2[0].contents) == 0:
            st2[0].contents.append('')
        
        status = st1[0].contents[0] + ' ' + st2[0].contents[0]
        status = status.replace('&nbsp;', ' ')
        
        return str.strip(str(status))
    
    
    
    def get_points(self, trs, sport, league):
        tds = []
        tds.append(trs[0]('td'))
        tds.append(trs[1]('td'))
        point1 = point2 = None
        
        if sport == 'basketball':
            point1, point2 = tds[0][-1].contents[0], tds[1][-1].contents[0]
        
        elif sport == 'baseball':
            point1, point2 = tds[0][11].contents[0], tds[1][11].contents[0]
        
        point1, point2 = self.format_point(point1), self.format_point(point2)
        
        return point1, point2
        
    
    
    def format_point(self, point):
        if point == u'&nbsp;':
            point = '0'
        return int(point)


if __name__ == '__main__':
    espn = EspnParser()
    scores = espn.get_scores('basketball')
    for score in scores:
        print score
    
    