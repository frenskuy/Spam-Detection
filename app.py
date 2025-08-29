import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io

# ===============================
# INITIALIZE SESSION STATE
# ===============================
if 'page_selection' not in st.session_state:
    st.session_state.page_selection = "📊 Overview & Metrics"
if 'filter_type' not in st.session_state:
    st.session_state.filter_type = "All"

# ===============================
# PAGE CONFIG & CUSTOM CSS
# ===============================
st.set_page_config(
    page_title="Twitter Spam Detection Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Dark Theme CSS
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
    
    /* Stremlit Container Background Override */
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
    
    .css-1y4p8pa {
        background: var(--secondary-dark) !important;
    }
    
    /* Sidebar Text Colors */
    .css-1d391kg .css-10trblm,
    .css-1d391kg .css-1cpxqw2,
    .css-1d391kg label,
    .css-1d391kg p,
    .css-1d391kg span {
        color: var(--text-primary) !important;
    }
    
    .css-1d391kg h2,
    .css-1d391kg h3 {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }
    
    /* Sidebar Controls */
    .css-1d391kg .stSelectbox > div > div {
        background: var(--tertiary-dark) !important;
        border-color: var(--border-color) !important;
        color: var(--text-primary) !important;
    }
    
    .css-1d391kg .stCheckbox > label {
        color: var(--text-primary) !important;
    }
    
    /* Sidebar Toggle Button */
    .css-vk3wp9 {
        background-color: var(--tertiary-dark) !important;
        border: 1px solid var(--border-color) !important;
    }
    
    .css-vk3wp9:hover {
        background-color: var(--hover-bg) !important;
    }
    
    /* Dataframe Styling */
    .stDataFrame {
        background: var(--secondary-dark) !important;
    }
    
    .stDataFrame [data-testid="stDataFrameResizeHandle"] {
        background: var(--border-color) !important;
    }
    
    /* Download Buttons */
    .stDownloadButton > button {
        background: var(--accent-blue) !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    
    .stDownloadButton > button:hover {
        background: var(--accent-purple) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Plotly Chart Dark Theme */
    .js-plotly-plot {
        background: var(--secondary-dark) !important;
        border-radius: 8px !important;
        border: 1px solid var(--border-color) !important;
    }
    
    /* Remove Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Markdown Content */
    .stMarkdown {
        color: var(--text-primary) !important;
    }
    
    /* Typography Improvements */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    p, span, div {
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Code blocks */
    code {
        background: var(--tertiary-dark) !important;
        color: var(--accent-blue) !important;
        padding: 0.2em 0.4em !important;
        border-radius: 3px !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .metric-card h2 {
            font-size: 2rem;
        }
        
        .css-1d391kg {
            min-width: 250px !important;
        }
    }
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--primary-dark);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border-color);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent-blue);
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
    <p style="font-size: 1rem; opacity: 0.7;">Dataset Period: 1 Agustus 2025 – 26 Agustus 2025</p>
</div>
""", unsafe_allow_html=True)

# ===============================
# SIDEBAR + MAIN NAVIGATION
# ===============================
st.sidebar.markdown("## 🎯 Navigation")

# Gunakan session state untuk page selection
page_options = ["📊 Overview & Metrics", "📋 Detailed Data", "📈 Visualizations", "📝 Reports", "💡 Insights"]
selected_page = st.sidebar.selectbox(
    "Choose Analysis Section:",
    page_options,
    index=page_options.index(st.session_state.page_selection),
    key="sidebar_page_selector"
)

# Update session state ketika ada perubahan
if selected_page != st.session_state.page_selection:
    st.session_state.page_selection = selected_page

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

# Professional navigation buttons
st.markdown("### 🧭 Quick Navigation")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("📊 Overview", use_container_width=True):
        st.session_state.page_selection = "📊 Overview & Metrics"
        st.rerun()
with col2:
    if st.button("📋 Data", use_container_width=True):
        st.session_state.page_selection = "📋 Detailed Data"
        st.rerun()
with col3:
    if st.button("📈 Charts", use_container_width=True):
        st.session_state.page_selection = "📈 Visualizations"
        st.rerun()
with col4:
    if st.button("📝 Report", use_container_width=True):
        st.session_state.page_selection = "📝 Reports"
        st.rerun()
with col5:
    if st.button("💡 Insights", use_container_width=True):
        st.session_state.page_selection = "💡 Insights"
        st.rerun()

st.markdown("---")

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

if st.session_state.page_selection == "📊 Overview & Metrics":
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
        
        # Professional metrics cards
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>📊 Total Tweets</h3>
                <h2 style="color: var(--accent-blue);">{total_tweets:,}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>🚫 Spam Detected</h3>
                <h2 style="color: var(--accent-red);">{spam_count:,}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>✅ Non-Spam</h3>
                <h2 style="color: var(--accent-green);">{non_spam_count:,}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h3>📈 Spam Rate</h3>
                <h2 style="color: var(--accent-orange);">{spam_percentage:.1f}%</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # Professional donut chart with dark theme
        if 'spam_classification' in df_spam.columns:
            st.markdown("### 📊 Spam Distribution")
            classification_counts = df_spam['spam_classification'].value_counts()
            
            fig = go.Figure(data=[go.Pie(
                labels=classification_counts.index,
                values=classification_counts.values,
                hole=0.6,
                marker_colors=['#da3633', '#238636'],
                textinfo='label+percent',
                textfont_size=14,
                textfont_color='#f0f6fc'
            )])
            
            fig.update_layout(
                title={
                    'text': "Spam vs Non-Spam Distribution",
                    'x': 0.5,
                    'font': {'size': 18, 'color': '#f0f6fc'}
                },
                font=dict(size=16, color='#f0f6fc'),
                showlegend=True,
                height=400,
                paper_bgcolor='#161b22',
                plot_bgcolor='#161b22',
                annotations=[dict(
                    text=f'Total<br>{total_tweets:,}', 
                    x=0.5, y=0.5, 
                    font_size=20, 
                    font_color='#f0f6fc',
                    showarrow=False
                )],
                legend=dict(
                    font=dict(color='#f0f6fc')
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.markdown("""
        <div class="warning-box">
            ⚠️ <strong>Data files not found.</strong> Please ensure the following files exist:
            <br>• <code>Output/deteksi_spam_detail_20250828_070506.csv</code>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.page_selection == "📋 Detailed Data":
    st.markdown('<div class="section-header"><h2>📋 Detailed Spam Detection Results</h2></div>', unsafe_allow_html=True)
    
    if data_loaded and df_spam is not None:
        # Filter options hanya jika ada kolom spam_classification
        if 'spam_classification' in df_spam.columns:
            filter_options = ["All", "Spam", "Not Spam"]
            selected_filter = st.selectbox(
                "Filter by Type:",
                filter_options,
                index=filter_options.index(st.session_state.filter_type),
                key="data_filter"
            )
            
            # Update session state untuk filter
            if selected_filter != st.session_state.filter_type:
                st.session_state.filter_type = selected_filter
        else:
            selected_filter = "All"
            st.markdown("""
            <div class="info-box">
                ℹ️ <strong>Note:</strong> spam_classification column not found. Showing all data.
            </div>
            """, unsafe_allow_html=True)
        
        # Copy data
        filtered_df = df_spam.copy()
        try:
            if st.session_state.filter_type == "Spam":
                filtered_df = filtered_df[filtered_df['spam_classification'] == 'Spam']
            elif st.session_state.filter_type == "Not Spam":
                filtered_df = filtered_df[filtered_df['spam_classification'] == 'Not Spam']
        except Exception as e:
            st.error(f"Error applying filter: {str(e)}")
            filtered_df = df_spam.copy()
        
        # Professional download buttons
        col_dl1, col_dl2, col_dl3 = st.columns([1, 1, 2])
        
        with col_dl1:
            # Download CSV
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"spam_data_{st.session_state.filter_type.lower().replace(' ', '_')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col_dl2:
            # Download Excel
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                filtered_df.to_excel(writer, index=False, sheet_name='Spam Analysis')
            excel_data = output.getvalue()
            
            st.download_button(
                label="📊 Download Excel",
                data=excel_data,
                file_name=f"spam_analysis_{st.session_state.filter_type.lower().replace(' ', '_')}.xlsx",
                mime="application/vnd.ms-excel",
                use_container_width=True
            )
        
        st.markdown("---")
        
        # Display data with professional styling
        display_cols = ["processed_text", "spam_reason"]
        available_cols = [col for col in display_cols if col in filtered_df.columns]
        
        if not available_cols:
            st.markdown("""
            <div class="warning-box">
                ⚠️ <strong>Column Notice:</strong> processed_text / spam_reason columns not found in dataset.
            </div>
            """, unsafe_allow_html=True)
            st.dataframe(filtered_df.head(max_rows), use_container_width=True)
        else:
            try:
                st.dataframe(filtered_df[available_cols].head(max_rows), use_container_width=True)
            except Exception as e:
                st.error(f"Error displaying data: {str(e)}")
                st.dataframe(filtered_df.head(max_rows), use_container_width=True)
        
        # Statistics display
        st.markdown(f"""
        <div style="background: var(--secondary-dark); padding: 1rem; border-radius: 6px; border: 1px solid var(--border-color); margin-top: 1rem;">
            <strong>📊 Dataset Statistics:</strong> {len(filtered_df):,} records | 
            <strong>Filter:</strong> {st.session_state.filter_type} | 
            <strong>Showing:</strong> Top {min(max_rows, len(filtered_df))} rows
        </div>
        """, unsafe_allow_html=True)
    
    else:
        st.markdown('<div class="warning-box">⚠️ <strong>Data Unavailable:</strong> Spam detection data not found</div>', unsafe_allow_html=True)

elif st.session_state.page_selection == "📈 Visualizations":
    st.markdown('<div class="section-header"><h2>📈 Advanced Visualizations</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ☁️ Wordcloud Analysis")
        try:
            st.image("Output/wordcloud_spam_analysis_20250828_070512.png", 
                    caption="Wordcloud: Spam vs Non-Spam Terms", 
                    use_container_width=True)
        except:
            st.markdown('<div class="warning-box">⚠️ <strong>Image Missing:</strong> Wordcloud visualization not found</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📊 Detailed Spam Analysis")
        try:
            st.image("Output/visualisasi_spam_detail_20250828_070506.png", 
                    caption="Comprehensive Spam Detection Analysis", 
                    use_container_width=True)
        except:
            st.markdown('<div class="warning-box">⚠️ <strong>Image Missing:</strong> Analysis visualization not found</div>', unsafe_allow_html=True)

elif st.session_state.page_selection == "📝 Reports":
    st.markdown('<div class="section-header"><h2>📝 Comprehensive Analysis Report</h2></div>', unsafe_allow_html=True)
    
    if report_loaded and report_content:
        st.markdown(report_content)
        
        # Professional download button
        st.download_button(
            label="📥 Download Complete Report (MD)",
            data=report_content,
            file_name="spam_detection_comprehensive_report.md",
            mime="text/markdown",
            use_container_width=True
        )
    else:
        st.markdown('<div class="warning-box">⚠️ <strong>Report Unavailable:</strong> Analysis report file not found</div>', unsafe_allow_html=True)

elif st.session_state.page_selection == "💡 Insights":
    st.markdown('<div class="section-header"><h2>💡 Key Insights & Recommendations</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="success-box">
            <h3>✅ Key Findings</h3>
            <ul style="text-align: left; margin: 1rem 0; padding-left: 1.5rem;">
                <li><strong>High Accuracy:</strong> IBM Granite LLM demonstrates exceptional spam detection performance</li>
                <li><strong>Pattern Recognition:</strong> Spam tweets typically contain promotional content and shortened URLs</li>
                <li><strong>Natural Language:</strong> Non-spam content exhibits more natural language patterns and engagement</li>
                <li><strong>Clickbait Indicators:</strong> Sensational headlines and call-to-action phrases are strong spam predictors</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <h3>🚀 Future Enhancements</h3>
            <ul style="text-align: left; margin: 1rem 0; padding-left: 1.5rem;">
                <li><strong>Real-time Processing:</strong> Implement live sentiment analysis pipeline</li>
                <li><strong>Temporal Analysis:</strong> Add trend analysis and time-series forecasting</li>
                <li><strong>Dataset Expansion:</strong> Incorporate multilingual and diverse data sources</li>
                <li><strong>Advanced NLP:</strong> Integrate transformer models and contextual embeddings</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Additional insights section
    st.markdown("### 📈 Performance Metrics")
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("""
        <div style="background: var(--secondary-dark); border: 1px solid var(--border-color); border-left: 4px solid var(--accent-purple); padding: 1.5rem; border-radius: 8px;">
            <h4>🎯 Model Performance</h4>
            <p>The IBM Granite LLM model shows excellent performance in distinguishing between spam and legitimate content, with particular strength in identifying:</p>
            <ul style="margin: 1rem 0; padding-left: 1.5rem;">
                <li>Commercial promotional content</li>
                <li>Suspicious URL patterns</li>
                <li>Repetitive messaging structures</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with

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
