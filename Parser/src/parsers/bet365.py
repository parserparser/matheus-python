'''
Created on 07/04/2011

@author: Matheus
'''

import mechanize
import BeautifulSoup
from util import basics
import datetime


sports_links = {
    'basketball':{
        'nba':'http://www.bet365.com/home/mainpage.asp?rn=32517127837'
        #'ncaa':''
    },
    'baseball':{
        'mlb':''
    }
}

sports_preloading_urls = {
    'basketball':['http://www.bet365.com', 'http://www.bet365.com/home/default.asp?']
    #'baseball':['', '']
}


class Bet365Parser:
    
    def get_lines(self, sport):
        if (sport not in sports_links.keys()):
            return
        
        leagues_dict = sports_links[sport]
        leagues = sports_links[sport].keys()
        for league in leagues:
            url = leagues_dict[league]
            self.get_lines_for_league(url, sport, league)
    
    
    
    def get_lines_for_league(self, url, sport, league):
        br = mechanize.Browser()
        br.set_handle_robots(None)

        for preloading_url in sports_preloading_urls[sport]:
            br.open(preloading_url)
        
        br.open(url)
        html = br.response().read()
        
        
        soup = BeautifulSoup.BeautifulSoup(html)
        
        frame = soup('iframe')
        print frame
        
        
if __name__ == '__main__':
    bet355 = Bet365Parser()
    bet355.get_lines('basketball')