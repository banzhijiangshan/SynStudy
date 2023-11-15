import json

def binary_to_json(b):
    assert isinstance(b, bytes)
    decoded = b.decode()
    return json.loads(decoded)

def process_register_data(raw_data):
    json_res = binary_to_json(raw_data)
    return json_res

def process_login_data(raw_data):
    json_res = binary_to_json(raw_data)
    return json_res