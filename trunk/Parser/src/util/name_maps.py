#!/usr/bin/env python

import re
import pickle

# from sendmessages import sendSportsMessage
def sendSportsMessage(msg):
    print msg

missing_names = set()
sent_messages = []

def add_missing_name(site, sport, league, name):
    #try:
    #    fp = open('missing_names.dat', 'rb')
    #    missing = pickle.load(fp)
    #    fp.close()
    #except IOError:
    #    missing = []

    the_tuple = (site, sport, league, name)
    if the_tuple not in missing_names:
        missing_names.add(the_tuple)

    #fp = open('missing_names.dat', 'wb+')
    #pickle.dump(missing, fp)
    #fp.close()

def pitcher_name_standard(name, the_parser):
    parser = the_parser.split('-')[0]
    if parser == 'pinnacle':
        return name.split()[-1].lower()
    elif parser == 'betgameday':
        return name.split()[-1].lower()
    elif parser == 'bodog':
        return name.split()[-1].lower()
    elif parser == 'matchbook':
        return name.lower()
    elif parser == 'sportsia':
        return name.split()[-1].lower()
    elif parser == 'thegreek':
        name = name.lower().strip('-l').strip('-r').strip()
        return name.split()[-1].lower()
    elif parser == 'espn':
       return name.split()[-1].lower()
    
    # default
    return name.split()[-1].lower()

def team_name_standard(sport, league, team, the_parser, mode='loud'):
    parser = the_parser.split('-')[0]
    if parser == 'pinnacle':
        return team
    elif parser == 'betgameday':
        return betgameday_team_name(sport, league, team, mode)
    elif parser == 'bodog':
        return bodog_team_name(sport, league, team, mode)
    elif parser == 'matchbook':
        return matchbook_team_name(sport, league, team, mode)
    elif parser == 'sportsia':
        return sportsinteraction_team_name(sport, league, team, mode)
    elif parser == 'thegreek':
        return thegreek_team_name(sport, league, team, mode)
    elif parser == 'espn':
        return espn_team_name(sport, league, team, mode)


def betgameday_team_name(sport, league, team, mode):
    standard_name = {
        'football' :{
            'nfl'  :{},
            'ncaa' :{},
            },
        'basketball':{
            'nba'  :{
                'atlanta':'Atlanta Hawks',
                'boston':'Boston Celtics',
                'charlotte':'Charlotte Bobcats',
                'chicago':'Chicago Bulls',
                'cleveland':'Cleveland Cavaliers',
                'dallas':'Dallas Mavericks',
                'denver':'Denver Nuggets',
                'detroit':'Detroit Pistons',
                'golden state':'Golden State Warriors',
                'houston':'Houston Rockets',
                'indiana':'Indiana Pacers',
                'la clippers':'Los Angeles Clippers',
                'la lakers':'Los Angeles Lakers',
                'memphis':'Memphis Grizzlies',
                'miami':'Miami Heat',
                'milwaukee':'Milwaukee Bucks ',
                'minnesota':'Minnesota Timberwolves',
                'new jersey':'New Jersey Nets',
                'new orleans':'New Orleans Hornets',
                'new york':'New York Knicks',
                'orlando':'Orlando Magic',
                'philadelphia':'Philadelphia 76ers',
                'phoenix':'Phoenix Suns',
                'portland':'Portland Trail Blazers',
                'sacramento':'Sacramento Kings',
                'san antonio':'San Antonio Spurs',
                'seattle':'Seattle Supersonics',
                'toronto':'Toronto Raptors',
                'utah':'Utah Jazz',
                'washington':'Washington Wizards',
                },
            'wnba' :{
                'chicago sky':'Chicago Sky',
                'detroit shock':'Detroit Shock',
                'connecticut sun':'Connecticut Sun',
                'houston comets':'Houston Comets',
                'indiana':'Indiana Fever',
                'los angeles sparks':'LA Sparks',
                'minnesota lynx':'Minnesota Lynx',
                'phoenix mercury':'Phoenix Mercury',
                's.a. silver stars':'SA Silver Stars',
                'seattle storm':'Seattle Storm',
                'washington mystics':'Washington Mystics',
                },
            'ncaa' :{
                'florida':'Florida',
                'ohio st':'Ohio State',
                'tennessee': 'Tennessee Volunteers',
                },
            'wncaa':{
                'rutgers':'Rutgers',
                'tennessee':'Tennesse',
                },
            },
        'baseball':{
            'mlb'  :{
                'arizona':'Arizona D-Backs',
                'atlanta':'Atlanta Braves',
                'atl':'Atlanta Braves',
                'baltimore':'Baltimore Orioles',
                'boston':'Boston Red Sox',
                'bos':'Boston Red Sox',
                'chicago cubs':'Chicago Cubs',
                'chi white sox':'Chicago White Sox',
                'cws':'Chicago White Sox',
                'cincinnati':'Cincinnati Reds',
                'cleveland':'Cleveland Indians',
                'colorado':'Colorado Rockies',
                'detroit':'Detroit Tigers',
                'det':'Detroit Tigers',
                'florida':'Florida Marlins',
                'houston':'Houston Astros',
                'kansas city':'Kansas City Royals',
                'laa angels':'LAA Angels',
                'los dodgers':'Los Angeles Dodgers',
                'milwaukee':'Milwaukee Brewers',
                'minnesota':'Minnesota Twins',
                'ny mets':'New York Mets',
                'ny yankees':'New York Yankees',
                'nyy':'New York Yankees',
                'oakland':'Oakland Athletics',
                'philadelphia':'Philadelphia Phillies',
                'pittsburgh':'Pittsburgh Pirates',
                'seattle':'Seattle Mariners',
                'san diego':'San Diego Padres',
                'san francisco':'San Francisco Giants',
                'st. louis':'St Louis Cardinals',
                'tampa bay':'Tampa Bay Devil Rays',
                'texas':'Texas Rangers',
                'toronto':'Toronto Blue Jays',
                'washington':'Washington Nationals',
                },
            },
        'hockey':{
            'nhl'  :{
                'anaheim':'Anaheim Ducks',
                'atlanta':'Atlanta Thrashers',
                'boston':'Boston Bruins',
                'buffalo':'Buffalo Sabres',
                'calgary':'Calgary Flames',
                'carolina':'Carolina Hurricanes',
                'chicago':'Chicago Blackhawks',
                'colorado':'Colorado Avalanche',
                'columbus':'Columbus Blue Jackets',
                'dallas':'Dallas Stars',
                'detroit':'Detroit Red Wings',
                'edmonton':'Edmonton Oilers',
                'florida':'Florida Panthers',
                'los angeles':'Los Angeles Kings',
                'minnesota':'Minnesota Wild',
                'montreal':'Montreal Canadiens',
                'nashville':'Nashville Predators',
                'new jersey':'New Jersey Devils',
                'ny islanders':'New York Islanders',
                'ny rangers':'New York Rangers',
                'ottawa':'Ottawa Senators',
                'philadelphia':'Philadelphia Flyers',
                'phoenix':'Phoenix Coyotes',
                'pittsburgh':'Pittsburgh Penguins',
                'san jose':'San Jose Sharks',
                'st. louis':'St. Louis Blues',
                'tampa bay':'Tampa Bay Lightning',
                'toronto':'Toronto Maple Leafs',
                'vancouver':'Vancouver Canucks',
                'washington':'Washington Capitals',
                },
            'ncaa' :{
                'boston college':'Boston College',
                'maine':'Maine',
                'michigan st':'Michigan State',
                'north dakota':'North Dakota'
                },
            },
    }
    team = ' '.join(team.split())
    if sport == 'baseball':

        g1_flag = False
        g2_flag = False

        if team.find('Game') > -1:

            if team.find('Game 1') != -1:
                g1_flag = True
                team = team.replace(' - Game 1', '')
            elif parts[-1].find('Game 2') != -1:
                g2_flag = True
                team = team.replace(' - Game 2','')

    parts = team.split('-')
    if len(parts) == 1:
        name = ' '.join(parts[0].split()).lower()
    elif len(parts) == 3:
        name = ' '.join(parts[1].split()).lower()
    elif len(parts) == 2:
        if parts[1].strip().lower() != 'women':
            name = ' '.join(parts[1].split()).lower()
        else:
            name = ' '.join(parts[0].split()).lower()
    try:
        name = standard_name[sport][league][name]
    except KeyError:
        if name in ['yes', 'no']:
            return 'Team name not found'
        add_missing_name('betgameday', sport, league, name)
        alert_message = "New team name on Betgameday: " + sport + " " + league + " " + name
        already_sent = False
        for message in sent_messages:
            if alert_message == message:
                already_sent = True
        if not already_sent and mode == 'loud':
            try:
                sendSportsMessage(alert_message)
            except:
                print alert_message
        #print 'team not found: ' + name
        return 'Team name not found'

    if sport == 'baseball':
        if g1_flag:
            name = 'G1 ' + name
        elif g2_flag:
            name = 'G2 ' + name
    return name

def bodog_team_name(sport, league, team, mode):
    standard_name = {
        'football' :{
            'nfl'  :[],
            'ncaa' :[],
            },
        'basketball':{
            'nba'  :[
                'Atlanta Hawks',
                'Boston Celtics',
                'Charlotte Bobcats',
                'Chicago Bulls',
                'Cleveland Cavaliers',
                'Dallas Mavericks',
                'Denver Nuggets',
                'Detroit Pistons',
                'Golden State Warriors',
                'Houston Rockets',
                'Indiana Pacers',
                'Los Angeles Clippers',
                'Los Angeles Lakers',
                'Memphis Grizzlies',
                'Miami Heat',
                'Milwaukee Bucks ',
                'Minnesota Timberwolves',
                'New Jersey Nets',
                'New Orleans Hornets',
                'New York Knicks',
                'Orlando Magic',
                'Philadelphia 76ers',
                'Phoenix Suns',
                'Portland Trail Blazers',
                'Sacramento Kings',
                'San Antonio Spurs',
                'Seattle Supersonics',
                'Toronto Raptors',
                'Utah Jazz',
                'Washington Wizards',
                ],
            'wnba' :[
                'Chicago Sky',
                'Connecticut Sun',
                'Detroit Shock',
                'Houston Comets',
                'Indiana Fever',
                'LA Sparks',
                'Minnesota Lynx',
                'New York Liberty',
                'Phoenix Mercury',
                'Sacramento Monarchs',
                'SA Silver Stars',
                'Seattle Storm',
                'Washington Mystics',
                ],
            'ncaa' :[
                'Florida',
                'Ohio State',
                ],
            'wncaa':[
                'Rutgers',
                'Tennesse',
                ],
            },
        'baseball':{
            'mlb'  :[
                'Arizona D-Backs',
                'Atlanta Braves',
                'Baltimore Orioles',
                'Boston Red Sox',
                'Chicago White Sox',
                'Chicago Cubs',
                'Cincinnati Reds',
                'Cleveland Indians',
                'Colorado Rockies',
                'Detroit Tigers',
                'Florida Marlins',
                'Houston Astros',
                'Kansas City Royals',
                'LAA Angels',
                'Los Angeles Dodgers',
                'Milwaukee Brewers',
                'Minnesota Twins',
                'New York Yankees',
                'New York Mets',
                'Oakland Athletics',
                'Philadelphia Phillies',
                'Pittsburgh Pirates',
                'Seattle Mariners',
                'San Diego Padres',
                'San Francisco Giants',
                'St Louis Cardinals',
                'Tampa Bay Devil Rays',
                'Texas Rangers',
                'Toronto Blue Jays',
                'Washington Nationals',
                ],
            },
        'hockey':{
            'nhl'  :[
                'Anaheim Ducks',
                'Atlanta Thrashers',
                'Boston Bruins',
                'Buffalo Sabres',
                'Calgary Flames',
                'Carolina Hurricanes',
                'Chicago Blackhawks',
                'Colorado Avalanche',
                'Columbus Blue Jackets',
                'Dallas Stars',
                'Detroit Red Wings',
                'Edmonton Oilers',
                'Florida Panthers',
                'Los Angeles Kings',
                'Minnesota Wild',
                'Montreal Canadiens',
                'Nashville Predators',
                'New Jersey Devils',
                'New York Islanders',
                'New York Rangers',
                'Ottawa Senators',
                'Philadelphia Flyers',
                'Phoenix Coyotes',
                'Pittsburgh Penguins',
                'San Jose Sharks',
                'St. Louis Blues',
                'Tampa Bay Lightning',
                'Toronto Maple Leafs',
                'Vancouver Canucks',
                'Washington Capitals',
                ],
            'ncaa' :[
                'Boston College',
                'Maine',
                'Michigan State',
                'North Dakota'
                ],
            },
    }
    name = ' '.join(team.split())
    if sport in ['football','basketball']:
        name = name.replace(' (1H)','').replace(' (2H)','').replace(' (Women)', '').strip()
    if sport == 'baseball':

        g1_flag = False
        g2_flag = False
        if name.find('G1 ') != -1:
            name.replace('G1 ','')
            g1_flag = True
        elif name.find('G2 ') != -1:
            name.replace('G2 ', '')
            g2_flag = True

        name = team.replace(' (5inn.)','').strip()
        if name == 'Los Angeles Angels':
            return 'LAA Angels'
        elif name == 'St. Louis Cardinals':
            return 'St Louis Cardinals'
        elif name == 'Arizona Diamondbacks':
            return 'Arizona D-Backs'
    if sport == 'basketball':
        if name == 'San Antonio Silver Stars':
            name = 'SA Silver Stars'

    if name not in standard_name[sport][league]:
        add_missing_name('bodog', sport, league, name)
        alert_message = "New team name on Bodog: " + sport + " " + league + " " + name
        already_sent = False
        for message in sent_messages:
            if alert_message == message:
                already_sent = True
        if not already_sent and mode == 'loud':
            try:
                sendSportsMessage(alert_message)
            except:
                print alert_message
        return 'Team name not found'

    if sport == 'baseball':
        if g1_flag:
            name = 'G1 ' + name
        elif g2_flag:
            name = 'G2 ' + name
    return name

def matchbook_team_name(sport, league, team, mode):
    standard_name = {
        'football' :{
            'nfl'  :{},
            'ncaa' :{},
            },
        'basketball':{
            'nba'  :{
                'atlanta':'Atlanta Hawks',
                'boston':'Boston Celtics',
                'charlotte':'Charlotte Bobcats',
                'chicago':'Chicago Bulls',
                'cleveland':'Cleveland Cavaliers',
                'dallas':'Dallas Mavericks',
                'denver':'Denver Nuggets',
                'detroit':'Detroit Pistons',
                'golden state':'Golden State Warriors',
                'houston':'Houston Rockets',
                'indiana':'Indiana Pacers',
                'los angeles (c)':'Los Angeles Clippers',
                'los angeles (l)':'Los Angeles Lakers',
                'memphis':'Memphis Grizzlies',
                'miami':'Miami Heat',
                'milwaukee':'Milwaukee Bucks',
                'minnesota':'Minnesota Timberwolves',
                'new jersey':'New Jersey Nets',
                'new orleans':'New Orleans Hornets',
                'new york':'New York Knicks',
                'orlando':'Orlando Magic',
                'oklahoma city': 'Oklahoma City Thunder',
                'philadelphia':'Philadelphia 76ers',
                'phoenix':'Phoenix Suns',
                'portland':'Portland Trail Blazers',
                'sacramento':'Sacramento Kings',
                'san antonio':'San Antonio Spurs',
                'seattle':'Seattle Supersonics',
                'toronto':'Toronto Raptors',
                'utah':'Utah Jazz',
                'washington':'Washington Wizards',
                },
            'wnba' :{
                'chicago':'Chicago Sky',
                'connecticut':'Connecticut Sun',
                'houston':'Houston Comets',
                'indiana':'Indiana Fever',
                'los angeles':'LA Sparks',
                'minnesota':'Minnesota Lynx',
                'phoenix':'Phoenix Mercury',
                'san antonio':'SA Silver Stars',
                'seattle':'Seattle Storm',
                },
            'ncaa' :{
                'akron': 'Akron',
                'auburn': 'Auburn',
                'cal santa barbara': 'Cal Santa Barbara',
                'florida':'Florida',
                'nc greensboro': 'NC Greensboro',
                'ohio st':'Ohio State',
                'oregon state': 'Oregon State',
                'tennessee': 'Tennesse',
                'rutgers': 'Rutgers',
                'ul lafayette': 'UL Lafayette',
                'ul monroe': 'UL Monroe',
                'morehead st': 'Morehead State',
                'stony brook': 'Stony Brook',
                'florida atlantic': 'Florida Atlantic',
                'the citadel': 'The Citadel',
                'montana state': 'Montana State',
                'se missouri st': 'SE Missouri State',
                'eastern illinois': 'Eastern Illinois',
                'arizona': 'Arizona',
                'washington st': 'Washington State',
                },
            'wncaa':{},
            },
        'baseball':{
            'mlb'  :{
                'arizona':'Arizona D-Backs',
                'atlanta':'Atlanta Braves',
                'baltimore':'Baltimore Orioles',
                'boston':'Boston Red Sox',
                'chicago (a)':'Chicago White Sox',
                'chicago (n)':'Chicago Cubs',
                'cincinnati':'Cincinnati Reds',
                'cleveland':'Cleveland Indians',
                'colorado':'Colorado Rockies',
                'detroit':'Detroit Tigers',
                'florida':'Florida Marlins',
                'houston':'Houston Astros',
                'kansas city':'Kansas City Royals',
                'los angeles (a)':'LAA Angels',
                'los angeles (n)':'Los Angeles Dodgers',
                'milwaukee':'Milwaukee Brewers',
                'minnesota':'Minnesota Twins',
                'new york (a)':'New York Yankees',
                'new york (n)':'New York Mets',
                'oakland':'Oakland Athletics',
                'philadelphia':'Philadelphia Phillies',
                'pittsburgh':'Pittsburgh Pirates',
                'san diego':'San Diego Padres',
                'san francisco':'San Francisco Giants',
                'seattle':'Seattle Mariners',
                'st. louis':'St Louis Cardinals',
                'tampa bay':'Tampa Bay Devil Rays',
                'texas':'Texas Rangers',
                'toronto':'Toronto Blue Jays',
                'washington':'Washington Nationals',
                },
            },
        'hockey':{
            'nhl'  :{
                'anaheim':'Anaheim Ducks',
                'atlanta':'Atlanta Thrashers',
                'boston':'Boston Bruins',
                'buffalo':'Buffalo Sabres',
                'calgary':'Calgary Flames',
                'carolina':'Carolina Hurricanes',
                'chicago':'Chicago Blackhawks',
                'colorado':'Colorado Avalanche',
                'columbus':'Columbus Blue Jackets',
                'dallas':'Dallas Stars',
                'detroit':'Detroit Red Wings',
                'edmonton':'Edmonton Oilers',
                'florida':'Florida Panthers',
                'los angeles':'Los Angeles Kings',
                'minnesota':'Minnesota Wild',
                'montreal':'Montreal Canadiens',
                'nashville':'Nashville Predators',
                'new jersey':'New Jersey Devils',
                'ny islanders':'New York Islanders',
                'ny rangers':'New York Rangers',
                'ottawa':'Ottawa Senators',
                'philadelphia':'Philadelphia Flyers',
                'phoenix':'Phoenix Coyotes',
                'pittsburgh':'Pittsburgh Penguins',
                'san jose':'San Jose Sharks',
                'st. louis':'St. Louis Blues',
                'tampa bay':'Tampa Bay Lightning',
                'toronto':'Toronto Maple Leafs',
                'vancouver':'Vancouver Canucks',
                'washington':'Washington Capitals',
                },
            'ncaa' :{},
            },
    }
    name = ' '.join(team.lower().split())

    # we may need to take out the pitcher name
    if sport == 'baseball':

        g1_flag = False
        g2_flag = False
        if name.find('g1 ') != -1:
            name = name.replace('g1 ','')
            g1_flag = True
        elif name.find('g2 ') != -1:
            name = name.replace('g2 ', '')
            g2_flag = True

        match = re.match('(.*)(\(.*\))$', name)
        if match and match.groups()[1] not in ['(a)','(n)']:
            name = match.groups()[0].strip()
        else:
            #print 'matchbook team has no pitcher: ' + name
            pass

    try:
        name = standard_name[sport][league][name]
    except KeyError:
        add_missing_name('matchbook', sport, league, name)
        alert_message = "New team name on Matchbook: " + sport + " " + league + " " + name
        already_sent = False
        for message in sent_messages:
            if alert_message == message:
                already_sent = True
        if not already_sent and mode == 'loud':
            try:
                sendSportsMessage(alert_message)
            except:
                print alert_message
        #print 'team not found for matchbook:', name, sport, league
        return 'Team name not found'

    if sport == 'baseball':
        if g1_flag:
            name = 'G1 ' + name
        elif g2_flag:
            name = 'G2 ' + name
    return name

def sportsinteraction_team_name(sport, league, team, mode):
    standard_name = {
        'football' :{
            'nfl'  :{},
            'ncaa' :{},
            },
        'basketball':{
            'nba'  :{
                'atlanta':'Atlanta Hawks',
                'boston':'Boston Celtics',
                'charlotte':'Charlotte Bobcats',
                'chicago':'Chicago Bulls',
                'cleveland':'Cleveland Cavaliers',
                'dallas':'Dallas Mavericks',
                'denver':'Denver Nuggets',
                'detroit':'Detroit Pistons',
                'golden state':'Golden State Warriors',
                'houston':'Houston Rockets',
                'indiana':'Indiana Pacers',
                'la clippers':'Los Angeles Clippers',
                'la lakers':'Los Angeles Lakers',
                'memphis':'Memphis Grizzlies',
                'miami':'Miami Heat',
                'milwaukee':'Milwaukee Bucks ',
                'minnesota':'Minnesota Timberwolves',
                'new jersey':'New Jersey Nets',
                'new orleans':'New Orleans Hornets',
                'new york':'New York Knicks',
                'orlando':'Orlando Magic',
                'philadelphia':'Philadelphia 76ers',
                'phoenix':'Phoenix Suns',
                'portland':'Portland Trail Blazers',
                'sacramento':'Sacramento Kings',
                'san antonio':'San Antonio Spurs',
                'seattle':'Seattle Supersonics',
                'toronto':'Toronto Raptors',
                'utah':'Utah Jazz',
                'washington':'Washington Wizards',
                },
            'wnba' :{
                'chicago':'Chicago Sky',
                'houston':'Houston Comets',
                'indiana':'Indiana Fever',
                'los angeles':'LA Sparks',
                'minnesota':'Minnesota Lynx',
                'phoenix':'Phoenix Mercury',
                'san antonio':'SA Silver Stars',
                'seattle':'Seattle Storm',
                },
            'ncaa' :{
                'florida':'Florida',
                'ohio st':'Ohio State',
                },
            'wncaa':{
                'rutgers':'Rutgers',
                'tennesse':'Tennesse',
                },
            },
        'baseball':{
            'mlb'  :{
                'arizona':'Arizona D-Backs',
                'atlanta':'Atlanta Braves',
                'baltimore':'Baltimore Orioles',
                'boston':'Boston Red Sox',
                'chicago (a)':'Chicago White Sox',
                'chicago (n)':'Chicago Cubs',
                'cincinnati':'Cincinnati Reds',
                'cleveland':'Cleveland Indians',
                'colorado':'Colorado Rockies',
                'detroit':'Detroit Tigers',
                'florida':'Florida Marlins',
                'houston':'Houston Astros',
                'kansas city':'Kansas City Royals',
                'la anaheim':'LAA Angels',
                'los angeles':'Los Angeles Dodgers',
                'milwaukee':'Milwaukee Brewers',
                'minnesota':'Minnesota Twins',
                'new york (a)':'New York Yankees',
                'new york (n)':'New York Mets',
                'oakland':'Oakland Athletics',
                'philadelphia':'Philadelphia Phillies',
                'pittsburgh':'Pittsburgh Pirates',
                'seattle':'Seattle Mariners',
                'san diego':'San Diego Padres',
                'san francisco':'San Francisco Giants',
                'st louis':'St Louis Cardinals',
                'tampa bay':'Tampa Bay Devil Rays',
                'texas':'Texas Rangers',
                'toronto':'Toronto Blue Jays',
                'washington':'Washington Nationals',
                },
            },
        'hockey':{
            'nhl'  :{
                'anaheim':'Anaheim Ducks',
                'atlanta':'Atlanta Thrashers',
                'boston':'Boston Bruins',
                'buffalo':'Buffalo Sabres',
                'calgary':'Calgary Flames',
                'carolina':'Carolina Hurricanes',
                'chicago':'Chicago Blackhawks',
                'colorado':'Colorado Avalanche',
                'columbus':'Columbus Blue Jackets',
                'dallas':'Dallas Stars',
                'detroit':'Detroit Red Wings',
                'edmonton':'Edmonton Oilers',
                'florida':'Florida Panthers',
                'los angeles':'Los Angeles Kings',
                'minnesota':'Minnesota Wild',
                'montreal':'Montreal Canadiens',
                'nashville':'Nashville Predators',
                'new jersey':'New Jersey Devils',
                'ny islanders':'New York Islanders',
                'ny rangers':'New York Rangers',
                'ottawa':'Ottawa Senators',
                'philadelphia':'Philadelphia Flyers',
                'phoenix':'Phoenix Coyotes',
                'pittsburgh':'Pittsburgh Penguins',
                'san jose':'San Jose Sharks',
                'st louis':'St. Louis Blues',
                'tampa bay':'Tampa Bay Lightning',
                'toronto':'Toronto Maple Leafs',
                'vancouver':'Vancouver Canucks',
                'washington':'Washington Capitals',
                },
            'ncaa' :{
                'boston college':'Boston College',
                'maine':'Maine',
                'michigan st':'Michigan State',
                'north dakota':'North Dakota'
                },
            },
    }
    name = ' '.join(team.split(':')[0].lower().split())

    if sport == 'baseball':

        g1_flag = False
        g2_flag = False
        if name.find('g1 ') != -1:
            name = name.replace('g1 ','')
            g1_flag = True
        elif name.find('g2 ') != -1:
            name = name.replace('g2 ', '')
            g2_flag = True

    try:
        name = standard_name[sport][league][name]
    except KeyError:
        add_missing_name('sportsia', sport, league, name)
        alert_message = "New team name on Sportsinteraction: " + sport + " " + league + " " + name
        already_sent = False
        for message in sent_messages:
            if alert_message == message:
                already_sent = True
        if not already_sent and mode == 'loud':
            try:
                sendSportsMessage(alert_message)
            except:
                print alert_message
        #print 'team not found: ' + name
        return 'Team name not found'

    if sport == 'baseball':
        if g1_flag:
            name = 'G1 ' + name
        elif g2_flag:
            name = 'G2 ' + name
    return name

def thegreek_team_name(sport, league, team, mode):
    standard_name = {
        'football' :{
            'nfl'  :[],
            'ncaa' :[],
            },
        'basketball':{
            'nba'  :[
                'Atlanta Hawks',
                'Boston Celtics',
                'Charlotte Bobcats',
                'Chicago Bulls',
                'Cleveland Cavaliers',
                'Dallas Mavericks',
                'Denver Nuggets',
                'Detroit Pistons',
                'Golden State Warriors',
                'Houston Rockets',
                'Indiana Pacers',
                'Los Angeles Clippers',
                'Los Angeles Lakers',
                'Memphis Grizzlies',
                'Miami Heat',
                'Milwaukee Bucks ',
                'Minnesota Timberwolves',
                'New Jersey Nets',
                'New Orleans Hornets',
                'New York Knicks',
                'Orlando Magic',
                'Philadelphia 76ers',
                'Phoenix Suns',
                'Portland Trail Blazers',
                'Sacramento Kings',
                'San Antonio Spurs',
                'Seattle Supersonics',
                'Toronto Raptors',
                'Utah Jazz',
                'Washington Wizards',
                ],
            'wnba' :[
                'Chicago Sky',
                'Connecticut Sun',
                'Detroit Shock',
                'Houston Comets',
                'Indiana Fever',
                'LA Sparks',
                'Minnesota Lynx',
                'New York Liberty',
                'Phoenix Mercury',
                'Sacramento Monarchs',
                'SA Silver Stars',
                'Seattle Storm',
                'Washington Mystics',
                ],
            'ncaa' :[
                'Florida',
                'Ohio State',
                ],
            'wncaa':[
                'Rutgers',
                'Tennesse',
                ],
            },
        'baseball':{
            'mlb'  :[
                'Arizona D-Backs',
                'Atlanta Braves',
                'Baltimore Orioles',
                'Boston Red Sox',
                'Chicago White Sox',
                'Chicago Cubs',
                'Cincinnati Reds',
                'Cleveland Indians',
                'Colorado Rockies',
                'Detroit Tigers',
                'Florida Marlins',
                'Houston Astros',
                'Kansas City Royals',
                'LAA Angels',
                'Los Angeles Dodgers',
                'Milwaukee Brewers',
                'Minnesota Twins',
                'New York Yankees',
                'New York Mets',
                'Oakland Athletics',
                'Philadelphia Phillies',
                'Pittsburgh Pirates',
                'Seattle Mariners',
                'San Diego Padres',
                'San Francisco Giants',
                'St Louis Cardinals',
                'Tampa Bay Devil Rays',
                'Texas Rangers',
                'Toronto Blue Jays',
                'Washington Nationals',
                ],
            },
        'hockey':{
            'nhl'  :[
                'Anaheim Ducks',
                'Atlanta Thrashers',
                'Boston Bruins',
                'Buffalo Sabres',
                'Calgary Flames',
                'Carolina Hurricanes',
                'Chicago Blackhawks',
                'Colorado Avalanche',
                'Columbus Blue Jackets',
                'Dallas Stars',
                'Detroit Red Wings',
                'Edmonton Oilers',
                'Florida Panthers',
                'Los Angeles Kings',
                'Minnesota Wild',
                'Montreal Canadiens',
                'Nashville Predators',
                'New Jersey Devils',
                'New York Islanders',
                'New York Rangers',
                'Ottawa Senators',
                'Philadelphia Flyers',
                'Phoenix Coyotes',
                'Pittsburgh Penguins',
                'San Jose Sharks',
                'St. Louis Blues',
                'Tampa Bay Lightning',
                'Toronto Maple Leafs',
                'Vancouver Canucks',
                'Washington Capitals',
                ],
            'ncaa' :[
                'Boston College',
                'Maine',
                'Michigan State',
                'North Dakota'
                ],
            },
    }
    name = ' '.join(team.split())
    if sport == 'baseball':
        g1_flag = False
        g2_flag = False
        if name.find(' GM 1') != -1 or name.find(' GM1') != -1:
            name = name.replace(' GM 1', '').replace(' GM1', '')
            g1_flag = True
        elif name.find(' GM 2') != -1 or name.find(' GM2') != -1:
            name = name.replace(' GM 2', '').replace(' GM2', '')
            g2_flag = True
        if name == 'Los Angeles Angels':
            name = 'LAA Angels'
        elif name == 'Bos Red Sox':
            name = 'Boston Red Sox'
        elif name == 'Washington National':
            name = 'Washington Nationals'
        elif name == 'Milwakee Brewers':
            name = 'Milwaukee Brewers'
        elif name == 'Arizona Diamondbacks':
            name = 'Arizona D-Backs'
    if sport == 'basketball':
        if name == 'Los Angeles Sparks':
            name = 'LA Sparks'

    if name not in standard_name[sport][league]:
        add_missing_name('thegreek', sport, league, name)
        alert_message = "New team name on The Greek: " + sport + " " + league + " " + name
        already_sent = False
        for message in sent_messages:
            if alert_message == message:
                already_sent = True
        if not already_sent and mode == 'loud':
            try:
                sendSportsMessage(alert_message)
            except:
                print alert_message
        return 'Team name not found'

    if sport == 'baseball':
        if g1_flag:
            name = 'G1 ' + name
        elif g2_flag:
            name = 'G2 ' + name
    return name

def espn_team_name(sport, league, team, mode):
    standard_name = {
        'football' :{
            'nfl'  :{},
            'ncaa' :{},
            },
        'basketball':{
            'nba'  :{
                'atlanta':'Atlanta Hawks',
                'boston':'Boston Celtics',
                'charlotte':'Charlotte Bobcats',
                'chicago':'Chicago Bulls',
                'cleveland':'Cleveland Cavaliers',
                'dallas':'Dallas Mavericks',
                'denver':'Denver Nuggets',
                'detroit':'Detroit Pistons',
                'golden state':'Golden State Warriors',
                'houston':'Houston Rockets',
                'indiana':'Indiana Pacers',
                'la clippers':'Los Angeles Clippers',
                'la lakers':'Los Angeles Lakers',
                'memphis':'Memphis Grizzlies',
                'miami':'Miami Heat',
                'milwaukee':'Milwaukee Bucks ',
                'minnesota':'Minnesota Timberwolves',
                'new jersey':'New Jersey Nets',
                'no/oklahoma city':'New Orleans Hornets',
                'new york':'New York Knicks',
                'orlando':'Orlando Magic',
                'philadelphia':'Philadelphia 76ers',
                'phoenix':'Phoenix Suns',
                'portland':'Portland Trail Blazers',
                'sacramento':'Sacramento Kings',
                'san antonio':'San Antonio Spurs',
                'seattle':'Seattle Supersonics',
                'toronto':'Toronto Raptors',
                'utah':'Utah Jazz',
                'washington':'Washington Wizards',
                },
            'wnba' :{
                'chicago':'Chicago Sky',
                'connecticut':'Connecticut Sun',
                'detroit':'Detroit Shock',
                'houston':'Houston Comets',
                'indiana':'Indiana Fever',
                'la sparks':'LA Sparks',
                'minnesota':'Minnesota Lynx',
                'new york':'New York Liberty',
                'phoenix':'Phoenix Mercury',
                'sacramento':'Sacramento Monarchs',
                'san antonio':'SA Silver Stars',
                'seattle':'Seattle Storm',
                'washington':'Washington Mystics',},
            'ncaa' :{
                'florida':'Florida',
                'ohio st':'Ohio State',
                },
            'wncaa':{
                'rutgers':'Rutgers',
                'tennesse':'Tennesse',
                },
            },
        'baseball':{
            'mlb'  :{
                'arizona':'Arizona D-Backs',
                'atlanta':'Atlanta Braves',
                'baltimore':'Baltimore Orioles',
                'boston':'Boston Red Sox',
                'white sox':'Chicago White Sox',
                'cubs':'Chicago Cubs',
                'cincinnati':'Cincinnati Reds',
                'cleveland':'Cleveland Indians',
                'colorado':'Colorado Rockies',
                'detroit':'Detroit Tigers',
                'florida':'Florida Marlins',
                'houston':'Houston Astros',
                'kansas city':'Kansas City Royals',
                'la angels':'LAA Angels',
                'la dodgers':'Los Angeles Dodgers',
                'milwaukee':'Milwaukee Brewers',
                'minnesota':'Minnesota Twins',
                'ny yankees':'New York Yankees',
                'ny mets':'New York Mets',
                'oakland':'Oakland Athletics',
                'philadelphia':'Philadelphia Phillies',
                'pittsburgh':'Pittsburgh Pirates',
                'seattle':'Seattle Mariners',
                'san diego':'San Diego Padres',
                'san francisco':'San Francisco Giants',
                'st. louis':'St Louis Cardinals',
                'tampa bay':'Tampa Bay Devil Rays',
                'texas':'Texas Rangers',
                'toronto':'Toronto Blue Jays',
                'washington':'Washington Nationals',
                },
            },
        'hockey':{
            'nhl'  :{
                'anaheim':'Anaheim Ducks',
                'atlanta':'Atlanta Thrashers',
                'boston':'Boston Bruins',
                'buffalo':'Buffalo Sabres',
                'calgary':'Calgary Flames',
                'carolina':'Carolina Hurricanes',
                'chicago':'Chicago Blackhawks',
                'colorado':'Colorado Avalanche',
                'columbus':'Columbus Blue Jackets',
                'dallas':'Dallas Stars',
                'detroit':'Detroit Red Wings',
                'edmonton':'Edmonton Oilers',
                'florida':'Florida Panthers',
                'los angeles':'Los Angeles Kings',
                'minnesota':'Minnesota Wild',
                'montreal':'Montreal Canadiens',
                'nashville':'Nashville Predators',
                'new jersey':'New Jersey Devils',
                'ny islanders':'New York Islanders',
                'ny rangers':'New York Rangers',
                'ottawa':'Ottawa Senators',
                'philadelphia':'Philadelphia Flyers',
                'phoenix':'Phoenix Coyotes',
                'pittsburgh':'Pittsburgh Penguins',
                'san jose':'San Jose Sharks',
                'st. louis':'St. Louis Blues',
                'tampa bay':'Tampa Bay Lightning',
                'toronto':'Toronto Maple Leafs',
                'vancouver':'Vancouver Canucks',
                'washington':'Washington Capitals',
                },
            'ncaa' :{
                'boston college':'Boston College',
                'maine':'Maine',
                'michigan st':'Michigan State',
                'north dakota':'North Dakota'
                },
            },
    }
    name = ' '.join(team.split()).lower()

    if sport == 'baseball':
        g1_flag = False
        g2_flag = False
        if name.find(' 1') != -1:
            name = name.replace(' 1','')
            g1_flag = True
        elif name.find(' 2') != -1:
            name = name.replace(' 2', '')
            g2_flag = True

    try:
        name = standard_name[sport][league][name]
    except KeyError:
        add_missing_name('espn', sport, league, name)
        alert_message = "New team name on ESPN: " + sport + " " + league + " " + name
        already_sent = False
        for message in sent_messages:
            if alert_message == message:
                already_sent = True
        if not already_sent and mode == 'loud':
            try:
                sendSportsMessage(alert_message)
            except:
                print alert_message
        return 'Team name not found'
    
    if sport == 'baseball':
        if g1_flag:
            name = 'G1 ' + name
        elif g2_flag:
            name = 'G2 ' + name
    return name

def same_teams(line1, line2):
    team1 = []
    team2 = []
    team1.append(team_name_standard(line1.sport, line1.league, line1.team1, line1.site))
    team1.append(team_name_standard(line1.sport, line1.league, line1.team2, line1.site))
    team2.append(team_name_standard(line2.sport, line2.league, line2.team1, line2.site))
    team2.append(team_name_standard(line2.sport, line2.league, line2.team2, line2.site))
    for team in team1:
        if team not in team2:
            return False
    return True

def opposite_side(line1, line2):
    #ASSUMING line1.line_type = line2.line_type
    if not same_teams(line1, line2):
        return False

    if line1.line_type == 'overunder':
        if (line1.side == 'over' and line2.side == 'under') or (line2.side == 'over' and line1.side == 'under'):
            return True
    else:
        side1 = team_name_standard(line1.sport, line1.league, line1.side, line1.site)
        side2 = team_name_standard(line2.sport, line2.league, line2.side, line2.site)
        teams = [team_name_standard(line2.sport, line2.league, line2.team1, line2.site),
                 team_name_standard(line2.sport, line2.league, line2.team2, line2.site)]
        if (side1 == teams[0] and side2 == teams[1]) or (side2 == teams[0] and side1 == teams[1]):
            return True
    return False
