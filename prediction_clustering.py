import streamlit as st
import pandas as pd
import numpy as np
import pickle
import json
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.cluster import KMeans

# Load Model
with open('scaler_cluster.pkl', 'rb') as file_1:
  scaler = pickle.load(file_1)

with open('model_kmeans.pkl', 'rb') as file_2:
  km = pickle.load(file_2)

with open('model_pca.pkl', 'rb') as file_3:
  pca = pickle.load(file_3)

with open('onehot.pkl', 'rb') as file_4:
  ohe = pickle.load(file_4)

with open('list_kategorikal.txt', 'r') as file_5:
  kategorical = json.load(file_5)

with open('list_data_numerical.txt', 'r') as file_6:
  numerical = json.load(file_6)

#function run
def run() :
    data = pd.read_csv('melb_data.csv')
    with st.form('House Pricing Prediction'):
        rooms = st.selectbox('Pilih Jumlah Ruangan:', data['Rooms'].unique())
        type = st.selectbox('Pilih Tipe Properti:', data['Type'].unique())
        price = st.number_input('Price', min_value=0, max_value=9000000)
        method = st.selectbox('Pilih Status Lelang:', data['Method'].unique())
        cbddist = st.number_input('Masukan Jarak properti dengan CBD', min_value=0, max_value=48,value=0, help ='Menunjukkan Properti ke Kawasan Pusat Bisnis (Miles)')
        bedroom = st.selectbox('Pilih Jumlah Kamar Tidur:', data['Bedroom2'].unique())
        bathroom = st.selectbox('Pilih Jumlah Kamar Mandi:', data['Bathroom'].unique())
        car = st.number_input('Jumlah Parkir Mobil', min_value=0, max_value=10, value=0)
        landsize = st.number_input('Luas Tanah Properti', min_value=0, max_value=450000, value=0, help ='Menunjukkan Luas Tanah (Meter Persegi)')
        buildingarea = st.number_input('Luas Bangunan', min_value=0, max_value=45000, value=0, help ='Menunjukkan Luas Bangunan / Properti (Meter Persegi)')
        yearbuilt =  st.number_input('Tahun Properti Dibangun', min_value=1196, max_value=2018)
        propertycount =  st.number_input('Jumlah Properti di sekitar', min_value=250, max_value=22000)
        
        submitted = st.form_submit_button('Predict')

    data_inf = {
        'Rooms': rooms,
        'Type':type,
        'Price':price,
        'Method' : method,
        'Distance': cbddist,
        'Bedroom2': bedroom,
        'Bathroom' : bathroom,
        'Car': car,
        'Landsize': landsize,
        'BuildingArea': buildingarea,
        'YearBuilt': yearbuilt,
        'Propertycount': propertycount
    }
    
    data_inf = pd.DataFrame([data_inf])
    st.dataframe(data_inf)

    if submitted:
        data_inf_num = data_inf[numerical]
        data_inf_cat = data_inf[kategorical]
        data_inf_num_scaled = scaler.transform(data_inf_num)
        data_inf_cat_encoded = ohe.transform(data_inf_cat)
        data_inf_final = np.concatenate([data_inf_num_scaled, data_inf_cat_encoded], axis=1)

        y_pca_inf = pca.transform(data_inf_final)

        y_pred_inf = km.predict(y_pca_inf)

        st.write('#Prediksi Cluster : ', str(int(y_pred_inf)))


if __name__ == '__main__':
    run()
