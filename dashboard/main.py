import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Dashboard Analisis Penyewaan Sepeda")
st.sidebar.title("Dashboard by Naufal Yogi Aptana")
st.sidebar.markdown("[GitHub](https://github.com/NaufalYogiAptana)")
st.sidebar.markdown("[LinkedIn](https://www.linkedin.com/in/naufalyogiaptana)")

# Memuat Data
df = pd.read_csv('dashboard/data_clean.csv')
df['dteday'] = pd.to_datetime(df['dteday'])
df['year_month'] = df['dteday'].dt.to_period('M')

# Filter berdasarkan rentang tanggal
date_range = st.sidebar.date_input("Pilih Rentang Tanggal", [df['dteday'].min(), df['dteday'].max()])
if len(date_range) == 2:
    start_date, end_date = date_range
    df = df[(df['dteday'] >= pd.Timestamp(start_date)) & (df['dteday'] <= pd.Timestamp(end_date))]

# Filter berdasarkan musim
season_filter = st.sidebar.multiselect("Pilih Musim", df['season'].unique(), df['season'].unique())
df = df[df['season'].isin(season_filter)]

# Tren Bulanan
monthly_trend = df.groupby('year_month')[['casual', 'registered', 'cnt']].sum()

st.subheader("Tren Penyewaan Sepeda per Bulan")
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(monthly_trend.index.astype(str), monthly_trend['casual'], marker='o', label='Casual')
ax.plot(monthly_trend.index.astype(str), monthly_trend['registered'], marker='s', label='Registered')
ax.plot(monthly_trend.index.astype(str), monthly_trend['cnt'], marker='d', label='Total')
plt.xticks(rotation=45)
plt.xlabel("Bulan")
plt.ylabel("Jumlah Penyewa Sepeda")
plt.legend()
st.pyplot(fig)

# Pie Chart
st.subheader("Perbandingan Penyewaan Casual vs Registered")
total_casual = df['casual'].sum()
total_registered = df['registered'].sum()
labels = ['Casual', 'Registered']
sizes = [total_casual, total_registered]

fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, shadow=True)
plt.title("Perbandingan Penyewaan Casual vs Registered")
st.pyplot(fig)

# Pola Musiman
st.subheader("Pola Musiman Penyewaan Sepeda")
seasonal_trend = df.groupby('season')[['casual', 'registered', 'cnt']].sum()

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(seasonal_trend.index, seasonal_trend['casual'], label='Casual')
ax.bar(seasonal_trend.index, seasonal_trend['registered'], bottom=seasonal_trend['casual'], label='Registered')
plt.xlabel("Musim")
plt.ylabel("Jumlah Penyewa")
plt.legend()
st.pyplot(fig)

# Tren Per Jam Berdasarkan Musim
st.subheader("Tren Penyewaan Sepeda per Jam Berdasarkan Musim")
fig, ax = plt.subplots(figsize=(10, 6))
for season in df['season'].unique():
    hourly_trend = df[df['season'] == season].groupby('hr')['cnt'].mean()
    ax.plot(hourly_trend.index, hourly_trend.values, marker='o', label=f"Musim {season}")
plt.xlabel("Jam")
plt.ylabel("Rata-rata Jumlah Penyewa")
plt.legend()
st.pyplot(fig)
