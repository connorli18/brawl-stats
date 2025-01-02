
# TO-DO: track player stats over time / brawler usage
# TO-DO: track various player things (e.g. brawlers used, star players, favorite events, etc.)
# TO-DO: teammate comparisons
# only process new files --> use file timestamps

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
    
# def get_event_stats(df):
    
#     event_modes = set(df["event_mode"])
    
#     print(df.groupby('event_mode').agg({'battle_rank':'mean','battle_trophy_change':'mean'}))
    
    
#     print(df.groupby('battle_result').count())

def get_win_rates(df):
    
    def calc_wr(wins,loss):
        return wins / (wins+loss) if (wins+loss) else 0 
    
    # Total all wins
    arcade_wins = df.battle_result.value_counts()['victory']
    soloSS_wins = df[(df['event_mode'] == 'soloShowdown') & (df['battle_rank'] <= 4)]['battle_rank'].count()
    duoSS_wins = df[(df['event_mode'] == 'duoShowdown') & (df['battle_rank'] <= 2)]['battle_rank'].count()
    trioSS_wins = df[(df['event_mode'] == 'trioShowdown') & (df['battle_rank'] <= 2)]['battle_rank'].count()
    ttl_win = arcade_wins + soloSS_wins + duoSS_wins + trioSS_wins
    
    # Total All losses 
    arcade_loss = df.battle_result.value_counts()['defeat']
    soloSS_loss = df[(df['event_mode'] == 'soloShowdown') & (df['battle_rank'] > 4)]['battle_rank'].count()
    duoSS_loss = df[(df['event_mode'] == 'duoShowdown') & (df['battle_rank'] > 2)]['battle_rank'].count()
    trioSS_loss = df[(df['event_mode'] == 'trioShowdown') & (df['battle_rank'] > 2)]['battle_rank'].count()
    ttl_loss = arcade_loss + soloSS_loss + duoSS_loss + trioSS_loss
    
    # Total Battles Played (W + L)
    overall_win_rate = calc_wr(ttl_win,ttl_loss)
    arcade_win_rate = calc_wr(arcade_wins,arcade_loss) 
    soloSS_win_rate = calc_wr(soloSS_wins,soloSS_loss) 
    duoSS_win_rate = calc_wr(duoSS_wins,duoSS_loss) 
    trioSS_win_rate = calc_wr(trioSS_wins,trioSS_loss)
    
    print(f'''Win Rates:
    \tOverall:{round(overall_win_rate,2)}
    \tArcade:{round(arcade_win_rate,2)}
    \tSoloSS:{round(soloSS_win_rate,2)}
    \tDuoSS:{round(duoSS_win_rate,2)}
    \tTrioSS:{trioSS_win_rate if trioSS_win_rate else 0}
    ''')

def get_battle_stats(df):
    '''
    TODO: Avg. Trophy gain/loss
    TODO: Win Streak
    TODO: Most used brawler 
    '''
    
    get_win_rates(df)
    

    

def stat_gen(player_tag):
    
    try:
        battle_logs_df = pd.read_csv(f'created-logs-per-player/{player_tag}-battle-log-custom.csv')
    except FileNotFoundError:
        print(f"Couldn't find file at: created-logs-per-player/{player_tag}-battle-log-custom.csv")
        
    try:
        player_info_df = pd.read_csv(f'created-player-info-log/{player_tag}-player-log-custom.csv')
    except FileNotFoundError:
        print(f"Couldn't find file at: created-player-info-log/{player_tag}-player-log-custom.csv")
        
    get_battle_stats(battle_logs_df)



    


if __name__ == "__main__":

    stat_gen('2GL8YLVPGY')
    
    