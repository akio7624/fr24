import json
from pathlib import Path
from typing import Optional, Literal

from google.protobuf.json_format import MessageToDict

from fr24 import grpc
from schema import livefeed_pb2

class LiveFeedDump:
    @staticmethod
    def dump(typ: Literal["response", "request"], protobuf_raw: bytes) -> Optional[dict]:
        if typ == "request":
            msg = livefeed_pb2.LiveFeedRequest()
        elif typ == "response":
            msg = livefeed_pb2.LiveFeedResponse()
        else:
            raise Exception(f"{typ} is not supported")

        msg.ParseFromString(protobuf_raw)
        return MessageToDict(msg, preserving_proto_field_name=True)


if __name__ == "__main__":
    grpc_raw = Path("playground/request_body.bin").read_bytes()
    protobuf_raw = grpc.get_grpc_message(grpc_raw)
    result = LiveFeedDump.dump("request", protobuf_raw)
    print(json.dumps(result, indent=4, ensure_ascii=False))

    grpc_raw = Path("playground/response_body.bin").read_bytes()
    protobuf_raw = grpc.get_grpc_message(grpc_raw)
    result = LiveFeedDump.dump("response", protobuf_raw)
    print(json.dumps(result, indent=4, ensure_ascii=False))
