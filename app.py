import streamlit as st
import joblib
import re
import time
from datetime import datetime
import pandas as pd

# =========================================================
# 1. PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="SecuLink Model",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# 2. CUSTOM CSS - MODERN & PROFESSIONAL
# =========================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    
    .stApp {
        background: transparent;
    }
    
    /* Main Card Container */
    .main-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 3rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        margin: 2rem auto;
        max-width: 1200px;
    }
    
    /* Header Styling */
    h1 {
        font-size: 3rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem !important;
    }
    
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Author Card */
    .author-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .author-name {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }
    
    .author-title {
        font-size: 1rem;
        opacity: 0.9;
    }
    
    /* Button Styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        padding: 1rem 2rem;
        border-radius: 12px;
        border: none;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 30px rgba(102, 126, 234, 0.5);
    }
    
    /* Input Field */
    .stTextInput>div>div>input {
        border-radius: 12px;
        border: 2px solid #e0e0e0;
        padding: 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Result Cards */
    .result-safe {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 1rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(17, 153, 142, 0.3);
    }
    
    .result-danger {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        color: white;
        padding: 1rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(235, 51, 73, 0.3);
    }
    
    .result-warning {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(240, 147, 251, 0.3);
    }
    
    .result-icon {
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    
    .result-title {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .result-desc {
        font-size: 1.1rem;
        opacity: 0.95;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 1rem;
        font-weight: 600;
        color: #666;
    }
    
    [data-testid="metric-container"] {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
        border: 2px solid #f0f0f0;
        transition: all 0.3s ease;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
        border-color: #667eea;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #f8f9fa;
        border-radius: 10px;
        font-weight: 600;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
    }
    
    /* Feature Cards */
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
        border-left: 4px solid #667eea;
    }
    
    .feature-title {
        font-weight: 600;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: white;
        margin-top: 3rem;
    }
    
    /* Chart Styling */
    .stPlotlyChart {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. LOAD MODEL
# =========================================================
@st.cache_resource
def load_model():
    try:
        return joblib.load("url_security_model.pkl")
    except FileNotFoundError:
        st.error("⚠️ Model file not found! Ensure 'url_security_model.pkl' exists.")
        st.stop()

model = load_model()

# =========================================================
# 4. URL NORMALIZATION
# =========================================================
def clean_url(url):
    url = str(url).lower()
    url = re.sub(r"https?://", "", url)
    url = re.sub(r"www\.", "", url)
    url = url.split("/")[0]
    return url

# =========================================================
# 5. THREAT INFO
# =========================================================
def get_threat_info(pred):
    info = {
        "benign": {
            "icon": "✅",
            "title": "SAFE URL",
            "color": "success",
            "desc": "This URL is safe to visit. No threats detected.",
            "class": "result-safe"
        },
        "phishing": {
            "icon": "🎣",
            "title": "PHISHING DETECTED",
            "color": "error",
            "desc": "This URL may attempt to steal your personal information or credentials.",
            "class": "result-danger"
        },
        "malware": {
            "icon": "☠️",
            "title": "MALWARE THREAT",
            "color": "error",
            "desc": "This URL may contain harmful software that could damage your device.",
            "class": "result-danger"
        },
        "defacement": {
            "icon": "🔓",
            "title": "DEFACEMENT WARNING",
            "color": "warning",
            "desc": "This website may have been compromised by attackers.",
            "class": "result-warning"
        }
    }
    return info.get(pred, {
        "icon": "❓",
        "title": pred.upper(),
        "color": "warning",
        "desc": "Suspicious URL detected. Proceed with caution.",
        "class": "result-warning"
    })

# =========================================================
# 6. SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("""
    <div class='author-card'>
        <div class='author-name'>Ali Derouiche</div>
        <div class='author-title'>🛡️ Cybersecurity Engineering Student</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🎯 About This Tool")
    st.markdown("""
    <div class='feature-card'>
        <div class='feature-title'>🤖 AI-Powered Detection</div>
        Advanced machine learning algorithms analyze URLs for potential threats.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='feature-card'>
        <div class='feature-title'>⚡ Real-Time Analysis</div>
        Instant results with detailed probability distributions.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='feature-card'>
        <div class='feature-title'>🔍 Multiple Threat Types</div>
        Detects phishing, malware, defacement, and more.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📊 Statistics")
    st.info(f"🕒 Current Time: {datetime.now().strftime('%H:%M:%S')}")
    st.success("✅ Model Status: Active")

# =========================================================
# 7. MAIN CONTENT
# =========================================================
st.title("🔐 SecuLink Model (URL Security Checker)")
st.markdown("<p class='subtitle'>Protect yourself from phishing, malware, and compromised websites with AI-powered analysis</p>", unsafe_allow_html=True)

# Input Section
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    url_input = st.text_input(
        "Enter URL to scan",
        placeholder="https://example.com",
        label_visibility="collapsed"
    )
    analyze_button = st.button("🔍 Analyze URL", use_container_width=True)

# Analysis Section
if analyze_button:
    if not url_input.strip():
        st.warning("⚠️ Please enter a valid URL to analyze.")
    else:
        url_clean = clean_url(url_input)
        
        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)
            status_text.text(f"Analyzing... {i+1}%")
        
        status_text.empty()
        progress_bar.empty()

        try:
            pred = model.predict([url_clean])[0]
            probs = model.predict_proba([url_clean])[0]
            confidence = max(probs) * 100
            threat = get_threat_info(pred)

            # Result Display
            st.markdown(f"""
            <div class='{threat['class']}'>
                <div class='result-icon'>{threat['icon']}</div>
                <div class='result-title'>{threat['title']}</div>
                <div class='result-desc'>{threat['desc']}</div>
            </div>
            """, unsafe_allow_html=True)

            # Metrics
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3, gap="large")
            with col1:
                st.metric("🎯 Prediction", pred.upper())
            with col2:
                st.metric("📊 Confidence", f"{confidence:.1f}%")
            with col3:
                st.metric("⏱️ Analysis Time", "< 1s")
            st.markdown("<br>", unsafe_allow_html=True)

            # Probability Distribution
            st.markdown("### 📈 Threat Probability Distribution")
            df_probs = pd.DataFrame({
                "Category": model.classes_,
                "Confidence (%)": probs * 100
            }).sort_values("Confidence (%)", ascending=False)
            
            st.bar_chart(df_probs.set_index("Category"), use_container_width=True)

            # Detailed Information
            with st.expander("🔎 Detailed Analysis Report"):
                st.markdown(f"""
                **Original URL:** `{url_input}`  
                **Normalized URL:** `{url_clean}`  
                **Threat Classification:** `{pred.upper()}`  
                **Confidence Level:** `{confidence:.2f}%`  
                **Analysis Timestamp:** `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`  
                **Model Version:** `v1.0`
                
                ---
                
                **Probability Breakdown:**
                """)
                for cat, prob in zip(model.classes_, probs):
                    st.write(f"- **{cat.upper()}:** {prob*100:.2f}%")

        except Exception as e:
            st.error(f"❌ Error during analysis: {e}")
            st.info("Please ensure the model file is properly loaded and the URL format is correct.")

# Footer
st.markdown("---")
st.markdown("""
<div class='footer'>
    <p>🛡️ Developed by <strong>Ali Derouiche</strong> | Cybersecurity Engineering Student</p>
    <p>© 2026 SecuLink | All Rights Reserved</p>
</div>

""", unsafe_allow_html=True)

