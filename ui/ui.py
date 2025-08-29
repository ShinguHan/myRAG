import streamlit as st
import requests
import json

# FastAPI 백엔드 서버의 주소입니다.
# Docker Compose 환경에서는 서비스 이름('rag-app')으로 통신합니다.
BACKEND_URL = "http://rag-app:8000/query"

# Streamlit 앱의 제목과 페이지 설정을 합니다.
st.set_page_config(page_title="물류 AI 챗봇", page_icon="🤖")
st.title("물류 AI 챗봇 🤖")

# 세션 상태(session_state)를 초기화하여 대화 기록을 저장할 리스트를 만듭니다.
# 'messages'가 아직 세션 상태에 없으면, 초기 메시지를 추가합니다.
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "안녕하세요! 물류 관련 문서와 코드에 대해 무엇이든 물어보세요."}]

# 이전 대화 기록을 순회하며 화면에 표시합니다.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자가 새로운 질문을 입력할 수 있는 채팅 입력창을 만듭니다.
if prompt := st.chat_input("질문을 입력해주세요."):
    # 1. 사용자의 질문을 대화 기록에 추가하고 화면에 표시합니다.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. AI의 답변을 준비하는 동안 사용자에게 보여줄 메시지 공간을 만듭니다.
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("답변을 생각하고 있어요... 🤔")
        
        try:
            # 3. 백엔드 서버에 API 요청을 보냅니다.
            response = requests.post(BACKEND_URL, json={"text": prompt})
            response.raise_for_status()  # HTTP 에러가 발생하면 예외를 발생시킵니다.
            
            # 4. 백엔드로부터 받은 답변을 처리합니다.
            result = response.json()
            answer = result.get("answer", "답변을 가져오는 데 실패했습니다.")
            
            # 5. 생각 중이라는 메시지를 실제 답변으로 교체합니다.
            message_placeholder.markdown(answer)
            
            # 6. AI의 답변을 대화 기록에 추가합니다.
            st.session_state.messages.append({"role": "assistant", "content": answer})

        except requests.exceptions.RequestException as e:
            # 네트워크 또는 HTTP 에러 처리
            error_message = f"백엔드 서버에 연결할 수 없습니다: {e}"
            message_placeholder.error(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})
