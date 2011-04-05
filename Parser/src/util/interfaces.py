from zope.interface import Interface, Attribute


class ILine(Interface):

    site = Attribute("Name of the website")
    sport = Attribute("Sport name")
    league = Attribute("League of the game being played")
    game_part = Attribute(
        "To make difference of full game, 1st half, 1st quarter, etc. Should be either 'full', " + \
        "or a number plus the part name, like '1 half', '2 quarter', 'full' and so on." +\
        "If overtime is included, use 'full overtime', '2 half overtime' and so on")
    line_type = Attribute("Tell what is the line type, either 'moneyline', 'spread' or 'overunder'")
    team1 = Attribute("Name of first team")
    team2 = Attribute("Name of second team")
    team1_number = Attribute("Game number for first team")
    team2_number = Attribute("Game number for second team")
    odds = Attribute("Line odds")
    side = Attribute("The side of the line, either first team, second team or 'over' / 'under'")
    spread = Attribute("The line spread. For moneyline / overunder keep it at 0.0 (will be ignored either way)")
    overunder = Attribute("The over / under value. For moneyline / spread keep it at 0.0")
    max_bet = Attribute("Maximum value we can bet at it")
    min_bet = Attribute("Minimum allowed bet value")
    commission = Attribute("How much is the site commission")
    event_date = Attribute("The date of the event (DD/MM/YYYY)")
    event_time = Attribute("The time of the event (hh:mm)")
    locked = Attribute("True if line has already been bet, else False")
    expiration = Attribute("Time after which the line is deemed expired and no longer valid to determine arbs")
    extra_data = Attribute("Any extra data a line needs to place a bet")
    
    def as_dict():
        """ Returns the line attributes as a dictionary """

class IGameResult(Interface):
    sport = Attribute("Sport")
    league = Attribute("League")
    event_date = Attribute("Event date")
    team1 = Attribute("Team1 result for the game part")
    team2 = Attribute("Team2 result for the game part")
    team1_number = Attribute("Rotation number for team1")
    team2_number = Attribute("Rotation number for team2")
    final_score1 = Attribute("Final score for team1")
    final_score2 = Attribute("Final score for team2")
    
    def as_dict():
        """ Returns the game result as a dictionary """

class IParser(Interface):

    def setup(user, password, proxies=None):
        """Setup the parser with the specified user and password"""

    def get_lines(sport):
        """Returns all lines for a specifc sport and league.

        If sport is None should return all lines from the site."""


class IBettor(Interface):

    def setup(user, password):
        """Setup the bettor with the specified user and password"""

    def bet(line, amount, win_risk):
        """Starts placing the bet for the specified amount.

        Specifies if the amount is to risk or to win.

        Should return True or False depending if gets to the final confirmation
        step or not"""

    def confirm(line, amount, win_risk):
        """Confirms the bet on the specified line.

        If it is at the confirmation page, it should check for the line attributes
        like spread, teams, odds and so.

        Should return a tuple being first element either True or False if the bet was placed
        and confirmed ok and the second element being the confirmation token so we can
        later check for the bet. A third element takes place returning the actual amount
        that was bet, in cases we get only a partial match."""

    def reload():
        """Load some page to avoid expiring the cookies and/or login tokens.

        Should return a boolean (True / False)."""


class IResultsParser(IParser):

    def get_results_past_24():
        """Returns all the results for the bets placed in the last 24h."""

class IActiveBettor(IBettor):

    def get_lines(sport, league, page):
        """Gets the lines of the page the bettor is sitting on"""