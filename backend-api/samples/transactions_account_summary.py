"""Sample code to calculate risk for a couple of random portfolios.

Demonstrates usage of: /v2/data/pnl-transactions/<account_id>
Demonstrates usage of: /v2/data/clients/<client_id>/summary

"""

import os
from pprint import pprint

from dotenv import load_dotenv
import requests

# Install the python-dotenv package, to use an .env file for settings
load_dotenv()

NJORDA_API_TOKEN = os.environ["NJORDA_API_TOKEN"]
NJORDA_API_SERVER = os.environ["NJORDA_API_SERVER"]

# use global session to avoid, reconnecting for each request
session = requests.Session()
INS_ERICB = "SE0000108656"


def get_auth_headers() -> dict[str, str]:
    return {"Authorization": f"Bearer {NJORDA_API_TOKEN}"}


def create_client():
    """
    API call to create a client.
    """
    res = session.post(
        url=f"{NJORDA_API_SERVER}/v2/data/clients",
        headers=get_auth_headers(),
        json={
            "email": "example_client@example.com",
            "first_name": "New TEST",
            "last_name": "Client TEST",
            "personal_number": "111jn-ndw-nqwk332",
        },
    )
    return res.json()


def delete_client(client_id: str):
    """
    API call to delete a client.
    """
    res = session.delete(
        url=f"{NJORDA_API_SERVER}/v2/data/clients/{client_id}",
        headers=get_auth_headers(),
    )
    return res


def create_account(user_uuid: str):
    """
    API call to create an account.
    """
    res = session.post(
        url=f"{NJORDA_API_SERVER}/v2/data/accounts",
        headers=get_auth_headers(),
        json={
            "user_id": user_uuid,
            "type": "investment",
            "currency": "EUR",
            "is_manual_account": True,
        },
    )
    return res.json()


def upsert_transactions(account_id: str):
    """
    Adds transactions if not exist.
    Replaces existing transactions with new ones.
    """
    transactions = [
        # Put initial cash into account
        dict(
            type="TRANSFER",
            amount=1000,
            currency="SEK",
            fx_rate=1.0,
            date="2024-01-04 00:00:00",
            instrument="CASH.SEK",
            quantity=0,
        ),
        # Buy 10 Ericsson B shares
        dict(
            type="TRADE",
            amount=-10 * 56.1,
            currency="SEK",
            fx_rate=1.0,
            date="2024-02-02 00:00:00",
            instrument=INS_ERICB,
            quantity=10,
        ),
        # Sell half the position
        dict(
            type="TRADE",
            amount=5 * 58.59,
            currency="SEK",
            fx_rate=1.0,
            date="2024-03-14 00:00:00",
            instrument=INS_ERICB,
            quantity=-5,
        ),
        # Sell most of the rest, leaving two shares
        dict(
            type="TRADE",
            amount=3 * 61.9,
            currency="SEK",
            fx_rate=1.0,
            date="2024-05-14 00:00:00",
            instrument=INS_ERICB,
            quantity=-3,
        ),
    ]
    res = session.post(
        url=f"{NJORDA_API_SERVER}/v2/data/pnl-transactions/{account_id}",
        headers=get_auth_headers(),
        json={"items": transactions},
    )
    return res.json()


def creat_open_position(account_id: str):
    position = dict(
        account_id=account_id,
        quantity=2,
        ticker=INS_ERICB,
    )
    res = session.post(
        url=f"{NJORDA_API_SERVER}/v2/data/trades",
        headers=get_auth_headers(),
        json=position,
    )
    return res.json()


def get_transactions(account_id: str):
    res = session.get(
        url=f"{NJORDA_API_SERVER}/v2/data/pnl-transactions/{account_id}",
        headers=get_auth_headers(),
    )
    return res.json()


def get_client_summary(client_id):
    """
    API call to get summary of a client (risk_report, summary_report, positions_report, loans_summary,
    accounts_summary, allocations_report, risk_scenarios_report, pnl_report).
    """
    res = session.get(
        url=f"{NJORDA_API_SERVER}/v2/data/clients/{client_id}/summary?end_date=2024-06-12&start_date=2024-01-01",
        headers=get_auth_headers(),
    )
    return res.json()


def get_account_summary(account_id):
    """
    API call to get summary of a client (risk_report, summary_report, positions_report, loans_summary,
    accounts_summary, allocations_report, risk_scenarios_report, pnl_report).
    """
    res = session.get(
        url=f"{NJORDA_API_SERVER}/v2/data/accounts/{account_id}/summary?end_date=2024-06-12&start_date=2024-01-01",
        headers=get_auth_headers(),
    )
    return res.json()


def main():
    print(f" Server: {NJORDA_API_SERVER}")
    client = create_client()
    print(f" Created client: {client['id']}")
    account = create_account(client["id"])
    print(f" Created account: {account['id']}")
    transactions = upsert_transactions(account["id"])
    print(f" Created transactions: amount={len(transactions['items'])}")
    positions = creat_open_position(account["id"])
    print(f" Created positions: {positions}")
    client_summary = get_client_summary(client["id"])
    print(" Retrieved client summary")
    transactions = get_transactions(account["id"])
    print(f" Retrieved transactions: amount={len(transactions['items'])}")
    print(f" Clearing up...")
    delete_client(client["id"])
    print(
        f" Cleared up client and dependent records:\n"
        f" \t - account\n"
        f" \t\t - transactions\n"
    )
    pprint(client_summary)


if __name__ == "__main__":
    main()