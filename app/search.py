import argparse
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

# 벡터 DB와 임베딩 모델 경로를 설정합니다. ingest.py와 동일해야 합니다.
DB_PATH = "./db"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

def main():
    """
    명령줄 인자로 질문을 받아 ChromaDB에서 유사도 검색을 수행하고 결과를 출력합니다.
    """
    # 1. 임베딩 함수를 로드합니다.
    # 데이터를 DB에 저장할 때 사용했던 것과 '반드시' 동일한 모델을 사용해야 합니다.
    embedding_function = SentenceTransformerEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        # model_kwargs={'device': 'cpu'}
        model_kwargs={'device': 'cuda'}
    )

    # 2. 디스크에 저장된 벡터 DB를 로드합니다.
    vector_db = Chroma(
        persist_directory=DB_PATH,
        embedding_function=embedding_function
    )

    # 3. 명령줄에서 'query' 인자를 파싱합니다.
    parser = argparse.ArgumentParser(description="ChromaDB에서 유사도 검색을 수행합니다.")
    parser.add_argument("query", type=str, help="검색할 질문을 입력하세요.")
    args = parser.parse_args()
    query_text = args.query
    
    print(f"\n🔍 검색 질문: '{query_text}'")

    # 4. 유사도 검색을 수행합니다.
    # k=3은 가장 유사한 결과 3개를 가져오라는 의미입니다.
    results = vector_db.similarity_search(query_text, k=3)

    # 5. 검색 결과를 출력합니다.
    if results:
        print(f"\n✅ 총 {len(results)}개의 유사한 문서를 찾았습니다:")
        for i, doc in enumerate(results):
            # doc.page_content: 검색된 텍스트 조각의 내용
            # doc.metadata['source']: 해당 조각의 원본 파일 경로
            print("-" * 50)
            print(f"결과 {i+1}:")
            print(f"출처: {doc.metadata.get('source', 'N/A')}")
            print("내용:")
            print(doc.page_content)
            print("-" * 50)
    else:
        print("\n❌ 유사한 문서를 찾지 못했습니다.")

if __name__ == '__main__':
    main()
