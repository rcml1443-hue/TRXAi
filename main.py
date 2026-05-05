import streamlit as st
import pandas as pd

st.set_page_config(page_title="TRX AI Expert", layout="wide")

# ၁။ Data Loading & AI Training Logic
@st.cache_data
def train_ai_model(file_path):
    df = pd.read_csv(file_path)
    data = df['bs'].tolist()
    patterns = {}
    
    # AI က Pattern အရှည် ၃ ခုကနေ ၈ ခုအထိ အကုန်လေ့လာမယ်
    for length in range(3, 9):
        for i in range(len(data) - length):
            pat = tuple(data[i : i + length])
            nxt = data[i + length]
            if pat not in patterns:
                patterns[pat] = {'B': 0, 'S': 0}
            patterns[pat][nxt] += 1
    return patterns

# ၂။ Session State (လက်ရှိ ရိုက်ထည့်နေတဲ့ ရလဒ်များကို မှတ်ထားရန်)
if 'current_history' not in st.session_state:
    st.session_state.current_history = []

# ၃။ UI ပုံစံထုတ်ခြင်း
st.title("🎯 TRX AI Pattern Expert (Manual Input)")
st.write("အမြဲမထိုးပါနဲ့။ AI က **Confidence 85% ကျော်** ပြမှသာ ထိုးဖို့ အကြံပြုပါတယ်။")

try:
    patterns = train_ai_model("data.csv")
    
    # ရလဒ်ထည့်ရန် ခလုတ်များ
    col1, col2 = st.columns(2)
    if col1.button("BIG (B)", use_container_width=True):
        st.session_state.current_history.append("B")
    if col2.button("SMALL (S)", use_container_width=True):
        st.session_state.current_history.append("S")
    
    if st.button("Reset Session"):
        st.session_state.current_history = []
        st.rerun()

    # ၄။ AI Analysis Logic
    history = st.session_state.current_history[-10:] # နောက်ဆုံး ၁၀ ခုပဲ ယူမယ်
    st.subheader(f"Current Sequence: {' - '.join(history)}")

    # Pattern ရှာပုံတော်ဖွင့်ခြင်း
    found_signal = None
    if len(history) >= 3:
        for length in range(len(history), 2, -1):
            check_pat = tuple(history[-length:])
            if check_pat in patterns:
                stats = patterns[check_pat]
                total = stats['B'] + stats['S']
                if total >= 3: # အနည်းဆုံး ၃ ကြိမ် ဖြစ်ဖူးမှ စဉ်းစားမယ်
                    b_prob = (stats['B'] / total) * 100
                    s_prob = (stats['S'] / total) * 100
                    
                    # ၈၅% ကျော်ရင် Signal ပေးမယ်
                    if b_prob >= 85: found_signal = ("BIG", b_prob, total)
                    elif s_prob >= 85: found_signal = ("SMALL", s_prob, total)
                    
                    if found_signal: break # အရှည်ဆုံး Pattern ကိုပဲ ယူမယ်

    # ၅။ Display Signal
    st.divider()
    if found_signal:
        res, prob, count = found_signal
        st.success(f"🔥 **CONFIRMED SIGNAL: BET {res}**")
        st.metric(label="AI Confidence Score", value=f"{round(prob, 1)}%")
        st.info(f"သမိုင်းကြောင်းအရ ဒီ Pattern မျိုး {count} ကြိမ် ဖြစ်ဖူးပြီး {round(prob)}% နိုင်ခဲ့ပါတယ်။")
    else:
        st.warning("⚖️ **STATUS: WAIT / SKIP**")
        st.write("AI က သေချာတဲ့ Pattern မတွေ့သေးပါ။ ရလဒ်များ ဆက်လက်ထည့်သွင်းပေးပါ။")

except Exception as e:
    st.error("Error: 'data.csv' ဖိုင်ကို ရှာမတွေ့ပါ။ GitHub Repository ထဲမှာ data.csv ဖိုင် ထည့်ထားပေးပါဗျ။")
