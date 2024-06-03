import asyncio
import json
import logging

import grpc

from proto import (
    distance_calculator_service_pb2_grpc,
    distance_calculator_service_pb2,
)
from tools import OSMTools
from grpc import aio as grpc_aio
from grpc_reflection.v1alpha import reflection

tools = OSMTools()
logging.basicConfig(level=logging.DEBUG)


class DistanceCalculatorServiceServicer(
    distance_calculator_service_pb2_grpc.DistanceCalculatorServiceServicer
):
    async def CalculateDistance(
        self, request, context
    ):
        res = await tools.find_nearest_object(
            request.object,
            request.latitude,
            request.longitude,
            request.search_distance or 1000,
        )
        is_found = True if res else False
        res = res or {"distance": 0}

        return distance_calculator_service_pb2.CalculateDistanceResponse(
            is_found=is_found,
            distance=res["distance"],
            object=json.dumps(
                res, ensure_ascii=False
            ),
        )


async def serve():

    server = grpc_aio.server(
        options=[
            (
                "grpc.max_send_message_length",
                50 * 1024 * 1024,
            ),
            (
                "grpc.max_receive_message_length",
                50 * 1024 * 1024,
            ),
        ]
    )
    distance_calculator_service_pb2_grpc.add_DistanceCalculatorServiceServicer_to_server(
        DistanceCalculatorServiceServicer(),
        server,
    )
    listen_addr = "[::]:50051"
    service_names = (
        distance_calculator_service_pb2.DESCRIPTOR.services_by_name[
            "DistanceCalculatorService"
        ].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(
        service_names, server
    )

    server.add_insecure_port(listen_addr)
    await server.start()
    try:
        await server.wait_for_termination()
    finally:
        await server.stop(0)


if __name__ == "__main__":
    asyncio.run(serve())
