import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

def create_station_pm25_df(df):
    station_pm25_df = df.groupby("station")["PM2.5"].mean().sort_values(ascending=False).reset_index()
    return station_pm25_df

# Load data yang sudah bersih
all_df = pd.read_csv("dashboard/main_data.csv")

all_df["datetime"] = pd.to_datetime(all_df["datetime"])

st.header('Air Quality Dashboard :wind_facing_face:')

st.sidebar.title("Filter Stasiun")
stasiun_list = all_df['station'].unique()
stasiun_pilihan = st.sidebar.multiselect("Pilih Stasiun:", options=stasiun_list, default=stasiun_list)

main_df = all_df[all_df["station"].isin(stasiun_pilihan)]

# 1. Visualisasi Rata-rata PM2.5 per Stasiun
st.subheader("Rata-rata Konsentrasi PM2.5 per Stasiun")
station_pm25 = create_station_pm25_df(main_df)

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(
    x="PM2.5", 
    y="station", 
    data=station_pm25, 
    palette="viridis",
    ax=ax
)
ax.set_title("Rata-rata PM2.5 (2013-2017)", fontsize=15)
ax.set_xlabel("Konsentrasi (µg/m³)")
ax.set_ylabel("Stasiun")
st.pyplot(fig)

# 2. Visualisasi Heatmap Korelasi
st.subheader("Matriks Korelasi: PM10 vs Variabel Cuaca")
corr_matrix = main_df[['PM10', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']].corr()

fig_corr, ax_corr = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", ax=ax_corr)
st.pyplot(fig_corr)

st.caption('Copyright (C) Danis Keysara Saputra 2026')