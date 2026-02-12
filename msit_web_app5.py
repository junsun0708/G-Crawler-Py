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
    st.set_page_config(page_title="MSIT Analytics (v5)", layout="wide")
    st.markdown(f"<style>{msit_css.CARBON_CSS}</style>", unsafe_allow_html=True)
    all_data = load_data()
    
    msit_css.page_header("📊 지원사업 데이터 분석 (v5)", "Analytics & Calculator View")
    
    df = pd.DataFrame(all_data)
    
    # 1. 상단 분석 카드 (CarbonBox + Chart)
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.markdown('<div class="CarbonBox"><div class="CarbonBoxTitle"><b>분야별 공고 통계</b></div>', unsafe_allow_html=True)
        if not df.empty and 'deptName' in df.columns:
            chart_data = df['deptName'].value_counts()
            st.bar_chart(chart_data)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c2:
        st.markdown('<div class="CarbonBox"><div class="CarbonBoxTitle"><b>주요 키워드</b></div>', unsafe_allow_html=True)
        keywords = ["AI", "데이터", "클라우드", "바이오", "에너지"]
        for k in keywords:
            count = df['subject'].apply(lambda x: k in x).sum() if not df.empty else 0
            st.metric(k, f"{count}건")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 2. 예산 계산기 시뮬레이션 (CarbonCalcuWrap Style)
    st.write("")
    st.markdown("### 💰 예산 시뮬레이션 (Calculator Style)")
    
    # Horizontal Scroll Layout simulation
    st.markdown("""
    <div class="CarbonCalcuWrap" style="height: auto; min-height: 200px; padding: 20px; background-color: #fff; border-radius: 16px;">
        <div class="calcuList" style="overflow-x: auto; display: flex; gap: 20px;">
            <!-- Python loop to generate items -->
    """, unsafe_allow_html=True)
    
    # Generate items dynamically
    cols = st.columns(3)
    funding_scenario = [
        {"title": "R&D 초기지원", "amount": 5000},
        {"title": "사업화 지원", "amount": 3000},
        {"title": "글로벌 진출", "amount": 10000},
    ]

    for idx, item in enumerate(funding_scenario):
        with cols[idx]:
             st.markdown(f"""
             <div class="calcuBox" style="width: 100%; min-width: 0;">
                <div class="calcuCont" style="background-color: #f7f7f7; padding: 20px; border-radius: 8px;">
                    <div style="font-weight:bold; font-size:16px; margin-bottom:10px;">{item['title']}</div>
                    <div style="font-size:24px; color:#00a4e0; font-weight:bold;">{item['amount']:,} 만원</div>
                    <div style="font-size:12px; color:#666; margin-top:5px;">국비 지원 70%</div>
                </div>
             </div>
             """, unsafe_allow_html=True)
             
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 3. Interactive Slider
    st.write("")
    with st.expander("세부 예산 조정기"):
        budget = st.slider("총 사업비 예상 (단위: 억원)", 1, 100, 10)
        st.info(f"선택하신 사업비 {budget}억원에 대해, 정부출연금 최대 {budget * 0.7:.1f}억원까지 지원 가능합니다.")

if __name__ == "__main__":
    show_page()
