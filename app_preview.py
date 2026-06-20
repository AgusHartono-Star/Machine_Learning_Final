import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="SI-SAPI SULTRA (PREVIEW)",
    page_icon="🐄",
    layout="wide"
)

st.markdown("""
    <style>
    .main-header { font-size: 36px; color: #1E3A8A; font-weight: bold; text-align: center; margin-bottom: 10px; }
    .sub-header { font-size: 18px; color: #4B5563; text-align: center; margin-bottom: 30px; }
    .card { padding: 20px; border-radius: 8px; background-color: #F8FAFC; border: 1px solid #E2E8F0; margin-bottom: 15px; }
    .metric-val { font-size: 28px; font-weight: bold; color: #2563EB; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# DAFTAR MASTER DATA LENGKAP SULTRA
# ==========================================
KABUPATEN_SULTRA = [
    "Bombana", "Buton", "Buton Selatan", "Buton Tengah", "Buton Utara",
    "Kolaka", "Kolaka Timur", "Kolaka Utara", "Konawe", "Konawe Kepulauan",
    "Konawe Selatan", "Konawe Utara", "Muna", "Muna Barat", "Wakatobi",
    "Kota Baubau", "Kota Kendari"
]

SPESIES_SAPI = ["sapi", "sapi bali", "sapi brahman", "sapi PO", "limosin"]
GEJALA_MASTER = ['Diare', 'Bulu Kusam', 'Kurus', 'Demam Tinggi', 'Tidak Nafsu Makan', 'Lemas', 'Pincang', 'Air Liur Berlebih']

# ==========================================
# MEMUAT DATA (Membaca file asli jika ada)
# ==========================================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('Dataset_Khusus_Sapi.xlsx - Sheet1.csv')
        return df, "Data Asli Terdeteksi"
    except FileNotFoundError:
        # Jika file csv tidak ada, buat data dummy berbasis Master Data Sultra
        np.random.seed(42)
        bulan = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli']
        penyakit = ['Cacingan', 'Bovine Ephemeral Fever (BEF)', 'Malnutrisi', 'Diare Klinis']
        data = {
            'ID Kasus': [f"KASUS-{i}" for i in range(100, 150)],
            'Tanggal laporan': [datetime.now().strftime('%d/%m/%Y') for _ in range(50)],
            'Jumlah hewan terkena (ekor)': np.random.randint(1, 5, size=50),
            'Spesies': np.random.choice(SPESIES_SAPI, size=50),
            'Tanda': ['Bulu kusam, kurus, diare' for _ in range(50)],
            'Nama pengirim': np.random.choice(['Budi', 'Ali', 'Siti'], size=50),
            'Staf teknis dinas': ['Drh. Ridwan Alimin' for _ in range(50)],
            'Tipe investigasi': ['Kunjungan' for _ in range(50)],
            'Diagnosa sementara': np.random.choice(penyakit, size=50),
            'Sumber_Bulan': np.random.choice(bulan, size=50),
            'Kabupaten': np.random.choice(KABUPATEN_SULTRA, size=50),
            'Kecamatan': ['Kecamatan Sampolawa' for _ in range(50)],
            'Desa': ['Desa Bahari' for _ in range(50)]
        }
        return pd.DataFrame(data), "Mode Simulasi (CSV Asli Tidak Ditemukan)"

df_sapi, status_data = load_data()

# Ambil daftar unik secara dinamis jika membaca dari CSV asli
list_kabupaten = sorted(df_sapi['Kabupaten'].dropna().unique()) if 'Kabupaten' in df_sapi.columns and status_data == "Data Asli Terdeteksi" else KABUPATEN_SULTRA
list_spesies = sorted(df_sapi['Spesies'].dropna().unique()) if 'Spesies' in df_sapi.columns and status_data == "Data Asli Terdeteksi" else SPESIES_SAPI

# Simpan inputan baru sementara ke dalam session state agar simulasi tombol "Laporkan" berfungsi
if 'lokal_db' not in st.session_state:
    st.session_state.lokal_db = df_sapi.to_dict('records')

df_current = pd.DataFrame(st.session_state.lokal_db)

# ==========================================
# SIDEBAR NAVIGASI
# ==========================================
st.sidebar.title("Navigasi SI-SAPI 🐄")
st.sidebar.caption(f"Status Data: **{status_data}**")
menu = st.sidebar.radio(
    "Pilih Menu Aplikasi:",
    ["📊 Dashboard & Analitik Tren", "🩺 Konsultasi & Diagnosa ML", "📝 Pelaporan Kasus Baru", "🔍 Eksplorasi Data Historis"]
)

# ==========================================
# TAMPILAN MENU 1: DASHBOARD
# ==========================================
if menu == "📊 Dashboard & Analitik Tren":
    st.markdown("<div class='main-header'>📊 Dashboard Sebaran & Analitik Penyakit</div>", unsafe_allow_html=True)
    
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.markdown(f"<div class='card'><p>Total Laporan Kasus</p><p class='metric-val'>{len(df_current)} Kejadian</p></div>", unsafe_allow_html=True)
    with m2: st.markdown(f"<div class='card'><p>Total Sapi Terinfeksi</p><p class='metric-val'>{int(df_current['Jumlah hewan terkena (ekor)'].sum())} Ekor</p></div>", unsafe_allow_html=True)
    with m3: st.markdown(f"<div class='card'><p>Hotspot Terbanyak</p><p class='metric-val'>{df_current['Kabupaten'].mode()[0] if not df_current.empty else 'N/A'}</p></div>", unsafe_allow_html=True)
    with m4: st.markdown(f"<div class='card'><p>Penyakit Terbanyak</p><p class='metric-val'>{df_current['Diagnosa sementara'].mode()[0] if not df_current.empty else 'N/A'}</p></div>", unsafe_allow_html=True)

    g1, g2 = st.columns(2)
    with g1:
        st.subheader("📈 Tren Kasus Per Bulan")
        df_bulan = df_current.groupby('Sumber_Bulan').size().reset_index(name='Jumlah Kasus')
        fig_bulan = px.line(df_bulan, x='Sumber_Bulan', y='Jumlah Kasus', markers=True, color_discrete_sequence=['#2563EB'])
        st.plotly_chart(fig_bulan, use_container_width=True)
    with g2:
        st.subheader("🗺️ Sebaran Kasus per Kabupaten (Sultra)")
        df_kab = df_current.groupby('Kabupaten').size().reset_index(name='Jumlah Kasus')
        fig_kab = px.bar(df_kab, x='Jumlah Kasus', y='Kabupaten', orientation='h', color='Jumlah Kasus', color_continuous_scale='Blues')
        st.plotly_chart(fig_kab, use_container_width=True)

# ==========================================
# TAMPILAN MENU 2: DIAGNOSA MODEL
# ==========================================
elif menu == "🩺 Konsultasi & Diagnosa ML":
    st.markdown("<div class='main-header'>🩺 Sistem Pakar Diagnosa Dini Penyakit</div>", unsafe_allow_html=True)
    
    st.write("### Masukkan Data Pemeriksaan Lapangan")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.text_input("Nama Pengirim / Pemilik Ternak:", value="Pak Subhan")
        st.selectbox("Rumpun/Spesies Sapi:", options=list_spesies)
    with c2:
        st.selectbox("Kabupaten Lokasi Kejadian (Sultra):", options=list_kabupaten)
        st.number_input("Jumlah Sapi yang Mengalami Gejala (Ekor):", min_value=1, value=1)
    with c3:
        st.text_input("Nama Petugas Teknis Dinas:", value="Drh. Ridwan Alimin")
        st.radio("Tipe Investigasi Lapangan:", ["Kunjungan Direct", "Laporan Online"])
        
    st.write("---")
    st.write("### Pilih Gejala Klinis Hasil Pemeriksaan Fisik")
    gejala_terpilih = st.multiselect("Centang Gejala Sapi yang Terlihat:", options=GEJALA_MASTER, default=['Bulu Kusam', 'Kurus'])
    
    if st.button("🚀 Proses & Keluarkan Diagnosa Medis", type="primary"):
        st.success("🎉 Simulasi Analisis Model Berhasil Dijalankan!")
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.markdown("""
            <div style='background-color: #FEF2F2; padding: 25px; border-left: 5px solid #DC2626; border-radius: 5px;'>
                <h4 style='color: #991B1B; margin:0;'>SIMULASI DIAGNOSA UTAMA:</h4>
                <h2 style='color: #DC2626; margin: 5px 0;'>🔥 Cacingan</h2>
                <p style='color: #7F1D1D; font-size: 14px; margin-bottom: 0;'>
                    Model mendeteksi indikasi kuat penyakit parasit internal. Disarankan pemberian anthelmintik (obat cacing).
                </p>
            </div>
            """, unsafe_allow_html=True)
        with res_col2:
            st.write("📊 **Tingkat Keyakinan Model:**")
            df_prob_dummy = pd.DataFrame({
                'Penyakit': ['Cacingan', 'Malnutrisi', 'BEF', 'Diare'],
                'Keyakinan (%)': [84.2, 11.5, 3.1, 1.2]
            })
            st.bar_chart(df_prob_dummy.set_index('Penyakit'))

# ==========================================
# TAMPILAN MENU 3: PELAPORAN (Simulasi Aktif!)
# ==========================================
elif menu == "📝 Pelaporan Kasus Baru":
    st.markdown("<div class='main-header'>📝 Formulir Pelaporan Masuk Kasus Baru</div>", unsafe_allow_html=True)
    st.write("Fitur ini mensimulasikan penambahan data ke database secara dinamis.")
    
    with st.form("form_kasus_baru"):
        st.write("#### 1. Lokasi Administratif")
        f1, f2 = st.columns(2)
        with f1: 
            kab_input = st.selectbox("Kabupaten:", options=KABUPATEN_SULTRA)
        with f2: 
            des_input = st.text_input("Desa / Kelurahan:", value="Mendikonu")
            
        st.write("#### 2. Informasi Kasus")
        f3, f4 = st.columns(2)
        with f3:
            spe_input = st.selectbox("Rumpun Sapi:", options=SPESIES_SAPI)
        with f4:
            jml_input = st.number_input("Jumlah Hewan Terkena (Ekor):", min_value=1, value=1)
            
        txt_gejala = st.text_area("Deskripsi Tanda Klinis:")
        
        if st.form_submit_button("📁 Kirim Laporan"):
            # Proses simulasi memasukkan data ke dalam list session state
            new_row = {
                'ID Kasus': f"KASUS-{len(st.session_state.lokal_db) + 100}",
                'Tanggal laporan': datetime.now().strftime('%d/%m/%Y'),
                'Jumlah hewan terkena (ekor)': jml_input,
                'Spesies': spe_input,
                'Tanda': txt_gejala if txt_gejala else "Diare",
                'Nama pengirim': "Pelaporan Mandiri",
                'Staf teknis dinas': "Belum Ditugaskan",
                'Tipe investigasi': "Laporan Online",
                'Diagnosa sementara': "Menunggu Konfirmasi",
                'Sumber_Bulan': datetime.now().strftime('%B'),
                'Kabupaten': kab_input,
                'Kecamatan': "Kecamatan Input",
                'Desa': des_input
            }
            st.session_state.lokal_db.append(new_row)
            st.success(f"✅ Berhasil! Kasus baru di **{kab_input}** telah direkam. Silakan cek data terbaru di menu Dashboard atau Menu Riwayat.")

# ==========================================
# TAMPILAN MENU 4: RIWAYAT DATA
# ==========================================
elif menu == "🔍 Eksplorasi Data Historis":
    st.markdown("<div class='main-header'>🔍 Riwayat Log Seluruh Rekam Medis</div>", unsafe_allow_html=True)
    st.dataframe(df_current, use_container_width=True)
    st.download_button("📥 Unduh Data Terbaru (.CSV)", data=df_current.to_csv(index=False).encode('utf-8'), mime='text/csv')