import json
from pathlib import Path
from typing import Optional, Literal

from google.protobuf.json_format import MessageToDict

from fr24 import grpc
from schema import followflight_pb2  # protoc --python_out=. --pyi_out=. followflight.proto

class FollowFlightDump:
    @staticmethod
    def dump(typ: Literal["response", "request"], protobuf_raw: bytes) -> Optional[dict]:
        if typ == "request":
            msg = followflight_pb2.FollowFlightRequest()
        elif typ == "response":
            msg = followflight_pb2.FollowFlightResponse()
        else:
            raise Exception(f"{typ} is not supported")

        msg.ParseFromString(protobuf_raw)
        return MessageToDict(msg, preserving_proto_field_name=True)


if __name__ == "__main__":
    grpc_raw = Path("testground/follow_req.bin").read_bytes()
    protobuf_raw = grpc.get_grpc_message(grpc_raw)
    result = FollowFlightDump.dump("request", protobuf_raw)
    print(json.dumps(result, indent=4, ensure_ascii=False))

    print("-------------")

    grpc_raw = Path("testground/chunk_first.bin.bak").read_bytes()
    protobuf_raw = grpc.get_grpc_message(grpc_raw)
    result = FollowFlightDump.dump("response", protobuf_raw)
    print(json.dumps(result, indent=4, ensure_ascii=False))

    print("-------------")

    grpc_raw = Path("testground/chunk_middle.bin.bak").read_bytes()
    protobuf_raw = grpc.get_grpc_message(grpc_raw)
    result = FollowFlightDump.dump("response", protobuf_raw)
    print(json.dumps(result, indent=4, ensure_ascii=False))
