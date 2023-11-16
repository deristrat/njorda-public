"""Demo of collecting holdings, where all steps are handled in iframe"""
import os
from time import sleep

import api_client as njorda


def collect_holdings():
    # 1. Create user object
    user = njorda.create_user({
        # Optionally pass person nbr: "personal_number": "19940508-7223"
    })

    # 2. Create data session
    data_session = njorda.create_data_session({
        "user_id": user["id"],
        "data_types": ["identity", "accounts", "investments"],
    })
    print(f"\nCreated data session: {data_session}")


    # 3. Generate link to Iframe and display to user
    connect_server = os.environ["NJORDA_API_SERVER"].replace("api-v2", "connect")
    iframe_url = f"{connect_server}v1/connect-banks?data_session={data_session['id']}"
    print(f"\nOpen this link in browser to connect your bank account: {iframe_url}")

    # 4. Wait for data collection to finish
    while True:
        data_session2 = njorda.get_data_session(data_session["id"])
        print(data_session2)
        state = data_session2.get("state", "no state provided")
        print(f"Waiting for data collection to complete. state={state}")
        if state == "completed":
            break
        else:
            sleep(2)

    # 5. Get collected data
    accounts = njorda.get_user_accounts(user["id"])
    positions = njorda.get_user_positions(user["id"])
    print("\nCollected accounts:")
    print(accounts)

    print("\nCollected positions:")
    print(positions)

    print("\nDone!")


if __name__ == "__main__":
    collect_holdings()
