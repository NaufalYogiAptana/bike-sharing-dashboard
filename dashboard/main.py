import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Dashboard Analisis Penyewaan Sepeda")
st.sidebar.title("Dashboard by Naufal Yogi Aptana")
st.sidebar.markdown("[GitHub](https://github.com/NaufalYogiAptana)")
st.sidebar.markdown("[LinkedIn](https://www.linkedin.com/in/naufalyogiaptana)")

# Memuat Data
@st.cache_data
def load_data():
    return pd.read_csv('./data_clean.csv')

df = load_data()

# Tren Bulanan
df['dteday'] = pd.to_datetime(df['dteday'])
df['year_month'] = df['dteday'].dt.to_period('M')
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

st.markdown("- Dibandingkan tahun 2011, jumlah penyewaan di tahun 2012 mengalami peningkatan. Penyewaan mulai meningkat tajam sejak Maret 2012, dengan puncak di pertengahan tahun, terutama di bulan Agustus dan September.")

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

st.markdown("- Sebagian besar penyewaan dilakukan oleh pengguna terdaftar (registered), yang menyumbang 81,2% dari total penyewaan, sedangkan penyewaan oleh pengguna casual hanya mencakup 18,8% dari total penyewaan.")

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

st.markdown("- Jumlah penyewaan sepeda menunjukkan pola musiman yang jelas. Penyewaan cenderung meningkat pada musim semi dan musim panas dan menurun pada musim dingin.")

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

st.markdown("- Terdapat dua puncak utama dalam aktivitas penyewaan sepeda di setiap musim, yaitu pada pagi hari sekitar pukul 08:00 dan sore hari sekitar pukul 17:00. Pola ini kemungkinan besar mencerminkan waktu perjalanan pulang-pergi kerja atau sekolah.")