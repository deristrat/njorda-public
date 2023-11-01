"""
Demo of uploading a portfolio and then calculating, market value, pnl
and portfolio scenarios

"""

import api_client as njorda


def upload_portfolio():
    # create user
    user_data = {
        "first_name": "Demo",
        "last_name": "User",
    }
    user = njorda.create_user(user_data)

    # get list of institutions
    institutions = njorda.get_institutions()

    # upload portfolio
    portfolio_data = {
        "user_id": user["id"],
        "accounts": [
            {
                "name": "Investment account",
                "currency": "SEK",
                "balance": 10000,
                "type": "investment",
                "investment_type": "isk",
                "institution_id": institutions["items"][0]["id"],
                "positions": [
                    {
                        "isin": "US0378331005",
                        "quantity": 100,
                        "acquisition_price": 141.9,
                        "timestamp": "2023-03-03T12:51",
                    },
                    {
                        "isin": "US30303M1027",
                        "quantity": 200,
                        "acquisition_price": 173.5,
                        "timestamp": "2023-03-03T12:51",
                    },
                    {
                        "isin": "US88160R1014",
                        "quantity": 50,
                        "acquisition_price": 186.1,
                        "timestamp": "2023-10-12T16:20",
                    },
                ],
            },
            {
                "name": "Small investment account",
                "currency": "SEK",
                "balance": 2000,
                "type": "investment",
                "investment_type": "isk",
                "institution_id": institutions["items"][1]["id"],
                "positions": [
                    {
                        "isin": "SE0000108656",
                        "quantity": 50,
                        "acquisition_price": 60.5,
                        "timestamp": "2023-03-03T12:51",
                    },
                    {
                        "isin": "SE0011527613",
                        "quantity": 50,
                        "acquisition_price": 165.3,
                        "timestamp": "2023-03-03T16:20",
                    },
                ],
            },
        ],
    }

    portfolio = njorda.upload_portfolio(portfolio_data)
    account_ids = [acc["id"] for acc in portfolio["accounts"]]

    # market value
    accounts_market_value = njorda.calculate_accounts_market_value(account_ids)
    print("\nAccounts market value:")
    print(accounts_market_value)

    # you can also pass user_id as parameter
    portfolio_scenario = njorda.calculate_user_portfolio_scenario(user["id"], 2)
    print("\nPortfolio scenario:")
    print(portfolio_scenario)

    # pnl
    accounts_pnl = njorda.calculate_accounts_pnl(
        account_ids, "2023-09-01", "2023-09-30"
    )
    print("\nAccounts PNL:")
    print(accounts_pnl)

    print("\nDone!")


if __name__ == "__main__":
    upload_portfolio()
