import requests
import json
import configparser
import datetime


def make_api_call(endpoint: str, file_save_path: str) -> dict:
    """
    Generic API Call function to make a call to the Brawl Stars API
    """
    # API Boilerplate
    config = configparser.ConfigParser()
    config.read('config.ini')
    config_section = get_public_ip_to_config()

    API_KEY = config[config_section]['api_key']
    BASE_URL = config[config_section]['base_url']

    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }

    try:
        response = requests.get(BASE_URL + endpoint, headers=headers)

        # successful response
        if response.status_code == 200:
            data = response.json()

            with open(file_save_path, 'w') as file:
                json.dump(data, file, indent=2)

            return data

        # unsuccessful API request
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
    except:
        print("A request error occurred.")
        return None

def get_player_battle_log(player_tag: str) -> dict:
    """
    Gets player battle log from Brawl Stars API
    """
    endpoint = f'/players/%23{player_tag}/battlelog'
    file_save_path = f'player-battle-log/{player_tag}_battle_log_{datetime.datetime.now().strftime("%Y%m%d%H")}.json'

    return make_api_call(endpoint=endpoint, file_save_path=file_save_path)

def get_player_info(player_tag: str) -> dict: 
    """
    Gets player information from Brawl Stars API
    """
    # API boilerplate
    endpoint = f'/players/%23{player_tag}'
    file_save_path = f'player-info/{player_tag}_report_{datetime.datetime.now().strftime("%Y%m%d")}.json'

    return make_api_call(endpoint=endpoint, file_save_path=file_save_path)

def get_brawlers_info() -> dict:
    """
    Gets brawlers information from Brawl Stars API
    """
    endpoint = '/brawlers'
    file_save_path = f'brawlers/brawlers_info_{datetime.datetime.now().strftime("%Y%m%d")}.json'

    return make_api_call(endpoint=endpoint, file_save_path=file_save_path)

def get_event_rotation() -> dict:
    """
    Gets the event rotation for the current section
    """
    endpoint = '/events/rotation'
    file_save_path = f'events/events_{datetime.datetime.now().strftime("%Y%m%d")}.json'

    return make_api_call(endpoint=endpoint, file_save_path=file_save_path)


def get_public_ip_to_config() -> str:
    """
    Returns public IP Address
    """
    ip_address_to_config = {
        "193.52.24.14": "cite_uni",
        "193.54.67.91": "sciences_po_2",
        "193.54.67.92": "sciences_po",
        "193.54.67.93": "sciences_po_3",
        "176.57.33.226": "reid_hall_classroom",
        "172.58.1.111": "nad_ned",
        "172.56.70.145": "minecraft_wool",
        "172.56.69.11": "minecraft_iron",
    }

    try:
        response = requests.get('https://api.ipify.org?format=json')
        response.raise_for_status()  
        ip_data = response.json()

        if ip_data['ip'] in ip_address_to_config:
            return ip_address_to_config[ip_data['ip']]
        else:
            raise ValueError(f"IP Address {ip_data['ip']} not found in config file, please create a new key here: \n https://developer.brawlstars.com/#/account")
    
    except requests.RequestException as e:
        print(f"Error fetching public IP address: {e}")
        return None

###################################################
#                                                 #
#              MAIN (TEST) FUNCTIONS              #
#                                                 #               
###################################################


def main_player_test():
    # NOTE: watch out for the player-tag, most start with a # --> converted to a %23 in the API endpoint call
    # NOTE: space sensitive, make sure to not have trailing spaces
    player_tag = {
        'nguyen': '2LV0PLP8G',
        'ranger': '8LQCJPGR',
        'colin': 'LQQYGCV29',
        'geoffrey': '2898CGQUU', 
        'connor': 'LV9QQLR08',
        'dale': '89RPYYQJG',
        'bolu': 'JJVGPCLP',
        'aaron': 'QJ092J8CU',
        'jackson': '8JYJY298', 
        'rishi': 'V2LLC89Q'
    }

    for player_tag in player_tag.values(): 
        example_player_desc = get_player_info(player_tag=player_tag)
        print(str(example_player_desc)[0:90])
        example_battle_log = get_player_battle_log(player_tag=player_tag)
        print(str(example_battle_log)[0:90])

    print("Done!")

def main_brawlers():
    get_brawlers_info()

def main_events():
    get_event_rotation()

if __name__ == "__main__":
    
    config_section = 'cite_uni'
    
    main_events()
    main_brawlers()
    main_player_test()