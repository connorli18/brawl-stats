
# TO-DO: track player stats over time / brawler usage
# TO-DO: track various player things (e.g. brawlers used, star players, favorite events, etc.)
# TO-DO: teammate comparisons
# only process new files --> use file timestamps

import pandas as pd


def get_battle_stats(file_path):
    
    stats = {}
    data = pd.read_csv(file_path)
    
    
    
    get_favorites(stats,data)
    
    
def get_most_freq(stats,data):
    
    columns = ['event_mode','player_brawler_name','event_map']
    
    for column in columns:
        stats["most_freq_"+column] = data[column].value_counts().idxmax()
    
    print(stats)

    
    
    
        

if __name__ == "__main__":
    fp = "./created-logs-per-player/QJ092J8CU-battle-log-custom.csv"
    get_battle_stats(fp)
