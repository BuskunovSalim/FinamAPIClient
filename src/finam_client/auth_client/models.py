from ..generated.tradeapi.v1.auth.auth_service_pb2 import MDPermission, AuthRequest, AuthResponse, TokenDetailsRequest, TokenDetailsResponse
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod
from google.protobuf.message import Message
from typing import Self
from datetime import datetime
from enum import Enum
from ..core.utils import datetime_to_timestamp, timestamp_to_datetime

@dataclass
class Model(ABC):
    
    @property
    @abstractmethod
    def protobuf_fmt(self) -> Message:
        ...

    @classmethod
    @abstractmethod
    def from_protobuf(cls, message: Message) -> Self:
        ...




@dataclass(slots=True)
class AuthRequestModel(Model):
    secret: str

    @property
    def protobuf_fmt(self) -> AuthRequest:
        return AuthRequest(
            secret=self.secret
        )
    
    @classmethod
    def from_protobuf(cls, message: AuthRequest) -> Self:
        return cls(
            secret=message.secret or "",
        )

@dataclass(slots=True)
class AuthResponseModel(Model):
    token: str

    @property
    def protobuf_fmt(self) -> AuthResponse:
        return AuthResponse(
            token=self.token
        )
    
    @classmethod
    def from_protobuf(cls, message: AuthResponse) -> Self:
        return cls(
            token=message.token or "",
        )

@dataclass(slots=True)
class TokenDetailsRequestModel(Model):
    token: str

    @property
    def protobuf_fmt(self) -> TokenDetailsRequest:
        return TokenDetailsRequest(
            token=self.token
        )
    
    @classmethod
    def from_protobuf(cls, message: TokenDetailsRequest) -> Self:
        return cls(
            token=message.token or "",
        )

class QuoteLevelEnum(Enum):
    QUOTE_LEVEL_UNSPECIFIED = 0
    QUOTE_LEVEL_LAST_PRICE = 1
    QUOTE_LEVEL_BEST_BID_OFFER = 2
    QUOTE_LEVEL_DEPTH_OF_MARKET = 3
    QUOTE_LEVEL_DEPTH_OF_BOOK = 4
    QUOTE_LEVEL_ACCESS_FORBIDDEN = 5

    @classmethod
    def from_proto_enum(cls, protobuf_enum: MDPermission.QuoteLevel) -> Self:
        return cls(protobuf_enum)

@dataclass(slots=True)
class MDPermissionModel(Model):
    quote_level: QuoteLevelEnum
    delay_minutes: int
    mic: str | None = None
    country: str | None = None
    continent: str | None = None
    worldwide: bool | None = None

    @property
    def protobuf_fmt(self) -> MDPermission:
        raw_data = asdict(self)
        return MDPermission(
            **{
                k: v
                for k, v in raw_data.items()
                if v is not None
            }
        )
    
    @classmethod
    def from_protobuf(cls, message: MDPermission) -> Self:
        condition_field = message.WhichOneof("condition")
        condition = {
            condition_field: getattr(message, condition_field)}
        return cls(
            quote_level=QuoteLevelEnum.from_proto_enum(message.quote_level),
            delay_minutes=message.delay_minutes,
            **condition,
        )


@dataclass(slots=True)
class TokenDetailsResponseModel(Model):
    created_at: datetime
    expires_at: datetime
    md_permissions: tuple[MDPermissionModel, ...]
    account_ids: tuple[str, ...]
    readonly: bool

    @property
    def protobuf_fmt(self) -> TokenDetailsResponse:
        return TokenDetailsResponse(
            created_at=datetime_to_timestamp(self.created_at),
            expires_at=datetime_to_timestamp(self.expires_at),
            md_permissions=tuple(
                permission.protobuf_fmt
                for permission in self.md_permissions
            ),
            account_ids=self.account_ids,
            readonly=self.readonly,
        )
    
    @classmethod
    def from_protobuf(cls, message: TokenDetailsResponse) -> Self:
        return cls(
            created_at=timestamp_to_datetime(message.created_at),
            expires_at=timestamp_to_datetime(message.expires_at),
            md_permissions=tuple(
                MDPermissionModel.from_protobuf(permission)
                for permission in message.md_permissions
            ),
            account_ids=tuple(
                account_id
                for account_id in message.account_ids 
            ),
            readonly=message.readonly
        )
