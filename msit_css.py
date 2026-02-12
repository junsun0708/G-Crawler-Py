
CARBON_CSS = """
@charset "UTF-8";
@import url("https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&family=Roboto:wght@700&display=swap");
@import url("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable.min.css");

:root {
  --bg-color: #14192d;
  --card-bg: #1e2a4a;
  --text-color: #ffffff;
  --sub-text: #d4ddea;
  --accent-color: #3ebdf3;
  --border-color: #2e3c5a;
}

/* Custom Scrollbar */
::-webkit-scrollbar {
  width: 10px;
  height: 10px;
}
::-webkit-scrollbar-track {
  background: #14192d; 
}
::-webkit-scrollbar-thumb {
  background: #2e3c5a; 
  border-radius: 5px;
}
::-webkit-scrollbar-thumb:hover {
  background: #3ebdf3; 
}

/* Global Streamlit Overrides (Dark Mode) */
.stApp {
    background-color: var(--bg-color) !important;
    color: var(--text-color) !important;
}
header[data-testid="stHeader"] {
    display: none;
}
.main .block-container {
    padding-top: 0.5rem !important;
    margin-top: 0 !important;
}
.stMainBlockContainer {
    padding-top: 0 !important;
}
.stVerticalBlock {
    gap: 0.5rem !important;
}
section.main > div {
    padding-top: 0 !important;
}
h1, h2, h3, h4, h5, h6, p, span, div, label {
    color: var(--text-color) !important;
}

/* Inputs */
.stTextInput > div > div > input {
    background-color: var(--card-bg) !important;
    color: var(--text-color) !important;
    border: 1px solid var(--border-color) !important;
}
.stTextInput label, .stRadio label {
    color: var(--sub-text) !important;
}

/* Buttons */
.stButton > button, button.ty1Button {
    background-color: var(--accent-color) !important;
    color: #14192d !important; /* Dark text on bright button */
    font-weight: 700 !important;
    border: none !important;
    border-radius: 4px;
}
.stButton > button:hover {
    background-color: #2663c6 !important;
    color: #fff !important;
}

/* Carbon Design Classes (Dark Adapted) */
.ThingsCarbon {
  width: 100%;
  background-color: var(--bg-color);
}

/* DashGrid */
.DashGrid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 20px;
  margin-top: 10px;
}
.DashGrid .DashGridItem {
  background-color: var(--card-bg);
  border-radius: 16px;
  padding: 20px; /* Reduced padding from 30px */
  box-shadow: 0 4px 10px 0 rgba(0, 0, 0, 0.3);
  border: 1px solid var(--border-color);
}

.DashGrid .DashGridItem p.DashItemTitle {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px; /* Reduced margin from 24px */
}
.DashGrid .DashGridItem p.DashItemTitle b {
  font-size: 18px;
  color: var(--text-color);
}
.DashGrid .DashGridItem p.DashItemTitle span {
  font-size: 12px;
  color: var(--sub-text);
}
.DashGrid .DashGridItem .totalCnt {
  display: flex;
  align-items: baseline;
  justify-content: flex-end; /* Align to right */
  gap: 8px; /* Space between number and unit */
}
.DashGrid .DashGridItem .totalCnt strong {
  display: block;
  color: var(--text-color);
  font-size: 40px;
  margin-bottom: 0px; /* Remove bottom margin */
  line-height: 1;
}
.DashGrid .DashGridItem .totalCnt em {
  display: block;
  color: var(--accent-color);
  font-size: 24px;
  font-weight: 700;
  line-height: 1;
}

/* CarbonBox */
.CarbonBox {
  border-radius: 16px;
  background: var(--card-bg);
  box-shadow: 0 4px 10px 0 rgba(0, 0, 0, 0.3);
  padding: 30px;
  position: relative;
  margin-bottom: 20px;
  border: 1px solid var(--border-color);
}
.CarbonBox .CarbonBoxTitle b {
  display: block;
  font-size: 18px;
  color: var(--text-color);
  margin-bottom: 15px;
}

/* Tables in DashGrid (if any) */
.DashGrid .DashGridItem table {
    width: 100%;
}
.DashGrid .DashGridItem table thead th {
    color: #939498;
    border-bottom: 1px solid #4a5568;
    padding: 10px;
}
.DashGrid .DashGridItem table tbody td {
    color: var(--sub-text);
    border-bottom: 1px solid var(--border-color);
    padding: 10px;
}

/* Badges */
.badge {
    background-color: #2663c6;
    color: #fff;
    padding: 4px 12px;
    border-radius: 6px;
    font-size: 0.85rem;
    margin-right: 8px;
    display: inline-block;
}

/* Link Colors */
a {
    color: var(--accent-color) !important;
    text-decoration: none;
}
"""

import streamlit as st

def load_css():
    st.markdown(f'<style>{CARBON_CSS}</style>', unsafe_allow_html=True)

def page_header(title, label=None):
    # Header Removed/Hidden per user request in v2, but keeping function for others if needed
    if label:
        st.markdown(f"""
        <div style="margin-bottom: 20px;">
            <strong style="font-size: 24px;">{title}</strong>
            <span style="color: #ccc; margin-left: 10px;">{label}</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="margin-bottom: 20px;">
             <strong style="font-size: 24px;">{title}</strong>
        </div>
        """, unsafe_allow_html=True)

def card_template(title, content):
    st.markdown(f"""
    <div class="CarbonBox">
        <div class="CarbonBoxTitle"><b>{title}</b></div>
        {content}
    </div>
    """, unsafe_allow_html=True)
