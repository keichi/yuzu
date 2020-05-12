# yuzu


```
poetry install
```

```
poetry run python -m grpc.tools.protoc -I protos --python_out=yuzu/pb --grpc_python_out=yuzu/pb collector.proto
```
