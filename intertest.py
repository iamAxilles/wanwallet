import warnings
warnings.filterwarnings(
    "ignore",
    message="pkg_resources is deprecated as an API",
    category=UserWarning,
)

import json, os, pytest, requests, responses
from unittest.mock import patch

from ankr import AnkrWeb3
from ankr.types import GetAccountBalanceRequest

from dotenv import load_dotenv
load_dotenv()

# from mymodule import tr
# from toke import balance_generator


RPC_URL = os.environ.get("RPC")
PAYLOAD_DATA = json.loads(os.environ.get("payload"))

ankr_w3 = AnkrWeb3(os.environ.get("k"))
wallet = os.environ.get("w")


# @pytest.fixture
# def setup_env(monkeypatch):
#     monkeypatch.setenv("RPC", RPC_URL)
#     monkeypatch.setenv("payload", json.loads(PAYLOAD_DATA))
from requests.exceptions import HTTPError

def tr():
    try:
        response = requests.post(
            RPC_URL,
            json=PAYLOAD_DATA,
            timeout=60,
        )
        response.raise_for_status()
        # print(response.status_code)
        return response.json()
    except HTTPError as e:
        return {"error": e}


@responses.activate
def test_503Unavailable():
    responses.add(responses.POST, RPC_URL, status=503)
    assert tr()["error"].response.status_code == 503


@responses.activate
def test_toomany():
    responses.add(responses.POST, RPC_URL, status=429)
    assert tr()["error"].response.status_code == 429


@pytest.mark.inter
def test_tr_real_rpc_success():#setup_env
    """Тест запроса к Ankr."""
    data = tr()
    assert data is not None
    assert "result" in data
    assert "transfers" in data["result"]
    # assert isinstance(data["result"]["transfers"], list)

@pytest.mark.inter
def test_ankr_balance():
    balance_generator = ankr_w3.token.get_account_balance(
        request=GetAccountBalanceRequest(
            walletAddress=wallet,
            blockchain=["polygon"],
        )
    )

    balances = [vars(asset) for asset in balance_generator]
    assert balances


@pytest.mark.inter
def test_timeout():
    with patch(
        "requests.post",
        side_effect=requests.Timeout("Connection timed out"),
    ):
        with pytest.raises(requests.Timeout):
            tr()





