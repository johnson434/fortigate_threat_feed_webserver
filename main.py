import os
import sys
import glob
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

app = FastAPI()

# 환경 변수 설정
BASE_DIR = os.getenv("BASE_DIR", "res")


def get_latest_file():
    # 폴더 내에서 가장 최근의 .txt 파일을 반환합니다.
    files = sorted(glob.glob(os.path.join(BASE_DIR, "*.txt")))
    return files[-1] if files else None


@app.on_event("startup")
async def startup_event():
    if not os.path.isdir(BASE_DIR):
        print(f"\n [CRITICAL ERROR] Directory '{BASE_DIR}' not found.")
        sys.exit(1)


@app.get("/")
async def get_server_list():
    # 가장 최신 파일을 찾습니다.
    latest_file = get_latest_file()
    if latest_file and os.path.exists(latest_file):
        return FileResponse(
            path=latest_file,
            filename=os.path.basename(latest_file),
            media_type="text/plain",
        )
    raise HTTPException(status_code=404, detail="No txt files found.")


# ... (이하 동일)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
