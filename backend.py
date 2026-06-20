import pandas as pd
import numpy as np
import joblib
import streamlit as st
from datetime import datetime

# Master Data Fallback (Cadangan jika CSV tidak sengaja terhapus)
KABUPATEN_SULTRA = [
    "Bombana", "Buton", "Buton Selatan", "Buton Tengah", "Buton Utara",
    "Kolaka", "Kolaka Timur", "Kolaka Utara", "Konawe", "Konawe Kepulauan",
    "Konawe Selatan", "Konawe Utara", "Muna", "Muna Barat", "Wakatobi",
    "Kota Baubau", "Kota Kendari"
]
SPESIES_SAPI = ["sapi", "sapi bali", "sapi po", "sapi limosin", "Sapi Peranakan Ongole", "sapi brahman", "sapi simental"]
GEJALA_MASTER = ['bulu_kusam', 'bulu_rontok', 'kekurusan', 'diare', 'anorexia', 
                 'demam', 'lemah', 'radang_mata', 'mata_berair', 'kornea_keruh', 
                 'gatal', 'anemia', 'liur_berlebihan', 'luka_kaki', 'pincang', 
                 'rahim_bengkak', 'obstipasi', 'radang_kulit', 'konstipasi', 
                 'luka_berdarah', 'kembung', 'rhinitis', 'bersin', 'batuk']

class SapiBackend:
    @staticmethod
    @st.cache_resource
    def get_artifacts():
        """Memuat 'otak' AI asli dari file joblib secara aman."""
        try:
            return joblib.load('model_prediksi_sapi.joblib')
        except FileNotFoundError:
            return None

    @staticmethod
    def load_initial_data():
        """Memuat data rekam medis historis langsung dari file CSV asli Anda."""
        artifacts = SapiBackend.get_artifacts()
        status_ai = "🤖 AI Engine: AKTIF" if artifacts else "⚠️ AI Engine: SIMULASI"
        
        try:
            df = pd.read_csv('Dataset_Khusus_Sapi.csv')
            for col in df.select_dtypes(include='object').columns:
                df[col] = df[col].str.strip()
            return df, f"Data Asli Terdeteksi | {status_ai}"
        except FileNotFoundError:
            kolom = ['ID Kasus', 'Tanggal laporan', 'Jumlah hewan terkena (ekor)', 'Spesies', 
                     'Tanda', 'Nama pengirim', 'Lokasi', 'Tanggal diinvestigasi', 
                     'Staf teknis dinas', 'Tipe investigasi', 'Diagnosa sementara', 
                     'Sumber_Bulan', 'Provinsi', 'Kabupaten', 'Kecamatan', 'Desa']
            return pd.DataFrame(columns=kolom), f"Mode Preview (CSV Tidak Ditemukan) | {status_ai}"

    @staticmethod
    def process_new_report(kabupaten, desa, spesies, jumlah, gejala_list):
        """Memproses entri pelaporan kasus baru ke dalam memori aplikasi."""
        return {
            'ID Kasus': f"KASUS-{np.random.randint(1000, 9999)}",
            'Tanggal laporan': datetime.now().strftime('%d/%m/%Y'),
            'Jumlah hewan terkena (ekor)': jumlah,
            'Spesies': spesies,
            'Tanda': ", ".join(gejala_list) if gejala_list else "Gejala Ringan",
            'Nama pengirim': "Pelaporan App",
            'Staf teknis dinas': "Petugas Wilayah",
            'Tipe investigasi': "Laporan Online",
            'Diagnosa sementara': "Menunggu Konfirmasi",
            'Sumber_Bulan': datetime.now().strftime('%B'),
            'Kabupaten': kabupaten,
            'Kecamatan': "Kecamatan Setempat",
            'Desa': desa
        }

    @staticmethod
    def hitung_prediksi_ai(gejala_terpilih, jumlah_hewan, ambang_batas=60.0):
        """Menghitung prediksi AI dengan filter fitur, decoding teks target, dan batas threshold."""
        artifacts = SapiBackend.get_artifacts()
        
        if not artifacts:
            bobot = len(gejala_terpilih)
            if bobot >= 3: return "Cacingan Kronis (Simulasi)", {'Cacingan': 85.0, 'Malnutrisi': 15.0}
            return "Indikasi Malnutrisi (Simulasi)", {'Malnutrisi': 70.0, 'Cacingan': 30.0}
        
        selected_mask = artifacts.get('selected_mask', None)
        target_names = artifacts.get('target_names', None) # Mengambil kamus teks nama penyakit asli
        
        if selected_mask is None:
            return "VERSI_MODEL_LAMA", {}
            
        model = artifacts['model']
        mlb = artifacts['mlb']
        
        # 1. Preprocessing Input
        gejala_encoded = mlb.transform([gejala_terpilih])
        jumlah_hewan_log = np.log1p(jumlah_hewan)
        
        # 2. Gabungkan Fitur (26 dimensi awal)
        fitur_penuh = np.hstack([gejala_encoded, [[jumlah_hewan_log]]])
        
        # 3. Filter Fitur Seleksi (Memotong 26 dimensi menjadi 13 dimensi terpilih)
        try:
            fitur_input_terpilih = fitur_penuh[:, selected_mask]
            prediksi_raw = model.predict(fitur_input_terpilih)[0]
        except Exception:
            return "VERSI_MODEL_LAMA", {}
        
        # 4. Kalkulasi Probabilitas & Translasi Angka Ke Teks Penyakit Asli
        prob_dict = {}
        skor_tertinggi = 0.0
        prediksi_kelas = "Gejala Tidak Dikenal"
        
        if hasattr(model, "predict_proba"):
            probabilitas = model.predict_proba(fitur_input_terpilih)[0]
            for kelas_idx, prob in zip(model.classes_, probabilitas):
                prob_persen = round(prob * 100, 2)
                
                # Mengubah indeks angka (misal 2) menjadi nama teks penyakit asli (misal Cacingan)
                if target_names and kelas_idx < len(target_names):
                    nama_penyakit = target_names[kelas_idx]
                else:
                    nama_penyakit = f"Kelas {kelas_idx}"
                    
                if prob_persen > 0.5:
                    prob_dict[nama_penyakit] = prob_persen
                
                if prob_persen > skor_tertinggi:
                    skor_tertinggi = prob_persen
                    prediksi_kelas = nama_penyakit
        else:
            # Langkah cadangan jika model yang dimasukkan tidak mendukung fungsi probabilitas
            if target_names and isinstance(prediksi_raw, (int, np.integer)) and prediksi_raw < len(target_names):
                prediksi_kelas = target_names[prediksi_raw]
            else:
                prediksi_kelas = str(prediksi_raw)
        
        # 5. Proteksi Keamanan Ambang Batas 60% (Solusi Keamanan Penyakit Langka)
        if skor_tertinggi < ambang_batas:
            prediksi_kelas = "Gejala Tidak Dikenal / Terindikasi Penyakit Langka"
                    
        return prediksi_kelas, prob_dict