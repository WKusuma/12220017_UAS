import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame
import streamlit as st
import numpy as np
import pandas as pd
import json
from matplotlib import cm, colors
from PIL import Image

##### Tittle
st.set_page_config(layout="wide")  # this needs to be the first Streamlit command called
st.title("Statistik Produksi Minyak Mentah Berbagai Negara")


##### Sidebar
image = Image.open('logo_itb_1024.png')
st.sidebar.image(image)

st.sidebar.markdown("Wijaya Kusuma")
st.sidebar.markdown("12220017")
st.sidebar.title("Pengaturan")
col1, col2, col3 = st.columns(3)

##### Read Data CSV dan ubah ke data frame
csv = pd.read_csv("produksi_minyak_mentah.csv")
df = pd.DataFrame(csv)

kode_csv = list(df['kode_negara'].unique())
#print(f"kode_negara: {kode_csv}")

total_produksi = []
for c in kode_csv:
    produksi = df[df['produksi']==c]['produksi'].astype(float)
    total_produksi.append(produksi.sum())
#print(f"Total produksi: {total_produksi}")

##### Read Data Json
with open ("kode_negara_lengkap.json") as f:
    file_json = json.load(f)
df2 = pd.DataFrame(file_json)

##### Mengambil value alpha-3 dan mengubahnya menjadi list
#kode_json = list(map(lambda kode_json: kode_json['alpha-3'], file_json))
kode_json = df2['alpha-3'].tolist()
#print(kode_json)

##### Mengambil value name dan mengubahnya menjadi list
#nama_negara = list(map(lambda nama_negara: nama_negara['name'], file_json))
nama_negara = df2['name'].tolist()
#print(nama_negara)

##### User inputs on the control panel
st.sidebar.subheader("Pengaturan konfigurasi tampilan")
list_kode=[]
for k in kode_csv:
    if k not in kode_json:
        continue
    list_kode.append(k)
#print(list_kode)

##### Menghilangkan yang bukan Negara
for v in kode_csv:
    if v in list_kode:
        continue
    df = df[df.kode_negara != v]
#print(df)

##### Membuat list nama-nama Negara
list_negara=[]
for i in file_json:
    if i['alpha-3'] not in list_kode:
        continue
    list_negara.append(i['name'])
#print(list_negara)

##### User input
negara = st.sidebar.selectbox("Pilih Negara", list_negara)
kode = df2[df2['name']==negara]['alpha-3'].tolist()[0]
n_tampil = st.sidebar.number_input("Jumlah baris dalam tabel yang ditampilkan", min_value=1, max_value=len(list_kode), value=10)

list_tahun = list(df['tahun'].unique())
tahun = st.sidebar.selectbox("Pilih Tahun", list_tahun)

##### APLIKASI #####

# A #
dfA = pd.DataFrame(df, columns=['kode_negara', 'tahun', 'produksi'])
dfA = dfA.loc[dfA['kode_negara']==kode]
dfA['produksi'] = pd.to_numeric(dfA['produksi'], errors='coerce')

figA, ax = plt.subplots()
ax.plot(dfA['tahun'], dfA['produksi'], label = negara)
ax.set_title("Grafik Jumlah Produksi terhadap Tahun")
ax.set_xlabel("Tahun", fontsize = 13)
ax.set_ylabel("Jumlah Produksi", fontsize = 13)
ax.legend(fontsize = 10)
#st.pyplot(fig)

with col1:
    col1.subheader("A) Jumlah Produksi Minyak Suatu Negara")
    col1.markdown("Tabel representasi data")
    col1.dataframe(dfA)
    col1.pyplot(figA)

# B #
dfB = pd.DataFrame(df,columns= ['kode_negara','tahun','produksi'])
dfB = dfB.loc[dfB['tahun']==tahun]
dfB['produksi'] = pd.to_numeric(dfB['produksi'], errors='coerce')
dfB = dfB.sort_values(by='produksi', ascending = False)

figB, ax = plt.subplots()
cmap = cm.get_cmap('tab10')
colors = cmap.colors[:len(list_negara)]
ax.bar(dfB['kode_negara'].head(n_tampil), dfB['produksi'].head(n_tampil) ,label=list_negara, color=colors)
ax.set_title(f'Grafik Jumlah Produksi Minyak {n_tampil} besar Negara pada Tahun {tahun}')
ax.set_xlabel("Kode Negara", fontsize=13)
ax.set_ylabel("Jumlah Produksi", fontsize=13)
#st.pyplot(figB)

with col2:
    col2.subheader("B) B-besar Negara dengan Produksi Minyak Terbesar pada Tahun T")
    col2.markdown(f"{n_tampil} Besar Negara dengan Jumlah Produksi Terbesar pada Tahun {tahun}")
    col2.dataframe(dfB.head(n_tampil))
    col2.pyplot(figB)


# C #
total_produksi = []
for c in list_kode:
    produksi = df[df['kode_negara']==c]['produksi'].astype(float)
    total_produksi.append(produksi.sum())
#print(f"Total produksi: {total_produksi}")

dfC = pd.DataFrame(list(zip(list_kode, total_produksi)), columns=['kode_negara', 'total_produksi'])
dfC = dfC.sort_values(by=['total_produksi'], ascending=False)
#print(dfC)

figC, ax = plt.subplots()
cmap = cm.get_cmap('tab20')
colors = cmap.colors[:len(list_negara)]
ax.bar(dfC['kode_negara'].head(n_tampil), dfC['total_produksi'].head(n_tampil), label=negara, color=colors)
ax.set_title(f'Grafik Jumlah Produksi Minyak \n {n_tampil} besar Negara Secara Kumulatif')
ax.set_xlabel("Kode Negara", fontsize=13)
ax.set_ylabel("Jumlah Produksi Kumulatif", fontsize=13)
#st.pyplot(figC)

with col3:
    col3.subheader("C) B-besar Negara dengan Jumlah Produksi Kumulatif Terbesar")
    col3.markdown(f"{n_tampil} Besar Negara dengan Jumlah Produksi Kumulatif Terbanyak")
    col3.dataframe(dfC.head(n_tampil))
    col3.pyplot(figC)


# D #
col1.header("D) Summary")

#Bagian 1 (Produksi terbesar pada tahun T dan kumulatif)
##### Tahun T
jumlah_produksi = dfB[:1].iloc[0]['produksi']
kode_negara = dfB[:1].iloc[0]['kode_negara']
nama = []
region = []
subregion = []

for i in range(len(df2)):
    if list(df2['alpha-3'])[i]==kode_negara:
        nama = list(df2['name'])[i]
        region = list(df2['region'])[i]
        subregion = list(df2['sub-region'])[i]

with st.container():
    col1.subheader(f"Negara dengan jumlah Produksi Terbesar pada Tahun {tahun}")
    col1.markdown(f"Kode Negara: {kode_negara}")
    col1.markdown(f"Nama Negara: {nama}")
    col1.markdown(f"Region: {region}")
    col1.markdown(f"Sub-Region: {subregion}")
    col1.markdown(f"Produksi: {jumlah_produksi}")

##### Kumulatif
jumlah_produksi = dfC[:1].iloc[0]['total_produksi']
kode_negara = dfC[:1].iloc[0]['kode_negara']
nama = []
region = []
subregion = []

for i in range(len(df2)):
    if list(df2['alpha-3'])[i]==kode_negara:
        nama = list(df2['name'])[i]
        region = list(df2['region'])[i]
        subregion = list(df2['sub-region'])[i]

with st.container():
    col2.subheader("Negara dengan jumlah Produksi Terbesar pada Keseluruhan Tahun")
    col2.markdown(f"Kode Negara: {kode_negara}")
    col2.markdown(f"Nama Negara: {nama}")
    col2.markdown(f"Region: {region}")
    col2.markdown(f"Sub-Region: {subregion}")
    col2.markdown(f"Produksi: {jumlah_produksi}")


# Bagian 2 (Produksi Terkecil !=0 pada Tahun T dan Kumulatif)
##### Tahun T
dfkT = dfB[dfB.produksi !=0]
dfkT = dfkT.sort_values(by=['produksi'],ascending=True)
jumlah_produksi = dfkT[:1].iloc[0]['produksi']
kode_negara = dfkT[:1].iloc[0]['kode_negara']
nama = []
region = []
subregion = []
                                    
for i in range(len(df2)):
    if list(df2['alpha-3'])[i]==kode_negara:
        nama = list(df2['name'])[i]
        region = list(df2['region'])[i]
        subregion  = list(df2['sub-region'])[i]

with st.container():
    col3.subheader(f"Negara dengan jumlah Produksi Terkecil (Tidak Sama dengan Nol) pada Tahun {tahun}")
    col3.markdown(f"Kode Negara: {kode_negara}")
    col3.markdown(f"Nama Negara: {nama}")
    col3.markdown(f"Region: {region}")
    col3.markdown(f"Sub-Region: {subregion}")
    col3.markdown(f"Produksi: {jumlah_produksi}")

##### Kumulatif
dfk = dfC[dfC.total_produksi !=0]
dfk = dfk.sort_values(by=['total_produksi'],ascending=True)
jumlah_produksi = dfk[:1].iloc[0]['total_produksi']
kode_negara = dfk[:1].iloc[0]['kode_negara']
nama = []
region = []
subregion = []

for i in range(len(df2)):
    if list(df2['alpha-3'])[i]==kode_negara:
        nama = list(df2['name'])[i]
        region = list(df2['region'])[i]
        subregion = list(df2['sub-region'])[i]

with st.container():
    col1.subheader("Negara dengan jumlah Produksi Terkecil (Tidak Sama dengan Nol) pada Keseluruhan Tahun")
    col1.markdown(f"Kode Negara: {kode_negara}")
    col1.markdown(f"Nama Negara: {nama}")
    col1.markdown(f"Region: {region}")
    col1.markdown(f"Sub-Region: {subregion}")
    col1.markdown(f"Produksi: {jumlah_produksi}")


# Bagian 3 (Produksi = 0 pada Tahun T dan Kumulatif)
##### Tahun T
df0T = dfB[dfB.produksi ==0]
nama = []
region = []
subregion = []

for i in range(len(df0T)):
    for j in range(len(df2)):
        if list(df0T['kode_negara'])[i]==list(df2['alpha-3'])[j]:
            nama.append(list(df2['name'])[j])
            region.append(list(df2['region'])[j])
            subregion.append(list(df2['sub-region'])[j])

df0T ['Negara'] = nama
df0T ['Region'] = region
df0T ['Sub-Region'] = subregion

with st.container():
    col2.subheader(f"Negara dengan jumlah Produksi = 0 pada Tahun {tahun}")
    df0T = pd.DataFrame(df0T, columns=['Negara','kode_negara','Region','Sub-Region'])
    col2.dataframe(df0T)


##### Kumulatif
df0K = dfC[dfC.total_produksi ==0]
nama = []
region = []
subregion = []

for i in range(len(df0K)):
    for j in range(len(df2)):
        if list(df0K['kode_negara'])[i]==list(df2['alpha-3'])[j]:
            nama.append(list(df2['name'])[j])
            region.append(list(df2['region'])[j])
            subregion.append(list(df2['sub-region'])[j])

df0K ['Negara'] = nama
df0K ['Region'] = region
df0K ['Sub-Region'] = subregion

with st.container():
    col3.subheader(f"Negara dengan jumlah Produksi = 0 Secara Kumulatif")
    df0K = pd.DataFrame(df0K, columns=['Negara','kode_negara','Region','Sub-Region'])
    col3.dataframe(df0K)
