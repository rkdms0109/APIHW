# main.py
from fastapi import FastAPI
from score import score_router  # 수정: score_router에 모든 요약 로직 위임

app = FastAPI()
app.include_router(score_router, prefix="")  # prefix를 필요에 따라 조정

@app.get("/")
async def start() -> dict:
    return { 'msg': 'start' }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
