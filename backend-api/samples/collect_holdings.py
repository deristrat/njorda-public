"""Demo of collecting holdings, where we manually handle bank selection"""

from time import sleep

import api_client as njorda


def collect_holdings():
    user_data = {}
    # you can pass personal_number to prefill username if connect iframe
    # user_data = {"personal_number": "19940508-7223"}
    user = njorda.create_user(user_data)

    # create data session
    data_session = njorda.create_data_session({"user_id": user["id"]})

    # These are all providers available for the organization
    data_providers = njorda.get_data_providers()

    providers_data = []
    for provider in data_providers['items']:
        # Multiple providers can be selected, for test just select one
        if provider['name'] == 'Avanza':
            providers_data.append({
                    "id": provider['id'],
                    "id_hint": "Demo User",
                    "data_types": ["accounts", "investments"],
                    "input_username": "19940508-7223",
            })

    r = njorda.commit_data_session(data_session["id"], providers_data)
    connect_iframe_url = r["url"]
    print("\nOpen this link in browser to connect your bank account:")
    print(connect_iframe_url)

    # waiting for data collection to finish
    while True:
        data_session = njorda.get_data_session(data_session["id"])
        print(
            f"Waiting for data collection to complete."
            f" Current state: {data_session['state']}"
        )
        if data_session["state"] == "completed":
            break
        else:
            sleep(1)

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
