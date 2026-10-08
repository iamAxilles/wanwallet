import warnings
warnings.filterwarnings(
    "ignore",
    message="pkg_resources is deprecated as an API",
    category=UserWarning,
)

import os, pytest
from dotenv import load_dotenv
load_dotenv()

from ankr import AnkrWeb3
from ankr.types import GetAccountBalanceRequest


ankr_w3 = AnkrWeb3(os.environ.get("k"))
wallet = os.environ.get("w")

balance_generator = ankr_w3.token.get_account_balance(
    request=GetAccountBalanceRequest(
        walletAddress=wallet,
        blockchain=["polygon"]
    )
)


balances_list = []
for asset in balance_generator:
    # Use vars() or __dict__ to convert the Balance object into a JSON-serializable dict
    balances_list.append(vars(asset))

from fastapi import FastAPI
import transfers
from contextlib import asynccontextmanager


@asynccontextmanager
# @app.on_event("startup")
async def lifespan(app: FastAPI):
    with connect:
        with connect.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tokens (
                    id SERIAL PRIMARY KEY,
                    token_name TEXT NOT NULL,
                    balance NUMERIC(30, 18) NOT NULL DEFAULT 0,

                    CONSTRAINT tokens_token_name_unique
                    UNIQUE (token_name)
                );
            """)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(transfers.transf)


import psycopg2
connect = psycopg2.connect(os.environ.get("baza"))



@app.get("/balance")
def balance():
    with connect:
        with connect.cursor() as cursor:

            for i in range(len(balances_list)):
                tokenName = balances_list[i]["tokenName"]
                balance = balances_list[i]["balance"]

                cursor.execute("""
                    INSERT INTO tokens (token_name, balance)
                    VALUES (%s, %s)
                    ON CONFLICT (token_name)
                    DO UPDATE SET
                        balance = EXCLUDED.balance;
                """, (
                    tokenName,
                    balance,
                ))

                cursor.execute("""
                    SELECT token_name, balance
                    FROM tokens
                    ORDER BY id;
                """)

                rows = []
                for token_name, balance in cursor.fetchall():
                    rows.append({
                        token_name,
                        balance,
                    })

    return rows


from fastapi.testclient import TestClient


@app.get("/Hello")
async def read_main():
    return {"msg": "Hello World"}


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}

