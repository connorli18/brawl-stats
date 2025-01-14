# TO-DO: track player stats over time / brawler usage
# TO-DO: track various player things (e.g. brawlers used, star players, favorite events, etc.)
# TO-DO: teammate comparisons
# only process new files --> use file timestamps
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import json

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


def get_best_win_streaks(df:pd.DataFrame,gamemodes:set,showdown_ranks:dict)->dict:
    def calc_streaks(group,rank):
        if rank: 
            streaked_df = group.assign(streak_id = (group['battle_rank'] >= rank).cumsum())
            return streaked_df[(streaked_df['battle_rank'] <= rank)]['streak_id'].value_counts().max()
        else:
            streaked_df = group.assign(streak_id = (group['battle_result'] != group['battle_result'].shift()).cumsum())
            return streaked_df[(streaked_df['battle_result'] == 'victory')]['streak_id'].value_counts().max()
    
    filtered_df = df[df['event_mode'].isin(gamemodes)]
    
    return filtered_df.groupby('event_mode').apply(lambda group : calc_streaks(group,showdown_ranks.get(group.name,0)),include_groups=False).to_dict()

     
def get_win_rates(df:pd.DataFrame,gamemodes:set,showdown_ranks:dict) -> dict:
    def _calc_win_rate(gamemode_df:pd.DataFrame,rank=None) -> float:
        w = l = 0
        if rank:
            w = gamemode_df[gamemode_df['battle_rank'] <= rank]['battle_rank'].count()
            l = gamemode_df[gamemode_df['battle_rank'] > rank]['battle_rank'].count()
        else:
            w_l_counts = gamemode_df[gamemode_df['event_mode'] == gamemode]['battle_result'].value_counts()
            w = w_l_counts.get('victory',0)
            l = w_l_counts.get('defeat',0)
        return (round((w / (w+l) if (w+l) else 0),2),w,l)
    
    w_total = l_total = 0
    win_rates = {}
    
    filtered_df = df[df['event_mode'].isin(gamemodes)]
    grouped = filtered_df.groupby('event_mode')
    
    for gamemode in gamemodes:
        gamemode_df = grouped.get_group(gamemode)
        (rate,curr_w,curr_l) = _calc_win_rate(gamemode_df,showdown_ranks.get(gamemode,None))
        win_rates[gamemode] = rate
        w_total += curr_w
        l_total += curr_l
    
    win_rates['overall'] = ((w_total / (w_total+l_total) if (w_total+l_total) else 0))
    return win_rates

    
def get_battle_stats(df,stats,player_tag):
    showdown_ranks = {'soloShowdown':4,'duoShowdown':2,'trioShowdown':2}
    gamemodes = set(df.event_mode)
        
    gamemodes.difference_update({'unknown',np.nan})
    
    stats["avg_trophy_change"] = round(df.battle_trophy_change.mean(),2)
    stats['win_rates'] = get_win_rates(df,gamemodes,showdown_ranks)
    stats['win_streaks'] = get_best_win_streaks(df,gamemodes,showdown_ranks)
    stats["most_played_brawler"] = df['player_brawler_name'].value_counts().idxmax()
    stats["most_played_event"] = df['event_mode'].value_counts().idxmax()
    stats['star_player_count'] = df[(df['star_player_tag'] == "#"+player_tag)]['star_player_tag'].count()


def plot_trends(df):
    # Trophy Gain/Loss
    df.plot(x='battle_time',y='battle_trophy_change')
    plt.show()
    

def stat_gen(player_tag):
    date_str = datetime.datetime.now().strftime("%Y%m%d")
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
        
    get_battle_stats(battle_logs_df,stats,player_tag)
    # plot_trends(battle_logs_df)
    

    
    with open(f'./created-player-stats/{player_tag}_stats_{date_str}','w') as outfile:
        json.dump(stats,outfile,indent=4, sort_keys=True,
              separators=(', ', ': '), ensure_ascii=False,
              cls=NpEncoder)

if __name__ == "__main__":
    player_tags = {
    '2LV0PLP8G',
    '8LQCJPGR',
        'LQQYGCV29',
        '2898CGQUU', 
        'LV9QQLR08',
        '89RPYYQJG',
        'JJVGPCLP',
        'QJ092J8CU',
        '8JYJY298', 
        'V2LLC89Q',
        '2GL8YLVPGY'
    }
    for tag in player_tags:
        stat_gen(tag)