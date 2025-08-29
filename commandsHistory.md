RAG 챗봇 프로젝트 명령어 치트 시트이 문서는 프로젝트의 각 단계에서 사용된 핵심 명령어들을 정리한 요약본입니다.1주차: 프로젝트 설정 및 데이터 처리폴더 및 가상 환경 설정# 1. 프로젝트 폴더 생성 및 이동
mkdir rag-docker-app
cd rag-docker-app
mkdir app data

# 2. Python 가상 환경 생성

python -m venv venv

# 3. 가상 환경 활성화 (Windows PowerShell)

.\venv\Scripts\activate

# 3. 가상 환경 활성화 (macOS/Linux)

source venv/bin/activate
Git 버전 관리# 1. Git 저장소 초기화
git init

# 2. 모든 변경사항을 스테이징

git add .

# 3. "메시지"와 함께 커밋 (변경사항 기록)

git commit -m "feat: Initial data ingestion pipeline"
Python 라이브러리 관리# 1. requirements.txt 파일에 명시된 모든 라이브러리 설치
pip install -r requirements.txt

# 2. (에러 해결) pip 자체를 업그레이드

python.exe -m pip install --upgrade pip
스크립트 실행# 데이터 처리 스크립트 실행 (DB 생성)
python app/ingest.py

# 의미 기반 검색 테스트 스크립트 실행

python app/search.py "검색할 질문"
2주차: LLM 연동 (Ollama & LangChain)Ollama 모델 관리# 1. Ollama 설치 확인
ollama

# 2. Llama 3 모델 다운로드 (최초 1회)

ollama pull llama3
스크립트 실행# RAG 체인을 통해 답변을 생성하는 스크립트 실행
python app/rag_chain.py "답변을 원하는 질문"
(선택) GPU용 PyTorch 설치 (에러 발생 시)# 1. 기존 CPU 버전 PyTorch 삭제
pip uninstall torch torchvision torchaudio

# 2. CUDA 지원 GPU 버전 PyTorch 설치 (공식 홈페이지에서 명령어 확인)

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
3주차: API 서버 및 Docker 이미지화FastAPI 서버 실행# 1. FastAPI 실행에 필요한 uvicorn 등 설치
pip install "fastapi[all]"

# 2. FastAPI 서버 실행 (개발 모드)

uvicorn app.main:app --reload
Docker 이미지 및 컨테이너 관리# 1. Dockerfile을 기반으로 이미지 빌드 (-t 로 이름 지정)
docker build -t my-rag-app .

# 2. 내 컴퓨터에 빌드된 이미지 목록 확인

docker images

# 3. 이미지로 컨테이너를 백그라운드에서 실행 (-d)하고 포트 연결 (-p)

docker run -d -p 8000:8000 my-rag-app

# 4. 현재 실행 중인 컨테이너 목록 확인

docker ps

# 5. 컨테이너의 로그 실시간으로 확인 (-f)

docker logs -f <컨테이너*이름*또는\_ID>

# 6. 실행 중인 컨테이너 중지

docker stop <컨테이너*이름*또는\_ID>

# 7. 중지된 컨테이너 삭제

docker rm <컨테이너*이름*또는\_ID>
4주차: Docker Compose로 시스템 통합Docker Compose 실행# 1. docker-compose.yml 파일 기준으로 모든 서비스 실행 및 이미지 빌드
docker-compose up --build

# 2. 백그라운드에서 실행

docker-compose up -d

# 3. 모든 서비스 중지 및 컨테이너/네트워크 삭제

docker-compose down
실행 중인 서비스와 상호작용# ollama 서비스 컨테이너 안으로 들어가서 'ollama pull llama3' 명령어 실행
docker-compose exec ollama ollama pull llama3
(에러 해결) 포트 충돌 시 (PowerShell)# 1. 8000번 포트를 사용 중인 프로세스의 ID 찾기
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess

# 2. 찾은 ID로 프로세스 강제 종료

Stop-Process -Id <프로세스\_ID> -Force
