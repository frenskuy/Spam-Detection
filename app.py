import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ===============================
# PAGE CONFIG & CUSTOM CSS
# ===============================
st.set_page_config(
    page_title="Twitter Spam Detection Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Main background */
    .main > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #1f4037, #99f2c8);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        color: white;
        font-size: 3rem;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        font-family: 'Poppins', sans-serif;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        margin: 0;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Card styling */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        text-align: center;
        margin: 0.5rem;
        transition: transform 0.3s ease;
        font-family: 'Poppins', sans-serif;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    /* Section headers */
    .section-header {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 1.5rem 0 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        font-family: 'Poppins', sans-serif;
    }
    
    /* Warning boxes */
    .warning-box {
        background: linear-gradient(45deg, #ffa726, #ff7043);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        text-align: center;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Success boxes */
    .success-box {
        background: linear-gradient(45deg, #66bb6a, #4caf50);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Footer */
    .footer {
        background: linear-gradient(45deg, #2c3e50, #34495e);
        color: white;
        text-align: center;
        padding: 2rem;
        border-radius: 10px;
        margin-top: 3rem;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Sidebar Fixes - IMPORTANT! */
    .css-1d391kg, .css-1y4p8pa {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
    }
    
    /* Sidebar text color */
    .css-1d391kg .css-10trblm {
        color: white !important;
    }
    
    .css-1d391kg .css-1cpxqw2 {
        color: white !important;
    }
    
    /* Sidebar when collapsed */
    .css-1y4p8pa {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%) !important;
    }
    
    /* Sidebar toggle button */
    .css-vk3wp9 {
        background-color: rgba(255,255,255,0.1) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
    }
    
    .css-vk3wp9:hover {
        background-color: rgba(255,255,255,0.2) !important;
    }
    
    /* Sidebar content when expanded */
    .css-1d391kg .block-container {
        padding: 1rem !important;
    }
    
    /* Remove default streamlit styling */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Font family for all elements */
    .css-1d391kg, .css-1d391kg * {
        font-family: 'Poppins', sans-serif !important;
    }
    
    /* Sidebar responsive fix */
    @media (max-width: 768px) {
        .css-1d391kg {
            min-width: 250px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ===============================
# MAIN HEADER
# ===============================
st.markdown("""
<div class="main-header">
    <h1>🚀 Twitter Spam Detection Dashboard</h1>
    <p>Advanced Sentiment Analysis & Spam Detection using IBM Granite LLM</p>
    <p style="font-size: 1rem; opacity: 0.8;">Dataset Period: 1 Agustus 2025 – 26 Agustus 2025</p>
</div>
""", unsafe_allow_html=True)

# ===============================
# SIDEBAR + MAIN NAVIGATION
# ===============================
st.sidebar.markdown("## 🎯 Navigation")
page_selection = st.sidebar.selectbox(
    "Choose Analysis Section:",
    ["📊 Overview & Metrics", "📋 Detailed Data", "📈 Visualizations", "📝 Reports", "💡 Insights"]
)

# Fallback navigation di main area jika sidebar bermasalah
st.markdown("### 🧭 Quick Navigation")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("📊 Overview", use_container_width=True):
        page_selection = "📊 Overview & Metrics"
with col2:
    if st.button("📋 Data", use_container_width=True):
        page_selection = "📋 Detailed Data"
with col3:
    if st.button("📈 Charts", use_container_width=True):
        page_selection = "📈 Visualizations"
with col4:
    if st.button("📝 Report", use_container_width=True):
        page_selection = "📝 Reports"
with col5:
    if st.button("💡 Insights", use_container_width=True):
        page_selection = "💡 Insights"

st.markdown("---")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔧 Settings")
show_raw_data = st.sidebar.checkbox("Show Raw Data", value=False)
max_rows = st.sidebar.slider("Max Rows to Display", 10, 100, 20)

st.sidebar.markdown("---")
st.sidebar.markdown("""
### 📊 Quick Stats
- **Total Tweets**: Loading...
- **Spam Detected**: Loading...
- **Accuracy**: Loading...
""")

# ===============================
# LOAD DATA WITH ERROR HANDLING
# ===============================
@st.cache_data
def load_spam_data():
    try:
        df = pd.read_csv("Output/deteksi_spam_detail_20250828_070506.csv")
        return df, True
    except Exception as e:
        return None, False

@st.cache_data
def load_report():
    try:
        with open("Output/spam_detection_report_20250828_070511.md", "r", encoding="utf-8") as f:
            return f.read(), True
    except:
        return None, False

df_spam, data_loaded = load_spam_data()
report_content, report_loaded = load_report()

# ===============================
# PAGE CONTENT BASED ON SELECTION
# ===============================

if page_selection == "📊 Overview & Metrics":
    st.markdown('<div class="section-header"><h2>📊 Dashboard Overview</h2></div>', unsafe_allow_html=True)
    
    if data_loaded and df_spam is not None:
        # Create metrics with error handling
        col1, col2, col3, col4 = st.columns(4)
        
        try:
            total_tweets = len(df_spam)
            
            # Hitung spam & non-spam dari kolom spam_classification
            if 'spam_classification' in df_spam.columns:
                classification_counts = df_spam['spam_classification'].value_counts()
                spam_count = classification_counts.get('Spam', 0)
                non_spam_count = classification_counts.get('Not Spam', 0)
                spam_percentage = (spam_count / total_tweets * 100) if total_tweets > 0 else 0
            else:
                spam_count = 0
                non_spam_count = total_tweets
                spam_percentage = 0
                
        except Exception as e:
            st.error(f"Error calculating metrics: {str(e)}")
            total_tweets = spam_count = non_spam_count = spam_percentage = 0
        
        # Metrics cards
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #667eea;">📊 Total Tweets</h3>
                <h2 style="color: #2c3e50;">{total_tweets:,}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #ff6b6b;">🚫 Spam Detected</h3>
                <h2 style="color: #e74c3c;">{spam_count:,}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #4ecdc4;">✅ Non-Spam</h3>
                <h2 style="color: #27ae60;">{non_spam_count:,}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #ffa726;">📈 Spam Rate</h3>
                <h2 style="color: #f39c12;">{spam_percentage:.1f}%</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # Donut chart
        if 'spam_classification' in df_spam.columns:
            st.markdown("### 📊 Spam Distribution")
            classification_counts = df_spam['spam_classification'].value_counts()
            
            fig = go.Figure(data=[go.Pie(
                labels=classification_counts.index,
                values=classification_counts.values,
                hole=0.6,
                marker_colors=['#ff6b6b', '#4ecdc4'],
                textinfo='label+percent',
                textfont_size=14
            )])
            
            fig.update_layout(
                title="Spam vs Non-Spam Distribution",
                title_x=0.5,
                font=dict(size=16),
                showlegend=True,
                height=400,
                annotations=[dict(text='Total<br>' + str(total_tweets), 
                                  x=0.5, y=0.5, font_size=20, showarrow=False)]
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.markdown("""
        <div class="warning-box">
            ⚠️ Data files not found. Please ensure the following files exist:
            <br>• Output/deteksi_spam_detail_20250828_070506.csv
        </div>
        """, unsafe_allow_html=True)

elif page_selection == "📋 Detailed Data":
    st.markdown('<div class="section-header"><h2>📋 Detailed Spam Detection Results</h2></div>', unsafe_allow_html=True)
    
    if data_loaded and df_spam is not None:
        # Filter options hanya Spam/Not Spam
        if 'spam_classification' in df_spam.columns:
            filter_type = st.selectbox("Filter by Type:", ["Spam", "Not Spam"], index=0)
        else:
            filter_type = "All"
            st.info("ℹ️ spam_classification column not found. Showing all data.")
        
        # Apply filters
        filtered_df = df_spam.copy()
        try:
            if filter_type == "Spam" and 'spam_classification' in df_spam.columns:
                filtered_df = filtered_df[filtered_df['spam_classification'] == 'spam']
            elif filter_type == "Not Spam" and 'spam_classification' in df_spam.columns:
                filtered_df = filtered_df[filtered_df['spam_classification'] != 'spam']
        except Exception as e:
            st.error(f"Error applying filter: {str(e)}")
            filtered_df = df_spam.copy()
        
        # Tampilkan hanya kolom processed_text & spam_reason
        display_cols = ["processed_text", "spam_reason"]
        available_cols = [col for col in display_cols if col in filtered_df.columns]
        
        if not available_cols:
            st.warning("⚠️ Kolom processed_text / spam_reason tidak ditemukan dalam dataset.")
        else:
            try:
                st.dataframe(filtered_df[available_cols].head(max_rows), use_container_width=True)
            except Exception as e:
                st.error(f"Error displaying data: {str(e)}")
                st.dataframe(filtered_df.head(max_rows), use_container_width=True)
    
    else:
        st.markdown('<div class="warning-box">⚠️ Spam detection data not available</div>', unsafe_allow_html=True)

elif page_selection == "📈 Visualizations":
    st.markdown('<div class="section-header"><h2>📈 Advanced Visualizations</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ☁️ Wordcloud Analysis")
        try:
            st.image("Output/wordcloud_spam_analysis_20250828_070512.png", 
                    caption="Wordcloud: Spam vs Non-Spam Terms", 
                    use_container_width=True)
        except:
            st.markdown('<div class="warning-box">⚠️ Wordcloud image not found</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📊 Detailed Spam Analysis")
        try:
            st.image("Output/visualisasi_spam_detail_20250828_070506.png", 
                    caption="Comprehensive Spam Detection Analysis", 
                    use_container_width=True)
        except:
            st.markdown('<div class="warning-box">⚠️ Visualization image not found</div>', unsafe_allow_html=True)

elif page_selection == "📝 Reports":
    st.markdown('<div class="section-header"><h2>📝 Comprehensive Analysis Report</h2></div>', unsafe_allow_html=True)
    
    if report_loaded and report_content:
        st.markdown(report_content)
    else:
        st.markdown('<div class="warning-box">⚠️ Analysis report not available</div>', unsafe_allow_html=True)
    
    # Add download button for report
    if report_loaded and report_content:
        st.download_button(
            label="📥 Download Report (MD)",
            data=report_content,
            file_name="spam_detection_report.md",
            mime="text/markdown"
        )

elif page_selection == "💡 Insights":
    st.markdown('<div class="section-header"><h2>💡 Key Insights & Recommendations</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="success-box">
            <h3>✅ Key Findings</h3>
            <ul style="text-align: left; margin: 0;">
                <li>Spam detection shows high accuracy with IBM Granite LLM</li>
                <li>Spam tweets typically contain promotional content and short links</li>
                <li>Non-spam content shows more natural language patterns</li>
                <li>Clickbait patterns are strong indicators of spam content</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(45deg, #667eea, #764ba2); color: white; 
                   padding: 1.5rem; border-radius: 8px; margin: 1rem 0;">
            <h3>🚀 Future Enhancements</h3>
            <ul style="text-align: left; margin: 0;">
                <li>Implement real-time sentiment analysis</li>
                <li>Add temporal trend analysis</li>
                <li>Expand dataset for better representation</li>
                <li>Integrate advanced NLP techniques</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ===============================
# FOOTER
# ===============================
st.markdown("""
<div class="footer">
    <h3>🚀 Twitter Spam Detection System</h3>
    <p>Powered by IBM Granite LLM • Built with Streamlit • © 2025</p>
    <p style="font-size: 0.9rem; opacity: 0.8;">
        Advanced AI-driven spam detection and sentiment analysis platform
    </p>
</div>
""", unsafe_allow_html=True)
