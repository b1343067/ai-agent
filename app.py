import streamlit as st
import pandas as pd
import time

# 設定網頁標題與風格
st.set_page_config(page_title="貨銀第八組 - 財政貨幣協調 AI Agent", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { background-color: #ffd700; color: black; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 財政與貨幣政策協調 AI Agent")
st.subheader("第八組專題：總體政策模擬決策系統")

# ==========================================
# 優化 1：一鍵載入歷史經典情境
# ==========================================
with st.sidebar:
    st.header("📂 情境資料庫")
    scenario = st.selectbox("快速載入歷史情境", ["自訂輸入 (當前現況)", "2022 疫情後大通膨", "2008 金融海嘯"])
    
    # 根據選擇的情境，自動設定滑桿的預設值
    if scenario == "2022 疫情後大通膨":
        def_val, debt_val, cpi_val, rate_val = 12.3, 120.0, 9.1, 2.5
    elif scenario == "2008 金融海嘯":
        def_val, debt_val, cpi_val, rate_val = 9.8, 67.0, -0.4, 0.25
    else:
        def_val, debt_val, cpi_val, rate_val = 6.0, 123.0, 2.1, 5.5

    st.markdown("---")
    st.header("📊 經濟數據觀測站")
    
    deficit_gdp = st.slider("財政赤字 / GDP (%)", min_value=0.0, max_value=20.0, value=float(def_val), step=0.1)
    debt_gdp = st.slider("公債餘額 / GDP (%)", min_value=0.0, max_value=150.0, value=float(debt_val), step=0.1)
    inflation = st.slider("通膨率 CPI (%)", min_value=-2.0, max_value=15.0, value=float(cpi_val), step=0.1)
    policy_rate = st.slider("政策基準利率 (%)", min_value=0.0, max_value=10.0, value=float(rate_val), step=0.1)
    
    analyze_btn = st.button("啟動 AI 決策演算法")

# 核心邏輯：AI 自動判斷貨幣政策立場
if policy_rate > inflation + 1.0:
    monetary_stance = "緊縮 (升息)"
elif policy_rate < inflation - 0.5:
    monetary_stance = "寬鬆 (降息)"
else:
    monetary_stance = "中性"

# ==========================================
# 主畫面內容：戰情儀表板
# ==========================================
col1, col2 = st.columns([1, 1])

with col1:
    st.write("## 🏦") 
    st.write("### 狀態空間 (State) 看板")
    m1, m2 = st.columns(2)
    m1.metric(label="財政赤字 / GDP", value=f"{deficit_gdp}%", delta="-警戒" if deficit_gdp > 5.0 else "安全", delta_color="inverse")
    m2.metric(label="公債餘額 / GDP", value=f"{debt_gdp}%", delta="持續攀升", delta_color="inverse")
    
    # 優化 2：公債健康度視覺化血條
    st.caption("公債壓力指數")
    progress_val = min(debt_gdp / 150.0, 1.0) # 換算成 0.0 ~ 1.0
    st.progress(progress_val)
    
    m3, m4 = st.columns(2)
    m3.metric(label="通膨率 CPI", value=f"{inflation}%", delta="偏高" if inflation > 2.0 else "達標", delta_color="inverse")
    m4.metric(label="自動判定貨幣立場", value=monetary_stance, delta=f"基準利率 {policy_rate}%", delta_color="off")

with col2:
    st.write("### AI 決策網路 (Policy)")
    if inflation > 3.0:
        st.warning("⚠️ 觀測狀態：高通膨，系統優先尋求『緊縮協調』")
    elif deficit_gdp > 5.0:
        st.error("🚨 觀測狀態：財政赤字過高，啟動『排擠效應』風險預警")
    elif inflation < 0:
        st.info("❄️ 觀測狀態：通縮風險，系統尋求『寬鬆刺激』")
    else:
        st.success("✅ 觀測狀態：總體經濟指標穩定")

st.divider()

# ==========================================
# AI 輸出區
# ==========================================
if analyze_btn:
    with st.spinner('🤖 AI Agent 正在進行政策模擬與協調性運算...'):
        time.sleep(1.5) 
    st.toast('決策分析完成！', icon='✅')
    
    st.write("## 🎯 AI Agent 決策報告 (Action)")
    
    tab1, tab2 = st.tabs(["政策協調分析", "模擬結果預測"])
    report_text = ""
    
    with tab1:
        st.markdown("### 1. 政策協調性評估")
        if inflation > 3.0 and monetary_stance == "緊縮 (升息)" and deficit_gdp > 5.0:
            st.error("❌ **政策衝突 (不協調)**：央行正在『升息』打通膨，但政府卻維持高赤字 (大撒幣)，兩者作用互相抵銷！建議政府應縮減支出以配合央行。")
            report_text += "[政策衝突] 央行升息與政府高赤字互相抵銷，應縮減支出。\n"
        elif inflation > 2.0 and monetary_stance == "寬鬆 (降息)":
            st.error("❌ **嚴重不協調**：目前通膨偏高，但貨幣政策卻『降息』放水，等於提油救火，將導致通膨失控。")
            report_text += "[嚴重不協調] 高通膨下實施寬鬆政策，將導致通膨失控。\n"
        elif inflation < 0.0 and monetary_stance == "緊縮 (升息)":
            st.error("❌ **經濟衰退危機**：已出現通縮現象，央行卻持續緊縮，將引發嚴重經濟衰退。")
            report_text += "[衰退危機] 通縮環境下持續升息，將引發嚴重衰退。\n"
        elif inflation < 2.0 and deficit_gdp < 3.0 and monetary_stance == "緊縮 (升息)":
            st.warning("⚠️ **過度緊縮風險**：通膨已偏低且財政保守，若央行仍持續升息，恐壓抑經濟動能。")
            report_text += "[過度緊縮] 通膨偏低且財政保守，持續升息恐壓抑動能。\n"
        else:
            st.success("✅ **目前政策尚屬協調**：貨幣與財政步調相對一致，有助於維持總體經濟穩定。")
            report_text += "[政策協調] 貨幣與財政步調一致，有助經濟穩定。\n"
            
    with tab2:
        st.markdown("### 2. 排擠效應與調整建議")
        st.write("若政府在此刻擴大財政刺激，預計會導致市場利率上升，進而產生**排擠效應**。")
        st.write("👉 **建議調整**：央行應維持目前利率水準，以防止債務貨幣化。")
        report_text += "排擠效應警告：擴大刺激將推升利率，建議央行維持目前水位。\n"
        
        st.divider()
        st.markdown("#### 📊 政策執行後模擬走勢 (未來三季)")
        if monetary_stance == "緊縮 (升息)":
            chart_data = pd.DataFrame({
                "預估通膨率 CPI (%)": [inflation, inflation - 0.5, inflation - 1.2],
                "預估財政赤字 (%)": [deficit_gdp, deficit_gdp + 0.2, deficit_gdp + 0.5]
            }, index=["Q1", "Q2", "Q3"])
        else:
            chart_data = pd.DataFrame({
                "預估通膨率 CPI (%)": [inflation, inflation + 0.8, inflation + 1.5],
                "預估財政赤字 (%)": [deficit_gdp, deficit_gdp - 0.1, deficit_gdp - 0.3]
            }, index=["Q1", "Q2", "Q3"])
            
        st.line_chart(chart_data)
        
    st.divider()
    download_content = f"【G8 財政與貨幣政策協調 AI 評估報告】\n\n當前指標：\n赤字率：{deficit_gdp}%\n債務比：{debt_gdp}%\n通膨率：{inflation}%\n基準利率：{policy_rate}%\n\nAI 診斷結果：\n{report_text}"
    st.download_button("📥 下載 AI 決策備忘錄 (.txt)", data=download_content, file_name="G8_Policy_Report.txt", mime="text/plain")

else:
    st.info("👈 請於左側設定觀測指標，並點擊『啟動 AI 決策演算法』")

# ==========================================
# 優化 3：隱藏式防禦武器 (理論區)
# ==========================================
st.markdown("<br><br>", unsafe_allow_html=True) # 增加一些下方留白
with st.expander("📚 系統核心理論與 MARL 架構對照 (點擊展開)"):
    st.markdown("""
    **本系統基於《貨幣銀行學》理論與 MARL 架構開發：**
    * **Agent (智能體)**：G8 財政貨幣協調決策系統。
    * **State (狀態)**：左側輸入之赤字率、債務比、通膨率與利率。
    * **Policy (策略)**：透過實質利率 (基準利率-通膨率) 判定貨幣立場，並比對赤字水位判斷是否發生衝突。
    * **排擠效應 (Crowding Out)**：政府透過發行公債籌措擴張性財政政策之資金，導致市場利率攀升，進而使民間投資減少之現象。
    """)
