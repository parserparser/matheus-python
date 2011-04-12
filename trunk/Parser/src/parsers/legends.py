'''
Created on 08/04/2011

@author: Matheus
'''

import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup as Soup
import datetime
import re

from util import basics


sports = {
        'basketball':{
            'NBA - Second Half':'https://www.secureserver365.com/BOSSWagering/Sportsbook/InternetWagering2010-03a2/IBLines/Lines8.asp?SPORTTYPES=2&DUMMY=10&SSC=3940'
            #'ncaa':'http://'
        },
        'baseball':{
            'mlb':'https://www.secureserver365.com/BOSSWagering/Sportsbook/InternetWagering2010-03a2/IBLines/Lines8.asp?SPORTTYPES=15&DUMMY=10&SSC=3940'
        },
        'soccer':{
            'Soccer - English Premier League': 'https://www.secureserver365.com/BOSSWagering/Sportsbook/InternetWagering2010-03a2/IBLines/Lines8.asp?SPORTTYPES=15&DUMMY=10&SSC=3940'
        }
}




class LegendsParser:
    
    def get_browser(self):
        # Browser
        browser = mechanize.Browser()
        
        # Cookie Jar
        cj = cookielib.LWPCookieJar()
        browser.set_cookiejar(cj)
        
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
        
        browser = self.login(browser)
        
        return browser
    
    def login(self, browser):
        # The site we will navigate into, handling it's session
        browser.open('http://www.legends.com')
        
        
        browser.select_form(nr=0)
        
        # User credentials
        browser.form['txtcode'] = 'zz48649'
        browser.form['txtpassword'] = 'fuckme11'
        
        # Login
        browser.submit()
        
        browser.select_form(nr=0)
        browser.submit()
        
        browser.select_form(nr=0)
        browser.submit()
        
        return browser
    
    
    
    def get_scores(self, sport):
        if sport not in sports.keys():
            return 
        
        browser = self.get_browser()
        
        
        leagues_dict = sports[sport]
        leagues = leagues_dict.keys()
        
        for league in leagues:
            url = leagues_dict[league]
            html = browser.open(url).read()
            self.parser_scores(sport, league, html)
    
    
    
    def parser_scores(self, sport, league, html):
        
        #regex = re.compile(r'id=\'(header[0-9]+)\'', re.IGNORECASE)
        #ids = re.findall(regex, html)
        
        soup = Soup(html)
        form = soup.findAll('form', {'id':'frmLines', 'name':'frmLines'})
        divs = form[0]('div')
        div = None
        
        if(len(divs) == 0):
            return
        
        for i in range(0, len(divs), 2):
            
            title = divs[i]('strong')[0].contents[2]
            #print title.upper() + ' - ' + league.upper()
            if title.upper() == league.upper(): # Substituir por League
                div = divs[i+1]
                break
        
        if not div:
            return
        
        trs = div('tr', {'class':'RCB'})
        
        for i in range(0, len(trs), 3):
            date = trs[i]('strong')[0].contents[0]
            
            tds1 = trs[i+1]('td')
            team1 =  tds1[0].contents[0] 
            money1 = tds1[1].contents[0]
            spread1 = tds1[2].contents[0]
            total1 = tds1[3].contents[0]
            
            tds2 = trs[i+2]('td')
            team2 =  tds2[0].contents[0] 
            money2 = tds2[1].contents[0]
            spread2 = tds2[2].contents[0]
            total2 = tds2[3].contents[0]
            
            basics.BasicLine('Legends', sport, league, 'full overtime', 'Money Line', 
                             team1, team2, 0, 0, odds, 
                             side, spread, overunder, max_bet, min_bet, 
                             commission, date, event_time, 
                             locked=False, expiration="", extra_data="")
        '''
        
            INSTACIAR OS OBJETOS E RETORNAR
         
        '''

if __name__ == '__main__':
    
    legends = LegendsParser()
    legends.get_scores('basketball')
    