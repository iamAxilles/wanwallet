import warnings
warnings.filterwarnings(
    "ignore",
    message="pkg_resources is deprecated as an API",
    category=UserWarning,
)

import json, os, pytest, requests
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

def tr():
    try:
        response = requests.post(
            RPC_URL,
            json=PAYLOAD_DATA,
            timeout=60,
        )
        response.raise_for_status()
        # print(response.json())
        return response.json()
    except HTTPError:
        return {"error": HTTPError}


from requests.exceptions import HTTPError
import responses

@responses.activate
def test_503():
    url = RPC_URL
    responses.add(responses.POST, url, status=503)
    assert tr() == {"error": HTTPError}


@pytest.mark.integration
def test_tr_real_rpc_success():#setup_env
    """Тест запроса к Ankr API."""
    data = tr()

    assert data is not None
    assert "result" in data
    assert "transfers" in data["result"]
    # assert isinstance(data["result"]["transfers"], list)

@pytest.mark.integration
def test_ankr_balance():
    balance_generator = ankr_w3.token.get_account_balance(
        request=GetAccountBalanceRequest(
            walletAddress=wallet,
            blockchain=["polygon"],
        )
    )

    balances = [vars(asset) for asset in balance_generator]
    assert balances



@pytest.mark.integration
def toomany():
    response = requests.Response()
    response.status_code = 429
    response.url = RPC_URL
    with patch("requests.post", return_value=response):
        with pytest.raises(requests.HTTPError) as exc_info:
            tr()
    assert exc_info.value.response.status_code == 429


@pytest.mark.integration
def test_timeout():
    with patch(
        "requests.post",
        side_effect=requests.Timeout("Connection timed out"),
    ):
        with pytest.raises(requests.Timeout):
            tr()





