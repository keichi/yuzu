# @generated by generate_proto_mypy_stubs.py.  Do not edit!
import sys
from google.protobuf.descriptor import (
    Descriptor as google___protobuf___descriptor___Descriptor,
    EnumDescriptor as google___protobuf___descriptor___EnumDescriptor,
)

from google.protobuf.message import (
    Message as google___protobuf___message___Message,
)

from typing import (
    List as typing___List,
    Optional as typing___Optional,
    Text as typing___Text,
    Tuple as typing___Tuple,
    Union as typing___Union,
    cast as typing___cast,
)

from typing_extensions import (
    Literal as typing_extensions___Literal,
)


builtin___bool = bool
builtin___bytes = bytes
builtin___float = float
builtin___int = int
builtin___str = str
if sys.version_info < (3,):
    builtin___buffer = buffer
    builtin___unicode = unicode


class TimerType(builtin___int):
    DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
    @classmethod
    def Name(cls, number: builtin___int) -> builtin___str: ...
    @classmethod
    def Value(cls, name: builtin___str) -> 'TimerType': ...
    @classmethod
    def keys(cls) -> typing___List[builtin___str]: ...
    @classmethod
    def values(cls) -> typing___List['TimerType']: ...
    @classmethod
    def items(cls) -> typing___List[typing___Tuple[builtin___str, 'TimerType']]: ...
    READ_IO = typing___cast('TimerType', 0)
    COMPUTE = typing___cast('TimerType', 1)
    WRITE_IO = typing___cast('TimerType', 2)
    TOTAL = typing___cast('TimerType', 3)
READ_IO = typing___cast('TimerType', 0)
COMPUTE = typing___cast('TimerType', 1)
WRITE_IO = typing___cast('TimerType', 2)
TOTAL = typing___cast('TimerType', 3)
global___TimerType = TimerType

class Common(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    app_name = ... # type: typing___Text
    step = ... # type: builtin___int
    elapsed = ... # type: builtin___float

    def __init__(self,
        *,
        app_name : typing___Optional[typing___Text] = None,
        step : typing___Optional[builtin___int] = None,
        elapsed : typing___Optional[builtin___float] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> Common: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> Common: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"app_name",b"app_name",u"elapsed",b"elapsed",u"step",b"step"]) -> None: ...
global___Common = Common

class TimerTelemetry(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    timer_type = ... # type: global___TimerType
    duration = ... # type: builtin___float

    @property
    def common(self) -> global___Common: ...

    def __init__(self,
        *,
        common : typing___Optional[global___Common] = None,
        timer_type : typing___Optional[global___TimerType] = None,
        duration : typing___Optional[builtin___float] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> TimerTelemetry: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> TimerTelemetry: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"common",b"common"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"common",b"common",u"duration",b"duration",u"timer_type",b"timer_type"]) -> None: ...
global___TimerTelemetry = TimerTelemetry

class DataSizeTelemetry(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    size = ... # type: builtin___int

    @property
    def common(self) -> global___Common: ...

    def __init__(self,
        *,
        common : typing___Optional[global___Common] = None,
        size : typing___Optional[builtin___int] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> DataSizeTelemetry: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> DataSizeTelemetry: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"common",b"common"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"common",b"common",u"size",b"size"]) -> None: ...
global___DataSizeTelemetry = DataSizeTelemetry

class TelemetryReply(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    def __init__(self,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> TelemetryReply: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> TelemetryReply: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
global___TelemetryReply = TelemetryReply
