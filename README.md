# Threat Feed Web Server
## 1. 실행

### 운영 모드 (최신 파일 반환)
``` bash
docker run -d --name threat-prod -p 9000:80 -v $(pwd)/res:/app/res threat-feed-api
```

### 테스트 모드 (test.txt 반환)
```bash
docker run -d --name threat-test -p 9001:80 -e env=test -v $(pwd)/res:/app/res threat-feed-api
```

## 2. API
- `GET /` : 최신 또는 지정 파일 반환
- `GET /{date}` : 특정 날짜 파일 반환
