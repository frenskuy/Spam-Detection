import streamlit as st
import pandas as pd

# Judul
st.title("🚀 Capstone Project – Analisis Sentimen & Deteksi Spam Twitter")
st.markdown("""
Proyek ini berfokus pada **Data Classification & Summarization** menggunakan **IBM Granite LLM**.  
Dataset: Twitter 1 Agustus 2025 – 26 Agustus 2025.
""")

# ===============================
# Bagian 1: Output CSV
# ===============================
st.header("📊 Hasil Deteksi Spam (CSV)")

try:
    df_deteksi = pd.read_csv("Output/deteksi_spam_detail_20250828_070506.csv")
    st.dataframe(df_deteksi.head(20))  # tampilkan 20 baris pertama
except Exception as e:
    st.warning("⚠️ File deteksi_spam_detail_20250828_070506.csv tidak ditemukan.")

st.markdown("---")

# ===============================
# Bagian 2: Ringkasan (MD Report)
# ===============================
st.header("📝 Laporan Ringkas")

try:
    with open("Output/spam_detection_report_20250828_070511.md", "r", encoding="utf-8") as f:
        laporan = f.read()
    st.markdown(laporan)
except:
    st.warning("⚠️ File spam_detection_report_20250828_070511.md tidak ditemukan.")

st.markdown("---")

# ===============================
# Bagian 3: Wordcloud & Visualisasi
# ===============================
st.header("☁️ Wordcloud & Visualisasi")

st.subheader("Wordcloud Spam vs Non-Spam")
st.image("Output/wordcloud_spam_analysis_20250828_070512.png", caption="Wordcloud Spam Analysis", use_column_width=True)

st.subheader("Detail Visualisasi Spam")
st.image("Output/visualisasi_spam_detail_20250828_070506.png", caption="Visualisasi Detail Spam", use_column_width=True)

st.markdown("---")

# ===============================
# Bagian 4: Ringkasan Eksekutif
# ===============================
st.header("✅ Kesimpulan")
st.markdown("""
- Spam di Twitter pada periode analisis relatif kecil dibanding non-spam.  
- Pola spam didominasi promosi, link pendek, dan clickbait.  
- Non-spam lebih banyak opini & komentar alami.  
""")

st.header("📌 Rekomendasi")
st.markdown("""
- Tambahkan analisis **sentimen (positif/negatif/netral)**.  
- Analisis tren spam berdasarkan **timeline (tanggal/waktu)**.  
- Perluasan dataset agar hasil lebih representatif.  
""")
