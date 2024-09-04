"""Demo of collecting holdings, where all steps are handled in iframe"""
import os
from json import dumps
from time import sleep

import requests
from dotenv import load_dotenv

load_dotenv()

NJORDA_API_SERVER = "https://api-v2.njorda-uat.se/"
NJORDA_API_TOKEN = os.getenv("NJORDA_API_TOKEN")
print(NJORDA_API_TOKEN)
auth_headers = {'Authorization': 'Bearer ' + NJORDA_API_TOKEN}
auth_json_headers = {'Content-Type': 'application/json', **auth_headers}


def get(url, params=None):
    return requests.get(NJORDA_API_SERVER + url, headers=auth_headers,
                        params=params).json()


def post(url, data):
    return requests.post(NJORDA_API_SERVER + url, headers=auth_json_headers,
                         data=dumps(data)).json()


def collect_holdings():
    # 1. Create user object
    client = post("/v2/data/clients", data={
        # Optionally pass person nbr: "personal_number": "19940508-7223"
    })

    # 2. Create data session
    data_session = post("/v2/data/data-sessions", data={
        "user_id": client["id"],
        "data_types": ["identity", "loans", "investments"],
    })

    print(f"\nCreated data session: {data_session}")

    # 3. Generate link to Iframe and display to user
    connect_server = NJORDA_API_SERVER.replace("api-v2", "connect")
    iframe_url = f"{connect_server}v1/connect-banks?data_session={data_session['id']}"
    print(f"\nOpen this link in browser to connect your bank account: {iframe_url}")

    # 4. Wait for data collection to finish
    while True:
        data_session_info = get("/v2/data/data-sessions/" + data_session["id"])
        state = data_session_info.get("state", "no state provided")
        print(f"Waiting for data collection to complete. state={state}")
        if state == "completed":
            break
        else:
            sleep(2)

    # 5. Get some of the collected data
    res = get("/v2/data/holdings/positions", params={"user_id": client['id']})
    for pos in res['data']:
        account, instrument, mv = pos['account'], pos['instrument'], pos['mv']
        print(f"Account: {account['name']}, Instrument: {instrument['name']}, MV: {mv}")

    print("\nDone!")


if __name__ == "__main__":
    collect_holdings()
