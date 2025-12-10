import json
from google.protobuf.json_format import ParseDict

from fr24 import grpc
from schema import livefeed_pb2

class MakeRequestGrpc:
    def __init__(self):
        self.PAYLOAD_DICT: dict = {}

    def set_data_from_json(self, path: str):
        self.PAYLOAD_DICT = json.loads(open(path).read())

    def make(self) -> bytes:
        req = livefeed_pb2.LiveFeedRequest()
        ParseDict(self.PAYLOAD_DICT, req)
        body = req.SerializeToString()
        grpc_raw = grpc.serialize_grpc_message(body, compressed=False)

        return grpc_raw


if __name__ == "__main__":
    request_builder = MakeRequestGrpc()
    request_builder.set_data_from_json("playground/request.json")
    request_payload = request_builder.make()
    print(len(request_payload))
