# 1. 파이썬 경량화 이미지 사용
FROM python:3.11-slim

# 2. 컨테이너 내 작업 디렉토리 설정
WORKDIR /app

# 3. 파이썬 환경 변수 설정
# .pyc 파일을 생성하지 않도록 설정
ENV PYTHONDONTWRITEBYTECODE=1
# 로그가 버퍼링 없이 즉시 출력되도록 설정
ENV PYTHONUNBUFFERED=1

# 4. 필수 라이브러리 설치
# 가상 환경 없이 컨테이너 환경에 직접 설치합니다.
RUN pip install --no-cache-dir fastapi uvicorn

# 5. 소스 코드 복사
# 작성하신 main.py 파일을 컨테이너로 복사합니다.
COPY main.py .

# 6. 데이터 디렉토리 생성
# 코드에서 체크하는 'res' 폴더를 미리 만들어 둡니다.
RUN mkdir -p res

# 7. res 파일 복사
COPY res/*.txt res/

EXPOSE 80

# 8. 서버 실행
# 코드 하단의 uvicorn.run(port=80) 로직을 실행합니다.
CMD ["python", "main.py"]
