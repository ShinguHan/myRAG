# 1. 베이스 이미지 설정
FROM python:3.11-slim

# 2. 작업 디렉토리 설정
WORKDIR /code

# 3. 의존성 파일 복사
COPY ./ui/requirements.txt /code/requirements.txt

# 4. 의존성 설치
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 5. 소스 코드 복사 (이제 ui 폴더의 내용만 복사됩니다)
COPY ./ui /code

# 6. UI 실행 명령어
CMD ["streamlit", "run", "ui.py", "--server.port=8501", "--server.address=0.0.0.0"]
