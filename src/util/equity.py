
def to_decimal(american):
    """ Converts american odds to european decimal odds. """
    if american > 0:
        return (american + 100) / 100.0
    
    return abs(100.0/american) + 1

def to_american(decimal):
    """ converts decimal to american odds. """
    if decimal >= 2.0:
        return 100.0 * (decimal - 1)
    return -100.0 / (decimal - 1)

def odds_to_pct(odds):
    if odds > 0:
        return 100.0 / (odds + 100.0)
    odds *= -1
    return odds / (odds + 100.0)

def gods_odds(odds1, odds2):
    odds1 = to_american(odds1)
    odds2 = to_american(odds2)
    #print odds1, odds2
    pct1, pct2 = odds_to_pct(odds1), odds_to_pct(odds2)
    total = pct1 + pct2
    #print total
    no_juice = pct1 / total
    # print no_juice
    if no_juice > 0.5:
        no_juice_odds = 100.0 * no_juice / ( 1 - no_juice )
    else:
        no_juice_odds = 100/no_juice - 100
    #print no_juice_odds
    return no_juice_odds

if __name__ == '__main__':
    print gods_odds(to_decimal(+450), to_decimal(-650))