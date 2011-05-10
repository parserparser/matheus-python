#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 08/04/2011

@author: Matheus
'''

import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup as Soup
from datetime import datetime
import re

from util import basics, parser_exception
import util.equity as equity



sports = {
        'basketball':{
            'NBA':'https://www.secureserver365.com/BOSSWagering/Sportsbook/InternetWagering2010-03a2/IBLines/Lines8.asp?SPORTTYPES=2&DUMMY=10&SSC=3940',
            'NCAA':'https://www.secureserver365.com/BOSSWagering/Sportsbook/InternetWagering2010-03a2/IBLines/Lines8.asp?SPORTTYPES=2&DUMMY=10&SSC=3940'
        },
        'baseball':{
            'MLB - National League':'https://www.secureserver365.com/BOSSWagering/Sportsbook/InternetWagering2010-03a2/IBLines/Lines8.asp?SPORTTYPES=15&DUMMY=10&SSC=3940',
            'MLB - American League':'https://www.secureserver365.com/BOSSWagering/Sportsbook/InternetWagering2010-03a2/IBLines/Lines8.asp?SPORTTYPES=15&DUMMY=10&SSC=3940'
        }
}




class LegendsParser:
    
    browser = None
    logged = None
    
    def __init__(self):
        self.browser = self.get_browser()
        self.logged = False
    
    def get_browser(self):
        # Browser
        browser = mechanize.Browser()
        
        # Cookie Jar
        #cj = cookielib.LWPCookieJar()
        #browser.set_cookiejar(cj)
        
        # Browser options
        browser.set_handle_equiv(True)
        #browser.set_handle_gzip(True)
        browser.set_handle_redirect(True)
        browser.set_handle_referer(True)
        browser.set_handle_robots(False)
        
        # Follows refresh 0 but not hangs on refresh > 0
        browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        
        # User-Agent (this is cheating, ok?)
        browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        
        return browser
    
    def login(self):
        
        try:
            # The site we will navigate into, handling it's session
            self.browser.open('http://www.legends.com')
            
            
            self.browser.select_form(nr=0)
            
            # User credentials
            self.browser.form['txtcode'] = 'zz48649'
            self.browser.form['txtpassword'] = 'fuckme11'
            
            # Login
            self.browser.submit()
            
            self.browser.select_form(nr=0)
            self.browser.submit()
            
            self.browser.select_form(nr=0)
            self.browser.submit()
            self.logged = True
        except Exception:
            raise parser_exception.LoginError()
    
    
    
    def get_lines(self, sport):
        
        if(not self.logged):
            self.login()
        
        if sport not in sports.keys():
            return 
        
        leagues_dict = sports[sport]
        leagues = leagues_dict.keys()
        
        for league in leagues:
            url = leagues_dict[league]
            html = self.browser.open(url).read()
            yield self.parser_scores(sport, league, html)
    
    
    
    def parser_scores(self, sport, league, html):
        
        all_lines = []
        
        soup = Soup(html)
        form = soup.findAll('form', {'id':'frmLines', 'name':'frmLines'})
        divs = form[0]('div')
        div = None
        
        if(len(divs) == 0):
            return all_lines
        
        for i in range(0, len(divs), 2):
            
            title = str(divs[i]('strong')[0].contents[2]).strip()
            if title.upper() == league.upper(): 
                div = divs[i+1]
                break
        
        if not div:
            return all_lines
        
        trs = div('tr', {'class':'RCB'})
        
        for i in range(0, len(trs), 3):
            date_str = trs[i]('strong')[0].contents[0]
            date_str = datetime.now().strftime('%Y-%m-%d ') + date_str[-8:]
            date = datetime.strptime(date_str, '%Y-%m-%d %I:%M %p')
            
            
            # Getting frist team
            
            tds1 = trs[i+1]('td')
            team1 =  tds1[0].contents[0].split('. ')[1]
            team1_number = tds1[0].contents[0].split('. ')[0]
            
            try:
                money1 = int(tds1[1]('a')[0].contents)
            except:
                money1 = 1
            
            
            spread_odds1 = tds1[2]('a')[0].contents[0]
            spread1 = float(spread_odds1.split(' ')[0].replace(u'½', '.5'))
            odds = equity.to_decimal(int(spread_odds1.split(' ')[1]))
            total1 = tds1[3]('a')[0].contents[0].replace(u'½', '.5')
            overunder = float(total1.split()[1])
            
            
            # Getting second team
            
            tds2 = trs[i+2]('td')
            team2 =  tds2[0].contents[0].split('. ')[1]
            team2_number = tds2[0].contents[0].split('. ')[0]
            
            try:
                money2 = int(tds2[1]('a')[0].contents)
            except:
                money2 = 1
            
            spread_odds2 = tds2[2]('a')[0].contents[0]
            spread2 = float(spread_odds2.split(' ')[0].replace(u'½', '.5'))
            total2 = tds2[3]('a')[0].contents[0].replace(u'½', '.5')
            
            
                        
            line1 = basics.BasicLine('Legends', sport, league, 'full overtime', 'spread', 
                                     team1, team2, team1_number, team2_number, odds, 
                                     team1, spread1, overunder, 1000.0, 0.5, 
                                     0, date.strftime('%d-%m-%y'), date.strftime('%I:%M %p')) 
            
            line2 = basics.BasicLine('Legends', sport, league, 'full overtime', 'spread', 
                                     team1, team2, team1_number, team2_number, odds, 
                                     team2, spread2, overunder, 1000.0, 0.5, 
                                     0, date.strftime('%d-%m-%y'), date.strftime('%I:%M %p')) 
                        
            all_lines.extend([line1, line2])
            return all_lines



if __name__ == '__main__':
    
    legends = LegendsParser()
    legends.login()
    
    for lines in legends.get_lines('baseball'):
        print lines
    