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
        'nba':'',
        'ncaa':''
    },
    'baseball':{
        'mlb':''
    }
}

sports_preloading_urls = {
    'basketball':['', ''],
    'baseball':['', '']
}


class bet365Parser:
    
    def get_lines(self, sport):
        if (sport not in sports_links.keys()):
            return
        
        leagues_dict = sports_links[sport]
        leagues = sports_links[sport].keys()
        for league in leagues:
            url = leagues_dict[league]
            yield self.get_lines_for_league(url, sport, league)
    
    
    
    def get_lines_for_league(self, url, sport, league):
        br = mechanize.Browser()
        br.set_handle_robots(None)

        for preloading_url in sports_preloading_urls[sport]:
            br.open(preloading_url)

        br.open(url)

        html = br.response().read()
        soup = BeautifulSoup.BeautifulSoup(html)
        
        lines = []
        
        #TODO: Iterar elementos HTML e preencher lines