from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.dependencies.db import get_db_session
from app.models.user_models import User
from app.models.mystocks_models import MyStocks
from app.models.parameter_models import stock_to_buy, SellStockReq

router = APIRouter(
    prefix = '/trade'
)
class buyResp(): #�����
    login_id: str
    access_token: str
    stock_code : int
    quantity: int

@router.post("/buy") #req: ����, �ݾ�, �ֽ� �ڵ�, 
def buy_stock(req: stock_to_buy, db: Session = Depends(get_db_session), authorization: str =Header(None)):

    if not authorization:
        raise HTTPException(status_code=401, detail="�α����ϼž� �մϴ�.")
    
    token = authorization.split(" ")[1]
    user = db.query(User).filter(User.access_token == token).first()
    if not user:
        raise HTTPException(status_code=401, detail= "��ȿ���� ���� ��ū�Դϴ�")
    
    # ��ū ������ ��
    # 2. ���� �ִ��� ������ Ȯ��������
    total_price = req.stock_price * req.quantity
    if user.balance < total_price:
        raise HTTPException(status_code=400, detail="�ܾ��� �����մϴ�.")
    
    # ���� ������ User�� �� ���ݸ�ŭ ���� ���̰�

    change = user.balance - total_price
    db.query(User).filter(User.id == user.id).update({"balance": change})
    #�ܵ����� ���� ������Ʈ�� �Ŀ�

    existing_stock = db.query(MyStocks).filter(MyStocks.stock_code == req.stock_code).first()

    if existing_stock:
        db.query(MyStocks).filter(MyStocks.stock_code == req.stock_code).update({"quantity": MyStocks.quantity + req.quantity})
        
        new_avg_price = (total_price + existing_stock.avg_price*existing_stock.quantity) / (req.quantity + existing_stock.quantity)
        db.query(MyStocks).filter(MyStocks.stock_code == req.stock_code).update({"avg_price": new_avg_price})
        db.commit()
        #DB�� �ֽ��� �߰����ش�

    else:
        new_stock = MyStocks(
            login_id = user.login_id,
            stock_code=req.stock_code,
            quantity=req.quantity,
            access_token= user.access_token,
            avg_price = req.stock_price
        )
        db.add(new_stock)
    db.commit()
    
    return {"msg": "���� �Ϸ�"}




@router.post('/sell')
def sell_order(req: SellStockReq, db = Depends(get_db_session),authorization: str = Header(None)):

    '''��ū����'''

    
    if not authorization:
        raise HTTPException(status_code=401, detail="���� ��ū�� �ʿ��մϴ�.")
    token = authorization.split(" ")[1]  # "Bearer <��ū>"���� ��ū�� ����
    #table�� �ش� ��ū�� �ִ��� Ȯ��
    user = db.query(User).filter(User.access_token == token).first()
    if not user:
        raise HTTPException(status_code=401, detail="��ȿ���� ���� ��ū�Դϴ�.")
    

    '''mystocks db�� �� �����ֽ� ���� ����'''
    # �����ֽ� Ȯ��
    mystock = db.query(MyStocks).filter(
        MyStocks.login_id == user.login_id,
        MyStocks.stock_code == req.stock_code).first()
    
    if not mystock:
        raise HTTPException(status_code=404, detail="Not Found")
    
    if mystock.quantity > req.quantity:
        db.query(MyStocks).filter(
            MyStocks.login_id == user.login_id,
            MyStocks.stock_code == req.stock_code
        ).update({"quantity": MyStocks.quantity - req.quantity})
    
    
    elif mystock.quantity == req.quantity:
        db.delete(mystock)

    db.commit()
    #   db.refresh(MyStocks)  


    '''���� ��ġ �ҷ��ͼ� user db�� �ܰ� �� �߰�'''
    total_earned = req.current_price * req.quantity
    
    db.query(User).filter(User.id == user.id).update({"balance": User.balance + total_earned})
    db.commit()

    return {
        'msg' : '�ŵ� ����'
    }



