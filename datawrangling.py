import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='darkgrid')

# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe
def create_monthly_service_df(df):
    monthly_service_df = df.groupby('bulan').agg({
        'jumlah_yang_dilayani': 'sum'
    }).reset_index()
    return monthly_service_df

def create_service_by_type_df(df):
    service_by_type_df = df.groupby('jenis_pelayanan').agg({
        'jumlah_yang_dilayani': 'sum'
    }).reset_index()
    return service_by_type_df

# Load dataset
kpem_df = pd.read_csv('kekerasan-perempuan.csv')

# Convert 'periode_data' to datetime
kpem_df['periode_data'] = pd.to_datetime(kpem_df['periode_data'], format='%Y%m')

# Create date-related columns
kpem_df['bulan'] = kpem_df['periode_data'].dt.month

# Filter data for Streamlit
min_date = kpem_df['periode_data'].min().date()
max_date = kpem_df['periode_data'].max().date()

with st.sidebar:
    st.image("./pictreadytouse.jpg")
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter the data based on selected dates
filtered_df = kpem_df[(kpem_df['periode_data'] >= pd.Timestamp(start_date)) & 
                      (kpem_df['periode_data'] <= pd.Timestamp(end_date))]

# Prepare various dataframes
monthly_service_df = create_monthly_service_df(filtered_df)
service_by_type_df = create_service_by_type_df(filtered_df)

# Streamlit app
st.title('Dashboard Analisis Data Kekerasan Terhadap Perempuan 2023 DKI Jakarta')

# Display initial data
st.subheader('Data Awal')
st.write(filtered_df.head())

# Statistics
st.subheader('Statistik Deskriptif')
st.write(filtered_df['jumlah_yang_dilayani'].describe())

# Monthly Service
st.subheader('Jumlah Korban Berdasarkan Bulan')
fig, ax = plt.subplots(figsize=(16, 8))
sns.lineplot(x='bulan', y='jumlah_yang_dilayani', data=monthly_service_df, marker='o', ax=ax)
ax.set_title('Jumlah Korban Berdasarkan Bulan', fontsize=20)
ax.set_xlabel('Bulan', fontsize=15)
ax.set_ylabel('Jumlah Korban', fontsize=15)
st.pyplot(fig)

# Service by Type
st.subheader('Jumlah Korban Berdasarkan Jenis Pelayanan')
fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(x='jumlah_yang_dilayani', y='jenis_pelayanan', data=service_by_type_df, palette='viridis', ax=ax)
ax.set_title('Jumlah Korban Berdasarkan Jenis Pelayanan', fontsize=20)
ax.set_xlabel('Jumlah Korban', fontsize=15)
ax.set_ylabel('Jenis Pelayanan', fontsize=15)
st.pyplot(fig)

# Total Statistics
total_cases = filtered_df['jumlah_yang_dilayani'].sum()
st.subheader('Total Statistik')
st.metric("Total Kasus", value=total_cases)

# Additional Insights
st.subheader('Insight Tambahan')
average_cases = filtered_df['jumlah_yang_dilayani'].mean()
st.metric("Rata-rata Kasus per Bulan", value=average_cases)

# Footer
st.caption('Copyright © 2023 Created Benzodiahmad')
