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
    st.set_page_config(page_title="MSIT Wizard (v4)", layout="wide")
    st.markdown(f"<style>{msit_css.CARBON_CSS}</style>", unsafe_allow_html=True)
    
    if 'wizard_step' not in st.session_state:
        st.session_state.wizard_step = 1
    if 'selected_dept' not in st.session_state:
        st.session_state.selected_dept = None
    if 'selected_tag' not in st.session_state:
        st.session_state.selected_tag = None

    all_data = load_data()
    depts = sorted(list(set([d.get('deptName') for d in all_data if d.get('deptName')])))
    tags = ["전체", "에너지", "AI", "제조", "스마트공장", "ESG", "R&D", "ICT", "바이오"]

    # --- Header ---
    st.markdown("""
    <div class="CarbonPageTitle">
        <strong>🧙‍♀️ 맞춤 지원사업 찾기 (v4)</strong>
        <p style="color:#666; margin-left:20px;">단계별로 원하시는 사업을 찾아드립니다.</p>
    </div>
    """, unsafe_allow_html=True)

    # --- Step Indicator (Visual only, simulates .CarbonStep styles) ---
    step_class = f"stepCnt3 step{st.session_state.wizard_step}"
    
    # HTML Animation Style injection specifically for this page's dynamic step
    st.markdown(f"""
    <div class="CarbonStepWrap" style="margin-bottom: 40px;">
        <div class="CarbonBox" style="padding: 40px 0;">
             <div class="CarbonStep {step_class}">
                <ul class="{f'step{st.session_state.wizard_step}'}">
                    <li>1</li>
                    <li>2</li>
                    <li>3</li>
                </ul>
             </div>
             <div style="text-align:center; margin-top:20px; font-weight:bold;">
                {'소관부처 선택' if st.session_state.wizard_step == 1 else '분야 태그 선택' if st.session_state.wizard_step == 2 else '결과 확인'}
             </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # --- Content Area ---
    container = st.container()
    
    with container:
        if st.session_state.wizard_step == 1:
            st.markdown("### 🏢 소관부처를 선택해주세요")
            cols = st.columns(4)
            for idx, dept in enumerate(depts):
                with cols[idx % 4]:
                    if st.button(dept, key=f"dept_{idx}", use_container_width=True):
                        st.session_state.selected_dept = dept
                        st.session_state.wizard_step = 2
                        st.rerun()
            
            st.write("")
            if st.button("건너뛰기 (전체 부처)", use_container_width=True):
                st.session_state.selected_dept = "전체"
                st.session_state.wizard_step = 2
                st.rerun()

        elif st.session_state.wizard_step == 2:
            st.markdown(f"### 🏷️ 분야를 선택해주세요 (선택된 부처: {st.session_state.selected_dept})")
            cols = st.columns(3)
            for idx, tag in enumerate(tags):
                with cols[idx % 3]:
                    if st.button(tag, key=f"tag_{idx}", use_container_width=True):
                        st.session_state.selected_tag = tag
                        st.session_state.wizard_step = 3
                        st.rerun()
             
            st.write("")
            col_prev, col_skip = st.columns(2)
            with col_prev:
                 if st.button("⬅️ 이전 단계"):
                    st.session_state.wizard_step = 1
                    st.rerun()

        elif st.session_state.wizard_step == 3:
            # Filtering Logic
            dept = st.session_state.selected_dept
            tag = st.session_state.selected_tag
            
            filtered = all_data
            if dept and dept != "전체":
                filtered = [d for d in filtered if d.get('deptName') == dept]
            if tag and tag != "전체":
                filtered = [d for d in filtered if tag in d.get('subject', '') or tag in d.get('deptName', '')]
            
            st.markdown(f"### 🎉 찾은 결과: {len(filtered)}건")
            st.caption(f"조건: 부처[{dept}], 태그[{tag}]")
            
            if not filtered:
                st.warning("조건에 맞는 공고가 없습니다.")
            else:
                 for item in filtered:
                    st.success(f"[{item.get('deptName')}] {item.get('subject')}")
            
            st.write("")
            if st.button("🔃 처음부터 다시 찾기"):
                st.session_state.wizard_step = 1
                st.session_state.selected_dept = None
                st.session_state.selected_tag = None
                st.rerun()

if __name__ == "__main__":
    show_page()
