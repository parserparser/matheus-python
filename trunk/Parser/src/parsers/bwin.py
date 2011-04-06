import mechanize
import BeautifulSoup
from util import basics
import datetime

sports_links = {
    'football' : {
        # this link is for the NFL playoffs and may need to be changed when next season starts
        'nfl' : 'https://www.bwin.com/betviewiframe.aspx?leagueIDs=(1)BD5&selectedLeagues=1&bv=bb&ShowDays=2147483647&categoryIDs=58,57,63',
        'ncaa' : 'https://www.bwin.com/betviewiframe.aspx?leagueIDs=(1)V1&selectedLeagues=1&bv=bb&ShowDays=2147483647&categoryIDs=58,57,63',
    },

    'basketball' : {
        'nba' : 'https://www.bwin.com/betviewiframe.aspx?leagueIDs=(1)MA4&selectedLeagues=1&bv=bb&ShowDays=2147483647&categoryIDs=43,44,48',
        'ncaa': 'https://www.bwin.com/betviewiframe.aspx?leagueIDs=(1)b4&selectedLeagues=1&bv=bb&ShowDays=2147483647&categoryIDs=43,44,48',
    },
    'hockey' : {
        'nhl' : 'https://www.bwin.com/betviewiframe.aspx?leagueIDs=(1)D4&selectedLeagues=1&bv=bb&ShowDays=2147483647&categoryIDs=65,67,71,64',
    },
    'baseball' : {
        'mlb' : 'https://www.bwin.com/betviewiframe.aspx?leagueIDs=(1)Cl3C12&selectedLeagues=2&bv=bb&ShowDays=2147483647&categoryIDs=110,112,243',
    },
}

# due to cookie issues, we will load some urls before loading the real one
sports_preloading_urls = {
    'football' : [ 'https://www.bwin.com', 'https://www.bwin.com/american-football' ],
    'basketball' : [ 'https://www.bwin.com', 'https://www.bwin.com/basketball' ],
    'hockey' : ['https://www.bwin.com', 'https://www.bwin.com/ice-hockey'],
    'baseball' : ['https://www.bwin.com', 'https://www.bwin.com/baseball'],
}


class BwinParser:

    def setup(self, user, password):
        return True

    def is_logged_in(self):
        return True

    # gets all lines for the given sport
    def get_lines(self, sport):
        if (sport not in sports_links.keys()):
            return
        leagues_dict = sports_links[sport];
        leagues = leagues_dict.keys()
        for league in leagues:
            url = leagues_dict[league]
            yield self.get_lines_for_league(url, sport, league)

    # gets all lines for the given league
    def get_lines_for_league(self, url, sport, league):
        br = mechanize.Browser()
        br.set_handle_robots(None)

        for preloading_url in sports_preloading_urls[sport]:
            br.open(preloading_url)

        br.open(url)

        html = br.response().read()
        soup = BeautifulSoup.BeautifulSoup(html)
        #print html
        #print url
        lines = []
        bet_lists = soup.findAll('div', {'class' : 'bet-list'})
        for k in range(0, len(bet_lists), 2):
            linetype = bet_lists[k].find('h1').contents[0].strip()
            if linetype in ('Money Line', '2Way - Who will win?'):
                components = bet_lists[k+1].findAll('div', {'class' : 'collapsableComponent'})
                mlines = self.parse_moneyline(components, sport, league)
                #print mlines
                lines.extend(mlines)
            elif linetype in ('Handicap/Spread', 'Spread', '2Way Handicap/Spread', 'Run Line'):
                # it's Handicap/Spread for basketball and Spread for nfl and 2Way Handicap/Spread for hockey
                # and Run Line for baseball
                components = bet_lists[k+1].findAll('div', {'class' : 'collapsableComponent'})
                #tables = bet_lists[k+1].findAll('table', {'class' : 'listing '})
                slines = self.parse_spread(components, sport, league)
                #for sline in slines:
                #    print sline
                lines.extend(slines)
            elif linetype == 'Totals':
                components = bet_lists[k+1].findAll('div', {'class' : 'collapsableComponent'})
                tlines = self.parse_totals(components, sport, league)
                #for tline in tlines:
                #    print tline
                lines.extend(tlines)
            elif linetype == '3Way':
                components = bet_lists[k+1].findAll('div', {'class' : 'collapsableComponent'})
                mlines = self.parse_3way_moneylines(components, sport, league)
                lines.extend(mlines)

        for line in lines:
            d, t = convert_datetime(line.event_date, line.event_time)
            line.event_date = d
            line.event_time = t

        return lines


    def parse_moneyline(self, components, sport, league):
        all_lines = []
        for component in components:
            datespan = component.find('span', {'class' : 'spanInnerLeft'})
            date = datespan.contents[0]
            #table = component.find('table', {'class' : 'listing '})
            linerows = component.findAll('tr', {'class' : 'normal'})
            for linerow in linerows:
                #item = linerow.find('table', { 'class' : 'item'})
                time = linerow.find('td').contents[0].strip()
                both_teams = linerow.findAll('td', { 'class' : 'label'})
                both_odds = linerow.findAll('td', { 'class' : 'odd'})

                # for basketball and hockey we want both_teams[x].contents[1]
                # for football we want both_teamas[x].contents[0]
                contents_index = 0
                if sport in ('basketball', 'hockey', 'baseball'):
                    contents_index = 1
                elif sport == 'football':
                    contents_index = 0

                team1 = both_teams[0].contents[contents_index].strip()
                team1_odds = float(both_odds[0].contents[0])
                team2 = both_teams[1].contents[contents_index].strip()
                team2_odds = float(both_odds[1].contents[0])

                extra_data = dict(team1=team1, team2=team2)
                line1 = basics.BasicLine('bwin', sport, league, 'full overtime', 'moneyline', team1, team2, 0, 0,
                                  team1_odds, team1, 0, 0, 1000.0, 0.5, 0, date, time, extra_data=extra_data)
                line2 = basics.BasicLine('bwin', sport, league, 'full overtime', 'moneyline', team1, team2, 0, 0,
                                  team2_odds, team2, 0, 0, 1000.0, 0.5, 0, date, time, extra_data=extra_data)
                all_lines.append(line1)
                all_lines.append(line2)
        return all_lines

    def parse_3way_moneylines(self, components, sport, league, game_part='full'):
        all_lines = []
        for component in components:
            datespan = component.find('span', {'class' : 'spanInnerLeft'})
            date = datespan.contents[0]
            #table = component.find('table', {'class' : 'listing '})
            linerows = component.findAll('tr', {'class' : 'normal'})
            for linerow in linerows:
                #item = linerow.find('table', { 'class' : 'item'})
                time = linerow.find('td').contents[0].strip()
                both_teams = linerow.findAll('td', { 'class' : 'label'})
                three_odds = linerow.findAll('td', { 'class' : 'odd'})

                # for basketball and hockey we want both_teams[x].contents[1]
                # for football we want both_teamas[x].contents[0]
                contents_index = 0
                if sport in ('basketball', 'hockey'):
                    contents_index = 1
                elif sport == 'football':
                    contents_index = 0

                team1 = both_teams[0].contents[contents_index].strip()
                team1_odds = float(three_odds[0].contents[0])
                team2 = both_teams[2].contents[contents_index].strip()
                team2_odds = float(three_odds[2].contents[0])
                tie_odds = float(three_odds[1].contents[0])

                extra_data = dict(team1=team1, team2=team2)
                line1 = basics.BasicLine('bwin', sport, league, game_part, 'moneyline', team1, team2, 0, 0,
                                  team1_odds, team1, 0, 0, 1000.0, 0.5, 0, date, time, extra_data=extra_data)
                line2 = basics.BasicLine('bwin', sport, league, game_part, 'moneyline', team1, team2, 0, 0,
                                  team2_odds, team2, 0, 0, 1000.0, 0.5, 0, date, time, extra_data=extra_data)
                line3 = basics.BasicLine('bwin', sport, league, game_part, 'moneyline', team1, team2, 0, 0,
                                  tie_odds, 'tie', 0, 0, 1000.0, 0.5, 0, date, time, extra_data=extra_data)
                all_lines.append(line1)
                all_lines.append(line2)
                all_lines.append(line3)
        return all_lines

    def parse_spread(self, components, sport, league):
        all_lines = []
        def get_team_and_spread(contents):
            if len(contents) == 1:
                parts = contents[0].split()
                name = ' '.join(parts[:-1])
                spread = parts[-1]
            else:
                parts = contents[0].split()
                name = ' '.join(parts[:-1])
                spread = '-' + contents[1].contents[0]
                if spread.startswith('Upstate'):
                    name = '%s-%s' % (name, 'Upstate')
                    spread = spread.split()[-1]

            spread = spread.replace(',', '.')
            return name, float(''.join(c for c in spread if c in '-0123456789.'))
#            print name, spread, item.find('td', { 'class' : 'odd'}).contents[0]
        for component in components:
            datespan = component.find('span', {'class' : 'spanInnerLeft'})
            date = datespan.contents[0]
            linerows = component.findAll('tr', {'class' : 'normal'})
            for linerow in linerows:
                time = linerow.find('td').contents[0].strip()

                both_teams = linerow.findAll('td', {'class' : 'label'})
                team1, spread1 = get_team_and_spread(both_teams[0].contents)
                team2, spread2 = get_team_and_spread(both_teams[1].contents)

                both_odds = linerow.findAll('td', { 'class' : 'odd'})
                team1_odds = float(both_odds[0].contents[0])
                team2_odds = float(both_odds[1].contents[0])

                extra_data = dict(team1=team1, team2=team2)

                line1 = basics.BasicLine('bwin', sport, league, 'full overtime', 'spread', team1, team2, 0, 0,
                                  team1_odds, team1, spread1, 0, 1000.0, 0.5, 0, date, time, extra_data=extra_data)
                line2 = basics.BasicLine('bwin', sport, league, 'full overtime', 'spread', team1, team2, 0, 0,
                                  team2_odds, team2, spread2, 0, 1000.0, 0.5, 0, date, time, extra_data=extra_data)
                all_lines.append(line1)
                all_lines.append(line2)
        return all_lines




    def parse_totals(self, components, sport, league):
        #count = 0
        all_lines = []

        # Most of the time, the input will be of the form "Team 1 at Team 2 - Time"
        # but for bowl games it is in the form "Team 1 - Team 2 (Bowl Name at City, State) - Time"
        # If the string has two dashes then it is the second way
        def extract_team1_team2_time(contents):
            if len(contents.split(' - ')) == 3:
                # Texas A&M; - LSU (Cotton Bowl played at Arlington, TX) - 2:00 AM
                data = contents.split(' - ')
                team1 = data[0].strip()
                team2 = data[1].split('(')[0].strip()
                time = data[2].strip()
            else:
                data1 = contents.split(' at ')
                # data1 == [u'Los Angeles Lakers', u'Phoenix Suns - 4:35 AM']
                team1 = data1[0]
                # team1 == Los Angeles Lakers
                data2 = data1[1].split(' - ')
                # data2 == [u'Phoenix Suns', u'4:35 AM']
                team2 = data2[0]
                # team2 == Phoenix Suns
                time = data2[1]
                # time == 4:35 AM
            return (team1, team2, time)

        for component in components:
            # Each collapsable component corresponds to a date
            datespan = component.find('span', {'class' : 'spanInnerLeft'})
            date = datespan.contents[0]
            #print date

            #team_names_row = component.findAll('tr', {'class' : 'def'})

            # store all info (team names and time) in a list of triples
            game_info_list = []
            #infos = component.findAll('h4')
            infos = component.findAll('td', {'class' : 'leftcell'})
            for info in infos:
                game_info_list.append(extract_team1_team2_time(info.contents[0].strip()))
            #print 'game info list is ' , len(game_info_list)

            items = component.findAll('table', {'class' : 'item'})
            #print 'items is %d' % len(items)
            num_processed = 0
            for item in items:
                contents1 = item.find('td', { 'class' : 'label'}).contents
                over_under_split = contents1[0].split()
                #
                if sport=='hockey' and over_under_split[0] in ('Odd', 'Even'):
                    num_processed += 1 # need to advance the counter because
                    # game_info_list has unnecessary game info elements
                    continue
                if over_under_split[0] not in ('Over', 'Under'):
                    continue
                if sport=='baseball':
                    description = item.parent.parent.findPreviousSibling('tr').find('h5').contents[0].strip()
                    # most of the time description is 'Totals' but sometimes it is '1st 5 innings'
                    if description == '1st 5 innings - Totals':
                        num_processed += 1
                        continue
                side = over_under_split[0].lower()
                over_under = float(over_under_split[1].replace(',', '.'))
                contents2 = item.find('td', {'class' : 'odd'}).contents
                odds = float(contents2[0])
                #print over_under, odds

                index = num_processed / 2;
                team1 = game_info_list[index][0]
                team2 = game_info_list[index][1]
                time = game_info_list[index][2]

                extra_data = dict(team1=team1, team2=team2)
                line = basics.BasicLine('bwin', sport, league, 'full overtime', 'overunder', team1, team2, 0, 0,
                                         odds, side, 0, over_under, 1000.0, 0.5, 0, date, time, extra_data=extra_data)
                all_lines.append(line)


                num_processed += 1
                #count = count + 1
                #print contents
            #print '----- between tables -----'
        #print count
        return all_lines

def convert_datetime(date, time):
    d = datetime.datetime.strptime(date + ' ' + time, '%A, %B %d, %Y %I:%M %p')
    d2 = d - datetime.timedelta(hours=6)
    return (d2.strftime('%d-%m-%Y'), d2.strftime('%H:%M'))

def main():
    parser = BwinParser()
    res = parser.get_lines('baseball')
    for x in res:
        for y in x:
            print y

if __name__ == '__main__':
    main()
