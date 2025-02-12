from fastapi import APIRouter, Depends, HTTPException, Header
from app.models.parameter_models import *
from pydantic import BaseModel
from app.models.user_models import User
from app.dependencies.db import *
from app.dependencies.jwt_utils import JWTUtil
from app.services.auth_service import AuthService


router = APIRouter(
    prefix='/auth'
)

#회원가입
@router.post('/register', response_model=AuthResp)
def register(req: AuthSignupReq, db=Depends(get_db_session),
             jwtUtil: JWTUtil = Depends(),
             authService: AuthService = Depends()):
    existing_user = db.query(User).filter(User.login_id == req.login_id).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="ID already exists")

    new_user = authService.signup(db,req.login_id, req.pwd, req.name)

    if not new_user:
        raise HTTPException(status_code=400, detail="not found")
    
    return AuthResp(
        message= "User registered successfully",
        user = new_user
    )

#로그인
@router.post('/login')
def login(req: AuthSigninReq,
          db=Depends(get_db_session), jwtUtil: JWTUtil = Depends(),
          authService: AuthService = Depends()):
    
    user = authService.signin(db,req.login_id,req.pwd)
    if not user:
        raise HTTPException(status_code=401, detail="Login failed")
    
    user.access_token = jwtUtil.create_token(user.model_dump())
    db.query(User).filter(User.id == user.id).update({"access_token": user.access_token})
    db.commit()
    return AuthResp(
        message="로그인 되었습니다.",
        user=user,
        access_token=user.access_token
    )

#로그아웃
@router.post('/logout')
def auth_logout(db: Session=Depends(get_db_session), authorization: str=Header(None)):  # 헤더에서 토큰을 받음
    if not authorization:
        raise HTTPException(status_code=401, detail="인증 토큰이 필요합니다.")

    token = authorization.split(" ")[1]  # "Bearer <토큰>"에서 토큰만 추출
    
    # table에 해당 토큰이 있는지 확인
    user = db.query(User).filter(User.access_token == token).first()
    if not user:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")

    # 현재 유저의 토큰을 삭제 (NULL 처리)
    db.query(User).filter(User.id == user.id).update({"access_token": None})
    db.commit()

    return {"message": "로그아웃 되었습니다."}