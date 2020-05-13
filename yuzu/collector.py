from concurrent.futures import ThreadPoolExecutor
from typing import Dict

import grpc

from .application import Application
from .pb.collector_pb2 import TelemetryReply, TimerType
from .pb.collector_pb2_grpc import (YuzuCollectorServicer,
                                    add_YuzuCollectorServicer_to_server)


class CollectorServicer(YuzuCollectorServicer):
    def __init__(self, apps: Dict[str, Application]):
        self.apps = apps

    def ReportTimer(self, request, context):  # noqa: N802

        app_name = request.common.app_name

        if app_name not in self.apps:
            print(f"Received timer telemetry from unknown app {app_name}")
            return TelemetryReply()

        app = self.apps[app_name]

        if request.timer_type == TimerType.READ_IO:
            app.time_read[request.common.step] = request.duration
        elif request.timer_type == TimerType.COMPUTE:
            app.time_compute[request.common.step] = request.duration
        elif request.timer_type == TimerType.WRITE_IO:
            app.time_write[request.common.step] = request.duration
        elif request.timer_type == TimerType.TOTAL:
            app.time_total[request.common.step] = request.duration
        else:
            print(f"Unknown timer type {request.timer_type}")

        return TelemetryReply()

    def ReportDataSize(self, request, context):  # noqa: N802
        return TelemetryReply()


def create_collector(apps) -> grpc.Server:
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    add_YuzuCollectorServicer_to_server(CollectorServicer(apps),
                                        server)

    return server


def start_collector(server: grpc.Server) -> None:
    print("Starting gRPC collector server")

    server.add_insecure_port("[::]:50051")
    server.start()
