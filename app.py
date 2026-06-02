import streamlit as st
import pandas as pd

# 設定網頁標題與風格
st.set_page_config(page_title="貨銀第八組 - 財政貨幣協調 AI Agent", layout="wide")

# 自定義 CSS 讓網頁看起來像你們的黑金簡報風格
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { background-color: #ffd700; color: black; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 財政與貨幣政策協調 AI Agent")
st.subheader("第八組專題：總體政策模擬決策系統")

# 側邊欄：輸入數據區
with st.sidebar:
    st.header("📊 經濟數據輸入")
    region = st.selectbox("選擇研究地區", ["美國", "台灣", "自定義"])
    
    # 對應你們簡報中的變數
    deficit_gdp = st.number_input("財政赤字 / GDP (%)", value=6.0, step=0.1)
    debt_gdp = st.number_input("公債餘額 / GDP (%)", value=123.0, step=0.1)
    inflation = st.number_input("通膨率 CPI (%)", value=2.1, step=0.1)
    monetary_stance = st.selectbox("目前貨幣政策立場", ["緊縮 (升息)", "中性", "寬鬆 (降息)"])
    
    analyze_btn = st.button("開始 AI 決策分析")

# 主畫面內容
col1, col2 = st.columns([1, 1])

with col1:
    st.write("## 🏦") # 已修復：改用 Emoji 避免圖片網址失效破圖
    st.write("### 當前情境摘要")
    st.info(f"地區：{region}\n\n財政狀況：赤字 {deficit_gdp}%，債務 {debt_gdp}%\n\n通膨壓力：{inflation}%\n\n貨幣立場：{monetary_stance}")

with col2:
    st.write("### AI 決策邏輯 (邏輯鏈)")
    if inflation > 3.0:
        st.warning("⚠️ 偵測到高通膨：系統優先建議『緊縮協調』")
    elif deficit_gdp > 5.0:
        st.error("🚨 財政赤字過高：注意『排擠效應』風險")
    else:
        st.success("✅ 經濟現況尚屬穩定")

st.divider()

# AI 輸出區
if analyze_btn:
    st.write("## 🤖 AI Agent 決策報告")
    
    tab1, tab2, tab3 = st.tabs(["政策協調分析", "模擬結果預測", "🌉 跨群橋梁 (G3 引用)"])
    
    with tab1:
        st.markdown("### 1. 政策協調性評估")
        if inflation > 2.0 and monetary_stance == "寬鬆 (降息)":
            st.write("❌ **不協調**：目前通膨偏高，但貨幣政策過於寬鬆，財政支出應縮減以避免經濟過熱。")
        else:
            st.write("✅ **目前政策尚屬協調**：貨幣與財政立場一致，有助於維持總體經濟穩定。")
            
    with tab2:
        st.markdown("### 2. 排擠效應與調整建議")
        st.write(f"若政府在此刻擴大財政刺激，預計會導致市場利率上升，進而產生**排擠效應**。")
        st.write("👉 **建議調整**：央行應維持目前利率水準，不宜過早降息，以防止債務貨幣化。")
        
    with tab3:
        st.markdown("### 3. 給第三組 (G3 匯率組) 的數據摘要")
        bridge_text = f"【G8 橋梁任務】由於目前{region}財政赤字達 {deficit_gdp}%，且公債比高達 {debt_gdp}%，預期國債發行量增加將推升殖利率。根據利率平價理論，這將吸引外資流入，對本幣匯率造成升值壓力，請 G3 納入匯率預測模型。"
        st.code(bridge_text, language="markdown")
        st.success("此摘要可直接複製給 G3 使用")

else:
    st.info("請點擊左側『開始 AI 決策分析』按鈕查看結果") # 已修復：解決 st.light 造成的 AttributeError
