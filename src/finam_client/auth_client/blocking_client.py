from ..generated.tradeapi.v1.auth.auth_service_pb2_grpc import AuthServiceStub
from grpc import secure_channel, ssl_channel_credentials, Channel
from .models import AuthRequestModel, AuthResponseModel, TokenDetailsResponseModel, TokenDetailsRequestModel

class AuthClient:
    def __init__(
        self,
        host: str,
        port: int,
    ) -> None:
        self.endpoint = f"{host}:{port}"
        self.credential = ssl_channel_credentials()
        self._channel: Channel | None = None
        self._stub: AuthServiceStub | None = None
        self._setup()

    def _setup(self) -> None:
        self._channel = secure_channel(target=self.endpoint, credentials=self.credential)
        self._stub = AuthServiceStub(channel=self._channel)
    
    def auth(self, request: AuthRequestModel) -> AuthResponseModel:
        if self._stub:
            grpc_request = request.protobuf_fmt
            grpc_response = self._stub.Auth(grpc_request)
            response = AuthResponseModel.from_protobuf(grpc_response)
            return response
        else:
            raise RuntimeError
        
    def token_details(self, request: TokenDetailsRequestModel) -> TokenDetailsResponseModel:
        if self._stub:
            grpc_request = request.protobuf_fmt
            grpc_response = self._stub.TokenDetails(grpc_request)
            response = TokenDetailsResponseModel.from_protobuf(grpc_response)
            return response
        else:
            raise RuntimeError
