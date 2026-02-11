import streamlit as st
import json
import os

# 데이터 로드 함수
def load_data():
    if os.path.exists('msit_data.json'):
        with open('msit_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def show_page():
    # 1. 페이지 설정
    st.set_page_config(page_title="정부지원사업 공고 조회", layout="wide")
    
    # 관심사업 저장을 위한 세션 상태 초기화
    if 'favorites' not in st.session_state:
        st.session_state.favorites = []

    # 커스텀 CSS (이미지 UI 재현)
    st.markdown("""
        <style>
        .main { background-color: #0e1117; color: white; }
        .stApp { background-color: #0e1117; }
        
        /* 상단 대시보드 (이미지 9a7856.png 스타일) */
        .dashboard-container {
            background-color: #1e2a4a;
            padding: 40px;
            border-radius: 20px;
            display: flex;
            justify-content: space-around;
            text-align: center;
            margin-bottom: 30px;
        }
        .stat-box h2 { font-size: 3rem; margin: 10px 0; color: white; }
        .stat-label { background-color: #007bff; padding: 2px 10px; border-radius: 4px; font-size: 0.9rem; }
        
        /* 공고 카드 (이미지 9a133a.png 스타일) */
        .announcement-card {
            background-color: white;
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 15px;
            color: #333;
        }
        .tag-container { margin-bottom: 10px; }
        .badge {
            background-color: #f1f3f5;
            color: #495057;
            padding: 4px 12px;
            border-radius: 6px;
            font-size: 0.85rem;
            margin-right: 8px;
            display: inline-block;
        }
        .project-title { color: #000; font-weight: 700; margin-bottom: 15px; }
        </style>
    """, unsafe_allow_html=True)

    # 2. 프로젝트명 노출 및 탭 구성
    st.title("🚀 정부지원사업 통합 포털")
    tab1, tab2 = st.tabs(["📊 전체 공고", "⭐ 관심 사업"])

    all_data = load_data()

    with tab1:
        # 상단 대시보드
        st.markdown(f"""
            <div class="dashboard-container">
                <div class="stat-box"><span class="stat-label">누적 사업공고</span><h2>{len(all_data):,}개</h2></div>
                <div class="stat-box"><span class="stat-label">이번주 사업공고</span><h2>24개</h2></div>
                <div class="stat-box"><span class="stat-label">정보 제공기관</span><h2>104개</h2></div>
            </div>
        """, unsafe_allow_html=True)

        # 검색 및 태그
        search_query = st.text_input("🔍 어떤 지원사업을 찾으시나요?", placeholder="에너지, AI, 제조 등 검색어 입력")
        tags = ["전체", "#에너지", "#AI", "#제조", "#스마트공장", "#ESG", "#R&D", "#ICT", "#바이오"]
        selected_tag = st.pills("인기 태그", tags, selection_mode="single", default="전체")

        keyword = search_query if search_query else (selected_tag.replace('#', '') if selected_tag != "전체" else "")
        filtered = [i for i in all_data if keyword in i.get('subject', '') or keyword in i.get('deptName', '')]

        st.subheader(f"전체 {len(filtered)}개")

        # 리스트 출력
        for idx, item in enumerate(filtered):
            with st.container():
                # 카드 본문 (HTML)
                st.markdown(f"""
                    <div class="announcement-card">
                        <div class="tag-container">
                            <span class="badge">{item.get('deptName', '과기부')}</span>
                            <span class="badge">정보통신</span>
                            <span class="badge">과학기술</span>
                        </div>
                        <h2 class="project-title">{item.get('subject')}</h2>
                        <p style="color:#666;">📅 등록일: {item.get('pressDt')} | 👤 담당: {item.get('managerName', '-')} ({item.get('managerTel', '-')})</p>
                    </div>
                """, unsafe_allow_html=True)
                
                # 버튼 레이아웃 (Streamlit)
                c1, c2, _ = st.columns([1, 1.5, 3])
                with c1:
                    if item.get('viewUrl'):
                        st.link_button("공고확인 🔗", item.get('viewUrl'), use_container_width=True)
                with c2:
                    # 저장 기능 구현
                    is_saved = item in st.session_state.favorites
                    btn_label = "관심사업 해제 ❌" if is_saved else "관심사업 저장 ⭐"
                    if st.button(btn_label, key=f"save_{idx}", use_container_width=True):
                        if is_saved:
                            st.session_state.favorites.remove(item)
                            st.toast("관심사업에서 삭제되었습니다.")
                        else:
                            st.session_state.favorites.append(item)
                            st.toast("관심사업에 추가되었습니다!")
                        st.rerun()
                st.write("")

    with tab2:
        st.subheader(f"내가 저장한 사업 ({len(st.session_state.favorites)}건)")
        if not st.session_state.favorites:
            st.info("아직 저장된 관심 사업이 없습니다.")
        else:
            for f_idx, fav in enumerate(st.session_state.favorites):
                with st.expander(f"⭐ {fav.get('subject')}"):
                    st.write(f"🏢 부서: {fav.get('deptName')}")
                    st.write(f"📅 등록일: {fav.get('pressDt')}")
                    if fav.get('viewUrl'):
                        st.link_button("링크 바로가기", fav.get('viewUrl'))
                    if st.button("삭제", key=f"del_{f_idx}"):
                        st.session_state.favorites.remove(fav)
                        st.rerun()