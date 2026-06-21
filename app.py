import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
import hashlib
import base64
from backend import SapiBackend

# ==========================================
# PEMANGGILAN BOOTSTRAP CDN
# ==========================================
bootstrap_cdn = '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">'
st.markdown(bootstrap_cdn, unsafe_allow_html=True)

# ==========================================
# FUNGSI BASE64 UNTUK KONVERSI GAMBAR LOKAL
# ==========================================
def get_base64_of_bin_file(bin_file):
    if not os.path.exists(bin_file): 
        # Fallback menggunakan avatar siluet default jika file belum ada di folder
        return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
    with open(bin_file, "rb") as f:
        data = f.read()
    return f"data:image/jpeg;base64,{base64.b64encode(data).decode()}"

# Konversi semua aset foto lokal ke Base64 secara aman
img_base64 = get_base64_of_bin_file("sapi.jpg")
foto_coach = get_base64_of_bin_file("coach.jpg")
foto_dosen = get_base64_of_bin_file("dosen_pengampu.jpg")
foto_ketua = get_base64_of_bin_file("Ketua_Kelompok.jpeg")
foto_agus  = get_base64_of_bin_file("anggota.jpeg")

# ==========================================
# 1. INJEKSI CSS PREMIUM CYBER GLASSMORPHISM V3
# ==========================================
SapiUI_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

/* Latar Belakang Aplikasi Global dengan Gambar sapi.jpg + Overlay Gelap */
html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
    background-image: linear-gradient(rgba(11, 15, 25, 0.85), rgba(11, 15, 25, 0.85)), url("{img_base64}") !important;
    background-size: cover !important;
    background-position: center !important;
    background-attachment: fixed !important;
    color: #F8FAFC !important; 
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}}

/* Fallback lokal jika diakses tanpa static routing tertentu */
[data-testid="stAppViewContainer"] {{
    background-image: linear-gradient(rgba(11, 15, 25, 0.88), rgba(11, 15, 25, 0.88)), url("{img_base64}") !important;
    background-size: cover !important;
    background-position: center !important;
    background-attachment: fixed !important;
}}

/* Kustomisasi Sidebar Menu */
[data-testid="stSidebar"] {{
    background-color: rgba(17, 24, 39, 0.85) !important; 
    backdrop-filter: blur(12px) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.05);
}}

/* Semua Label Form & Widget Teks */
.stWidgetLabel p, label, .stSelectbox p, .stNumberInput p, .stMultiSelect p, .stRadio p, p, span {{
    color: #94A3B8 !important; 
    font-weight: 500;
}}
h1, h2, h3, h4, h5, h6 {{ color: #F8FAFC !important; font-family: 'Plus Jakarta Sans', sans-serif !important; font-weight: 700 !important; }}

/* Banner Header Premium */
.modern-banner {{
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.6) 0%, rgba(30, 58, 138, 0.6) 50%, rgba(2, 132, 199, 0.6) 100%);
    backdrop-filter: blur(8px);
    padding: 35px 25px;
    border-radius: 16px;
    color: white;
    text-align: center;
    margin-bottom: 30px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.4);
}}
.modern-banner h1 {{ color: #FFFFFF !important; font-size: 30px !important; margin: 0; }}
.modern-banner p {{ color: #38BDF8 !important; font-size: 14px; margin-top: 10px; }}

/* Komponen KPI Card Grid dengan Hover Neon Glow */
.kpi-container {{ display: flex; flex-wrap: wrap; gap: 16px; margin-bottom: 25px; }}
.kpi-card {{ 
    flex: 1; min-width: 220px; 
    background: rgba(17, 24, 39, 0.7) !important; 
    backdrop-filter: blur(8px);
    padding: 24px; border-radius: 14px; border: 1px solid rgba(255, 255, 255, 0.05); 
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}}
.kpi-card:hover {{ transform: translateY(-4px); border-color: #0EA5E9; box-shadow: 0 10px 20px -5px rgba(14, 165, 233, 0.2); }}
.kpi-title {{ font-size: 11px; color: #6B7280; font-weight: 700; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px; }}
.kpi-value {{ font-size: 24px; font-weight: 700; color: #F9FAFB; }}

/* Pembungkus Blok Grafik & Form (Card Container Layout) */
.glass-panel {{ 
    background-color: rgba(17, 24, 39, 0.65) !important; 
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.05); 
    border-radius: 14px; padding: 20px; margin-bottom: 25px; 
}}
.diagnosa-box {{ 
    background: rgba(17, 24, 39, 0.75); 
    border-left: 6px solid #EF4444; padding: 24px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.05); margin-bottom: 25px; 
}}

/* Desain Tombol Premium */
.stButton>button {{
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
    color: white !important; border: none !important; padding: 12px 24px !important; font-weight: 600 !important; border-radius: 10px !important;
}}
.stButton>button:hover {{ transform: translateY(-1px) !important; box-shadow: 0 6px 15px rgba(37, 99, 235, 0.4) !important; }}

/* ========================================== */
/* HACK CSS UNTUK SIDEBAR MENU GAYA BOOTSTRAP */
/* ========================================== */

/* Sembunyikan titik radio asli */
div[data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child {{
    display: none;
}}

/* Mengubah item radio menjadi blok menu Bootstrap */
div[data-testid="stSidebar"] div[role="radiogroup"] > label {{
    background-color: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    color: #CBD5E1;
    border-radius: 12px;
    padding: 12px 16px;
    margin-bottom: 8px;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
}}

/* Efek Sorot Menu (Hover) */
div[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {{
    background-color: rgba(37, 99, 235, 0.15);
    border-color: #2563EB;
    color: white;
}}

/* Efek Menu Terpilih (Active Bootstrap State) */
div[data-testid="stSidebar"] div[role="radiogroup"] > label[data-selected="true"] {{
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
    color: white !important;
    border-color: transparent !important;
    font-weight: 600;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}}

/* Penyelarasan Posisi Ikon Emoji */
div[data-testid="stSidebar"] div[role="radiogroup"] > label > div:nth-child(2) {{
    margin-left: -5px;
}}

/* Gaya CSS Khusus untuk Efek Carousel Tim Pengembang */
.carousel-container {{
    display: flex;
    overflow-x: auto;
    gap: 20px;
    padding: 15px 5px 25px 5px;
    scroll-behavior: smooth;
}}
.carousel-container::-webkit-scrollbar {{
    height: 6px;
}}
.carousel-container::-webkit-scrollbar-track {{
    background: rgba(255, 255, 255, 0.02);
    border-radius: 10px;
}}
.carousel-container::-webkit-scrollbar-thumb {{
    background: rgba(56, 189, 248, 0.3);
    border-radius: 10px;
}}
.carousel-container::-webkit-scrollbar-thumb:hover {{
    background: rgba(56, 189, 248, 0.6);
}}
.profile-card {{
    flex: 0 0 250px;
    background: rgba(17, 24, 39, 0.6) !important;
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 16px;
    padding: 25px 20px;
    text-align: center;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}}
.profile-card:hover {{
    transform: translateY(-8px) scale(1.02);
    border-color: #0EA5E9;
    box-shadow: 0 20px 25px -5px rgba(14, 165, 233, 0.15), 0 0 15px rgba(14, 165, 233, 0.1);
    background: rgba(17, 24, 39, 0.85) !important;
}}
.profile-img {{
    width: 105px;
    height: 105px;
    border-radius: 50%;
    object-fit: cover;
    margin: 0 auto 15px auto;
    border: 3px solid rgba(255, 255, 255, 0.1);
    transition: all 0.3s ease;
}}
.profile-card:hover .profile-img {{
    border-color: #38BDF8;
    transform: scale(1.05);
}}
.badge-coach {{ background-color: rgba(16, 185, 129, 0.15); color: #34D399; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 600; }}
.badge-dosen {{ background-color: rgba(245, 158, 11, 0.15); color: #FBBF24; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 600; }}
.badge-ketua {{ background-color: rgba(59, 130, 246, 0.15); color: #60A5FA; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 600; }}
.badge-anggota {{ background-color: rgba(156, 163, 175, 0.15); color: #9CA3AF; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 600; }}
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
# 3. SIDEBAR NAVIGATION MENU (PERBAIKAN MENU)
# ==========================================
st.sidebar.title("SI-SAPI SULTRA 🐄")
st.sidebar.caption(f"Status: **{st.session_state.status_context}**")

# Memasukkan opsi "👤 Profil Pengguna" ke sistem navigasi utama
menu = st.sidebar.radio(
    "Menu Navigasi Laporan:",
    ["📈 Analitik & Dashboard", "🔬 Konsultasi Diagnosa AI", "✍️ Input Kasus Baru", "📋 Database Historis", "👤 Profil Pengembang"]
)
st.sidebar.markdown("---")
st.sidebar.caption("💡 *Tip Mobile: Tekan panah (<) di pojok kiri atas HP Anda untuk menutup/membuka menu.*")

# ==========================================
# HALAMAN 1: ANALITIK & DASHBOARD
# ==========================================
if menu == "📈 Analitik & Dashboard":
    st.markdown(f"<div class='modern-banner'><h1>Dashboard Sistem Deteksi Dini Penyakit Ternak Sapi di Sultra</h1><p>Pemantauan Distribusi Kasus Secara Real-Time Wilayah Sulawesi Tenggara</p></div>", unsafe_allow_html=True)
    
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
            
            if penyakit_pred == "VERSI_MODEL_LAMA":
                st.error("❌ Mismatch Versi Model Terdeteksi!")
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
            else:
                st.markdown(f"""
                    <div class='diagnosa-box'>
                        <span style='color: #F87171; font-weight: 700; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px;'>Hasil Analisis Komputasi Artificial Intelligence</span>
                        <h2 style='margin: 8px 0 10px 0; color: #F8FAFC; font-size: 24px;'>🚨 {penyakit_pred}</h2>
                        <p style='color: #E2E8F0; font-size: 14px; line-height: 1.6; margin: 0;'>Ternak sapi rumpun <b>{spesies}</b> berjumlah <b>{jumlah} ekor</b> di <b>{kab}</b> terindikasi kuat mengalami penyakit tersebut berdasarkan kalkulasi bobot pohon keputusan Random Forest.</p>
                    </div>
                """, unsafe_allow_html=True)
            
            if prob_dict:
                st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
                st.write("#### 📊 Grafik Tingkat Keyakinan Penyakit Terdeteksi:")
                df_chart = pd.DataFrame(list(prob_dict.items()), columns=['Penyakit', 'Persentase (%)']).sort_values(by='Persentase (%)', ascending=True)
                fig_pred = px.bar(df_chart, x='Persentase (%)', y='Penyakit', orientation='h', 
                                  text='Persentase (%)', template='plotly_dark',
                                  color='Persentase (%)', color_continuous_scale='Bluered')
                fig_pred.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                                       margin=dict(l=10, r=10, t=10, b=10), coloraxis_showscale=False)
                fig_pred.update_traces(texttemplate='%{text}%', textposition='inside')
                st.plotly_chart(fig_pred, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# HALAMAN 3: INPUT KASUS BARU (PERBAIKAN SINTAKS)
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
        
        # Pembersihan sintaks ganda st.st
        submit = st.form_submit_button("📁 Simpan Laporan Masuk", use_container_width=True)
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

# ==========================================
# HALAMAN 5: PROFIL PENGGUNA & TIM (STRUKTUR GRID STABIL)
# ==========================================
elif menu == "👤 Profil Pengembang":
    st.markdown("<div class='modern-banner'><h1>Pusat Manajemen Akun & Tim</h1><p>Struktur tim pengembang sistem dan kredensial akademik pendukung</p></div>", unsafe_allow_html=True)
    
    # 1. BLOK KREDENSIAL PEMERIKSA (SIMULASI SECURE SESSION)
    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    st.write("### 🪪 Informasi Hak Otoritas Sistem")
    st.markdown(f"""
        <div style='background-color: rgba(31, 41, 55, 0.4); padding: 20px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); margin-top: 10px;'>
            <table style='width: 100%; border-collapse: collapse; border: none; color: #F8FAFC;'>
                <tr style='border-bottom: 1px solid rgba(31, 41, 55, 0.5);'><td style='padding: 8px 0; font-weight: bold; color: #94A3B8; width: 30%;'>Instansi Otoritas</td><td style='padding: 8px 0; font-size: 14px;'>Dinas Tanaman Pangan & Peternakan Provinsi Sulawesi Tenggara</td></tr>
                <tr><td style='padding: 8px 0; font-weight: bold; color: #94A3B8;'>Sesi Demo Status</td><td style='padding: 8px 0; color: #10B981; font-weight: 500;'>🟢 Terkoneksi Lokal (Secure Sandbox Mode)</td></tr>
            </table>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 2. STRUKTUR TIM PENGEMBANG (MENGGUNAKAN ST.COLUMNS ANTI-PECAH)
    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    st.write("### 🎓 Struktur Pengembang Sistem & Pembimbing")
    
    # Injeksi CSS Desain Kartu (Tanpa f-string agar aman dari KeyError)
# Injeksi CSS Desain Kartu (Tanpa f-string agar aman dari KeyError)
    st.markdown("""
        <style>
        .custom-profile-card {
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
            text-align: center !important;
            background: rgba(17, 24, 39, 0.6) !important;
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 16px;
            padding: 25px 20px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
            margin-bottom: 15px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            width: 100% !important;
            min-height: 295px; /* 🔥 Kunci utama agar semua ukuran kartu sama rata */
        }
        
        /* Memaksa semua teks di dalam kartu rata tengah */
        .custom-profile-card h5, 
        .custom-profile-card p {
            text-align: center !important;
            width: 100% !important;
            margin: 0 auto !important;
        }
        
        .custom-profile-img {
            width: 105px;
            height: 105px;
            border-radius: 50%;
            object-fit: cover;
            margin: 0 auto 15px auto !important;
            border: 3px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
            display: block !important;
        }
        .custom-profile-card:hover {
            transform: translateY(-6px) scale(1.02);
            border-color: #0EA5E9;
            box-shadow: 0 20px 25px -5px rgba(14, 165, 233, 0.15);
            background: rgba(17, 24, 39, 0.85) !important;
        }
        .custom-profile-card:hover .custom-profile-img {
            border-color: #38BDF8;
            transform: scale(1.05);
        }
        .custom-badge {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 600;
            display: inline-block !important;
            margin: 0 auto 10px auto !important;
            text-align: center !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # --- BARIS ATAS: DOSEN PANGAMPU (DITENGAHKAN SECARA SIMETRIS) ---
    col_d1, col_d2, col_d3 = st.columns([1, 1.8, 1])
    with col_d2:
        st.markdown(f"""
            <div class='custom-profile-card'>
                <img class='custom-profile-img' src='{foto_dosen}'>
                <div class='custom-badge' style='background-color: rgba(245, 158, 11, 0.15); color: #FBBF24;'>🎓 Dosen Pengampu</div>
                <h5 style='margin: 0 0 5px 0; color: #F8FAFC;'>Rizal Adi Saputra, S.T., M.Kom.</h5>
                <p style='margin: 0; font-size: 13px; color: #94A3B8;'>Dosen Teknik Informatika Universitas Halu Oleo</p>
            </div>
        """, unsafe_allow_html=True)
        
    # Garis pembatas tipis yang elegan
    st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin: 25px 0;'>", unsafe_allow_html=True)
    
    # --- BARIS BAWAH: STRUKTUR TIM INTI KELOMPOK (3 KOLOM SEJAJAR) ---
    col_t1, col_t2, col_t3 = st.columns(3)
    
    with col_t1:
        st.markdown(f"""
            <div class='custom-profile-card'>
                <img class='custom-profile-img' src='{foto_coach}'>
                <div class='custom-badge' style='background-color: rgba(16, 185, 129, 0.15); color: #34D399;'>💼 Coach</div>
                <h5 style='margin: 0 0 5px 0; color: #F8FAFC;'>Vyola Cecilia Potto</h5>
                <p style='margin: 0; font-size: 13px; color: #94A3B8;'>NIM. E1E1240279</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col_t2:
        st.markdown(f"""
            <div class='custom-profile-card'>
                <img class='custom-profile-img' src='{foto_ketua}'>
                <div>
                    <span class='custom-badge' style='background-color: rgba(59, 130, 246, 0.15); color: #60A5FA;'>⚡ Ketua Kelompok</span>
                </div>
                <h5 style='margin: 5px 0 5px 0; color: #F8FAFC; font-weight: 700;'>Wa Ode Yurismawati</h5>
                <p style='margin: 0; font-size: 13px; color: #94A3B8;'>NIM. E1E124080</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col_t3:
        st.markdown(f"""
            <div class='custom-profile-card'>
                <img class='custom-profile-img' src='{foto_agus}'>
                <div class='custom-badge' style='background-color: rgba(156, 163, 175, 0.15); color: #9CA3AF;'>🧬 Anggota Kelompok</div>
                <h5 style='margin: 0 0 5px 0; color: #F8FAFC;'> Agus Hartono</h5>
                <p style='margin: 0; font-size: 13px; color: #94A3B8;'>NIM. E1E124025</p>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)