# Threat Feed Web Server

## 0. 컨테이너 이미지 Pull
``` bash
docker pull jonathan434/threat-feed-api
```

## 1. 실행

### 
``` bash
docker run -d --name threat-prod -p 외부포트:80
```

## 2. API
- `GET /` : test.txt 반환
