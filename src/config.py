TEAM_NAME_MAPPING = {
    'NYY': 'New York Yankees',
    'KCR': 'Kansas City Royals',
    'LAD': 'Los Angeles Dodgers',
    'BAL': 'Baltimore Orioles',
    'NYM': 'New York Mets',
    'BOS': 'Boston Red Sox',
    'CLE': 'Cleveland Guardians',
    'CIN': 'Cincinnati Reds',
    'ARI': 'Arizona Diamondbacks',
    'TOR': 'Toronto Blue Jays',
    'SFG': 'San Francisco Giants',
    'MIL': 'Milwaukee Brewers',
    'SEA': 'Seattle Mariners',
    'SDP': 'San Diego Padres',
    'HOU': 'Houston Astros',
    'PHI': 'Philadelphia Phillies',
    'OAK': 'Oakland Athletics',
    'ATL': 'Atlanta Braves',
    'TEX': 'Texas Rangers',
    'CHC': 'Chicago Cubs',
    'MIN': 'Minnesota Twins',
    'TBR': 'Tampa Bay Rays',
    'LAA': 'Los Angeles Angels',
    'DET': 'Detroit Tigers',
    'MIA': 'Miami Marlins',
    'STL': 'St. Louis Cardinals',
    'PIT': 'Pittsburgh Pirates',
    'COL': 'Colorado Rockies',
    'CHW': 'Chicago White Sox',
    'WSN': 'Washington Nationals'
}

STAT_MAPPING = {
    'G': 'Games Played',
    'PA': 'Plate Appearances',
    'HR': 'Home Runs',
    'R': 'Runs',
    'RBI': 'RBI',
    'SB': 'Stolen Bases',
    'BB%': 'Walk Percentage',
    'K%': 'Strikeout Percentage',
    'ISO': 'Isolated Power',
    'BABIP': 'Batting Average on Balls in Play',
    'AVG': 'Batting Average',
    'OBP': 'On-Base Percentage',
    'SLG': 'Slugging Percentage',
    'wOBA': 'Weighted On-Base Average',
    'xwOBA': 'Expected Weighted On-Base Average',
    'wRC+': 'Weighted Runs Created Plus',
    'BsR': 'Base Running',
    'Off': 'Offense',
    'Def': 'Defense',
    'WAR': 'Wins Above Replacement'
}

STAT_DESCRIPTIONS = {
    'Games Played': 'Games played by the player',
    'Plate Appearances': 'The total number of times the player has come up to bat, including walks and sacrifices',
    'Home Runs': 'The number of home runs hit by the player, which are hits that allow the player to round all bases and score',
    'Runs': 'The total number of times the player has crossed home plate to score a point for their team',
    'RBI': "The number of runs that scored as a result of the player's actions, excluding their own runs from home runs",
    'Stolen Bases': 'The number of bases the player has successfully stolen from the opposing team',
    'Walk Percentage': 'The percentage of plate appearances in which the player receives a "walk," or is allowed to advance to first base without a hit',
    'Strikeout Percentage': 'The percentage of plate appearances in which the player strikes out, meaning they fail to hit the ball successfully within three strikes',
    'Isolated Power': "A measure of a player's power, calculated by subtracting batting average from slugging percentage (SLG); highlights extra-base hits",
    'Batting Average on Balls in Play': 'A measure of how often a ball in play (excluding home runs) results in a hit',
    'Batting Average': "The player's average of successful hits per at-bat, calculated by dividing hits by at-bats",
    'On-Base Percentage': 'The percentage of times the player reaches base, including hits, walks, and being hit by a pitch',
    'Slugging Percentage': "A measure of the player's batting power, calculated by the total bases divided by at-bats",
    'Weighted On-Base Average': 'An advanced statistic that gives a weighted value to each outcome (e.g., singles, doubles) to assess overall offensive performance',
    'Expected Weighted On-Base Average': 'A version of wOBA that factors in the quality of contact (exit velocity and launch angle) to show what the player’s wOBA should be based on how they hit the ball',
    'Weighted Runs Created Plus': 'A statistic that quantifies runs created, adjusted for ballpark factors and league averages, with 100 as league average. Values above 100 are better than average',
    'Base Running': "A measure of the player's value as a baserunner, factoring in stolen bases, caught stealing, and other baserunning plays",
    'Offense': "A metric combining a player's hitting and baserunning contributions to measure their total offensive impact",
    'Defense': "A measure of the player's defensive contributions, based on fielding plays and position",
    'Wins Above Replacement': "An overall measure of a player's value, representing how many additional wins the player contributed to their team over a replacement-level player"
}