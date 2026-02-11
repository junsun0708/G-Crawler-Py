import streamlit as st
import json
import os

# 데이터를 로드하는 함수
def load_data():
    file_path = 'msit_data.json'
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# 메인 화면을 그리는 함수 (이 이름이 반드시 show_page 여야 합니다)
def show_page():
    # 데이터 가져오기
    all_data = load_data()
    
    # --- 상단 디자인 ---
    st.title("🏛️ 과학기술정보통신부 지원사업")
    
    # 대시보드 (이미지 UI 참고)
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("누적 공고", f"{len(all_data):,}개")
    with c2: st.metric("정보 제공기관", "104개")
    with c3: st.metric("업데이트", "실시간")

    st.markdown("---")

    # --- 검색 및 태그 필터 ---
    search_query = st.text_input("🔍 에너지, AI, 제조 등 검색어로 지원사업을 검색해 보세요", placeholder="검색어 입력 후 엔터")
    
    # 해시태그 (이미지 999a5d.png 스타일)
    st.write("인기 태그")
    tags = ["전체", "에너지", "AI", "제조", "스마트공장", "ESG", "R&D", "ICT", "바이오"]
    # pills가 지원되지 않는 구버전일 경우를 대비해 radio로 구현 (가로 배치)
    selected_tag = st.radio("태그 선택", tags, horizontal=True, label_visibility="collapsed")

    # 필터링 로직
    keyword = search_query if search_query else (selected_tag if selected_tag != "전체" else "")
    
    filtered_data = [
        item for item in all_data 
        if keyword in item.get('subject', '') or keyword in item.get('deptName', '')
    ]

    # --- 공고 리스트 출력 (이미지 9a133a.png 스타일) ---
    st.subheader(f"전체 {len(filtered_data)}개")

    if not filtered_data:
        st.info("검색 결과가 없습니다.")
    else:
        for idx, item in enumerate(filtered_data):
            # 카드 스타일 컨테이너
            with st.container(border=True):
                col_text, col_btn = st.columns([4, 1])
                
                with col_text:
                    # 제목 및 태그
                    st.markdown(f"### {item.get('subject')}")
                    st.markdown(f":blue[[{item.get('deptName')}]] :green[[과학기술]] :orange[[정보통신]]")
                    st.write(f"📅 등록일: {item.get('pressDt', '-')}")
                    st.caption(f"👤 담당: {item.get('managerName', '-')} ({item.get('managerTel', '-')})")
                
                with col_btn:
                    # 우측 버튼 레이아웃
                    st.write("") # 상단 여백
                    if item.get('viewUrl'):
                        st.link_button("공고확인 🔗", item.get('viewUrl'), use_container_width=True)
                    st.button("관심사업 저장 ⭐", key=f"fav_btn_{idx}", use_container_width=True)

# 만약 이 파일만 단독으로 실행했을 때를 대비
if __name__ == "__main__":
    show_page()