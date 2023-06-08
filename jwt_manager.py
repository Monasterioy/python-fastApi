from jwt import encode, decode

def create_token(payload: any):
    token: str = encode(payload, key="my_secret", algorithm='HS256')
    return  token

def validate_token(token):
    try:
        payload = decode(token, key="my_secret", algorithms=['HS256'])
        return payload
    except:
        return None