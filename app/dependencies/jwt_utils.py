#app/dependencies/jwt_utils.py
from datetime import datetime, timedelta, timezone
from jose import jwt

SECRET_KEY = '1234' #임시값
ALG = "HS256"

class JWTUtil:
    # 1. JWT 토큰 생성 함수
    def create_token(self, payload: dict, expires_delta: timedelta | 
                     None = timedelta(minutes=30)):
        payload_to_encode = payload.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        payload_to_encode.update(
            {'exp': expire}
        )
        return jwt.encode(payload_to_encode, SECRET_KEY,algorithm=ALG)
    
    #2. token 문자열로 payload 만드는 함수

    def decode_token(self, token: str) -> dict | None:
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALG]) #조필8
        except:
            pass
        return None






