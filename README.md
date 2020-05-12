# yuzu


```
poetry install
```

Python

```
poetry run python -m grpc.tools.protoc -I protos --python_out=yuzu/pb --grpc_python_out=yuzu/pb collector.proto
```

C++

```
protoc -I protos --cpp_out=. --grpc_out=. --plugin=protoc-gen-grpc=`which grpc_cpp_plugin` protos/collector.proto

```
