import streamlit as st
from streamlit_extras.app_logo import add_logo
import pandas as pd
from PIL import Image
import prediction, prediction_clustering

page = st.sidebar.selectbox(label='Pilih Halaman ⬇️:', options=['📚 Beranda', '🏘️ Property Clustering', '🖥️ Estimasi Harga'])
     
if page == '📚 Beranda':
    st.write('')
    image = Image.open('logo.png')
    st.image(image, width = 800)
    st.write('')
    st.write('Property Prognosis membawa revolusi ke dunia real estate dengan memanfaatkan teknologi Machine Learning untuk memprediksi harga rumah secara akurat. Kami tidak hanya menawarkan estimasi harga yang handal, tetapi juga memberikan fungsionalitas unggul untuk mengelompokkan tipe rumah ke dalam klaster atau segmentasi yang tepat. Apa yang membuat Property Prognosis istimewa? Kami tidak hanya memberikan angka-angka, tetapi juga memberikan pemahaman mendalam tentang preferensi pembeli. Dengan menggunakan data yang kaya dan canggih, kami membantu Anda memahami perilaku pembeli potensial dengan lebih baik, memungkinkan Anda membuat keputusan yang lebih cerdas dan efektif.')
    st.write('')
    st.markdown('****')
    st.markdown("<h1 style='text-align: center; color: black;'>WELCOME</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: black;'>HOPE YOU ENJOY</h1>", unsafe_allow_html=True)
    st.write('')
    st.write('')
    st.subheader('Mardi Kurnianto 👨‍🎓')
    st.write('')
    st.subheader('Nicholas Halasan 👨‍🎓')
    st.write('')
    st.subheader('Taara Mona Theresia 👩‍🎓')
    st.write('')
    st.subheader('Zaky Ramdhani 👨‍🎓')
    st.markdown('****')
    st.caption('Property Prognosis tidak hanya sekadar aplikasi prediksi harga rumah, tetapi sebuah alat integral yang membantu Anda menjelajahi potensi pasar dengan lebih cermat dan efisien. Bergabunglah dengan kami di Property Prognosis dan buat keputusan properti Anda dengan percaya diri!')
elif page == '🏘️ Property Clustering':
    image = Image.open('house_type.png')
    st.image(image, width = 800)
    st.write('Identifikasi dan kelompokkan calon pembeli berdasarkan preferensi tipe rumah, memungkinkan Anda untuk menyesuaikan dengan karakteristik rumah yang anda cari.')
    st.markdown('****')
    st.markdown("<h1 style='text-align: center; color: green;'>Let's Try Here</h1>", unsafe_allow_html=True)
    prediction_clustering.run()
else:
    image = Image.open('harga_predict.png')
    st.image(image, width = 700)
    st.write('Prediksi Harga Akurat: Gunakan teknologi canggih kami untuk mendapatkan perkiraan harga rumah yang paling akurat, memberi Anda keunggulan dalam perencanaan dan penawaran')
    st.markdown('****')
    st.markdown("<h1 style='text-align: center; color: green;'>Let's Try Here</h1>", unsafe_allow_html=True)
    prediction.run()

