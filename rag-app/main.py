from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager
from rag_chain import get_rag_chain # rag_chain.py에서 함수를 가져옵니다.

# AI 체인을 저장할 전역 변수를 선언합니다.
rag_chain = None

# FastAPI의 lifespan 이벤트를 관리하는 컨텍스트 매니저를 정의합니다.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- 서버 시작 시 실행될 로직 ---
    global rag_chain
    print("🚀 서버가 시작되었습니다. RAG 체인을 로드합니다...")
    # get_rag_chain 함수를 호출하여 무거운 모델들을 미리 로드합니다.
    rag_chain = get_rag_chain()
    print("✅ RAG 체인 로드가 완료되었습니다.")
    
    yield # 이 지점에서 API 서버가 실행됩니다.
    
    # --- 서버 종료 시 실행될 로직 (필요하다면 여기에 추가) ---
    print("👋 서버가 종료됩니다.")

# FastAPI 애플리케이션을 생성하며, lifespan을 지정합니다.
app = FastAPI(lifespan=lifespan)

# 사용자가 질문을 보낼 때 사용할 데이터 형식을 정의합니다.
class Query(BaseModel):
    text: str

# '/query'라는 주소로 POST 요청을 처리할 API 엔드포인트를 정의합니다.
@app.post("/query")
def get_answer(query: Query):
    """
    사용자의 질문을 받아 RAG 체인을 통해 답변과 출처를 반환합니다.
    """
    if not rag_chain:
        return {"error": "RAG chain is not loaded yet."}, 503

    # 사용자의 질문 텍스트를 가져옵니다.
    query_text = query.text
    
    # 로드된 RAG 체인을 실행하여 결과를 받습니다.
    result = rag_chain.invoke({"query": query_text})

    # 필요한 정보만 추출하여 클라이언트에게 반환합니다.
    response = {
        "answer": result.get("result"),
        "source_documents": [
            {
                "source": doc.metadata.get("source", "N/A"),
                "content": doc.page_content
            }
            for doc in result.get("source_documents", [])
        ]
    }
    return response

# 서버의 상태를 확인할 수 있는 기본 엔드포인트를 정의합니다.
@app.get("/")
def read_root():
    return {"message": "RAG API 서버가 정상적으로 실행 중입니다."}
