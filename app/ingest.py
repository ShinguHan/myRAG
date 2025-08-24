import os
from langchain_community.document_loaders import (
    DirectoryLoader,
    PyPDFLoader,
    TextLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredPowerPointLoader,
    UnstructuredExcelLoader,
    UnstructuredMarkdownLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
import time

# 데이터가 저장될 경로와 벡터 DB가 저장될 경로를 설정합니다.
DATA_PATH = "./data"
DB_PATH = "./db"

# --- 이 함수를 통째로 교체해주세요 ---
def load_documents():
    """data 폴더에 있는 모든 문서를 순회하며 적절한 로더를 사용해 로드합니다."""
    documents = []
    # loader_map 대신, 파일 확장자와 로더 클래스를 직접 매핑합니다.
    ext_to_loader_map = {
        ".pdf": PyPDFLoader,
        ".docx": UnstructuredWordDocumentLoader,
        ".pptx": UnstructuredPowerPointLoader,
        ".xlsx": UnstructuredExcelLoader,
        ".md": UnstructuredMarkdownLoader,
        ".java": TextLoader,
        ".py": TextLoader,
        ".txt": TextLoader,
    }

    # data 폴더의 모든 파일을 순회합니다.
    for root, _, files in os.walk(DATA_PATH):
        for file in files:
            file_path = os.path.join(root, file)
            # 파일 확장자를 가져옵니다.
            file_ext = os.path.splitext(file)[1].lower()
            
            # 매핑된 로더가 있는지 확인합니다.
            if file_ext in ext_to_loader_map:
                loader_class = ext_to_loader_map[file_ext]
                try:
                    # 해당 로더를 초기화하고 문서를 로드합니다.
                    print(f"Loading {file_path} with {loader_class.__name__}...")
                    loader = loader_class(file_path)
                    loaded_docs = loader.load()
                    documents.extend(loaded_docs)
                except Exception as e:
                    print(f"Error loading file {file_path}: {e}")
            else:
                print(f"Skipping file {file_path} as no loader is available for extension {file_ext}")

    return documents

def split_documents(documents):
    """로드된 문서를 언어에 맞춰 의미있는 단위(Chunk)로 분할합니다."""
    chunks = []
    # 일반 텍스트 분할기
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    # Java 코드용 분할기
    java_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.JAVA, chunk_size=1000, chunk_overlap=200
    )
    # Python 코드용 분할기 추가
    python_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON, chunk_size=1000, chunk_overlap=200
    )

    for doc in documents:
        # 파일 확장자를 기준으로 적절한 분할기를 선택합니다.
        file_extension = os.path.splitext(doc.metadata.get("source", ""))[1]
        
        if file_extension == ".java":
            split_chunks = java_splitter.split_documents([doc])
        elif file_extension == ".py":
            split_chunks = python_splitter.split_documents([doc])
        else:
            split_chunks = text_splitter.split_documents([doc])
        
        chunks.extend(split_chunks)
        
    return chunks

def save_to_vector_db(chunks):
    """분할된 청크를 벡터로 변환하여 ChromaDB에 저장합니다."""
    if not chunks:
        print("분할된 문서가 없어 DB 저장을 건너뜁니다.")
        return

    embedding_function = SentenceTransformerEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
    
    vector_db = Chroma.from_documents(
        chunks,
        embedding_function,
        persist_directory=DB_PATH
    )
    
    print(f"총 {len(chunks)}개의 문서 청크가 성공적으로 벡터 DB에 저장되었습니다.")

def main():
    """전체 데이터 처리 파이프라인을 실행하는 메인 함수입니다."""
    start = time.time()
    print("1. 문서를 로드합니다...")
    documents = load_documents()
    if not documents:
        print("로드할 문서가 없습니다. data 폴더를 확인해주세요.")
        return
    print(f"총 {len(documents)}개의 문서를 성공적으로 로드했습니다.")
    
    print("\n2. 문서를 의미있는 단위로 분할합니다...")
    chunks = split_documents(documents)
    print(f"문서를 총 {len(chunks)}개의 청크로 분할했습니다.")
    
    print("\n3. 분할된 문서를 벡터 DB에 저장합니다...")
    save_to_vector_db(chunks)
    
    print("\n🎉 모든 데이터 처리 과정이 완료되었습니다!")
    end = time.time()
    elapsed = end - start
    print(f'경과 시간은 {elapsed}초 입니다')
if __name__ == '__main__':
    main()
