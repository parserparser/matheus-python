from util import selenium
import os
import sys
import time
import datetime
from BeautifulSoup import BeautifulSoup
from util.basics import BasicLine
from util import equity
#test

kSportsbookUrl = 'http://www.sportsbook.com/'
kLoginButtonId = "header_menu_login"
#kSportsbookUrl = ''


kLoginSelector = 'css=input[name=username]'
kPasswordSelector = 'css=input[name=password]'
kLoginButtonSelector = 'css=input[name=LOGIN]'
kDefaultWait = 45000

class SportsbookBettor(object):

    def login(self, user, password):
        self.selenium = selenium.selenium('localhost', 4444, '*firefox', kSportsbookUrl)
        s = self.selenium
        s.start()
        s.set_timeout(kDefaultWait)
        try:
            s.open(kSportsbookUrl)
        except Exception:
            return False, 0.0, "couldn't open url %s" % kSportsbookUrl
        s.window_maximize()

        s.type(kLoginSelector, user)
        s.type(kPasswordSelector, password)
        s.click(kLoginButtonSelector)
        try:
            s.wait_for_page_to_load(kDefaultWait)
        except Exception:
            return False, 0.0, "couldn't log in"
        time.sleep(1)
        if s.is_element_present('link=Close'):
            time.sleep(1)
            s.click('link=Close')     
        return s

    def bet(self, line, amount):
        try:
            return self.do_bet(line, amount)
        except:
            import traceback
            traceback.print_exc()
            return False, 0.0, 'Exception raised on bettor'

    def get_balance(self):
        balance = self.selenium.get_text('id=custbalance')
        if not balance:
            return 0.0
        self.balance = float(''.join(c for c in balance if c in '0123456789.'))
        return self.balance

    def do_bet(self, line, amount):
        ok = False
        if line.sport == 'basketball':
            link = 'link=Basketball'
            if line.league in ('nba', 'ncaa'):
                ok = True
                if line.league=='ncaa':leaguelink='link=NCAA Lines'
                if line.league=='nba':leaguelink='link=Playoff Lines'
        elif line.sport == 'hockey':
            link = 'link=Hockey'
            if line.league in ('nhl'):
                ok = True
                if line.league=='nhl':leaguelink='link=NHL Lines'
        elif line.sport == 'baseball':
            link = 'link=Baseball'
            if line.league in ('mlb'):
                ok = True
                if line.league=='mlb':leaguelink='link=MLB Lines'
        if not ok:
            return False, 0.0, 'Cannot bet other leagues'

        #date_to_search_for = datetime.datetime.strptime(line.event_date, '%d-%m-%Y').date()
        s = self.selenium
        s.click(link)
        s.wait_for_page_to_load(kDefaultWait)
        s.click(leaguelink)
        s.wait_for_page_to_load(kDefaultWait)
        s.select_frame("BETTING")
        s.select_frame("TICKET")
        balance = self.get_balance()
        if balance < amount:
            return False, 0.0, 'balance too low (%.2f)' % balance
        #remove previous bet attempts if there are any
        if s.is_element_present("link=Remove all"):
            s.click("link=Remove all")
        #make sure line is decimal
        s.select_frame('relative=up')
        if s.get_selected_value("oddsFormatId")!='EURO':
            s.select("oddsFormatId","value=EURO")
            s.wait_for_frame_to_load("ODDS",kDefaultWait)
            time.sleep(2)
        s.select_frame("ODDS")
        #check odds_
        current_odds=float(s.get_attribute("selection["+line.extra_data['id']+"]@value").split('|')[-1])
        if line.odds>current_odds:
            return False, 0.0, 'Odds on the site (%.2f) is lower than wanted (%.2f)' % (current_odds, line.odds)
        current=float(s.get_attribute("selection["+line.extra_data['id']+"]@value").split('|')[-2])/2
        if line.line_type=='overunder':
            if line.side=='under' and current<line.overunder:
                return False, 0.0, 'Under on the site (%.2f) is lower than wanted (%.2f)' % (current,line.overunder)
            elif line.side=='over' and current>line.overunder:
                return False, 0.0, 'Over on the site (%.2f) is higher than wanted (%.2f)' % (current,line.overunder)
        elif line.line_type=='spread':
            if current<line.spread:
                return False, 0.0, 'Spread on the site (%.2f) is not what is wanted (%.2f)' % (current,line.spread)
        s.click("selection["+line.extra_data['id']+"]")
        time.sleep(1)
        s.type("betAmount", amount)
        time.sleep(1)
        s.click("placeBetImg")
        s.wait_for_page_to_load(kDefaultWait)
 #       s.wait_for_frame_to_load("TICKET",kDefaultWait)
        s.select_frame("relative=top")
        s.select_frame("TICKET")
        time.sleep(1)
        s.click("//input[@name='confirm']")
        time.sleep(1)
        s.click("submitImg")
        s.wait_for_page_to_load(kDefaultWait)
        #confirming bet
        s.select_frame("relative=up")
        s.select_frame("relative=up")
        return self.confirm_bet(line)
    
    def confirm_bet(self,line):
        s=self.selenium
        s.click("link=My Account")
        try:
            s.wait_for_page_to_load(kDefaultWait)
            time.sleep(2)
        except Exception:
            return False, 0.0, 'Failed to load page after bet confirmation'
        s.click("link=My Activities")
        try:
            s.wait_for_page_to_load(kDefaultWait)
            time.sleep(1)
        except Exception:
            return False, 0.0, 'Failed to load page after bet confirmation'
        s.click("link=view")
        try:
            s.wait_for_page_to_load(kDefaultWait)
            time.sleep(2)
        except Exception:
            return False, 0.0, 'Failed to load page after bet confirmation'
        s.click("link=View ALL Pending Wagers")
        try:
            s.wait_for_page_to_load(kDefaultWait)
            time.sleep(1)
        except Exception:
            return False, 0.0, 'Failed to load page after bet confirmation'
        s.select_frame("name=myaccount")
        s.select_frame("name=navBarIframe")
        acc_soup=BeautifulSoup(s.get_html_source())
        try:
            bet_id_tag=acc_soup.find("span","pendingHeader")
        except:
            return False, 0.0, 'Failed to find pending bet on page'
        return self.get_conf_info(bet_id_tag,line)
    
    def get_bet_history(self):
        s=self.selenium
        s.select_frame('relative=top')
        s.click("link=My Account")
        try:
            s.wait_for_page_to_load(kDefaultWait)
            time.sleep(2)
        except Exception:
            return False, 0.0, 'Failed to load page after bet confirmation'
        s.click("link=My Activities")
        try:
            s.wait_for_page_to_load(kDefaultWait)
            time.sleep(1)
        except Exception:
            return False, 0.0, 'Failed to load page after bet confirmation'
        s.click("link=view")
        try:
            s.wait_for_page_to_load(kDefaultWait)
            time.sleep(2)
        except Exception:
            return False, 0.0, 'Failed to load page after bet confirmation'
        s.click("link=View Pending and Processed Wagers (last 30 days)")
        try:
            s.wait_for_page_to_load(kDefaultWait)
            time.sleep(1)
        except Exception:
            return False, 0.0, 'Failed to load page after bet confirmation'
        s.select_frame("name=myaccount")
        s.select_frame("name=navBarIframe")
        acc_soup=BeautifulSoup(s.get_html_source())
        return self.get_bet_history_info(acc_soup)
    
    def get_wagered(self):
        wagered=0
        s=self.selenium
        s.select_frame('relative=top')
        s.click("link=My Account")
        try:
            s.wait_for_page_to_load(kDefaultWait)
            time.sleep(2)
        except Exception:
            return False, 0.0, 'Failed to load page after bet confirmation'
        s.click("link=My Activities")
        try:
            s.wait_for_page_to_load(kDefaultWait)
            time.sleep(1)
        except Exception:
            return False, 0.0, 'Failed to load page after bet confirmation'
        s.click("link=view")
        try:
            s.wait_for_page_to_load(kDefaultWait)
            time.sleep(2)
        except Exception:
            return False, 0.0, 'Failed to load page after bet confirmation'
        s.click("link=View ALL Pending Wagers")
        try:
            s.wait_for_page_to_load(kDefaultWait)
            time.sleep(1)
        except Exception:
            return False, 0.0, 'Failed to load page after bet confirmation'
        s.select_frame("name=myaccount")
        s.select_frame("name=navBarIframe")
        acc_soup=BeautifulSoup(s.get_html_source())
        bets=acc_soup.findAll("span","pendingHeader")
        for bet in bets:
            offset=0
            spans=bet.findAllNext(name="span",limit=10)
            bet_amount=float(spans[2+offset].text.split(' ')[1])
            wagered+=bet_amount
        return wagered

    def get_bet_history_info(self,acc_soup):
        bets=acc_soup.findAll("span","pendingHeader")

        for bet in bets:
            offset=0
            bet_id=bet.text.split()[-1][3:]
            spans=bet.findAllNext(name="span",limit=10)
            (bet_placed_date,bet_placed_time)=spans[1].text.split()
            bet_placed_date=bet_placed_date[3:5]+'-'+bet_placed_date[0:2]+'-20'+bet_placed_date[6:8]
            bet_placed_time=bet_placed_time.split('&nbsp;')[0]
            if spans[2].text=='':
                offset=2
                paid_amount=float(spans[2+offset].text.split()[6][:-1])
            else:
                offset=0
                paid_amount=0
            result=spans[3+offset].text.split(' ',1)[1]
            bet_amount=float(spans[2+offset].text.split(' ')[1])
            bet_odds=(float(spans[2+offset].text.split()[4])+bet_amount)/bet_amount
            (team1,team2)=[a for a in str(spans[4+offset]).replace('<br />','')[6:-7].split() if not a.isdigit()]
            (event_datetime,side,criteria)=spans[5+offset].text.split()
            event_date=event_datetime[3:5]+'-'+event_datetime[0:2]+'-20'+event_datetime[6:8]
            event_time=event_datetime.split('(')[-1]
            side=side[3:]
            criteria=float(criteria)
            spread=''
            overunder=criteria
            line_type='overunder'
            if not (side=='Over' or side=='Under'):
                if abs(equity.to_decimal(criteria)-bet_odds)<.01:
                    line_type='Moneyline'
                    overunder=''
                else:
                    line_type='Spread'
                    spread=criteria
                    overunder=''
            print result,bet_id,bet_amount,bet_odds,paid_amount,bet_placed_date, bet_placed_time,team1,team2,event_date,event_time,side,line_type,"spread",spread,"overunder",overunder
    
    def get_conf_info(self,bet_id_tag,line):
        bet_id=bet_id_tag.text[3:]
        spans=bet_id_tag.findAllNext(name="span",limit=10)
        bet_amount=float(spans[2].text.split(' ')[1])
        bet_odds=(float(spans[2].text.split(' ')[4])+bet_amount)/bet_amount
        if bet_odds<line.odds:
            return True, bet_odds, "Bet placed (%s), but wanted odds (%.1f) were greater than the bet odds(%.1f)"%(bet_id,line.odds,bet_odds)
        if spans[4].text!=line.extra_data['team1text']+line.extra_data['team2text']:
            return True, bet_odds, "Bet placed (%s), but wanted team1=%s, team2=%s - got %s" % (bet_id,line.extra_data['team1text'], line.extra_data['team2text'], spans[4].text)
        try:
            if line.line_type=="overunder":
                (bet_datetime,criteria)=spans[5].text.split(line.extra_data['sidetext'].title())
            else:
                (bet_datetime,criteria)=spans[5].text.split(line.extra_data['sidetext'])
        except:
            return True, bet_odds, "Bet placed (%s), but the side we wanted (%s) is not listed (%s)"%(bet_id, line.extra_data['sidetext'],spans[5].text)
        bet_date=bet_datetime[:8].replace('/','-')
        if bet_date[3:5]+'-'+bet_date[0:2]+'-20'+bet_date[6:8]!=line.event_date:
            return True, bet_odds, "Bet placed (%s) we wanted date=%s and bet date=%s"%(bet_id, line.event_date,bet_date)       
        bet_time=bet_datetime[9:-1]
        if line.line_type=='spread':
            bet_spread=float(criteria.split(' ')[0].strip())
            if bet_spread<line.spread:
                return True, bet_odds, "Bet placed (%s), but spread (%.2f) is lower than wanted (%.2f)"%(bet_id, bet_spread,line.spread)
            elif bet_spread>line.spread:
                return True, bet_odds, "Bet placed (%s), spread (%.2f) is better than wanted (%.2f)!"%(bet_id, bet_spread,line.spread)
        elif line.line_type=='overunder':
            bet_ou=float(criteria.split(' ')[1].strip())
            if line.side=='under':
                if bet_ou<line.overunder:
                    return True, bet_odds, 'Bet placed (%s), but under on the site (%.2f) is lower than wanted (%.2f)' % (bet_id, bet_ou,line.overunder)
                elif bet_ou>line.overunder:
                    return True, bet_odds, 'Bet placed (%s), under on the site (%.2f) is better than wanted (%.2f)!' % (bet_id, bet_ou,line.overunder)
            elif line.side=='over':
                if bet_ou>line.overunder:
                    return True, bet_odds, 'Bet placed (%s), but over on the site (%.2f) is higher than wanted (%.2f)' % (bet_id, bet_ou,line.overunder)
                elif bet_ou<line.overunder:
                    return True, bet_odds, 'Bet placed (%s), over on the site (%.2f) is better than wanted (%.2f)!' % (bet_id, bet_ou,line.overunder)
        return True, bet_odds, 'Bet placed (%s)'%(bet_id) 

if __name__ == '__main__':
    bettor=SportsbookBettor()
    bettor.login('arvsports','hellfire')
    line = BasicLine('sportsbook', 'basketball', 'nba', 0, 'overunder', 'Indiana Pacers', 'Milwaukee Bucks', '0', '0', 1.9, 'under', 0, 180, 100.0, 0.0, 0, '10-03-2011', '19:05', extra_data={'id':'Bskt-Blaze-Hawks-031211TLU'})
    bettor.bet(line,0)