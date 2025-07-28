from fastapi import FastAPI
import uvicorn
from pyngrok import ngrok
import nest_asyncio
from dotenv import load_dotenv
import os
from routers import generate

load_dotenv()
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
ngrok.set_auth_token(AUTH_TOKEN)

# ngrok 연결
tunnel = ngrok.connect(8000)
public_url = tunnel.public_url
print("Public URL:", public_url)

# FastAPI 앱 생성
app = FastAPI()
app.state.public_url = public_url

# 라우터 등록
app.include_router(generate.router)

# asyncio 패치
nest_asyncio.apply()

# 서버 실행
config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="debug")
server = uvicorn.Server(config)
await server.serve()