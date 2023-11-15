"""Sample code to calulate risk for a couple of random portfolios.

Demonstrates usage of: /v2/calculate/portfolio-scenario/positions

"""

import os
import random
from typing import TypedDict, List

import requests

NJORDA_API_TOKEN = os.environ["NJORDA_API_TOKEN"]
NJORDA_API_SERVER = "https://api-v2.njorda-uat.se/"

# use global session to avoid, reconnecting for each request
session = requests.Session()

# Sample instruments that are loaded in any all sandbox environments
instruments = [
    ["CH0012221716", "ABB"],
    ["SE0000115446", "Volvo B"],
    ["SE0000108656", "Ericsson B"],
    ["SE0000148884", "SEB A"],
    ["SE0017486889", "Atlas Copco A"],
    ["SE0007100599", "Handelsbanken A"],
    ["SE0000106270", "Hennes & Mauritz B"],
    ["SE0015810247", "Kinnevik B"],
    ["GB0009895292", "AstraZeneca PLC"],
    ["SE0015811963", "Investor B"],
    ["SE0018535684", "Betsson B"],
    ["US0567521085", "Baidu Inc"],
    ["US0378331005", "Apple"],
    ["US17275R1023", "Cisco Systems Inc."],
    ["US5949181045", "Microsoft"],
    ["US88160R1014", "Tesla Inc."],
    ["US67066G1040", "NVIDIA Corporation"],
    ["SE0000862278", "AMF Aktiefond Global"],
    ["SE0005281847", "Skandia Global Exponering"],
    ["SE0012428290", "Robur Access Edge Em. Markets"],
    ["SE0005796331", "Länsförsäkringar Tillväxmarknad Index A"],
    ["SE0004578615", "Öhman Emerging Markets A"],
    ["SE0001827692", "Simplicity Likviditet"],
    ["SE0002152140", "Spiltan Räntefond Sverige"],
    ["SE0001184961", "AMF Räntefond Kort"],
    ["SE0000429789", "Carnegie Sverigefond A"],
    ["SE0001015348", "Spiltan Aktiefond Stabil"],
    ["SE0000775298", "SEB Sverigefond"],
    ["SE0008992069", "Cliens Småbolag"],
]

Position = TypedDict("Position", {"isin": str, "quantity": float})


def calc_risk(positions: List[Position]) -> dict:
    res = session.post(
        url=f"{NJORDA_API_SERVER}/v2/calculate/portfolio-scenario/positions",
        headers={"Authorization": f"Bearer {NJORDA_API_TOKEN}"},
        json={
            "years_to_simulate": 1,
            "positions": positions
        })
    return res.json()


def calc_random_portfolio(num_positions: int):
    selected_instruments = random.sample(instruments, num_positions)
    positions = [{'isin': ins[0], 'quantity': random.randint(10, 20)} for ins in
                 selected_instruments]
    return calc_risk(positions)


def risk_random_portfolios():
    num_portfolios_per_size = 5
    for pf_size in [5, 10, 20]:
        for i in range(num_portfolios_per_size):
            res = calc_random_portfolio(pf_size)
            # Print a few of the returned values.
            print(f"Expected return: {res['expected_return']}, worst case: {res['worst_case']}")


if __name__ == "__main__":
    risk_random_portfolios()
