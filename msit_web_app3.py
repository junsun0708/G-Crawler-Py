import streamlit as st
import json
import os
import msit_css
import pandas as pd

def load_data():
    if os.path.exists('msit_data.json'):
        with open('msit_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def show_page():
    st.set_page_config(page_title="MSIT List View (v3)", layout="wide")
    st.markdown(f"<style>{msit_css.CARBON_CSS}</style>", unsafe_allow_html=True)
    
    if 'favorites' not in st.session_state:
        st.session_state.favorites = []

    all_data = load_data()
    
    # 1. 사이드바 (필터링 - Table view usually pairs well with sidebar filters)
    st.sidebar.title("검색 옵션")
    search_text = st.sidebar.text_input("검색어 입력", placeholder="사업명, 소관부처 등")
    
    # 부처 추출
    depts = sorted(list(set([d.get('deptName') for d in all_data if d.get('deptName')])))
    selected_depts = st.sidebar.multiselect("소관부처 선택", ["전체"] + depts, default="전체")
    
    # 날짜 필터 (가상)
    st.sidebar.date_input("등록일 범위")

    # 2. 메인 화면
    msit_css.page_header("📜 정부지원사업 통합 목록 (v3)", "List View Mode")

    # 필터링
    filtered = all_data
    if search_text:
        filtered = [d for d in filtered if search_text in d.get('subject', '') or search_text in d.get('deptName', '')]
    if "전체" not in selected_depts:
        filtered = [d for d in filtered if d.get('deptName') in selected_depts]

    # 3. 테이블형 리스트 (HTML Table for custom Carbon Design)
    st.markdown(f"""
    <div class="CarbonBox">
        <div class="CarbonBoxTitle">
            <b>검색 결과: <span style="color:#00a4e0;">{len(filtered)}</span>건</b>
        </div>
        <div class="DashGridItem" style="box-shadow: none; padding: 0;">
            <table class="table">
                <thead>
                    <tr>
                        <th style="width: 10%;">No</th>
                        <th style="width: 15%;">소관부처</th>
                        <th style="width: 45%;">공고명</th>
                        <th style="width: 15%;">등록일</th>
                        <th style="width: 15%;">관리</th>
                    </tr>
                </thead>
                <tbody>
    """, unsafe_allow_html=True)

    # 페이지네이션 흉내 (상위 20개만 표시)
    PAGE_SIZE = 20
    for idx, item in enumerate(filtered[:PAGE_SIZE]):
         # 상세 URL 
        url = item.get('viewUrl', '#')
        st.markdown(f"""
        <tr>
            <td style="text-align:center; color:#666;">{idx + 1}</td>
            <td style="text-align:center;"><span class="badge">{item.get('deptName')}</span></td>
            <td><a href="{url}" target="_blank" style="text-decoration:none; color:#2b2b2b; font-weight:500;">{item.get('subject')}</a></td>
            <td style="text-align:center; color:#666;">{item.get('pressDt')}</td>
            <td style="text-align:center;">
                <!-- Buttons are hard to embed in HTML string for Streamlit interaction, mostly functional placeholder here -->
                <span style="font-size:12px; cursor:pointer;">🔗 확인</span>
            </td>
        </tr>
        """, unsafe_allow_html=True)

    st.markdown("""
                </tbody>
            </table>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4. Streamlit Data Editor (Alternative "Modern" View)
    with st.expander("데이터 분석 뷰 (Data Editor)"):
        df = pd.DataFrame(filtered)
        if not df.empty:
            df_display = df[['subject', 'deptName', 'pressDt', 'managerName']]
            st.data_editor(
                df_display,
                column_config={
                    "subject": "공고명",
                    "deptName": st.column_config.TextColumn("소관부처", help="담당 부서"),
                    "pressDt": "등록일",
                    "managerName": "담당자"
                },
                hide_index=True,
                use_container_width=True
            )

if __name__ == "__main__":
    show_page()
