import json
import datetime
import os
import api_call_brawl_stars as bs_api
import pandas as pd
import re

def get_brawler_count_for_date(date_str: str = None) -> dict: 
    """
    Returns the number of brawlers at a certain date (defaults to today's date if field is empty)
    """

    if date_str is None:
        bs_api.get_brawlers_info()
        date_str = datetime.datetime.now().strftime("%Y%m%d")

    file_path = f'brawlers/brawlers_info_{date_str}.json'
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return len(data["items"])
    
    else:
        raise FileNotFoundError(f"File {file_path} not found. Most likely, date {date_str} is invalid!")


def process_individual_battle_log(player_id: str, data: dict) -> list:
    """
    Processes individual player battle log and returns a list of dictionaries
    """
    
    processed_data = []

    for battle in data["items"]:
        
        # player info
        players = battle.get("battle", {}).get("players", [])
        player_brawler_name = None
        for curr_player in players:
            if "#"+player_id == curr_player.get('tag',""):
                if curr_player.get("brawler", None):
                    player_brawler_name = curr_player["brawler"].get("name", None)

        # event stats
        battle_time = battle.get("battleTime", None)
        event_id = battle.get("event", {}).get("id", None)
        event_mode = battle.get("event", {}).get("mode", None)
        event_map = battle.get("event", {}).get("map", None)

        # battle info
        battle_type = battle.get("battle", {}).get("type", None)
        battle_mode = battle.get("battle", {}).get("mode", None)
        battle_result = battle.get("battle", {}).get("result", None)
        battle_duration = battle.get("battle", {}).get("duration", None)
        battle_rank = battle.get("battle", {}).get("rank", None)
        battle_trophy_change = battle.get("battle", {}).get("trophyChange", None)

        # star playe
        _star_player = battle.get("battle", {}).get("starPlayer", {})
        if _star_player == None:
            star_player_tag = None
            star_player_name = None
            star_player_brawler_id = None
            star_player_brawler_name = None
            star_player_brawler_power = None
            star_player_brawler_trophies = None
        
        else:
            star_player_tag = _star_player.get("tag", None)
            star_player_name = _star_player.get("name", None)
            _star_player_brawler = _star_player.get("brawler", {})
            star_player_brawler_id = _star_player_brawler.get("id", None)
            star_player_brawler_name = _star_player_brawler.get("name", None)
            star_player_brawler_power = _star_player_brawler.get("power", None)
            star_player_brawler_trophies = _star_player_brawler.get("trophies", None)


        teammate_info = {}
        _teams = battle.get("battle", {}).get("teams", [])
        for team in _teams:
            if player_id in str(team):
                for i in range(0,5):
                    


                    if i >= len(team):
                        teammate_info[f"teammate_{i+1}_tag"] = None
                        teammate_info[f"teammate_{i+1}_name"] = None
                        teammate_info[f"teammate_{i+1}_brawler_id"] = None
                        teammate_info[f"teammate_{i+1}_brawler_name"] = None
                        teammate_info[f"teammate_{i+1}_brawler_power"] = None
                        teammate_info[f"teammate_{i+1}_brawler_trophies"] = None
                    else:
                        if "#"+player_id == team[i].get('tag',None):
                            player_brawler_name = team[i]["brawler"].get("name", None)
                        teammate_info[f"teammate_{i+1}_tag"] = team[i].get("tag", None)
                        teammate_info[f"teammate_{i+1}_name"] = team[i].get("name", None)
                        _teammate_brawler = team[i].get("brawler", {})
                        if _teammate_brawler == None:
                            teammate_info[f"teammate_{i+1}_brawler_id"] = None
                            teammate_info[f"teammate_{i+1}_brawler_name"] = None
                            teammate_info[f"teammate_{i+1}_brawler_power"] = None
                            teammate_info[f"teammate_{i+1}_brawler_trophies"] = None
                        else:
                            teammate_info[f"teammate_{i+1}_brawler_id"] = _teammate_brawler.get("id", None)
                            teammate_info[f"teammate_{i+1}_brawler_name"] = _teammate_brawler.get("name", None)
                            teammate_info[f"teammate_{i+1}_brawler_power"] = _teammate_brawler.get("power", None)
                            teammate_info[f"teammate_{i+1}_brawler_trophies"] = _teammate_brawler.get("trophies", None)
        processed_data.append({
            "battle_time": battle_time,
            "event_id": event_id,
            "player_brawler_name":player_brawler_name,
            "event_mode": event_mode,
            "event_map": event_map,
            "battle_type": battle_type,
            "battle_mode": battle_mode,
            "battle_result": battle_result,
            "battle_duration": battle_duration,
            "battle_rank": battle_rank,
            "battle_trophy_change": battle_trophy_change,
            "star_player_tag": star_player_tag,
            "star_player_name": star_player_name,
            "star_player_brawler_id": star_player_brawler_id,
            "star_player_brawler_name": star_player_brawler_name,
            "star_player_brawler_power": star_player_brawler_power,
            "star_player_brawler_trophies": star_player_brawler_trophies,
            **teammate_info
        }
        )

    return pd.DataFrame(processed_data)


def get_player_battles_one_player(player_id: str) -> pd.DataFrame:
    """
    Logs player battles for a specific player and returns a DataFrame
    """
    
    df_list = []

    for file in os.listdir('player-battle-log'):
        if player_id in file:
            with open(f'player-battle-log/{file}', 'r') as file:
                data = json.load(file)
                processed_data = process_individual_battle_log(player_id, data)

                # Only append valid, non-empty DataFrames
                if not processed_data.empty:
                    df_list.append(processed_data)

    # Concatenate only if there are valid DataFrames in the list
    if df_list:
        df = pd.concat(df_list, ignore_index=True)
    else:
        df = pd.DataFrame()  # Return an empty DataFrame if no data to concatenate

    return df.drop_duplicates()


def get_unique_ids() -> set:
    """
    Extracts unique IDs from filenames in the specified directory
    """
    
    unique_ids = set()
    pattern = re.compile(r'^(.*?)_battle_log')  # Regex to match the part before '_battle_log'

    for filename in os.listdir("player-battle-log"):
        match = pattern.match(filename)
        if match:
            unique_ids.add(match.group(1))  # Extract the part before '_battle_log'

    return unique_ids


def get_all_player_battles() -> None:
    """
    All battles for all players are saved to a CSV file
    """
    
    all_player_ids = get_unique_ids()

    for id in all_player_ids:

        df_old = pd.DataFrame()

        if os.path.exists(f"created-logs-per-player/{id}-battle-log-custom.csv"):
            df_old = pd.read_csv(f"created-logs-per-player/{id}-battle-log-custom.csv")
        
        df_new = get_player_battles_one_player(id)

        df_final = pd.concat([df_old, df_new], ignore_index=True).drop_duplicates()
        
        write_path = f"created-logs-per-player/{id}-battle-log-custom.csv"
        
        df_final.sort_values(by='battle_time',inplace=True)
        
        df_final.to_csv(write_path, index=False)

        print(f"Player {id} battle log saved to {write_path}")
        
        
def process_player_info(data:dict):
    """
    Processes individual player info and returns a list of dictionaries
    """
    
    processed_data = [{
            "trophies": data.get('trophies',None),
            "3vs3Victories": data.get('3vs3Victories',None),
            "soloVictories": data.get('soloVictories',None),
            "duoVictories": data.get('duoVictories',None),
            "bestRoboRumbleTime": data.get('bestRoboRumbleTime',None),
    }]
    
    return pd.DataFrame(processed_data)

        
def get_player_info(player_id:str)-> None:
    """
    Logs player info for a specific player and returns a DataFrame.
    """
    
    df_list = []

    for file in os.listdir('player-info'):
        if player_id in file:
            with open(f'player-info/{file}', 'r') as file:
                data = json.load(file)
                processed_data = process_player_info(data)

                # Only append valid, non-empty DataFrames
                if not processed_data.empty:
                    df_list.append(processed_data)
    
    # Concatenate only if there are valid DataFrames in the list
    if df_list:
        df = pd.concat(df_list, ignore_index=True)
    else:
        df = pd.DataFrame()  # Return an empty DataFrame if no data to concatenate

    return df.drop_duplicates()


def get_all_player_info():
    """
    All metrics for all players are saved to a CSV file
    """
    
    all_player_ids = get_unique_ids()
    
    for player_id in all_player_ids:
        df_old = pd.DataFrame()

        if os.path.exists(f"created-player-info-log/{player_id}-player-log-custom.csv"):
            df_old = pd.read_csv(f"created-player-info-log/{player_id}-player-log-custom.csv")
        
        df_new = get_player_info(player_id)

        df_final = pd.concat([df_old, df_new], ignore_index=True).drop_duplicates()
        
        write_path = f"created-player-info-log/{player_id}-player-log-custom.csv"
        df_final.to_csv(write_path, index=False)

        print(f"Player {player_id} battle log saved to {write_path}")


###################################################
#                                                 #
#              MAIN (TEST) FUNCTIONS              #
#                                                 #               
###################################################

def test_get_brawler_logs():
    return get_player_battles_one_player("2LV0PLP8G")


if __name__ == "__main__":

    pd.set_option('display.max_columns', None)  # Show all columns
    pd.set_option('display.width', None)        # Auto-detect the width of the terminal

    #test_get_brawler_logs()
    #print("\n\n\n\n")

    get_all_player_battles()
    get_all_player_info()
    
    print("\n\n\n\n")