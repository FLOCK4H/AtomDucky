# analyzer.py

def analyze_payload(payload):
    tokens = []
    i = 0
    while i < len(payload):
        if payload[i] == "<":
            end_index = payload.find(">", i)
            if end_index != -1 and ' ' not in payload[i+1:end_index]:
                tokens.append(payload[i:end_index+1])
                i = end_index + 1
                continue
        tokens.append(payload[i])
        i += 1
    return tokens