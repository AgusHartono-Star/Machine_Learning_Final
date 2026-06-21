import streamlit as st
import pandas as pd

class SapiUI:
    @staticmethod
    def inject_modern_css():
        """Menyuntikkan CSS Premium Cyber Glassmorphism & Fix Sidebar Bootstrap."""
        # CSS Utama dipindahkan ke sini agar terpusat dan tidak saling menimpa
        pass

    @staticmethod
    def render_banner(title, subtitle):
        st.markdown(f"""
            <div class='modern-banner'>
                <h1>{title}</h1>
                <p>{subtitle}</p>
            </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def render_kpi_metrics(total_kasus, total_hewan, hotspot, utama):
        st.markdown(f"""
            <div class='kpi-container'>
                <div class='kpi-card'>
                    <div class='kpi-title'>Total Kasus</div>
                    <div class='kpi-value'>📁 {total_kasus} Laporan</div>
                </div>
                <div class='kpi-card'>
                    <div class='kpi-title'>Populasi Terinfeksi</div>
                    <div class='kpi-value'>🐄 {total_hewan} Ekor</div>
                </div>
                <div class='kpi-card'>
                    <div class='kpi-title'>Zonasi Hotspot</div>
                    <div class='kpi-value'>📍 {hotspot}</div>
                </div>
                <div class='kpi-card'>
                    <div class='kpi-title'>Tren Penyakit</div>
                    <div class='kpi-value'>⚠️ {utama}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def render_hasil_diagnosa(hasil, konteks_teks):
        st.markdown(f"""
            <div class='diagnosa-box'>
                <span style='color: #F87171; font-weight: 700; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px;'>Hasil Analisis Komputasi Artificial Intelligence</span>
                <h2 style='margin: 8px 0 10px 0; color: #F8FAFC; font-size: 24px;'>🚨 {hasil}</h2>
                <p style='color: #E2E8F0; font-size: 14px; line-height: 1.6; margin: 0;'>{konteks_teks}</p>
            </div>
        """, unsafe_allow_html=True)