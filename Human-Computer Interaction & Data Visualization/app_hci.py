import streamlit as st
import pandas as pd
import plotly.express as px

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="HCI & Data Visualization Dashboard", page_icon="📊", layout="wide")

st.title("📊 Dasbor Evaluasi HCI & Visualisasi Data")
st.caption("Studi Kasus: Human-Computer Interaction and Data Visualization (Dr. Arafat Febriandirza - BRIN)")
st.markdown("---")

# --- 1. DATA DUMMY EVALUASI USABILITY (SUS & FEEDBACK) ---
data_feedback = {
    "Respondent": ["User A (Lansia)", "User B (Profesional)", "User C (Gen Z)", "User D (Mahasiswa)", "User E (Umum)"],
    "Kategori_Pengguna": ["Senior", "Expert", "Student", "Student", "General"],
    "SUS_Score": [68.5, 85.0, 90.5, 78.0, 72.0],
    "Task_Completion_Time_sec": [45, 15, 20, 30, 40],
    "Tingkat_Kepuasan": ["Puas", "Sangat Puas", "Sangat Puas", "Puas", "Cukup"]
}
df_eval = pd.DataFrame(data_feedback)

# --- 2. SIDEBAR FILTER INTERAKTIF ---
st.sidebar.header("🔍 Filter Data Evaluasi HCI")
pilih_kategori = st.sidebar.multiselect(
    "Pilih Kategori Pengguna:",
    options=df_eval["Kategori_Pengguna"].unique(),
    default=df_eval["Kategori_Pengguna"].unique()
)

df_filtered = df_eval[df_eval["Kategori_Pengguna"].isin(pilih_kategori)]

# --- 3. MAIN LAYOUT: METRIK UTAMA ---
col1, col2, col3 = st.columns(3)
col1.metric("Rata-rata Skor SUS (Usability)", f"{df_filtered['SUS_Score'].mean():.1f} / 100", "+4.2% dari bulan lalu")
col2.metric("Rata-rata Waktu Selesai Tugas", f"{df_filtered['Task_Completion_Time_sec'].mean():.1f} Detik", "Lebih cepat 5s")
col3.metric("Total Responden Dievaluasi", len(df_filtered), "Pengguna Aktif")

st.markdown("---")

# --- 4. VISUALISASI DATA INTERAKTIF (PLOTLY) ---
c1, c2 = st.columns(2)

with c1:
    st.subheader("📈 Grafik Skor SUS per Responden")
    fig_bar = px.bar(
        df_filtered, 
        x="Respondent", 
        y="SUS_Score", 
        color="Tingkat_Kepuasan",
        text="SUS_Score",
        title="Evaluasi Tingkat Keterpakaian (System Usability Scale)"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with c2:
    st.subheader("⏱️ Korelasi Waktu vs Kepuasan")
    fig_scatter = px.scatter(
        df_filtered,
        x="Task_Completion_Time_sec",
        y="SUS_Score",
        size="SUS_Score",
        color="Kategori_Pengguna",
        hover_name="Respondent",
        title="Semakin Cepat Waktu Tugas, Apakah Skor SUS Semakin Tinggi?"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# --- 5. TABEL DATA MENTAH & PRINSIP NIELSEN ---
st.subheader("📋 Detail Log Evaluasi Pengguna")
st.dataframe(df_filtered, use_container_width=True, hide_index=True)

st.info("💡 **Prinsip HCI Penting:** *'You are not your user.'* Selalu lakukan evaluasi empiris (seperti pengujian SUS di atas) untuk memastikan antarmuka mudah dipahami oleh berbagai kalangan pengguna.")
