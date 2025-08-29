# 1. 베이스 이미지 설정
FROM python:3.11-slim

# 2. 작업 디렉토리 설정
WORKDIR /code

# 3. 의존성 파일 복사
COPY ./rag-app/requirements.txt /code/requirements.txt

# 4. 의존성 설치 (PyTorch 제외)
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 5. GPU 버전 PyTorch 설치 (⭐ 핵심 변경점)
# CUDA 12.1을 지원하는 PyTorch를 별도로 설치합니다.
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 6. 소스 코드 복사
COPY ./rag-app/. /code/

# 7. 서버 실행 명령어
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
