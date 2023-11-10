import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load all files
with open('best_model.pkl', 'rb') as file_1:
    model_rfr_best = pickle.load(file_1)

def run():
    # Membuat Form
    with st.form(key='Form'):
        type = st.selectbox(label='Type', options=['h', 'u', 't'], help='- h : rumah, pondok, villa, semi, teras, -u : unit, dupleks, -t : cluster, komplek')
        method = st.selectbox(label='Method', options=['S', 'SP', 'PI', 'VB', 'SA'], help='-PI: Properti tidak terjual karena tidak mencapai harga reserve, -S: Properti terjual di lelang, -SA: Properti terjual setelah lelang selesai, -SP: Properti terjual sebelum lelang dimulai, -VB: Penawaran yang diajukan oleh penjual (vendor) untuk mendorong harga naik')
        distance = st.number_input('Distance', min_value=1, max_value=50, value=1, help='Jarak properti ke pusat bisnis Melbourne(km)')
        car = st.number_input('Car', min_value=0, max_value=10, value=0, help='Jumlah tempat parkir mobil')
        landsize = st.slider('Land Size', 0, 450000, 0, help='Ukuran Lahan(m2)')
        buildingarea = st.slider('Building Area', 0, 45000, 0, help='Luas Bangunan(m2)')
        bedroom = st.number_input('Bedroom2', min_value=0, max_value=20, value=0, help='Jumlah kamar tidur')
        bathroom = st.number_input('Bathroom', min_value=1, max_value=8, value=1, help='Jumlah kamar mandi')

        # Menambahkan tombol submit di dalam form
        submitted = st.form_submit_button('Predict')

    data_inf = {
        'Type': type,
        'Method': method,
        'Distance': distance,
        'Car': car,
        'Landsize': landsize,
        'BuildingArea': buildingarea,
        'Bedroom2': bedroom,
        'Bathroom': bathroom
    }

    data_inf = pd.DataFrame([data_inf])
    st.dataframe(data_inf)

    if submitted:
        # Membuat kolom predict
        y_pred_inf = model_rfr_best.predict(data_inf)
        st.write('# Harga: ', str(int(y_pred_inf[0])))

if __name__ == '__main__':
    run()
