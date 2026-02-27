import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import time
import numpy as np

# --- CONFIG & THEME ---
st.set_page_config(page_title="LokalLogic Enterprise", layout="wide")

st.markdown("""
    <style>
    /* 1. Remove Top Black Band/Header but keep the Sidebar Toggle visible */
    header[data-testid="stHeader"] {
        background-color: rgba(0,0,0,0);
    }
    
    /* Ensure the sidebar toggle button is always visible and black for contrast */
    button[data-testid="stSidebarCollapsedControl"] {
        color: black !important;
        background-color: white !important;
        border-radius: 50%;
        border: 1px solid #ddd;
    }

    .main .block-container {padding-top: 1rem;}

    /* Main Background */
    .stApp { background-color: #F0F8FF; color: black; }
    
    /* SIDEBAR: Light Sky Blue */
    [data-testid="stSidebar"] { background-color: #87CEFA; }
    [data-testid="stSidebar"] * { color: black !important; }

    /* HEADING: Text White, Icons Black */
    h1, h2 { 
        color: white !important; 
        background-color: #4682B4; 
        padding: 15px; 
        border-radius: 10px;
        display: flex;
        align-items: center;
    }
    
    /* Hover Fade Effect for Interactive Blocks */
    div.stButton > button, div[data-testid="stMetric"] {
        transition: opacity 0.3s ease;
    }
    div.stButton > button:hover, div[data-testid="stMetric"]:hover {
        opacity: 0.7;
    }

    p, span, label { color: black !important; }
    
    .stButton>button { background-color: #4682B4; color: white; border-radius: 8px; font-weight: bold; }
    .ai-reply { color: #000080; font-weight: bold; background: white; padding: 15px; border-radius: 10px; border-left: 5px solid #4682B4; }
    
    [data-testid="stMetricValue"] { color: black !important; }
    [data-testid="stMetricLabel"] { color: #333 !important; }

    /* --- NEW CHANGES FOR HASHTAGS --- */
    /* Target the code container and remove default dark background */
    div[data-testid="stCodeBlock"], div[data-testid="stCodeBlock"] > div {
        background-color: white !important;
        border: 2px solid black !important;
        border-radius: 8px !important;
    }

    /* Target the actual text inside the code block */
    code {
        color: black !important;
        background-color: white !important;
        font-family: inherit !important;
        font-weight: bold !important;
    }

    /* Remove the copy button background to keep it clean */
    button[title="Copy to clipboard"] {
        background-color: transparent !important;
    }
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
        st.write("---")
        st.write("### 📂 Load Data")
        file = st.file_uploader("Upload CSV", type="csv")
        if file:
            st.session_state.data = pd.read_csv(file)
            st.success("CSV Connected!")

    elif menu == "Dashboard":
        st.title("Dashboard 📊")
        if st.session_state.data is not None:
            # 1. Financial Metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Earned", "$15,200", "+8%")
            col2.metric("Total Spent", "$9,100", "-1%")
            col3.metric("Net Profit", "40.1%", "↑ 5%")
            
            st.write("---")
            
            # 2. Daily Profit/Loss Analysis
            st.subheader("Daily Profit/Loss Analysis (30 Days) 📉")
            days = list(range(1, 31))
            daily_vals = np.random.randint(-150, 600, size=30)
            df_daily = pd.DataFrame({"Day": days, "Profit/Loss ($)": daily_vals})
            st.plotly_chart(px.area(df_daily, x="Day", y="Profit/Loss ($)", color_discrete_sequence=['#4682B4']), use_container_width=True)
            
            st.write("---")
            
            # 3. Individual Product Sale Graph
            st.subheader("Individual Product Sales Velocity 📈")
            st.plotly_chart(px.bar(st.session_state.data, 
                                   x=st.session_state.data.columns[0], 
                                   y=st.session_state.data.columns[1], 
                                   labels={st.session_state.data.columns[0]: "Units Sold", st.session_state.data.columns[1]: "Product"},
                                   color_discrete_sequence=['#87CEFA']), use_container_width=True)
        else:
            st.warning("Please upload CSV on Home page to view dashboard analytics.")

    elif menu == "AI Studio":
        st.title("AI Studio 📢")
        
        # 1. Capture user inputs
        k1 = st.text_input("Vibe Keyword (e.g. Trendy)", key="vibe_input")
        k2 = st.text_input("Product Keyword (e.g. Coffee Beans)", key="prod_input")
        k3 = st.text_input("Benefit Keyword (e.g. Extra Caffeine)", key="benefit_input")
        
        if st.button("Generate My Custom Post"):
            if k1 and k2 and k3:
                try:
                    # Request to your FastAPI backend
                    url = f"http://127.0.0.1:8000/generate-marketing"
                    params = {"k1": k1, "k2": k2, "k3": k3}
                    response = requests.get(url, params=params)
                    
                    if response.status_code == 200:
                        res = response.json()
                        
                        # FIX: Dynamic Image based on your Product Keyword (k2)
                        # We use Unsplash Source to find an image matching k2 instead of the vegetable link
                        st.image(f"https://source.unsplash.com/featured/?{k2.replace(' ', '')}", caption=f"Suggested Visual for {k2}")
                        
                        st.write("### 📝 Your Custom Caption")
                        # Forces the black text style you like
                        st.info(res['caption'])
                        
                        st.write("### 🏷️ Smart Hashtags")
                        # This will use your CSS for the white block/black border
                        st.code(res['hashtags'])
                    else:
                        st.error("Backend Error: Check if main.py is running.")
                except Exception as e:
                    st.error(f"Connection failed: {e}")
            else:
                st.warning("Please enter all three keywords to generate your post!")

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