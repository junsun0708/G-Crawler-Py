import streamlit as st
import json
import os
import msit_css  # Import the shared CSS module

# 데이터 로드 함수
def load_data():
    if os.path.exists('msit_data.json'):
        with open('msit_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def show_page():
    # 1. 페이지 설정
    st.set_page_config(page_title="MSIT Dashboard (v2)", layout="wide")
    
    # 2. CSS 로드
    st.markdown(f"<style>{msit_css.CARBON_CSS}</style>", unsafe_allow_html=True)
    
    # 관심사업 저장을 위한 세션 상태 초기화
    if 'favorites' not in st.session_state:
        st.session_state.favorites = []

    all_data = load_data()

    # 3. 헤더 (Carbon Page Title)


    # 4. 대시보드 그리드 (DashGrid)
    # 상단 요약 통계
    st.markdown(f"""
    <div class="DashGrid">
        <div class="DashGridItem">
            <p class="DashItemTitle">
                <b>누적 사업공고</b>
                <span>Total Announcements</span>
            </p>
            <div class="totalCnt">
                <strong>{len(all_data):,}</strong>
                <em>건</em>
            </div>
        </div>
        <div class="DashGridItem">
            <p class="DashItemTitle">
                <b>이번주 신규 공고</b>
                <span>Weekly New</span>
            </p>
            <div class="totalCnt">
                <strong>24</strong>
                <em>건</em>
            </div>
        </div>
        <div class="DashGridItem">
            <p class="DashItemTitle">
                <b>참여 기관</b>
                <span>Organizations</span>
            </p>
            <div class="totalCnt">
                 <strong>104</strong>
                 <em>개</em>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("") # Vertical Spacer

    # 5. 메인 콘텐츠 (Filter + Grid)
    c1, c2 = st.columns([1, 3])
    
    with c1:
        # Search Inputs directly without Box container
        search_query = st.text_input("키워드 검색", placeholder="예: AI, 에너지")
        st.write("---")
        st.caption("분야별 태그")
        tags = ["전체", "에너지", "AI", "제조", "스마트공장", "ESG", "R&D", "ICT", "바이오"]
        selected_tag = st.radio("태그 선택", tags)

    with c2:
        # 필터 로직
        keyword = search_query if search_query else (selected_tag if selected_tag != "전체" else "")
        filtered = [i for i in all_data if keyword in (i.get('subject') or '') or keyword in (i.get('deptName') or '')]
        
        # Grid Layout using Streamlit columns for the cards
        
        # Grid Layout using Streamlit columns for the cards
        if not filtered:
            st.info("검색 결과가 없습니다.")
        else:
            # 3열 그리드로 카드 배치 - Scrollable Container
            with st.container(height=700):
                cols = st.columns(3)
                for idx, item in enumerate(filtered):
                    col = cols[idx % 3]
                    with col:
                        # CarbonBox 스타일을 적용한 카드
                        # HTML/CSS로 카드 모양 잡기
                        is_saved = item in st.session_state.favorites
                        fav_icon = "⭐" if is_saved else "☆"
                    
                        st.markdown(f"""
                        <div class="CarbonBox" style="padding: 20px; min-height: 250px; margin-bottom: 20px;">
                            <span class="badge" style="background-color: #2663c6; color: #fff;">{item.get('deptName')}</span>
                            <h4 style="margin: 10px 0; font-size: 16px; height: 60px; overflow: hidden; text-overflow: ellipsis; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical;">
                                {item.get('subject')}
                            </h4>
                            <p style="font-size: 12px; color: #d4ddea; margin-bottom: 5px;">📅 {item.get('pressDt')}</p>
                            <p style="font-size: 12px; color: #d4ddea;">👤 {item.get('managerName', '-')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # 버튼은 Streamlit native로 처리 (이벤트 핸들링 위해)
                        # 카드 바로 아래에 버튼 배치 (약간의 트릭)
                        b1, b2 = st.columns(2)
                        with b1:
                            if item.get('viewUrl'):
                                st.link_button("상세보기", item.get('viewUrl'), use_container_width=True)
                        with b2:
                                if st.button(f"{fav_icon} 저장", key=f"fav_{idx}", use_container_width=True):
                                    if is_saved:
                                        st.session_state.favorites.remove(item)
                                    else:
                                        st.session_state.favorites.append(item)
                                    st.rerun()

if __name__ == "__main__":
    show_page()
