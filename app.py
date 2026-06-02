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

# 側邊欄：輸入數據區 (優化：改用動態滑桿 Slider)
with st.sidebar:
    st.header("📊 經濟數據輸入")
    region = st.selectbox("選擇研究地區", ["美國", "台灣", "自定義"])
    
    deficit_gdp = st.slider("財政赤字 / GDP (%)", min_value=0.0, max_value=15.0, value=6.0, step=0.1)
    debt_gdp = st.slider("公債餘額 / GDP (%)", min_value=50.0, max_value=150.0, value=123.0, step=0.1)
    inflation = st.slider("通膨率 CPI (%)", min_value=-2.0, max_value=10.0, value=2.1, step=0.1)
    monetary_stance = st.selectbox("目前貨幣政策立場", ["緊縮 (升息)", "中性", "寬鬆 (降息)"])
    
    analyze_btn = st.button("開始 AI 決策分析")

# 主畫面內容
col1, col2 = st.columns([1, 1])

# 優化：金融戰情儀表板 (Metrics)
with col1:
    st.write("## 🏦") 
    st.write("### 當前情境看板")
    m1, m2 = st.columns(2)
    m1.metric(label="財政赤字 / GDP", value=f"{deficit_gdp}%", delta="-警戒" if deficit_gdp > 5 else "安全", delta_color="inverse")
    m2.metric(label="公債餘額 / GDP", value=f"{debt_gdp}%", delta="持續攀升", delta_color="inverse")
    
    m3, m4 = st.columns(2)
    m3.metric(label="通膨率 CPI", value=f"{inflation}%", delta="偏高" if inflation > 2 else "達標", delta_color="inverse")
    m4.metric(label="貨幣立場", value=monetary_stance)

with col2:
    st.write("### AI 決策邏輯 (邏輯鏈)")
    if inflation > 3.0:
        st.warning("⚠️ 偵測到高通膨：系統優先建議『緊縮協調』")
    elif deficit_gdp > 5.0:
        st.error("🚨 財政赤字過高：注意『排擠效應』風險")
    else:
        st.success("✅ 經濟現況尚屬穩定")

st.divider()

# AI 輸出區 (移除 G3 橋梁任務)
if analyze_btn:
    st.write("## 🤖 AI Agent 決策報告")
    
    # 只保留兩個 Tab
    tab1, tab2 = st.tabs(["政策協調分析", "模擬結果預測"])
    
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
        
        # 優化：動態走勢圖 (Line Chart)
        st.divider()
        st.markdown("#### 📊 政策執行後模擬走勢 (未來三季)")
        if monetary_stance == "緊縮 (升息)":
            chart_data = pd.DataFrame({
                "預估通膨率 CPI (%)": [inflation, inflation - 0.3, inflation - 0.7],
                "預估財政赤字 (%)": [deficit_gdp, deficit_gdp + 0.2, deficit_gdp + 0.5]
            }, index=["Q1", "Q2", "Q3"])
        else:
            chart_data = pd.DataFrame({
                "預估通膨率 CPI (%)": [inflation, inflation + 0.5, inflation + 1.2],
                "預估財政赤字 (%)": [deficit_gdp, deficit_gdp - 0.1, deficit_gdp - 0.3]
            }, index=["Q1", "Q2", "Q3"])
            
        st.line_chart(chart_data)

else:
    st.info("請點擊左側『開始 AI 決策分析』按鈕查看結果")
