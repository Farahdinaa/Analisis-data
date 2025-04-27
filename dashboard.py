import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import datetime
from io import BytesIO

# data hour
df = pd.read_csv("hour.csv")
df['dteday'] = pd.to_datetime(df['dteday'])

# buat judul
st.set_page_config(page_title="Dashboard Penyewaan Sepeda", layout="wide", initial_sidebar_state="expanded")
st.title("DASHBOARD PENYEWAAN SEPEDA")

# filter tanggal
with st.sidebar:
    st.image("gambar.png", caption="Bike Sharing Dashboard")
    min_date = df['dteday'].min()
    max_date = df['dteday'].max()
    start_date, end_date = st.date_input(
        "Rentang Waktu",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

# jumlah sepeda menurut bulan
filtered_df = df[(df['dteday'] >= pd.to_datetime(start_date)) & (df['dteday'] <= pd.to_datetime(end_date))]
monthly_usage = filtered_df.groupby(filtered_df['dteday'].dt.month)['cnt'].mean().reset_index()
monthly_usage.rename(columns={'dteday': 'month', 'cnt': 'average_count'}, inplace=True)
monthly_usage['month'] = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']

max_month = monthly_usage.loc[monthly_usage['average_count'].idxmax()]

st.header("Penggunaan Sepeda Bulanan")

# buat 2 kolom atas
col1, col2 = st.columns(2)
with col1:
    st.metric(
        label="Bulan dengan penggunaan terbanyak",
        value=max_month['month'],
    )

with col2:
    st.metric(
        label="Jumlah",
        value=f"{max_month['average_count']:.2f}"
    )

# Membuat grafik  Sepeda tiap Bulanan
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(monthly_usage['month'], monthly_usage['average_count'], color=plt.cm.rainbow(np.linspace(0, 1, len(monthly_usage))))

ax.set_title("Rata-rata Penggunaan Sepeda Tiap Bulan", fontsize=14)  
ax.set_xlabel("Bulan", fontsize=12)  
ax.set_ylabel("Jumlah sepeda", fontsize=12)
ax.tick_params(axis='x', rotation=45) 
ax.tick_params(axis='y') 

for p in ax.patches:
    ax.annotate(f"{p.get_height():.1f}", (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', fontsize=10, color='black', xytext=(0, 5), textcoords='offset points')

st.pyplot(fig)

# penggunaan sepeda pada hari kerja dan libur
daily_usage = filtered_df.groupby('workingday')['cnt'].mean()
day_labels = ['Libur', 'Kerja']

st.header("Penggunaan Sepeda: Hari Kerja dan Hari Libur")

# kolom atasnya
col1, col2 = st.columns(2)
with col1:
    st.metric(
        label="Hari Libur",
        value=f"{daily_usage[0]:.2f}"
    )

with col2:
    st.metric(
        label="Hari Kerja",
        value=f"{daily_usage[1]:.2f}"
    )

# Buat grafik
fig, ax = plt.subplots(figsize=(8, 6))
ax.bar(day_labels, daily_usage, color=['#FF69B4', '#1E90FF'])
ax.set_title("Rata-rata Penggunaan Sepeda", fontsize=14)
ax.set_xlabel("Hari", fontsize=12)
ax.set_ylabel("Jumlah Pengguna", fontsize=12)
ax.tick_params(axis='x', rotation=0)  
ax.tick_params(axis='y')
for p in ax.patches:
    ax.annotate(f"{p.get_height():.1f}", (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', fontsize=10, color='black', xytext=(0, 5), textcoords='offset points')

st.pyplot(fig)

# Pengaruh Suhu terhadap Penggunaan Sepeda
st.header("Pengaruh Suhu terhadap Penggunaan Sepeda")

# Mengelompokkan data rendah, sedang, dan tinggi
cnt_temp = filtered_df[['cnt', 'temp']]
cnt_temp['suhu'] = pd.cut(cnt_temp['temp'], bins=[0, 0.3, 0.6, 1.0], labels=['Rendah', 'Sedang', 'Tinggi'], right=False)
suhu_cnt = cnt_temp.groupby('suhu')['cnt'].mean().reset_index()

# Membuat grafik
fig = px.bar(
    suhu_cnt, 
    x='suhu', 
    y='cnt', 
    color='suhu',
    title='Pengaruh Suhu terhadap Jumlah Pengguna Sepeda',
    labels={'cnt': 'Rata-rata Sepeda'},
    color_discrete_sequence=['#FF69B4', '#1E90FF', '#98FB98'],
    template='plotly_white'
)

# buat angka di atas grafik
for index, row in suhu_cnt.iterrows():
    fig.add_annotation(
        text=f"{row['cnt']:.2f}", 
        x=row['suhu'],
        y=row['cnt'] + 5,
        showarrow=False,
        font=dict(size=14, color='black'),
        align="center"
    )

fig.update_layout(
    title=dict(
        text="Pengaruh Suhu terhadap Jumlah Sepeda",
        x=0.5, 
        xanchor="center",
        font=dict(size=16, color='black')
    ),
    xaxis_title_font=dict(color='black'),
    yaxis_title_font=dict(color='black'),
    legend_title_font=dict(color='black'),
    font=dict(color='black'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        showgrid=False,
    ),
    yaxis=dict(
        showgrid=False
    ),
    showlegend=False,
    xaxis_linecolor='black',
    yaxis_linecolor='black',
)

st.plotly_chart(fig, use_container_width=False, key="grafik_suhu")