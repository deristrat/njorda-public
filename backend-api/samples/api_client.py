import os

import requests

NJORDA_API_SERVER = "https://api-v2.njorda-uat.se/"
NJORDA_API_TOKEN = os.environ["NJORDA_API_TOKEN"]


AUTH_HEADERS = {"Authorization": f"Bearer {NJORDA_API_TOKEN}"}


def create_user(user_data: dict) -> dict:
    return requests.post(
        url=f"{NJORDA_API_SERVER}/v2/data/users",
        headers=AUTH_HEADERS,
        json=user_data,
    ).json()


def get_data_providers() -> dict:
    return requests.get(
        url=f"{NJORDA_API_SERVER}/v2/data/data-providers",
        headers=AUTH_HEADERS,
    ).json()


def create_data_session(data_session_data: dict) -> dict:
    return requests.post(
        url=f"{NJORDA_API_SERVER}/v2/data/data-sessions",
        headers=AUTH_HEADERS,
        json=data_session_data,
    ).json()


def get_data_session(data_session_id: str) -> dict:
    return requests.get(
        url=f"{NJORDA_API_SERVER}/v2/data/data-sessions/{data_session_id}",
        headers=AUTH_HEADERS,
    ).json()


def commit_data_session(data_session_id: str, data_providers: list[dict]) -> dict:
    r = requests.patch(
        url=f"{NJORDA_API_SERVER}/v2/data/data-sessions/{data_session_id}",
        headers=AUTH_HEADERS,
        json={
            "data_providers": data_providers,
            "commit": True,
        },
    )
    return r.json()


def get_user_accounts(user_id: str) -> dict:
    return requests.get(
        url=f"{NJORDA_API_SERVER}/v2/data/holdings/accounts",
        headers=AUTH_HEADERS,
        params={"user_id": user_id},
    ).json()


def get_user_positions(user_id: str) -> dict:
    return requests.get(
        url=f"{NJORDA_API_SERVER}/v2/data/holdings/positions",
        headers=AUTH_HEADERS,
        params={"user_id": user_id},
    ).json()


def upload_portfolio(portfolio_data: dict) -> dict:
    return requests.post(
        url=f"{NJORDA_API_SERVER}/v2/data/portfolios",
        headers=AUTH_HEADERS,
        json=portfolio_data,
    ).json()


def get_institutions() -> dict:
    return requests.get(
        url=f"{NJORDA_API_SERVER}/v2/data/institutions",
        headers=AUTH_HEADERS,
    ).json()


def calculate_accounts_market_value(account_ids: list[str]) -> dict:
    return requests.get(
        url=f"{NJORDA_API_SERVER}/v2/calculate/market-value/accounts",
        headers=AUTH_HEADERS,
        params={"account_ids": ",".join(account_ids)},
    ).json()


def calculate_accounts_pnl(
    account_ids: list[str],
    start_date: str,
    end_data: str,
) -> dict:
    return requests.get(
        url=f"{NJORDA_API_SERVER}/v2/calculate/profit-and-loss/accounts",
        headers=AUTH_HEADERS,
        params={
            "account_ids": ",".join(account_ids),
            "start_date": start_date,
            "end_date": end_data,
        },
    ).json()


def calculate_user_portfolio_scenario(user_id: str, years: int) -> dict:
    return requests.get(
        url=f"{NJORDA_API_SERVER}/v2/calculate/portfolio-scenario/user",
        headers=AUTH_HEADERS,
        params={"user_id": user_id, "years_to_simulate": years},
    ).json()


def calculate_positions_market_value(positions_data: list[dict]) -> dict:
    return requests.post(
        url=f"{NJORDA_API_SERVER}/v2/calculate/market-value/positions",
        headers=AUTH_HEADERS,
        json={"positions": positions_data},
    ).json()


def calculate_positions_market_value_history(
    positions_data: list[dict],
    start_date: str,
    end_date: str,
) -> dict:
    return requests.post(
        url=f"{NJORDA_API_SERVER}/v2/calculate/market-value-history/positions",
        headers=AUTH_HEADERS,
        json={
            "positions": positions_data,
            "start_date": start_date,
            "end_date": end_date,
        },
    ).json()


def calculate_positions_expected_return(positions_data: list[dict]) -> dict:
    return requests.post(
        url=f"{NJORDA_API_SERVER}/v2/calculate/expected-return/positions",
        headers=AUTH_HEADERS,
        json={"positions": positions_data},
    ).json()


def calculate_positions_pnl(
    positions_data: list[dict],
    start_date: str,
    end_date: str,
) -> dict:
    return requests.post(
        url=f"{NJORDA_API_SERVER}/v2/calculate/profit-and-loss/positions",
        headers=AUTH_HEADERS,
        json={
            "positions": positions_data,
            "start_date": start_date,
            "end_date": end_date,
        },
    ).json()
