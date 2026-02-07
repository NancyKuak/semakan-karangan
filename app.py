import streamlit as st
import google.generativeai as genai
from PIL import Image

# Konfigurasi Halaman
st.set_page_config(page_title="Sistem Semakan Karangan AI", layout="centered")

st.title("📝 Cikgu AI: Semakan Karangan")
st.write("Muat naik gambar latihan murid, dan AI akan menyemaknya berdasarkan rubrik.")

# Input API Key (Supaya lebih selamat, pengguna masukkan sendiri atau set di secrets)
api_key = st.text_input("Masukkan Google Gemini API Key anda:", type="password")

# Input Rubrik
default_rubric = """
1. Tatabahasa (30 markah): Ejaan, tanda baca, struktur ayat.
2. Isi Kandungan (40 markah): Relevansi idea, huraian, contoh.
3. Gaya Bahasa (30 markah): Kosa kata luas, penggunaan peribahasa, kesinambungan.
"""
rubric = st.text_area("Rubrik Pemarkahan:", value=default_rubric, height=150)

# Upload Gambar
uploaded_file = st.file_uploader("Upload Gambar Karangan (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None and api_key:
    # Papar Gambar
    image = Image.open(uploaded_file)
    st.image(image, caption='Gambar Karangan Murid', use_column_width=True)

    # Butang Semak
    if st.button("Semak Sekarang"):
        with st.spinner('Cikgu AI sedang membaca tulisan tangan...'):
            try:
                # Setup Gemini
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')

                # Prompt Arahan
                prompt = f"""
                Bertindak sebagai guru Bahasa Melayu yang berpengalaman. 
                Tugas anda adalah:
                1. Transkripsikan (baca) tulisan tangan dalam gambar ini.
                2. Semak karangan ini berdasarkan rubrik berikut:
                {rubric}

                Sila berikan output dalam format berikut:
                - **Markah Keseluruhan:** [Markah]/100
                - **Ulasan Terperinci:** (Pecahan markah ikut rubrik)
                - **Kesalahan & Pembetulan:** Senaraikan kesalahan tatabahasa/ejaan yang dikesan.
                - **Saranan:** Satu ayat semangat untuk murid.
                """

                # Hantar ke AI
                response = model.generate_content([prompt, image])
                
                # Papar Hasil
                st.success("Semakan Selesai!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Berlaku ralat: {e}")

elif uploaded_file is not None and not api_key:
    st.warning("Sila masukkan API Key dahulu.")
