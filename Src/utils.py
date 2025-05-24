import hashlib
from Src import config
from typing import Any
import jwt

def one_way_encrypt(data: str, algorithm: str ='sha256') -> str:
    if algorithm not in hashlib.algorithms_guaranteed:
        guaranteed_algorithms = ', '.join(hashlib.algorithms_guaranteed)
        raise ValueError(f"Selected algorithm [{algorithm}] isn't guaranteed. List of guaranteed algorithms: {guaranteed_algorithms}")
    
    if not isinstance(data, str):
        raise TypeError("Expected [str] type of data parameter")
    
    data = data.encode('utf-8')
    hash_object = hashlib.new(algorithm)
    hash_object.update(data)
    
    return hash_object.hexdigest()

def encode_to_jwt(data: dict[str, Any]) -> str:
    if not all([
        bool(data.get('account_id', None))
    ]):
        raise ValueError('Field [account_id] is required to be encoded into jwt token')
    
    return jwt.encode(data, config.JWT_SECRET_KEY, algorithm='HS256')

def decode_from_jwt(token: str) -> dict[str, Any]:
    return jwt.decode(token, config.JWT_SECRET_KEY, algorithms='HS256')