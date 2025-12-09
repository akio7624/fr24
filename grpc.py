import struct


def serialize_grpc_message(data: bytes, compressed: bool = False) -> bytes:
    assert not compressed

    is_compressed = 1 if compressed else 0

    header = struct.pack(">BI", is_compressed, len(data))
    return header + data

def get_grpc_message(grpc_response: bytes) -> bytes:
    assert grpc_response[0] == 0
    msg_size = struct.unpack(">I", grpc_response[1:5])[0]

    return grpc_response[5:5+msg_size]
