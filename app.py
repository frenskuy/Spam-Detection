# ----------------------------
# IMPORTS
# ----------------------------
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io

# ----------------------------
# PAGE CONFIG (harus di atas)
# ----------------------------
st.set_page_config(
    page_title="Twitter Spam Detection Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================
# INISIALISASI SESSION STATE
# ===============================
# Catatan: gunakan SATU sumber kebenaran untuk halaman: 'page_selection'
if 'page_selection' not in st.session_state:
    st.session_state.page_selection = "📊 Overview & Metrics"
if 'filter_type' not in st.session_state:
    st.session_state.filter_type = "All"

# ===============================
# CUSTOM CSS (Dark Theme Profesional)
# ===============================
st.markdown("""
<style>
    /* Import Professional Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    /* Root Variables */
    :root {
        --primary-dark: #0d1117;
        --secondary-dark: #161b22;
        --tertiary-dark: #21262d;
        --accent-blue: #1f6feb;
        --accent-purple: #7c3aed;
        --accent-green: #238636;
        --accent-red: #da3633;
        --accent-orange: #fd7e14;
        --text-primary: #f0f6fc;
        --text-secondary: #8b949e;
        --text-muted: #6e7681;
        --border-color: #30363d;
        --hover-bg: #262c36;
    }
    
    /* Global Background */
    .main > div {
        background: var(--primary-dark);
        color: var(--text-primary);
        padding: 1.5rem;
        font-family: 'Inter', sans-serif;
    }
    
    /* Streamlit Container Background Override */
    .block-container {
        background: var(--primary-dark);
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Main Header */
    .main-header {
        background: linear-gradient(135deg, var(--secondary-dark) 0%, var(--tertiary-dark) 100%);
        border: 1px solid var(--border-color);
        padding: 2.5rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple), var(--accent-blue));
    }
    
    .main-header h1 {
        color: var(--text-primary);
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 0.8rem;
        font-family: 'Inter', sans-serif;
        letter-spacing: -0.02em;
    }
    
    .main-header p {
        color: var(--text-secondary);
        font-size: 1.1rem;
        margin: 0.5rem 0;
        font-weight: 500;
    }
    
    /* Professional Metric Cards */
    .metric-card {
        background: var(--secondary-dark);
        border: 1px solid var(--border-color);
        padding: 2rem 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple));
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        background: var(--tertiary-dark);
        border-color: var(--accent-blue);
        box-shadow: 0 12px 40px rgba(31, 111, 235, 0.15);
    }
    
    .metric-card:hover::before {
        opacity: 1;
    }
    
    .metric-card h3 {
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 1rem;
        color: var(--text-secondary);
    }
    
    .metric-card h2 {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* Section Headers */
    .section-header {
        background: var(--secondary-dark);
        border: 1px solid var(--border-color);
        border-left: 4px solid var(--accent-blue);
        color: var(--text-primary);
        padding: 1.5rem 2rem;
        border-radius: 8px;
        margin: 2rem 0 1.5rem 0;
        position: relative;
    }
    
    .section-header h2 {
        margin: 0;
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
    }
    
    /* Navigation Buttons */
    .stButton > button {
        background: var(--secondary-dark) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        height: 2.5rem !important;
    }
    
    .stButton > button:hover {
        background: var(--accent-blue) !important;
        border-color: var(--accent-blue) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Status Boxes */
    .warning-box {
        background: var(--secondary-dark);
        border: 1px solid var(--accent-orange);
        border-left: 4px solid var(--accent-orange);
        color: var(--text-primary);
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .success-box {
        background: var(--secondary-dark);
        border: 1px solid var(--accent-green);
        border-left: 4px solid var(--accent-green);
        color: var(--text-primary);
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .info-box {
        background: var(--secondary-dark);
        border: 1px solid var(--accent-blue);
        border-left: 4px solid var(--accent-blue);
        color: var(--text-primary);
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Footer */
    .footer {
        background: var(--secondary-dark);
        border: 1px solid var(--border-color);
        color: var(--text-primary);
        text-align: center;
        padding: 2.5rem;
        border-radius: 10px;
        margin-top: 3rem;
        position: relative;
    }
    
    .footer::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--accent-blue), transparent);
    }
    
    /* Sidebar Dark Theme */
    .css-1d391kg {
        background: var(--secondary-dark) !important;
        border-right: 1px solid var(--border-color) !important;
    }
    
    .
