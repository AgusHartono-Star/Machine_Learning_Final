import streamlit as st
import pandas as pd
import plotly.express as px
from backend import SapiBackend

# ==========================================
# 1. INJEKSI CSS PREMIUM CYBER DARK THEME V2
# ==========================================
SapiUI_CSS = """
<style>
/* Impor Font Modern */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

/* Latar Belakang Global Aplikasi & Font Master */
html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background-color: #0B0F19 !important; /* Deep Midnight Blue */
    color: #F8FAFC !important; 
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* Kustomisasi Sidebar Menu */
[data-testid="stSidebar"] {
    background-color: #111827 !important; /* Charcoal Dark */
    border-right: 1px solid #1F2937;
}

/* Memastikan Kontrol Radio Sidebar Terlihat Elegan */
[data-testid="stSidebar"] .stRadio > label {
    font-weight: 600 !important;
    color: #9CA3AF !important;
}

/* Semua Label Form & Widget Teks */
.stWidgetLabel p, label, .stSelectbox p, .stNumberInput p, .stMultiSelect p, .stRadio p, p, span {
    color: #94A3B8 !important; /* Soft Slate Gray */
    font-weight: 500;
}

/* Heading Typography */
h1, h2, h3, h4, h5, h6 {
    color: #F8FAFC !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
}

/* Banner Header Premium dengan Efek Mesh Gradient */
.modern-banner {
    background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 50%, #0284C7 100%);
    padding: 35px 25px;
    border-radius: 16px;
    color: white;
    text-align: center;
    margin-bottom: 30px;
    border: 1px solid #1E40AF;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.4), 0 0 15px rgba(2, 132, 199, 0.2);
}
.modern-banner h1 { color: #FFFFFF !important; font-size: 30px !important; margin: 0; letter-spacing: -0.5px; }
.modern-banner p { color: #38BDF8 !important; font-size: 14px; margin-top: 10px; font-weight: 400; }

/* Komponen KPI Card Grid dengan Hover Neon Glow */
.kpi-container { display: flex; flex-wrap: wrap; gap: 16px; margin-bottom: 25px; }
.kpi-card { 
    flex: 1; 
    min-width: 220px; 
    background: #111827; 
    padding: 24px; 
    border-radius: 14px; 
    border: 1px solid #1F2937; 
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3); 
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.kpi-card:hover { 
    transform: translateY(-4px); 
    border-color: #0EA5E9; 
    box-shadow: 0 10px 20px -5px rgba(14, 165, 233, 0.15), 0 0 15px rgba(14, 165, 233, 0.1);
}
.kpi-title { font-size: 11px; color: #6B7280; font-weight: 700; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px; }
.kpi-value { font-size: 24px; font-weight: 700; color: #F9FAFB; }

/* Pembungkus Blok Grafik & Form (Card Container Layout) */
.glass-panel {
    background-color: #111827;
    border: 1px solid #1F2937;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 25px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
}

/* Kotak Hasil Diagnosa AI Sukses (Red Theme Neon) */
.diagnosa-box { 
    background: #111827; 
    border-left: 6px solid #EF4444; 
    padding: 24px; 
    border-radius: 12px; 
    border-top: 1px solid #1F2937;
    border-right: 1px solid #1F2937;
    border-bottom: 1px solid #1F2937;
    box-shadow: 0 20px 25px -5px rgba(239, 68, 68, 0.07), 0 0 20px rgba(0,0,0,0.5); 
    margin-top: 20px; 
    margin-bottom: 25px;
}

/* Modifikasi Desain Tombol Streamlit (Primary Button Neon) */
.stButton>button {
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
    color: white !important;
    border: none !important;
    padding: 12px 24px !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    box-shadow: 0 4px 10px rgba(37, 99, 235, 0.2) !important;
    transition: all 0.2s !important;
}
.stButton>button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 15px rgba(37, 99, 235, 0.4), 0 0 10px rgba(56, 189, 248, 0.2) !important;
}
</style>
"""
st.markdown(SapiUI_CSS, unsafe_allow_html=True)

# ==========================================
# 2. SINKRONISASI DATA KE SESSION STATE
# ==========================================
if 'db_aktif' not in st.session_state:
    df_init, status_msg = SapiBackend.load_initial_data()
    st.session_state.db_aktif = df_init.to_dict('records')
    st.session_state.status_context = status_msg

df_current = pd.DataFrame(st.session_state.db_aktif)

# Ekstraksi Master Data Pilihan secara Dinamis dari CSV Asli Anda
if not df_current.empty:
    KABUPATEN_LIST = sorted(df_current['Kabupaten'].dropna().unique().tolist())
    SPESIES_LIST = sorted(df_current['Spesies'].dropna().unique().tolist())
else:
    KABUPATEN_LIST = ["Konawe", "Kolaka", "Bombana", "Kota Baubau"]
    SPESIES_LIST = ["sapi", "sapi bali", "sapi po", "sapi limosin"]

GEJALA_MASTER = ['bulu_kusam', 'bulu_rontok', 'kekurusan', 'diare', 'anorexia', 
                 'demam', 'lemah', 'radang_mata', 'mata_berair', 'kornea_keruh', 
                 'gatal', 'anemia', 'liur_berlebihan', 'luka_kaki', 'pincang', 
                 'rahim_bengkak', 'obstipasi', 'radang_kulit', 'konstipasi', 
                 'luka_berdarah', 'kembung', 'rhinitis', 'bersin', 'batuk']

# ==========================================
# 3. SIDEBAR NAVIGATION MENU
# ==========================================
st.sidebar.title("SI-SAPI SULTRA 🐄")
st.sidebar.caption(f"Status: **{st.session_state.status_context}**")
menu = st.sidebar.radio(
    "Menu Navigasi Laporan:",
    ["📈 Analitik & Dashboard", "🔬 Konsultasi Diagnosa AI", "✍️ Input Kasus Baru", "📋 Database Historis"]
)
st.sidebar.markdown("---")
st.sidebar.caption("💡 *Tip Mobile: Tekan panah (<) di pojok kiri atas HP Anda untuk menutup/membuka menu.*")

# ==========================================
# HALAMAN 1: ANALITIK & DASHBOARD
# ==========================================
if menu == "📈 Analitik & Dashboard":
    st.markdown(f"<div class='modern-banner'><h1>Dashboard Epidemiologi Kesehatan Ternak</h1><p>Pemantauan Distribusi Kasus Secara Real-Time Wilayah Sulawesi Tenggara</p></div>", unsafe_allow_html=True)
    
    total_laporan = len(df_current)
    total_sapi = int(df_current['Jumlah hewan terkena (ekor)'].sum()) if not df_current.empty else 0
    kab_top = df_current['Kabupaten'].mode()[0] if not df_current.empty else "N/A"
    penyakit_top = df_current['Diagnosa sementara'].mode()[0] if not df_current.empty else "N/A"
    
    st.markdown(f"""
        <div class='kpi-container'>
            <div class='kpi-card'><div class='kpi-title'>Total Kasus</div><div class='kpi-value'>📁 {total_laporan} Laporan</div></div>
            <div class='kpi-card'><div class='kpi-title'>Populasi Terinfeksi</div><div class='kpi-value'>🐄 {total_sapi} Ekor</div></div>
            <div class='kpi-card'><div class='kpi-title'>Zonasi Hotspot</div><div class='kpi-value'>📍 {kab_top}</div></div>
            <div class='kpi-card'><div class='kpi-title'>Tren Penyakit</div><div class='kpi-value'>⚠️ {penyakit_top}</div></div>
        </div>
    """, unsafe_allow_html=True)
    
    if not df_current.empty:
        g1, g2 = st.columns(2)
        with g1:
            st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
            st.subheader("📊 Peta Wilayah Terdampak Sultra")
            df_kab = df_current.groupby('Kabupaten').size().reset_index(name='Jumlah Kasus')
            fig_kab = px.bar(df_kab, x='Jumlah Kasus', y='Kabupaten', orientation='h', template='plotly_dark', color_discrete_sequence=['#38BDF8'])
            fig_kab.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=10, r=10, t=20, b=10))
            st.plotly_chart(fig_kab, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with g2:
            st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
            st.subheader("🕒 Dinamika Distribusi Bulanan")
            df_bulan = df_current.groupby('Sumber_Bulan').size().reset_index(name='Jumlah Kasus')
            fig_bulan = px.line(df_bulan, x='Sumber_Bulan', y='Jumlah Kasus', markers=True, template='plotly_dark', color_discrete_sequence=['#F43F5E'])
            fig_bulan.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=10, r=10, t=20, b=10))
            st.plotly_chart(fig_bulan, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# HALAMAN 2: KONSULTASI DIAGNOSA AI
# ==========================================
elif menu == "🔬 Konsultasi Diagnosa AI":
    st.markdown("<div class='modern-banner'><h1>Sistem Pakar Deteksi Dini</h1><p>Input data gejala klinis untuk memicu kalkulasi probabilitas Machine Learning</p></div>", unsafe_allow_html=True)
    
    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    st.write("### 🧬 Ringkasan Formulir Medis")
    c1, c2, c3 = st.columns(3)
    with c1:
        pemilik = st.text_input("Nama Pemilik Ternak:", "Kelompok Tani Bersama")
        spesies = st.selectbox("Spesies Rumpun Ternak:", options=SPESIES_LIST)
    with c2:
        kab = st.selectbox("Lokasi Kabupaten:", options=KABUPATEN_LIST)
        jumlah = st.number_input("Jumlah Hewan Sakit (Ekor):", min_value=1, value=1)
    with c3:
        st.text_input("Nama Pemeriksa Lapangan:", "Drh. Petugas Dinas")
        st.radio("Validasi Investigasi Lapangan:", ["Kunjungan Kandang", "Tele-Medicine"])
    st.markdown("</div>", unsafe_allow_html=True)
        
    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    st.write("### 🩺 Tanda Klinis Teramati pada Sapi")
    
    artifacts = SapiBackend.get_artifacts()
    if artifacts:
        opsi_gejala = sorted(artifacts['fitur_gejala'])
        label_status = "Model AI Asli Aktif"
    else:
        opsi_gejala = GEJALA_MASTER
        label_status = "Mode Cadangan Aktif"
        
    gejala = st.multiselect(f"Pilih Satu atau Beberapa Gejala Teramati ({label_status}):", options=opsi_gejala)
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("🚀 Jalankan Kalkulasi Model AI", type="primary", use_container_width=True):
        if not gejala:
            st.warning("⚠️ Mohon centang minimal satu tanda klinis.")
        else:
            with st.spinner("Mengomputasi matriks fitur model Random Forest..."):
                penyakit_pred, prob_dict = SapiBackend.hitung_prediksi_ai(gejala, jumlah)
            
            # KONDISI KHUSUS: Jika file berkas model lawas terdeteksi
            if penyakit_pred == "VERSI_MODEL_LAMA":
                st.error("❌ Mismatch Versi Model Terdeteksi!")
                st.info("File 'model_prediksi_sapi.joblib' di direktori Anda masih versi lama. Harap jalankan cell ekspor terbaru di Jupyter Notebook Anda untuk memuat 'target_names'.")
            
            # KONDISI A: Sistem Keamanan Batas Threshold Terpicu (< 60%)
            elif penyakit_pred == "Gejala Tidak Dikenal / Terindikasi Penyakit Langka":
                st.markdown(f"""
                    <div style='background-color: #111827; border-left: 6px solid #F97316; padding: 24px; border-radius: 12px; border: 1px solid #1F2937; box-shadow: 0 20px 25px -5px rgba(249, 115, 22, 0.08); margin-top: 20px; margin-bottom: 25px;'>
                        <span style='color: #F97316; font-weight: 700; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px;'>⚠️ Proteksi Diagnosa Terpicu</span>
                        <h2 style='margin: 8px 0 10px 0; color: #F8FAFC; font-size: 22px;'>🔍 Gejala Tidak Dikenal / Pola Klinis Langka</h2>
                        <p style='color: #E2E8F0; font-size: 14px; margin: 0; line-height: 1.6;'>
                            Model AI mendeteksi kombinasi gejala yang tidak biasa dengan tingkat keyakinan rendah (di bawah 60%). 
                            Sapi rumpun <b>{spesies}</b> berjumlah <b>{jumlah} ekor</b> di <b>{kab}</b> ini kemungkinan besar mengalami pola penyakit di luar data latih utama kami.
                            <br><br><b>Rekomendasi Petugas:</b> Segera hubungi Dokter Hewan berwenang untuk pemeriksaan laboratorium klinis secara manual.
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            
            # KONDISI B: Diagnosa Sukses Terhitung Komputer (> 60%)
            else:
                st.markdown(f"""
                    <div class='diagnosa-box'>
                        <span style='color: #F87171; font-weight: 700; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px;'>Hasil Analisis Komputasi Artificial Intelligence</span>
                        <h2 style='margin: 8px 0 10px 0; color: #F8FAFC; font-size: 24px;'>🚨 {penyakit_pred}</h2>
                        <p style='color: #E2E8F0; font-size: 14px; line-height: 1.6; margin: 0;'>Ternak sapi rumpun <b>{spesies}</b> berjumlah <b>{jumlah} ekor</b> di <b>{kab}</b> terindikasi kuat mengalami penyakit tersebut berdasarkan kalkulasi bobot pohon keputusan Random Forest.</p>
                    </div>
                """, unsafe_allow_html=True)
            
            # Tampilkan Grafik Alternatif dengan Custom Design Plotly Express
            if prob_dict:
                st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
                st.write("#### 📊 Grafik Tingkat Keyakinan Penyakit Terdeteksi:")
                df_chart = pd.DataFrame(list(prob_dict.items()), columns=['Penyakit', 'Persentase (%)']).sort_values(by='Persentase (%)', ascending=True)
                
                # Mengubah grafik bawaan menjadi horizontal bar chart Plotly yang premium
                fig_pred = px.bar(df_chart, x='Persentase (%)', y='Penyakit', orientation='h', 
                                  text='Persentase (%)', template='plotly_dark',
                                  color='Persentase (%)', color_continuous_scale='Bluered')
                fig_pred.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                                       margin=dict(l=10, r=10, t=10, b=10), coloraxis_showscale=False)
                fig_pred.update_traces(texttemplate='%{text}%', textposition='inside')
                st.plotly_chart(fig_pred, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# HALAMAN 3: INPUT KASUS BARU
# ==========================================
elif menu == "✍️ Input Kasus Baru":
    st.markdown("<div class='modern-banner'><h1>Pendaftaran Kasus Lapangan</h1><p>Formulir input resmi data surveilans penyakit hewan menular</p></div>", unsafe_allow_html=True)
    
    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    with st.form("form_baru", clear_on_submit=True):
        cc1, cc2 = st.columns(2)
        with cc1:
            kab_in = st.selectbox("Wilayah Kabupaten:", options=KABUPATEN_LIST)
            desa_in = st.text_input("Nama Desa / Kelurahan lokasi:", "Desa Mandiri")
        with cc2:
            spe_in = st.selectbox("Rumpun Sapi Ternak:", options=SPESIES_LIST)
            jml_in = st.number_input("Jumlah Kasus Sapi Terjangkit (Ekor):", min_value=1, value=1)
            
        gejala_in = st.multiselect("Daftar Tanda Klinis yang Ditemukan:", options=GEJALA_MASTER)
        
        submit = st.st.form_submit_button("📁 Simpan Laporan Masuk", use_container_width=True) if hasattr(st, "st") else st.form_submit_button("📁 Simpan Laporan Masuk", use_container_width=True)
        if submit:
            data_baru = SapiBackend.process_new_report(kab_in, desa_in, spe_in, jml_in, gejala_in)
            st.session_state.db_aktif.append(data_baru)
            st.success(f"🎉 Sukses! Kasus baru untuk wilayah **{kab_in}** berhasil direkam masuk database.")
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# HALAMAN 4: DATABASE HISTORIS
# ==========================================
elif menu == "📋 Database Historis":
    st.markdown("<div class='modern-banner'><h1>Log Data Rekam Medis Sultra</h1><p>Akses transparansi pencarian data kasus, audit sistem, dan ekspor berkas</p></div>", unsafe_allow_html=True)
    
    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    st.dataframe(df_current, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    csv_file = df_current.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Ekspor Seluruh Database (.CSV)", data=csv_file, file_name="Log_Penyakit_Sapi_Terbaru.csv", use_container_width=True)