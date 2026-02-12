import streamlit as st
import json
import os
import msit_css

def load_data():
    if os.path.exists('msit_data.json'):
        with open('msit_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def show_page():
    st.set_page_config(page_title="MSIT Report (v6)", layout="wide")
    st.markdown(f"<style>{msit_css.CARBON_CSS}</style>", unsafe_allow_html=True)
    
    all_data = load_data()
    msit_css.page_header("📑 상세 결과 보고서 (v6)", "Report & Detail View")

    # Layout: Left Sidebar List, Right Detail View
    c_list, c_detail = st.columns([1, 2])
    
    selected_idx = 0 
    
    with c_list:
        st.markdown(f"### 📋 공고 목록 ({len(all_data)})")
        selected_title = st.selectbox(
            "공고를 선택하세요",
            [d.get('subject') for d in all_data],
            index=0
        )
        
        # Find selected item
        selected_item = next((d for d in all_data if d.get('subject') == selected_title), None)

    with c_detail:
        if selected_item:
            # CarbonReportPop Style Implementation
            st.markdown(f"""
            <div class="CarbonReportPop">
                <div class="reportTitle">
                    <div>
                        <strong>상세 공고 보고서</strong>
                    </div>
                </div>
                <hr style="border: 0; border-top: 2px solid #14192d; margin: 20px 0;">
                
                <dl>
                    <dt>기본 정보</dt>
                    <dd>
                        <strong>{selected_item.get('subject')}</strong>
                        <table>
                            <tbody>
                                <tr>
                                    <th style="width:20%; background:#f7f7f7;">소관부처</th>
                                    <td>{selected_item.get('deptName')}</td>
                                </tr>
                                <tr>
                                    <th style="background:#f7f7f7;">등록일</th>
                                    <td>{selected_item.get('pressDt')}</td>
                                </tr>
                                <tr>
                                    <th style="background:#f7f7f7;">담당자</th>
                                    <td>{selected_item.get('managerName')} ({selected_item.get('managerTel')})</td>
                                </tr>
                            </tbody>
                        </table>
                    </dd>
                </dl>
                
                <dl>
                    <dt>세부 분석 (가상 데이터)</dt>
                    <dd>
                        <div class="ReportGrid">
                            <div class="grayBox">
                                <b>📊 지원 경쟁률 예상</b>
                                <p style="font-size:24px; color:#3ebdf3; margin-top:10px;">12.5 : 1</p>
                            </div>
                            <div class="grayBox">
                                <b>📅 예상 마감일</b>
                                <p style="font-size:24px; color:#2b2b2b; margin-top:10px;">D-15</p>
                            </div>
                        </div>
                    </dd>
                </dl>
                
                <div style="text-align:right; margin-top:20px;">
                    <a href="{selected_item.get('viewUrl')}" target="_blank" style="background-color:#14192d; color:#fff; padding:10px 20px; border-radius:4px; text-decoration:none;">원문 공고 보러가기 👉</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("좌측에서 공고를 선택해주세요.")

if __name__ == "__main__":
    show_page()
