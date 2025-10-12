# analyzer.py

def analyze_payload_stream(payload):
    if isinstance(payload, bytes):
        payload = payload.decode()
    i = 0
    while i < len(payload):
        if payload[i] == "<":
            end_index = payload.find(">", i)
            if end_index != -1 and " " not in payload[i+1:end_index]:
                yield payload[i:end_index+1]
                i = end_index + 1
                continue
        yield payload[i]
        i += 1