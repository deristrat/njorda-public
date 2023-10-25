import datetime

import api_client as njorda


def calculate_apis():
    # Note: all calculate APIs support user_id, accounts_ids, or positions data as input.
    # Use user_id or accounts_ids if you've already collected data from the user.

    positions_data = [
        {
            "isin": "SE0001718388",
            "quantity": 5.4,
        },
        {
            "isin": "US0378331005",
            "quantity": 2.1,
        },
    ]

    # expected return
    expected_return = njorda.calculate_positions_expected_return(positions_data)
    print(f"Expected return:")
    print(expected_return)

    # pnl
    trades_data = []
    for position in positions_data:
        trades_data.append(
            {
                "isin": position["isin"],
                "quantity": position["quantity"],
                "acquire_price": 100,
                "trade_date": "2023-09-10",
            }
        )
    pnl = njorda.calculate_positions_pnl(
        trades_data,
        start_date="2023-09-01",
        end_date="2023-09-30",
    )
    print(f"\nProfit and Loss:")
    print(pnl)

    # market value history
    market_value_history = njorda.calculate_positions_market_value_history(
        positions_data,
        start_date="2021-01-01",
        end_date=datetime.date.today().isoformat(),
    )
    print(f"\nMarket value history:")
    print(market_value_history)

    print("\nDone!")


if __name__ == "__main__":
    calculate_apis()
