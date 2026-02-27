import os
import sys
import uvicorn
import textwrap
from enum import Enum
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse


# 1. 제공 가능한 피드 타입 정의
class FeedType(str, Enum):
    ip_addresses = "ip-addresses"
    domain_names = "domain-names"
    fortiguard_categories = "fortiguard-categories"
    mac_addresses = "mac-addresses"
    malware_hashes = "malware-hashes"


# 2. 메인 설명 마크다운 (들여쓰기 제거 적용)
app_description = textwrap.dedent("""
    ## 🛡️ 위협 정보 피드 서버 가이드
    이 API는 보안 장비(FortiGate 등)에서 참조할 수 있는 **텍스트 기반 블랙리스트**를 제공합니다.

    ### 📌 제공 리소스 정보
    * **IP 주소**: 악성 활동이 탐지된 C&C 또는 스팸 IP
    * **도메인**: 피싱 사이트 및 위협 도메인
    * **카테고리**: 포티가드 웹 필터링용 커스텀 카테고리
    * **파일 해시**: 악성코드의 SHA256/MD5 값
""")

app = FastAPI(
    title="Threat Intelligence Feed API", description=app_description, version="1.1.0"
)

BASE_DIR = os.getenv("BASE_DIR", "res")


@app.get(
    "/feeds/{feed_type}",
    summary="위협 피드 파일 다운로드",
    description=textwrap.dedent("""
        지정한 유형의 피드 파일을 `.txt` 형식으로 반환합니다.
    """),
)
async def get_threat_feed(feed_type: FeedType):
    filename = f"{feed_type.value}.txt"
    file_path = os.path.join(BASE_DIR, filename)

    if not os.path.isfile(file_path):
        raise HTTPException(
            status_code=404, detail=f"Resource '{feed_type.value}' not found on server."
        )

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="text/plain",
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
