#!bin/bash
mkdir -p src/finam_client/generated \
&& python -m grpc_tools.protoc \
    --proto_path=src/finam_client/api/grpc/ \
    --python_out=src/finam_client/generated \
    --pyi_out=src/finam_client/generated \
    --grpc_python_out=src/finam_client/generated \
    gateway/protoc_gen_openapiv2/options/annotations.proto \
&& python -m grpc_tools.protoc \
    --proto_path=src/finam_client/api/grpc/ \
    --python_out=src/finam_client/generated \
    --pyi_out=src/finam_client/generated \
    --grpc_python_out=src/finam_client/generated \
    gateway/protoc_gen_openapiv2/options/openapiv2.proto \
&& python -m grpc_tools.protoc \
    --proto_path=src/finam_client/api/grpc/ \
    --python_out=src/finam_client/generated \
    --pyi_out=src/finam_client/generated \
    --grpc_python_out=src/finam_client/generated \
    google/api/annotations.proto \
&& python -m grpc_tools.protoc \
    --proto_path=src/finam_client/api/grpc/ \
    --python_out=src/finam_client/generated \
    --pyi_out=src/finam_client/generated \
    --grpc_python_out=src/finam_client/generated \
    google/api/http.proto \
&& python -m grpc_tools.protoc \
    --proto_path=src/finam_client/api/grpc/ \
    --python_out=src/finam_client/generated \
    --pyi_out=src/finam_client/generated \
    --grpc_python_out=src/finam_client/generated \
    tradeapi/v1/auth/auth_service.proto