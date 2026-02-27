import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import time

# --- CONFIG & THEME ---
st.set_page_config(page_title="LokalLogic Enterprise", layout="wide")

st.markdown("""
    <style>
    /* Main Background */
    .stApp { background-color: #F0F8FF; color: black; }
    
    /* SIDEBAR: Light Sky Blue */
    [data-testid="stSidebar"] { background-color: #87CEFA; }
    [data-testid="stSidebar"] * { color: black !important; }

    /* HEADING: Text White, Icons Black */
    /* This targets the main titles and subtitles */
    h1, h2 { 
        color: white !important; 
        background-color: #4682B4; 
        padding: 15px; 
        border-radius: 10px;
        display: flex;
        align-items: center;
    }
    /* Style for any icons within headers to appear black */
    h1 span, h2 span, .stIcon { color: black !important; }

    p, span, label { color: black !important; }
    
    .stButton>button { background-color: #4682B4; color: white; border-radius: 8px; font-weight: bold; }
    .ai-reply { color: #000080; font-weight: bold; background: white; padding: 15px; border-radius: 10px; border-left: 5px solid #4682B4; }
    
    /* Ensure metric labels are visible */
    [data-testid="stMetricValue"] { color: black !important; }
    [data-testid="stMetricLabel"] { color: #333 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'user_db' not in st.session_state: st.session_state.user_db = {}
if 'data' not in st.session_state: st.session_state.data = None

# --- LOGIN / SIGNUP ---
if not st.session_state.auth:
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    with tab2:
        st.header("Create Account 👤")
        new_email = st.text_input("Email ID")
        new_user = st.text_input("Set Username")
        new_pw = st.text_input("Set Password", type="password")
        biz_name = st.text_input("Business Name")
        if st.button("Register"):
            if new_user and new_pw:
                st.session_state.user_db = {"user": new_user, "pw": new_pw, "name": biz_name}
                st.success("Registered! Go to Login.")
    with tab1:
        st.header("Login 🔐")
        l_user = st.text_input("Username")
        l_pw = st.text_input("Password", type="password")
        if st.button("Enter Dashboard"):
            if st.session_state.user_db and l_user == st.session_state.user_db['user'] and l_pw == st.session_state.user_db['pw']:
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Check credentials.")

# --- APP ---
else:
    st.sidebar.title(f"🚀 {st.session_state.user_db.get('name', 'Business')}")
    menu = st.sidebar.radio("Navigation", ["Home", "Dashboard", "AI Studio", "AI Assistant", "Analytics"])

    if menu == "Home":
        st.title("Home 🏠")
        st.write(f"### Welcome to {st.session_state.user_db['name']} Management Portal")
        
        c1, c2, c3 = st.columns(3)
        with c1: st.info("📊 **Dashboard**")
        with c2: st.info("📢 **AI Studio**")
        with c3: st.info("💬 **AI Assistant**")
        
        st.write("---")
        st.write("### 📂 Load Data")
        file = st.file_uploader("Upload CSV", type="csv")
        if file:
            st.session_state.data = pd.read_csv(file)
            st.success("CSV Connected!")

    elif menu == "Dashboard":
        st.title("Dashboard 📊")
        if st.session_state.data is not None:
            col1, col2, col3 = st.columns(3)
            col1.metric("Earned", "$15,200", "+8%")
            col2.metric("Spent", "$9,100", "-1%")
            col3.metric("Profit", "40.1%", "↑ 5%")
            
            st.write("---")
            g1, g2 = st.columns(2)
            with g1:
                st.subheader("Profit vs Loss Graph 📉")
                pl_data = pd.DataFrame({"Time": ["T1", "T2", "T3", "T4"], "Amt": [100, -20, 250, 400]})
                st.plotly_chart(px.area(pl_data, x="Time", y="Amt", color_discrete_sequence=['#4682B4']), use_container_width=True)
            with g2:
                st.subheader("Product Sales Velocity 📈")
                st.plotly_chart(px.bar(st.session_state.data, x=st.session_state.data.columns[0], y=st.session_state.data.columns[1], color_discrete_sequence=['#87CEFA']), use_container_width=True)
        else:
            st.warning("Please upload CSV on Home page.")

    elif menu == "AI Studio":
        st.title("AI Studio 📢")
        # Ensure input labels are black
        k1 = st.text_input("Vibe Keyword (e.g. Fresh)")
        k2 = st.text_input("Product Keyword (e.g. Milk)")
        k3 = st.text_input("Benefit Keyword (e.g. Organic)")
        
        if st.button("Generate My Custom Post"):
            if k1 and k2 and k3:
                # Force backend to use the variables
                res = requests.get(f"http://127.0.0.1:8000/generate-marketing?k1={k1}&k2={k2}&k3={k3}").json()
                st.image("https://images.unsplash.com/photo-1542838132-92c53300491e?w=800")
                st.write("### 📝 Generated Caption")
                st.write(res['caption'])
                st.write("### 🏷️ Hashtags")
                st.code(res['hashtags'])
            else:
                st.error("Please fill all 3 keywords!")

    elif menu == "AI Assistant":
        st.title("AI Assistant 💬")
        q = st.chat_input("Ask about your strategy...")
        if q:
            with st.chat_message("user"): st.write(q)
            with st.chat_message("assistant"):
                res = requests.get(f"http://127.0.0.1:8000/ai-chat?query={q}").json()
                st.markdown(f"<div class='ai-reply'>{res['response']}</div>", unsafe_allow_html=True)

    elif menu == "Analytics":
        st.title("Analytics 📈")
        st.success("✅ **Strategy:** Sales are peaking at 6 PM. Suggestion: Start 'Evening Specials' at 5:30 PM.")
        st.info("💡 **Growth:** Your local market reach is up 15%. Focus on retention ads.")