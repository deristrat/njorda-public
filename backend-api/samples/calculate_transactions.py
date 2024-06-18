# https://gist.github.com/droos1/9606e78dd6dc8834c67d615e2cba2b6b


"""Sample code to calculate risk for a couple of random portfolios.
Demonstrates usage of: /v2/calculate/portfolio-scenario/transactions
"""

import os
from pprint import pprint

from dotenv import load_dotenv
import matplotlib.pyplot as plt
import pandas as pd
import requests

# Install the python-dotenv package, to use an .env file for settings

load_dotenv()

NJORDA_API_TOKEN = os.environ["NJORDA_API_TOKEN"]
NJORDA_API_SERVER = os.environ["NJORDA_API_SERVER"]

# use global session to avoid, reconnecting for each request
session = requests.Session()

INS_ERICB = "SE0000108656"


def calc_pnl(transactions):
    res = session.post(
        url=f"{NJORDA_API_SERVER}/v2/calculate/profit-and-loss/transactions",
        headers={"Authorization": f"Bearer {NJORDA_API_TOKEN}"},
        json={
            "start_date": "2024-01-01",
            "end_date": "2024-05-30",
            "transactions": transactions,
        },
    )
    print(res.content)
    return res.json()


def show_results(res, plot=True):
    df = pd.DataFrame(res["time_series"])
    df.set_index("date", inplace=True)
    if plot:
        df.plot(drawstyle="steps", figsize=(14, 8), grid=True, title="Time Series Data")
        plt.show()
    # limit amount of output by just showing last two dates:
    res["time_series"] = res["time_series"][-2:]
    pprint(res)


def calc_pnl_buy_close():
    positions = [
        # Put initial cash into account
        dict(
            type="TRANSFER",
            amount=1000,
            currency="SEK",
            fx_rate=1.0,
            date="2024-01-04",
            instrument=INS_ERICB,
            quantity=10,
        ),
        # Buy 10 Ericsson B shares
        dict(
            type="TRADE",
            amount=-10 * 56.1,
            currency="SEK",
            fx_rate=1.0,
            date="2024-02-02",
            instrument=INS_ERICB,
            quantity=10,
        ),
        # Sell half the position
        dict(
            type="TRADE",
            amount=5 * 58.59,
            currency="SEK",
            fx_rate=1.0,
            date="2024-03-14",
            instrument=INS_ERICB,
            quantity=-5,
        ),
        # Sell the rest
        dict(
            type="TRADE",
            amount=5 * 61.9,
            currency="SEK",
            fx_rate=1.0,
            date="2024-05-14",
            instrument=INS_ERICB,
            quantity=-5,
        ),
    ]
    res = calc_pnl(positions)
    show_results(res, plot=True)

    final_state = res["final_state"]
    print(f" RPL = {final_state['rpl']}")
    print(f" Cash = {final_state['cash']}")
    print(f" Market value investments = {final_state['market_value_investments']}")


if __name__ == "__main__":
    print(f" Server: {NJORDA_API_SERVER}")
    calc_pnl_buy_close()
