import streamlit as st
import pandas as pd

class SapiUI:
    @staticmethod
    def inject_modern_css():
        """Menyuntikkan CSS bergaya Modern Minimalis & Responsif Mobile."""
        st.markdown("""
            <style>
            /* Reset & Font Global */
            html, body, [data-testid="stAppViewContainer"] {
                background-color: ##4d4d4d !important;
                font-family: 'Inter', -apple-system, sans-serif;
            }
            
            /* Banner Header Modern */
            .modern-banner {
                background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
                padding: 30px 20px;
                border-radius: 16px;
                color: white;
                text-align: center;
                margin-bottom: 25px;
                box-shadow: 0 4px 20px rgba(59, 130, 246, 0.15);
            }
            .modern-banner h1 { color: white !important; font-size: 28px !important; font-weight: 700; margin: 0; }
            .modern-banner p { color: #E2E8F0 !important; font-size: 14px; margin-top: 8px; margin-bottom: 0; }
            
            /* Metrik Card Finansial/SaaS Dashboard */
            .kpi-container {
                display: flex;
                flex-wrap: wrap;
                gap: 15px;
                margin-bottom: 20px;
            }
            .kpi-card {
                flex: 1;
                min-width: 200px; /* Menjamin pembagian grid rapi di HP */
                background: white;
                padding: 20px;
                border-radius: 12px;
                border: 1px solid #E2E8F0;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
                transition: transform 0.2s;
            }
            .kpi-card:hover { transform: translateY(-2px); }
            .kpi-title { font-size: 13px; color: #64748B; text-transform: uppercase; font-weight: 600; margin-bottom: 5px;}
            .kpi-value { font-size: 24px; font-weight: 700; color: #0F172A; }
            
            /* Hasil Diagnosa Box */
            .diagnosa-box {
                background: white;
                border-left: 6px solid #EF4444;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
                margin-top: 15px;
            }
            </style>
        """, unsafe_allow_html=True)

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
                    <div class='kpi-title'>Total Laporan</div>
                    <div class='kpi-value'>📁 {total_kasus} Kasus</div>
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
                    <div class='kpi-title'>Tren Diagnosa</div>
                    <div class='kpi-value'>⚠️ {utama}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def render_hasil_diagnosa(hasil, konteks_teks):
        st.markdown(f"""
            <div class='diagnosa-box'>
                <span style='color: #DC2626; font-weight: 700; font-size: 12px; uppercase;'>Hasil Analisis Artificial Intelligence</span>
                <h2 style='margin: 5px 0 10px 0; color: #1E293B; font-size: 24px;'>🚨 {hasil}</h2>
                <p style='color: #475569; font-size: 14px; margin: 0; line-height: 1.5;'>{konteks_teks}</p>
            </div>
        """, unsafe_allow_html=True)