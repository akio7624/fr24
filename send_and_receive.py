import json
from pathlib import Path
import requests

from fr24 import grpc
from fr24.request_builder import MakeRequestGrpc
from fr24.response_dump import DumpResponse


request_builder = MakeRequestGrpc()
request_builder.set_data_from_json("playground/request.json")
request_payload = request_builder.make()

URL = "https://data-feed.flightradar24.com/fr24.feed.api.v1.Feed/LiveFeed"
headers = {
    "X-User-Agent": "grpc-web-javascript/0.1",
    "Fr24-Device-Id": "web-5dwifk6f8-fj2fdFi0DY2fvxsrAs71h",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
    "Content-Type": "application/grpc-web+proto",
    "X-Grpc-Web": "1",
}

resp = requests.post(URL, headers=headers, data=request_payload)
resp.raise_for_status()
# Path("output/response_body.bin").write_bytes(resp.content)

protobuf_raw = grpc.get_grpc_message(resp.content)
dump_result = DumpResponse().dump(protobuf_raw)
print(json.dumps(dump_result, indent=4, ensure_ascii=False))
