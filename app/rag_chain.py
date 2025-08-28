from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

# 설정값들을 상수로 정의하여 관리 용이성을 높입니다.
DB_PATH = "./db"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
OLLAMA_MODEL_NAME = "llama3"

def get_rag_chain():
    """
    RAG 체인을 설정하고 생성하여 반환하는 함수입니다.
    이 함수는 서버 시작 시 한 번만 호출됩니다.
    """
    # 1. 임베딩 함수 로드
    embedding_function = SentenceTransformerEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs={'device': 'cpu'} # CPU 모드로 되돌립니다.
    )

    # 2. 벡터 DB 로드
    vector_db = Chroma(
        persist_directory=DB_PATH,
        embedding_function=embedding_function
    )

    # 3. Retriever 생성
    retriever = vector_db.as_retriever(search_kwargs={"k": 5}) # 검색 결과 수를 5개로 늘립니다.

    # 4. 프롬프트 템플릿 정의
    prompt_template = """
    당신은 제공된 컨텍스트 정보만을 사용하여 사용자의 질문에 답변하는 AI 어시스턴트입니다.
    절대로 컨텍스트에 없는 내용을 지어내서 답변하면 안 됩니다.
    답변은 반드시 한국어로 작성해주세요.

    컨텍스트: {context}

    질문: {question}

    답변:
    """
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    # 5. Ollama LLM 설정
# 컨테이너가 Host PC의 Ollama에 접속할 수 있도록 base_url을 지정합니다.
    llm = Ollama(
    base_url="http://host.docker.internal:11434",
    model=OLLAMA_MODEL_NAME, 
    temperature=0)

    # 6. RetrievalQA 체인 생성
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": PROMPT},
        return_source_documents=True
    )
    
    return qa_chain

# 아래 부분은 이제 FastAPI 서버에서 직접 사용하므로 이 파일에서는 필요 없습니다.
# if __name__ == '__main__':
#     ...
