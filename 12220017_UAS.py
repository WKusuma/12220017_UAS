from pandas.core.frame import DataFrame
import streamlit as st
import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt
from matplotlib import cm, colors

##### Tittle
st.set_page_config(layout="wide")  # this needs to be the first Streamlit command called
st.title("Statistik Produksi Minyak Mentah Berbagai Negara")
st.markdown("**")

##### Sidebar
st.sidebar.title("Pengaturan")
left_col, right_col = st.columns(2)
col = st.columns(1)

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
left_col.header("A) Jumlah Produksi Minyak Suatu Negara")
left_col.subheader("Tabel representasi data")

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

left_col.dataframe(dfA)
left_col.pyplot(figA)


# B #
right_col.header("B) B-besar Negara dengan Produksi Minyak Terbesar pada Tahun T")
right_col.subheader(f"{n_tampil} Besar Negara dengan Jumlah Produksi Terbesar pada Tahun {tahun}")

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

right_col.dataframe(dfB.head(n_tampil))
right_col.pyplot(figB)


# C #
left_col.header("C) B-besar Negara dengan Jumlah Produksi Kumulatif Terbesar")
left_col.subheader(f"{n_tampil} Besar Negara dengan Jumlah Produksi Kumulatif Terbanyak")

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

left_col.dataframe(dfC.head(n_tampil))
left_col.pyplot(figC)


# D #
right_col.header("D) Summary")

#Bagian 1 (Produksi terbesar pada tahun T dan kumulatif)
##### Tahun T
right_col.subheader(f"Negara dengan jumlah Produksi Terbesar pada Tahun {tahun}")

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

right_col.markdown(f"Kode Negara: {kode_negara}")
right_col.markdown(f"Nama Negara: {nama}")
right_col.markdown(f"Region: {region}")
right_col.markdown(f"Sub-Region: {subregion}")
right_col.markdown(f"Produksi: {jumlah_produksi}")


##### Kumulatif
right_col.subheader("Negara dengan jumlah Produksi Terbesar pada Keseluruha Tahun")

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

right_col.markdown(f"Kode Negara: {kode_negara}")
right_col.markdown(f"Nama Negara: {nama}")
right_col.markdown(f"Region: {region}")
right_col.markdown(f"Sub-Region: {subregion}")
right_col.markdown(f"Produksi: {jumlah_produksi}")


# Bagian 2 (Produksi Terkecil !=0 pada Tahun T dan Kumulatif)
##### Tahun T
right_col.subheader(f"Negara dengan jumlah Produksi Terkecil (Tidak Sama dengan Nol) pada Tahun {tahun}")

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

right_col.markdown(f"Kode Negara: {kode_negara}")
right_col.markdown(f"Nama Negara: {nama}")
right_col.markdown(f"Region: {region}")
right_col.markdown(f"Sub-Region: {subregion}")
right_col.markdown(f"Produksi: {jumlah_produksi}")

##### Kumulatif
right_col.subheader("Negara dengan jumlah Produksi Terkecil (Tidak Sama dengan Nol) pada Keseluruha Tahun")

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

right_col.markdown(f"Kode Negara: {kode_negara}")
right_col.markdown(f"Nama Negara: {nama}")
right_col.markdown(f"Region: {region}")
right_col.markdown(f"Sub-Region: {subregion}")
right_col.markdown(f"Produksi: {jumlah_produksi}")


# Bagian 3 (Produksi = 0 pada Tahun T dan Kumulatif)
##### Tahun T
right_col.subheader(f"Negara dengan jumlah Produksi = 0 pada Tahun {tahun}")

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

df0T = pd.DataFrame(df0T, columns=['Negara','kode_negara','Region','Sub-Region'])
st.dataframe(df0T)


##### Kumulatif
right_col.subheader(f"Negara dengan jumlah Produksi = 0 Secara Kumulatif")

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

df0K = pd.DataFrame(df0K, columns=['Negara','kode_negara','Region','Sub-Region'])
st.dataframe(df0K)