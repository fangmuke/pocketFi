import json
import os
import urllib.parse

import requests


def get_headers(data):
    return {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
        'telegramRawData': data,
        'Referer': 'https://botui.pocketfi.org/',
        'Origin': 'https://botui.pocketfi.org',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
    }


def main(data):
    session = requests.Session()

    try:
        headers = get_headers(data)
        response = session.get('https://bot.pocketfi.org/mining/getUserMining', headers=headers)
        if response.status_code == 200:
            json_response = response.json()
            user_mining = json_response["userMining"]
            print(
                f'{("[Account " + str(user_mining["userId"]) + "]")}Request sent. Balance: {user_mining["gotAmount"]}/{user_mining["miningAmount"]} SWITCH Current speed: {user_mining["speed"]} switch/hour')
            if user_mining["miningAmount"] >= 1.25:
                response = session.post('https://bot.pocketfi.org/mining/claimMining', headers=headers)
                if response.status_code == 200:
                    print(
                        f'{("[Account " + str(user_mining["userId"]) + "]")}Claimed {user_mining["miningAmount"]} SWITCH')
        else:
            print('Error: PocketFI is down. Received status code:', response.status_code)
    except:
        print('error.')


if __name__ == '__main__':
    raw_datas = json.loads(os.environ["raw_datas"])

    for raw_data in raw_datas:
        main(urllib.parse.urlencode(raw_data))
