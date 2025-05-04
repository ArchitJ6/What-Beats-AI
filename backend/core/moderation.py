from profanity_check import predict

def is_clean(text: str) -> bool:
    return predict([text])[0] == 0
