# TO-DO: track player stats over time / brawler usage
# TO-DO: track various player things (e.g. brawlers used, star players, favorite events, etc.)
# TO-DO: teammate comparisons
# only process new files --> use file timestamps
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def get_streaks(df:pd.DataFrame,gamemodes:set,showdown_places:dict):
    
    streaks = {}
    

    for mode in gamemodes:
        print(mode.upper())
        print(df[(df['event_mode'] == mode)].head(10)['battle_result'])
    
    # df.assign(streak=(df['battle_result'] != df['WL'].shift()).cumsum())

    
def get_win_rates(df:pd.DataFrame,gamemodes:set,showdown_places:dict) -> dict:
    
    win_rates = {}
    
    def _calc_win_rate(gamemode:str,place=None) -> float:
        
        w = l = 0
        
        if place:
            w = df[(df['event_mode'] == gamemode) & (df['battle_rank'] <= place)]['battle_rank'].count()
            l = df[(df['event_mode'] == gamemode) & (df['battle_rank'] > place)]['battle_rank'].count()
        else:
            try:
                w = df[(df['event_mode'] == gamemode)]['battle_result'].value_counts()['victory']
                l = df[(df['event_mode'] == gamemode)]['battle_result'].value_counts()['defeat']
            except KeyError:
                print("Zero Wins or Zero Losses in ",gamemode)
        return (round((w / (w+l) if (w+l) else 0),2),w,l)
    
    w_total = l_total = 0
    
    for gamemode in gamemodes:
        
        (rate,curr_w,curr_l) = _calc_win_rate(gamemode,showdown_places.get(gamemode,None))
        win_rates[gamemode + "_win_rate"] = rate
        w_total += curr_w
        l_total += curr_l
    
    win_rates['overall'] = ((w_total / (w_total+l_total) if (w_total+l_total) else 0))
    
    return win_rates

        

def get_battle_stats(df,stats):
    '''
    TODO: Win Streak
    '''
        
    gamemodes = set(df.event_mode)
    gamemodes.difference_update({'unknown',np.nan})
    
    print(gamemodes)
    
    
    showdown_places = {'soloShowdown':4,'duoShowdown':2,'trioShowdown':2}
    
    
    
    # Avg Trophy gain/loss
    # stats["avg_trophy_change"] = round(df.battle_trophy_change.mean(),2)
    
    # Most Used Brawler
    # stats["main_brawler"] = df['player_brawler_name'].value_counts().idxmax()
    
    # Win Rates
    stats['win_rates'] = get_win_rates(df,gamemodes,showdown_places)
    
    # Calculate Win Streaks
    # get_streaks(df,gamemodes,showdown_places)
    
    for k,v in stats['win_rates'].items():
        print(k,v)
    

    
    return stats

def plot_trends(df):
    
    # Trophy Gain/Loss
    df.plot(x='date_formatted',y='battle_trophy_change')
    plt.show()
    

    

def stat_gen(player_tag):
    
    stats = {}
    
    try:
        battle_logs_df = pd.read_csv(f'created-logs-per-player/{player_tag}-battle-log-custom.csv')
        # battle_logs_df['date_formatted'] = pd.to_datetime(battle_logs_df['battle_time']).dt.strftime('%Y-%m-%d')
    except FileNotFoundError:
        print(f"Couldn't find file at: created-logs-per-player/{player_tag}-battle-log-custom.csv")
        
    try:
        player_info_df = pd.read_csv(f'created-player-info-log/{player_tag}-player-log-custom.csv')
    except FileNotFoundError:
        print(f"Couldn't find file at: created-player-info-log/{player_tag}-player-log-custom.csv")
        
    get_battle_stats(battle_logs_df,stats)


if __name__ == "__main__":
    stat_gen('2GL8YLVPGY')