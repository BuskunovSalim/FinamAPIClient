from finam_client.auth_client.blocking_client import AuthClient, AuthRequestModel, TokenDetailsRequestModel, TokenDetailsResponseModel
from grpc import RpcError, StatusCode
from pytest import mark, fixture, raises
from os import getenv
from dotenv import load_dotenv
from pathlib import Path

_env_path = Path(__file__).resolve().parent / ".env"

load_dotenv(_env_path)

TESTING_SECRET = getenv("TESTING_SECRET")

@fixture
def client() -> AuthClient:
    return AuthClient("api.finam.ru", 443)

@mark.parametrize(
    "token",
    ("", "broken-token"),
)
def test_bad_auth(client: AuthClient, token: str) -> None:
    request = AuthRequestModel(token)
    with raises(RpcError) as e:
        client.auth(request=request)
    assert e.value.code() == StatusCode.UNAUTHENTICATED

def test_good_auth(client: AuthClient) -> None:
    if TESTING_SECRET is not None:
        request = AuthRequestModel(TESTING_SECRET)
        result = client.auth(request=request)
        assert len(result.token) > 0
    else:
        raise Exception(f"Укажите параметр TESTING_SECRET=... в {_env_path}.")

def test_token_details(client: AuthClient) -> None:
    if TESTING_SECRET is not None:
        request = AuthRequestModel(TESTING_SECRET)
        result = client.auth(request=request)
        jwt = result.token
        token_model = TokenDetailsRequestModel(
            token=jwt,
        )
        info = client.token_details(
            request=token_model
        )
        assert info is not None
