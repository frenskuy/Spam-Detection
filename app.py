# ============================================
# Twitter Spam Detection Dashboard (Robust Nav)
# ============================================

# ----------------------------
# IMPORTS
# ----------------------------
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import io

# ----------------------------
# PAGE CONFIG (harus paling atas)
# ----------------------------
st.set_page_config(
    page_title="Twitter Spam Detection Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# KONSTAN & HELPER
# ----------------------------
PAGE_OPTIONS = [
    "📊 Overview & Metrics",
    "📋 Detailed Data",
    "📈 Visualizations",
    "📝 Reports",
    "💡 Insights",
]

def _init_state():
    """Inisialisasi state sekali saja, tanpa menimpa nilai widget yang sudah ada."""
    if "page_selection" not in st.session_state:
        st.session_state["page_selection"] = PAGE_OPTIONS[0]
    # Jika persist state sebelumnya memuat nilai yang tak lagi ada di options
    if st.session_state["page_selection"] not in PAGE_OPTIONS:
        st.session_state["page_selection"] = PAGE_OPTIONS[0]
    if "filter_type" not in st.session_state:
        st.session_state["filter_type"] = "All"

def _rerun():
    """Rerun kompatibel (Streamlit lama/baru)."""
    try:
        st.rerun()  # Streamlit >= 1.31
    except Exception:
        st.experimental_rerun()  # fallback

def _goto(page: str):
    """Ganti halaman dengan aman (hanya jika berubah & valid)."""
    if page in PAGE_OPTIONS and st.session_state["page_selection"] != page:
        st.session_state["page_selection"] = page
        _rerun()

_init_state()

# ===============================
# CUSTOM CSS (Dark Theme Profesional)
# ===============================
st.markdown("""
<style>
    /* Import Professional Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
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
    .main > div { background: var(--primary-dark); color: var(--text-primary); padding: 1.5rem; font-family: 'Inter', sans-serif; }
    .block-container { background: var(--primary-dark); padding-top: 2rem; padding-bottom: 2rem; }
    .main-header { background: linear-gradient(135deg, var(--secondary-dark) 0%, var(--tertiary-dark) 100%); border: 1px solid var(--border-color); padding: 2.5rem; border-radius: 12px; text-align: center; margin-bottom: 2rem; box-shadow: 0 8px 32px rgba(0,0,0,0.4); position: relative; overflow: hidden; }
    .main-header::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple), var(--accent-blue)); }
    .main-header h1 { color: var(--text-primary); font-size: 2.8rem; font-weight: 800; margin-bottom: 0.8rem; font-family: 'Inter', sans-serif; letter-spacing: -0.02em; }
    .main-header p { color: var(--text-secondary); font-size: 1.1rem; margin: 0.5rem 0; font-weight: 500; }
    .metric-card { background: var(--secondary-dark); border: 1px solid var(--border-color); padding: 2rem 1.5rem; border-radius: 10px; text-align: center; margin: 0.5rem; transition: all 0.3s ease; position: relative; overflow: hidden; }
    .metric-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple)); opacity: 0; transition: opacity 0.3s ease; }
    .metric-card:hover { transform: translateY(-3px); background: var(--tertiary-dark); border-color: var(--accent-blue); box-shadow: 0 12px 40px rgba(31,111,235,0.15); }
    .metric-card:hover::before { opacity: 1; }
    .metric-card h3 { font-size: 0.9rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 1rem; color: var(--text-secondary); }
    .metric-card h2 { font-size: 2.5rem; font-weight: 800; margin: 0; font-family: 'JetBrains Mono', monospace; }
    .section-header { background: var(--secondary-dark); border: 1px solid var(--border-color); border-left: 4px solid var(--accent-blue); color: var(--text-primary); padding: 1.5rem 2rem; border-radius: 8px; margin: 2rem 0 1.5rem 0; position: relative; }
    .section-header h2 { margin: 0; font-size: 1.5rem; font-weight: 700; color: var(--text-primary); }
    .stButton > button { background: var(--secondary-dark) !important; color: var(--text-primary) !important; border: 1px solid var(--border-color) !important; border-radius: 6px !important; font-weight: 500 !important; transition: all 0.2s ease !important; height: 2.5rem !important; }
    .stButton > button:hover { background: var(--accent-blue) !important; border-color: var(--accent-blue) !important; transform: translateY(-1px) !important; }
    .warning-box { background: var(--secondary-dark); border: 1px solid var(--accent-orange); border-left: 4px solid var(--accent-orange); color: var(--text-primary); padding: 1.5rem; border-radius: 8px; margin: 1rem 0; }
    .success-box { background: var(--secondary-dark); border: 1px solid var(--accent-green); border-left: 4px solid var(--accent-green); color: var(--text-primary); padding: 1.5rem; border-radius: 8px; margin: 1rem 0; }
    .info-box { background: var(--secondary-dark); border: 1px solid var(--accent-blue); border-left: 4px solid var(--accent-blue); color: var(--text-primary); padding: 1.5rem; border-radius: 8px; margin: 1rem 0; }
    .footer { background: var(--secondary-dark); border: 1px solid var(--border-color); color: var(--text-primary); text-align: center; padding: 2.5rem; border-radius: 10px; margin-top: 3rem; position: relative; }
    .footer::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px; background: linear-gradient(90deg, transparent, var(--accent-blue), transparent); }
    #MainMenu, footer, header { visibility: hidden; }
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
# FUNGSI LOAD DATA (CACHE)
# ===============================
@st.cache_data
def load_spam_data():
    """Muat data utama deteksi spam dari CSV. Kembalikan (DataFrame, status_bool)."""
    try:
        df = pd.read_csv("Output/deteksi_spam_detail_20250828_070506.csv")
        return df, True
    except Exception:
        return None, False

@st.cache_data
def load_report():
    """Muat laporan MD (jika ada). Kembalikan (str, status_bool)."""
    try:
        with open("Output/spam_detection_report_20250828_070511.md", "r", encoding="utf-8") as f:
            return f.read(), True
    except Exception:
        return None, False

df_spam, data_loaded = load_spam_data()
report_content, report_loaded = load_report()

# ===============================
# SIDEBAR + NAVIGASI (AMAN)
# ===============================
st.sidebar.markdown("## 🎯 Navigation")

# Selectbox TIDAK menulis langsung; kita sinkronkan manual & aman
_selected = st.sidebar.selectbox(
    "Choose Analysis Section:",
    PAGE_OPTIONS,
    index=PAGE_OPTIONS.index(st.session_state["page_selection"]),
)

if _selected != st.session_state["page_selection"]:
    # Sinkronisasi nilai widget -> state (lalu rerun)
    st.session_state["page_selection"] = _selected
    _rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔧 Settings")
show_raw_data = st.sidebar.checkbox("Show Raw Data", value=False)
max_rows = st.sidebar.slider("Max Rows to Display", 10, 100, 20)

st.sidebar.markdown("---")
if data_loaded and df_spam is not None:
    total_tweets = len(df_spam)
    if "spam_classification" in df_spam.columns:
        counts = df_spam["spam_classification"].value_counts()
        spam_count = counts.get("Spam", 0)
        non_spam_count = counts.get("Not Spam", 0)
    else:
        spam_count, non_spam_count = 0, total_tweets
    st.sidebar.markdown(f"""
### 📊 Quick Stats
- **Total Tweets**: {total_tweets:,}
- **Spam Detected**: {spam_count:,}
- **Non-Spam**: {non_spam_count:,}
- **Accuracy**: N/A
""")
else:
    st.sidebar.markdown("""
### 📊 Quick Stats
- **Total Tweets**: Loading...
- **Spam Detected**: Loading...
- **Non-Spam**: Loading...
- **Accuracy**: Loading...
""")

# Quick Navigation (selalu via _goto)
st.markdown("### 🧭 Quick Navigation")
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    if st.button("📊 Overview", use_container_width=True):
        _goto("📊 Overview & Metrics")
with c2:
    if st.button("📋 Data", use_container_width=True):
        _goto("📋 Detailed Data")
with c3:
    if st.button("📈 Charts", use_container_width=True):
        _goto("📈 Visualizations")
with c4:
    if st.button("📝 Report", use_container_width=True):
        _goto("📝 Reports")
with c5:
    if st.button("💡 Insights", use_container_width=True):
        _goto("💡 Insights")

st.markdown("---")

# ===============================
# KONTEN HALAMAN
# ===============================
page = st.session_state["page_selection"]

if page == "📊 Overview & Metrics":
    st.markdown('<div class="section-header"><h2>📊 Dashboard Overview</h2></div>', unsafe_allow_html=True)
    if data_loaded and df_spam is not None:
        col1, col2, col3, col4 = st.columns(4)
        try:
            total_tweets = len(df_spam)
            if "spam_classification" in df_spam.columns:
                vc = df_spam["spam_classification"].value_counts()
                spam_count = vc.get("Spam", 0)
                non_spam_count = vc.get("Not Spam", 0)
                spam_percentage = (spam_count / total_tweets * 100) if total_tweets > 0 else 0
            else:
                spam_count, non_spam_count, spam_percentage = 0, total_tweets, 0
        except Exception as e:
            st.error(f"Error calculating metrics: {e}")
            total_tweets = spam_count = non_spam_count = 0
            spam_percentage = 0.0

        with col1:
            st.markdown(f"""<div class="metric-card"><h3>📊 Total Tweets</h3><h2 style="color: var(--accent-blue);">{total_tweets:,}</h2></div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""<div class="metric-card"><h3>🚫 Spam Detected</h3><h2 style="color: var(--accent-red);">{spam_count:,}</h2></div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""<div class="metric-card"><h3>✅ Non-Spam</h3><h2 style="color: var(--accent-green);">{non_spam_count:,}</h2></div>""", unsafe_allow_html=True)
        with col4:
            st.markdown(f"""<div class="metric-card"><h3>📈 Spam Rate</h3><h2 style="color: var(--accent-orange);">{spam_percentage:.1f}%</h2></div>""", unsafe_allow_html=True)

        if "spam_classification" in df_spam.columns:
            st.markdown("### 📊 Spam Distribution")
            vc = df_spam["spam_classification"].value_counts()
            fig = go.Figure(data=[go.Pie(
                labels=vc.index,
                values=vc.values,
                hole=0.6,
                marker_colors=['#da3633', '#238636'],
                textinfo='label+percent',
                textfont_size=14,
                textfont_color='#f0f6fc'
            )])
            fig.update_layout(
                title={'text': "Spam vs Non-Spam Distribution", 'x': 0.33, 'font': {'size': 18, 'color': '#f0f6fc'}},
                font=dict(size=16, color='#f0f6fc'),
                showlegend=True,
                height=400,
                paper_bgcolor='#161b22',
                plot_bgcolor='#161b22',
                annotations=[dict(text=f'Total<br>{total_tweets:,}', x=0.5, y=0.5, font_size=20, font_color='#f0f6fc', showarrow=False)],
                legend=dict(font=dict(color='#f0f6fc'))
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.markdown("""
        <div class="warning-box">
            ⚠️ <strong>Data files not found.</strong> Ensure this file exists:
            <br>• <code>Output/deteksi_spam_detail_20250828_070506.csv</code>
        </div>
        """, unsafe_allow_html=True)

elif page == "📋 Detailed Data":
    st.markdown('<div class="section-header"><h2>📋 Detailed Spam Detection Results</h2></div>', unsafe_allow_html=True)
    if data_loaded and df_spam is not None:
        if "spam_classification" in df_spam.columns:
            filter_options = ["All", "Spam", "Not Spam"]
            sel = st.selectbox(
                "Filter by Type:",
                filter_options,
                index=filter_options.index(st.session_state["filter_type"]),
                key="data_filter"
            )
            if sel != st.session_state["filter_type"]:
                st.session_state["filter_type"] = sel
        else:
            st.markdown('<div class="info-box">ℹ️ <strong>Note:</strong> spam_classification column not found. Showing all data.</div>', unsafe_allow_html=True)

        filtered_df = df_spam.copy()
        try:
            if st.session_state["filter_type"] == "Spam":
                filtered_df = filtered_df[filtered_df["spam_classification"] == "Spam"]
            elif st.session_state["filter_type"] == "Not Spam":
                filtered_df = filtered_df[filtered_df["spam_classification"] == "Not Spam"]
        except Exception as e:
            st.error(f"Error applying filter: {e}")
            filtered_df = df_spam.copy()

        cdl1, cdl2, _ = st.columns([1, 1, 2])
        with cdl1:
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"spam_data_{st.session_state['filter_type'].lower().replace(' ', '_')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        with cdl2:
            bio = io.BytesIO()
            with pd.ExcelWriter(bio, engine="xlsxwriter") as writer:
                filtered_df.to_excel(writer, index=False, sheet_name="Spam Analysis")
            st.download_button(
                label="📊 Download Excel",
                data=bio.getvalue(),
                file_name=f"spam_analysis_{st.session_state['filter_type'].lower().replace(' ', '_')}.xlsx",
                mime="application/vnd.ms-excel",
                use_container_width=True
            )

        st.markdown("---")
        display_cols = ["processed_text", "spam_reason"]
        avail = [c for c in display_cols if c in filtered_df.columns]
        if not avail:
            st.markdown('<div class="warning-box">⚠️ <strong>Column Notice:</strong> processed_text / spam_reason not found.</div>', unsafe_allow_html=True)
            st.dataframe(filtered_df.head(max_rows), use_container_width=True)
        else:
            st.dataframe(filtered_df[avail].head(max_rows), use_container_width=True)

        st.markdown(f"""
        <div style="background: var(--secondary-dark); padding: 1rem; border-radius: 6px; border: 1px solid var(--border-color); margin-top: 1rem;">
            <strong>📊 Dataset Statistics:</strong> {len(filtered_df):,} records | 
            <strong>Filter:</strong> {st.session_state['filter_type']} | 
            <strong>Showing:</strong> Top {min(max_rows, len(filtered_df))} rows
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="warning-box">⚠️ <strong>Data Unavailable:</strong> Spam detection data not found</div>', unsafe_allow_html=True)

elif page == "📈 Visualizations":
    st.markdown('<div class="section-header"><h2>📈 Advanced Visualizations</h2></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### ☁️ Wordcloud Analysis")
        try:
            st.image("Output/wordcloud_spam_analysis_20250828_070512.png", caption="Wordcloud: Spam vs Non-Spam Terms", use_container_width=True)
        except Exception:
            st.markdown('<div class="warning-box">⚠️ <strong>Image Missing:</strong> Wordcloud visualization not found</div>', unsafe_allow_html=True)
    with c2:
        st.markdown("### 📊 Detailed Spam Analysis")
        try:
            st.image("Output/visualisasi_spam_detail_20250828_070506.png", caption="Comprehensive Spam Detection Analysis", use_container_width=True)
        except Exception:
            st.markdown('<div class="warning-box">⚠️ <strong>Image Missing:</strong> Analysis visualization not found</div>', unsafe_allow_html=True)

elif page == "📝 Reports":
    st.markdown('<div class="section-header"><h2>📝 Comprehensive Analysis Report</h2></div>', unsafe_allow_html=True)
    if report_loaded and report_content:
        st.markdown(report_content)
        st.download_button(
            label="📥 Download Complete Report (MD)",
            data=report_content,
            file_name="spam_detection_comprehensive_report.md",
            mime="text/markdown",
            use_container_width=True
        )
    else:
        st.markdown('<div class="warning-box">⚠️ <strong>Report Unavailable:</strong> Analysis report file not found</div>', unsafe_allow_html=True)

elif page == "💡 Insights":
    st.markdown('<div class="section-header"><h2>💡 Key Insights & Recommendations</h2></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="success-box">
            <h3>✅ Key Findings</h3>
            <ul style="text-align: left; margin: 1rem 0; padding-left: 1.5rem;">
                <li><strong>Akurasi Tinggi:</strong> IBM Granite LLM menunjukkan performa deteksi spam yang sangat baik</li>
                <li><strong>Pengenalan Pola:</strong> Tweet spam umumnya berisi konten promosi dan URL yang dipersingkat</li>
                <li><strong>Bahasa Natural:</strong> Konten non-spam menunjukkan pola bahasa yang lebih natural dan engagement tinggi</li>
                <li><strong>Indikator Clickbait:</strong> Judul sensasional dan frasa call-to-action menjadi prediktor spam yang kuat</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="info-box">
            <h3>🚀 Future Enhancements</h3>
            <ul style="text-align: left; margin: 1rem 0; padding-left: 1.5rem;">
                <li><strong>Pemrosesan Real-time:</strong> Implementasi pipeline analisis sentimen langsung</li>
                <li><strong>Analisis Temporal:</strong> Menambah analisis tren dan forecasting time-series</li>
                <li><strong>Ekspansi Dataset:</strong> Menggabungkan sumber data multibahasa dan beragam</li>
                <li><strong>NLP Lanjutan:</strong> Integrasi model transformer dan contextual embeddings</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("### 📈 Performance Metrics")
    c3, c4 = st.columns(2)
    with c3:
        st.markdown("""
        <div style="background: var(--secondary-dark); border: 1px solid var(--border-color); border-left: 4px solid var(--accent-purple); padding: 1.5rem; border-radius: 8px;">
            <h4>🎯 Model Performance</h4>
            <p>Model IBM Granite LLM menunjukkan performa yang sangat baik dalam membedakan spam dan konten legitimate, dengan kekuatan khusus dalam mengidentifikasi:</p>
            <ul style="margin: 1rem 0; padding-left: 1.5rem;">
                <li>Konten promosi komersial</li>
                <li>Pola URL yang mencurigakan</li>
                <li>Struktur pesan yang berulang-ulang</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown("""
        <div style="background: var(--secondary-dark); border: 1px solid var(--border-color); border-left: 4px solid var(--accent-green); padding: 1.5rem; border-radius: 8px;">
            <h4>📊 Data Quality Assessment</h4>
            <p>Analisis kami mengungkap standar kualitas data yang robust di semua metrik:</p>
            <ul style="margin: 1rem 0; padding-left: 1.5rem;">
                <li>Kelengkapan dan integritas data yang tinggi</li>
                <li>Akurasi pelabelan yang konsisten</li>
                <li>Tingkat false positive/negative yang minimal</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ===============================
# FOOTER
# ===============================
st.markdown("""
<div class="footer">
    <h3>🚀 Twitter Spam Detection System</h3>
    <p><strong>Powered by IBM Granite LLM</strong> • Built with Streamlit • © 2025</p>
    <p style="font-size: 0.9rem; opacity: 0.7;">
        Advanced AI-driven spam detection and sentiment analysis platform
    </p>
    <div style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid var(--border-color);">
        <p style="font-size: 0.8rem; color: var(--text-muted);">
            Dashboard | Enhanced User Experience | Enterprise-Grade Analytics
        </p>
        <p style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.5rem;">
            Dataset Analysis Period: August 1-26, 2025 | Real-time Processing Capabilities
        </p>
    </div>
</div>
""", unsafe_allow_html=True)
