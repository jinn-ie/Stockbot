from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.dependencies.db import *
from app.routers import (trade_routers,auth_routers, record_routers, mystocks_routers, stock_routers, set_page_routers)
from fastapi.staticfiles import StaticFiles

create_db_and_table()

app = FastAPI()

# ? CORS ���� �߰�
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ��� ������ ��� (���� �ÿ��� Ư�� ���������� ����)
    allow_credentials=True,
    allow_methods=["*"],  # ��� HTTP �޼��� ���
    allow_headers=["*"],  # ��� ��� ���
)

# ����Ʈ ����
app.mount("/front/assets", StaticFiles(directory="front/assets"), name="assets")
app.mount("/front/vendor", StaticFiles(directory="front/vendor"), name="vendor")
app.mount("/front2/assets", StaticFiles(directory="front2/assets"), name="assets")


app.include_router(mystocks_routers.router)
app.include_router(auth_routers.router)
app.include_router(record_routers.router)
app.include_router(stock_routers.router)
app.include_router(trade_routers.router)
app.include_router(set_page_routers.router)



# from fastapi.middleware.cors import CORSMiddleware
# from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# from app.dependencies.db import *
# from app.routers import auth_routers, record_routers, mystocks_routers, stock_routers
# from fastapi.responses import HTMLResponse, RedirectResponse
# from fastapi.staticfiles import StaticFiles
# from pydantic import BaseModel
# import os
# import asyncio
# import random
# import datetime

# # FastAPI ���ø����̼� �ʱ�ȭ
# app = FastAPI()

# create_db_and_table()
# put_temp_data()  # �ӽ� ������ �߰�

# # ? CORS ���� �߰�
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # ��� ������ ��� (���� �ÿ��� Ư�� ���������� ����)
#     allow_credentials=True,
#     allow_methods=["*"],  # ��� HTTP �޼��� ���
#     allow_headers=["*"],  # ��� ��� ���
# )

# # ? ����Ʈ���� ���� ����
# app.mount("/front/assets", StaticFiles(directory="front/assets"), name="assets")
# app.mount("/front/vendor", StaticFiles(directory="front/vendor"), name="vendor")
# app.mount("/front2/assets", StaticFiles(directory="front2/assets"), name="assets")

# # ? API ����� �߰�
# app.include_router(mystocks_routers.router)
# app.include_router(auth_routers.router)
# app.include_router(record_routers.router)
# app.include_router(stock_routers.router)

# # ? �⺻ ������ ���Ʈ
# @app.get("/", response_class=RedirectResponse)
# async def root():
#     return RedirectResponse(url="/front/index")

# @app.get("/front/{page_name}", response_class=HTMLResponse)
# async def get_page(page_name: str = "index"):
#     page_path = f"front/{page_name}.html"
#     if os.path.exists(page_path):
#         with open(page_path, "r", encoding="utf-8") as file:
#             content = file.read()
#         return HTMLResponse(content=content)
#     else:
#         return HTMLResponse(content="�������� ã�� �� �����ϴ�.", status_code=404)

# @app.get("/front2/{page_name}", response_class=HTMLResponse)
# async def get_page(page_name: str = "index"):
#     page_path = f"front2/{page_name}.html"
#     if os.path.exists(page_path):
#         with open(page_path, "r", encoding="utf-8") as file:
#             content = file.read()
#         return HTMLResponse(content=content)
#     else:
#         return HTMLResponse(content="�������� ã�� �� �����ϴ�.", status_code=404)


# ############################################## ? �ǽð� ���� �׽�Ʈ ������ ###################################

# # �׽�Ʈ�� �ֽ� ���� ����Ʈ
# STOCK_CODES = [
#     "005930",  # �Ｚ����
#     "000660",  # SK���̴н�
#     "005380",  # �����ڵ���
#     "000270",  # ���
#     "005490",  # POSCOȦ����
#     "012450",  # ��ȭ����ν����̽�
#     "403870",  # HPSP
#     "042700",  # �ѹ̹ݵ�ü
#     "086520",  # ��������
#     "247540",  # �������κ�
#     "066970",  # ���ؿ���
#     "278280",  # õ��
#     "253590",  # �׿���
#     "348370",  # ����
#     "028300",  # HLB
#     "196170",  # ���׿���
#     "092870",  # ������
#     "000250",  # ��õ������
#     "095610",  # �׽�
#     "210980"   # SK��ص�
# ]

# # �ֽ� ���� ��
# class StockPriceResponse(BaseModel):
#     stock_code: str
#     timestamp: str  # HHMMSS ����
#     current_price: int  # ���� ����

# # ? ������ �ڵ鷯 �߰�
# @app.websocket("/ws/stocks/1")
# async def websocket_stock_prices(websocket: WebSocket):
#     """Ŭ���̾�Ʈ�� ����Ǹ� 1�ʸ��� ���� �ֽ� �����͸� ���� (���� ������ ���� ����)"""
    
#     await websocket.accept()  # ������ ���� ����

#     try:
#         while True:
#             stock_data_list = []

#             # �����ϰ� �� �� �����͸� ���� (�ִ� 9������ ���� �� ����)
#             missing_count = 19 #random.randint(0, 9)
#             selected_stocks = random.sample(STOCK_CODES, len(STOCK_CODES) - missing_count)

#             for stock_code in selected_stocks:
#                 stock_price = 9999  # 5��~20�� �� ���� ���� ����
#                 timestamp = datetime.datetime.now().strftime("%H%M%S")  # HHMMSS ����

#                 stock_response = StockPriceResponse(
#                     stock_code=stock_code,
#                     timestamp=timestamp,
#                     current_price=stock_price,
#                 )
#                 stock_data_list.append(stock_response.dict())

#             # JSON ������ ����
#             await websocket.send_json(stock_data_list)
#             await asyncio.sleep(1)  # 1�� ������ ������Ʈ

#     except WebSocketDisconnect:
#         print("? Ŭ���̾�Ʈ ���� ����")