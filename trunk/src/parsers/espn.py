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
        scores = []
        if not date:
            date = datetime.today()
        
        date_url = date.strftime("%Y%m%d")
        date_formated = date.strftime("%d/%m/%Y")
        
        if sport == 'basketball':
            parser_scores = self.parse_basketball
            
        
        for league in urls.get(sport, []):
            url = urls[sport][league]
            if date:
                url = url + '?date=' + date_url
            html = self.mech.open(url).read()
            
            yield parser_scores(sport, league, date_formated, html)
        
        #return scores    
    
    
    def parse_basketball(self, sport, league, date, html):
        
        scores = []
        regex = re.compile(r'id="([0-9]+)-gameDetails', re.IGNORECASE)
        ids = re.findall(regex, html)
        soup = Soup(html)
        
        for id in ids:
            divs = soup('div', {'id' : id + '-gamebox'})
            div = divs[0]
            
            a = div('a')
            team1 = a[0].contents[0]
            team2 = a[1].contents[0]
            
            st1 = div('li', {'id' : id + '-statusLine1'})
            if len(st1[0].contents) == 0:
                st1[0].contents.append('')
           
            status1 = st1[0].contents[0]
            
            st2 = div('span', {'id' : id + '-statusLine2Left'})
            if len(st2[0].contents) == 0:
                st2[0].contents.append('')
            
            status2 = st2[0].contents[0]
            
            status = str(status1).replace('&nbsp;', ' ') + ' ' + str(status2).replace('&nbsp;', ' ')
            status = str.strip(status)
            
            
            tables = div('table', {'class':'game-details'})
            table = tables[0]
                        
            tbodys = table('tbody')
            tbody = tbodys[0]
            
            trs = tbody('tr')
            tr1 = trs[0]
            tr2 = trs[1]
            
            tds = tr1('td')
            if league == 'nba':
                tds = tds[3:]
                tds.pop(4)
            elif league == 'ncaa':
                tds = tds[4:]
                tds.pop(2)
                
            points1 = [td.contents[0] for td in tds]
            
            tds = tr2('td')
            if league == 'nba':
                tds = tds[3:]
                tds.pop(4)
            elif league == 'ncaa':
                tds = tds[4:]
                tds.pop(2)
            
            points2 = [td.contents[0] for td in tds]
            
            points1 = self.format_points(points1)
            points2 = self.format_points(points2)
            
            scores.append( BasicResult(sport, league, date, team1, team2,
                           0, 0, int(points1[-1]), int(points2[-1]), status))
        return scores
    
    
    def parse_baseball(self, sport, league, date, html):    
        pass
    
    
    
    def format_points(self, points):
        for i in range(len(points)):
            if points[i] == u'&nbsp;':
                points[i] = ''
        
        return points


if __name__ == '__main__':
    espn = EspnParser()
    scores = espn.get_scores('basketball')
    for score in scores:
        print score
    
    