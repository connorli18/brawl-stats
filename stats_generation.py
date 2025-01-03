# TO-DO: track player stats over time / brawler usage
# TO-DO: track various player things (e.g. brawlers used, star players, favorite events, etc.)
# TO-DO: teammate comparisons
# only process new files --> use file timestamps
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
    
def get_win_rates(df) -> dict:
    
    win_rates, gamemodes = {}, set(df.event_mode)

    gamemodes.discard('unknown')
    gamemodes.discard(np.nan)
    
    showdown_places = {'soloShowdown':4,'duoShowdown':2,'trioShowdown':2,}
    
    def _calc_win_rate(gamemode:str,place=None) -> float:
        w = l = 0
        if place:
            w = df[(df['event_mode'] == gamemode) & (df['battle_rank'] <= place)]['battle_rank'].count()
            l = df[(df['event_mode'] == gamemode) & (df['battle_rank'] > place)]['battle_rank'].count()
        else:
            try:
                w = df[(df['event_mode'] == gamemode)]['battle_result'].value_counts()['victory']
            except KeyError:
                print("Zero Wins in ",gamemode)
            try:                
                l = df[(df['event_mode'] == gamemode)]['battle_result'].value_counts()['defeat']
            except KeyError:
                print("Zero Losses in",gamemode)
        return round((w / (w+l) if (w+l) else 0),2)
    
    for gamemode in gamemodes:
        win_rates[gamemode+"_win_rate"] = _calc_win_rate(gamemode,showdown_places.get(gamemode,None))
    
    return win_rates

        

def get_battle_stats(df,stats):
    '''
    TODO: Win Streak
    '''
    
    
    get_win_rates(df)
    
    # Calculate Win Streaks
    # gay = df[df['event_mode'] == ('soloShowdown')]
    # print(gay)
    

    
    # Most Used Brawler
    stats["Main_Brawler"] = df['player_brawler_name'].value_counts().idxmax()

    
    # Avg Trophy gain/loss
    stats["avg_trophy_change"] = round(df.battle_trophy_change.mean(),2)
    # df.plot(x='date_formatted',y='battle_trophy_change')
    # plt.show()
    

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