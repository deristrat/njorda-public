"""Demo of collecting holdings, where all steps are handled in iframe"""
import os
from time import sleep

import api_client as njorda


def collect_holdings():
    # Create user object
    # Optinally pass person nbr: user_data = {"personal_number": "19940508-7223"}
    user_data = {}
    user = njorda.create_user(user_data)

    # create data session
    data_session = njorda.create_data_session({"user_id": user["id"]})
    print(f"\nCreated data session: {data_session}")

    # Generate link. This should be on form:
    #     https://connect.njorda.se/v1/connect-banks?data_session=<data_session_id>[&username=<username>][&data_types=data_type1,data_type2]
    connect_server = os.environ["NJORDA_API_SERVER"].replace("api-v2", "connect")
    iframe_url =f"{connect_server}/v1/connect-banks?data_session={data_session['id']}&data_types=accounts,investments"

    print(f"\nOpen this link in browser to connect your bank account: {iframe_url}")

    # waiting for data collection to finish
    while True:
        data_session = njorda.get_data_session(data_session["id"])
        print(data_session)
        print(
            f"Waiting for data collection to complete."
            f" Current state: {data_session['state']}"
        )
        if data_session["state"] == "completed":
            break
        else:
            sleep(10)

    # get collected data
    accounts = njorda.get_user_accounts(user["id"])
    positions = njorda.get_user_positions(user["id"])
    print("\nCollected accounts:")
    print(accounts)

    print("\nCollected positions:")
    print(positions)

    print("\nDone!")


if __name__ == "__main__":
    collect_holdings()
