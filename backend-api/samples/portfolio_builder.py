"""Demo of collecting holdings, where all steps are handled in iframe"""
import os
from json import dumps
from random import random

import dotenv
dotenv.load_dotenv()


import requests

NJORDA_API_SERVER = os.getenv("NJORDA_API_SERVER")
NJORDA_API_TOKEN = os.getenv("NJORDA_API_TOKEN")
print(f"API SERVER: {NJORDA_API_SERVER}")

auth_headers = {'Authorization': 'Bearer ' + NJORDA_API_TOKEN}
auth_json_headers = {'Content-Type': 'application/json', **auth_headers}


def get(url, params=None):
    return requests.get(NJORDA_API_SERVER + url, headers=auth_headers, params=params).json()


def post(url, data, raw=False):
    res = requests.post(NJORDA_API_SERVER + url, headers=auth_json_headers, data=dumps(data))
    return res if raw else res.json()



def get_proposal_pdf(proposal_id: str):
    res = post(
        f"/v2/data/proposals/{proposal_id}/export",
        data={},
        raw=True,
        #extra_headers={"Accept-Language": "sv"},
    )
    open("proposal.pdf", "wb").write(res.content)

def construct_portfolio():
    # 1. Create user object
    user = post("/v2/data/users", data={
        'first_name': "Test",
        'last_name': "API",
        'user_type': 'org_advisor',
        'email': str(random()) +'apitest@njorda.se',
        'password': "nopass" + str(random())
        # Optionally pass person nbr: "personal_number": "19940508-7223"#
    })
    print("Created user: ", user)
    user_id = user["id"]

    # 2. Create data session
    embed_urls = get(f"/v2/data/users/{user_id}/embedding-urls")
    url = embed_urls["portfolio_builder_embed_url"]

    #if client_id:
    #    url += f"&client_id={client_id}"
    print(f"\nEmbedding urls: {embed_urls}")

    print(f"Open this url in your browser:\n{url}")

    input("Press Enter to continue...")



if __name__ == "__main__":
    construct_portfolio()
    #get_proposal_pdf("UUID FOR SAVED PROPOSAL")
