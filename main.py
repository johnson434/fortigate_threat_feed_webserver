from fastapi import FastAPI
from fastapi.responses import FileResponse
import os

app = FastAPI()

# 파일 경로 설정
FILE_PATH = "server_list.txt"

@app.on_event("startup")
async def startup_event():
    # 프로그램 실행 시 파일이 없으면 테스트용으로 자동 생성
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            f.write("Server 1: 10.137.1.10\nServer 2: 10.137.1.11")

@app.get("/")
async def get_server_list():
    # 파일이 존재하는지 확인 후 반환
    if os.path.exists(FILE_PATH):
        return FileResponse(
            path=FILE_PATH, 
            filename="server_list.txt", # 다운로드 시 파일 이름
            media_type="text/plain"      # 텍스트 형식 지정
        )
    return {"error": "파일을 찾을 수 없습니다."}

if __name__ == "__main__":
    import uvicorn
    # 요청하신 로컬 호스트 IP로 실행
    uvicorn.run(app, host="0.0.0.0", port=8080)
