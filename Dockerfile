# 1. 베이스 이미지(Base Image) 설정
# Python 3.11 버전이 설치된 가벼운 리눅스 환경에서 시작합니다.
FROM python:3.11-slim

# 2. 작업 디렉토리(Working Directory) 설정
# 컨테이너 안에서 명령어를 실행할 기본 폴더를 '/code'로 지정합니다.
WORKDIR /code

# 3. 의존성 파일 복사
# 먼저 requirements.txt 파일만 컨테이너 안으로 복사합니다.
# (이렇게 하면 나중에 소스 코드만 바뀔 때 빌드 속도가 빨라집니다.)
COPY ./requirements.txt /code/requirements.txt

# 4. 의존성 설치
# 복사된 requirements.txt를 사용하여 필요한 모든 라이브러리를 설치합니다.
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 5. 소스 코드 복사
# 우리 프로젝트의 모든 파일과 폴더를 컨테이너 안으로 복사합니다.
COPY . /code

# 6. 서버 실행 명령어(Command)
# 컨테이너가 시작될 때 이 명령어를 자동으로 실행합니다.
# --host 0.0.0.0 은 컨테이너 외부에서도 접속할 수 있게 해주는 중요한 설정입니다.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
