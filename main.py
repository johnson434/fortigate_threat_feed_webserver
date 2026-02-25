import os
import sys
import glob
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

app = FastAPI()

# 환경 변수 설정: 파일 저장 경로는 유동적으로 바꿀 수 있게 유지합니다.
BASE_DIR = os.getenv("BASE_DIR", "res")


def get_latest_file():
    """res 폴더 내에서 가장 최근에 생성/수정된 .txt 파일을 반환합니다."""
    files = sorted(glob.glob(os.path.join(BASE_DIR, "*.txt")))
    return files[-1] if files else None


@app.on_event("startup")
async def startup_event():
    """서버 시작 시 데이터 디렉터리가 있는지 확인하고 없으면 종료합니다."""
    if not os.path.isdir(BASE_DIR):
        print(f"\n" + "=" * 50)
        print(f" [CRITICAL ERROR] Directory '{BASE_DIR}' not found.")
        print(f" Path: {os.path.abspath(BASE_DIR)}")
        print(f" Please mount the volume properly.")
        print("=" * 50 + "\n")
        sys.exit(1)


@app.get("/")
async def get_latest_server_list():
    """가장 최신 파일 내용을 반환합니다."""
    latest_file = get_latest_file()
    if latest_file and os.path.exists(latest_file):
        return FileResponse(
            path=latest_file,
            filename=os.path.basename(latest_file),
            media_type="text/plain",
        )
    raise HTTPException(status_code=404, detail="No txt files found.")


@app.get("/{date_str}")
async def get_server_list_by_date(date_str: str):
    """특정 날짜(파일명)의 파일을 반환합니다. (예: /2026-02-25)"""
    file_path = os.path.join(BASE_DIR, f"{date_str}.txt")
    if os.path.exists(file_path):
        return FileResponse(
            path=file_path, filename=f"{date_str}.txt", media_type="text/plain"
        )
    raise HTTPException(status_code=404, detail=f"File {date_str}.txt not found.")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
