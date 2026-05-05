import streamlit as st
import pandas as pd

st.set_page_config(page_title="TRX AI EXPERT", layout="centered")

# ၁။ AI Training Logic (Pattern Mining)
@st.cache_data
def train_ai(file_path):
    try:
        df = pd.read_csv(file_path)
        data = df['bs'].tolist()
        patterns = {}
        for length in range(3, 9):
            for i in range(len(data) - length):
                pat = tuple(data[i : i + length])
                nxt = data[i + length]
                if pat not in patterns:
                    patterns[pat] = {'B': 0, 'S': 0}
                patterns[pat][nxt] += 1
        return patterns
    except:
        return None

# ၂။ UI Design
st.title("🎯 TRX AI STRATEGY (60% CONFIDENCE)")
st.divider()

if 'history' not in st.session_state:
    st.session_state.history = []

# Input Buttons
c1, c2 = st.columns(2)
if c1.button("BIG (B)", use_container_width=True):
    st.session_state.history.append("B")
if c2.button("SMALL (S)", use_container_width=True):
    st.session_state.history.append("S")

if st.button("Reset All Data"):
    st.session_state.history = []
    st.rerun()

# ၃။ AI Analysis
patterns = train_ai("data.csv")

if patterns:
    h = st.session_state.history[-10:]
    st.write(f"**Current Sequence:** {' - '.join(h)}")
    
    signal = None
    if len(h) >= 3:
        for length in range(len(h), 2, -1):
            p = tuple(h[-length:])
            if p in patterns:
                stats = patterns[p]
                total = stats['B'] + stats['S']
                b_prob = (stats['B']/total)*100
                s_prob = (stats['S']/total)*100
                
                # ၆၀% ကျော်တာကို ရှာမယ်
                if b_prob >= 60: signal = ("BIG", b_prob, total)
                elif s_prob >= 60: signal = ("SMALL", s_prob, total)
                
                if signal: break

    # ၄။ Display Result
    st.subheader("AI Prediction Result")
    if signal:
        res, prob, count = signal
        color = "green" if prob >= 80 else "blue"
        st.markdown(f"### 📢 SUGGESTION: :red[{res}]")
        st.write(f"**Confidence:** {round(prob, 1)}% (Based on {count} past matches)")
        
        if prob < 75:
            st.warning("⚠️ Confidence ၇၅% အောက်မို့လို့ ဂရုစိုက်ထိုးပါဗျ။")
    else:
        st.info("📉 No strong pattern found. Continue entering results...")
else:
    st.error("Missing 'data.csv'! Please upload it to your GitHub repo.")
