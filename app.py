import streamlit as st
import pandas as pd

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard Keuangan", layout="wide")

st.title("💰 Dashboard Keuangan Pribadi")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("data_keuangan_banyak.csv")

data = load_data()

# Sidebar filter
st.sidebar.header("Filter Data")

jenis = st.sidebar.multiselect(
    "Pilih Jenis Transaksi (kosongkan untuk tampilkan semua)",
    options=data["Jenis"].unique()
)

kategori = st.sidebar.multiselect(
    "Pilih Kategori (kosongkan untuk tampilkan semua)",
    options=data["Kategori"].unique()
)

# Filter berdasarkan input user
filtered_data = data.copy()

if jenis:
    filtered_data = filtered_data[filtered_data["Jenis"].isin(jenis)]

if kategori:
    filtered_data = filtered_data[filtered_data["Kategori"].isin(kategori)]

# Ringkasan Keuangan
st.subheader("Ringkasan Keuangan")

total_pendapatan = filtered_data[filtered_data["Jenis"] == "Pendapatan"]["Nominal"].sum()
total_pengeluaran = filtered_data[filtered_data["Jenis"] == "Pengeluaran"]["Nominal"].sum()
saldo = total_pendapatan - total_pengeluaran

col1, col2, col3 = st.columns(3)
col1.metric("Total Pendapatan", f"Rp {total_pendapatan:,.0f}")
col2.metric("Total Pengeluaran", f"Rp {total_pengeluaran:,.0f}")
col3.metric("Saldo Akhir", f"Rp {saldo:,.0f}")

# Grafik Transaksi
st.subheader("Grafik Transaksi per Kategori")
if not filtered_data.empty:
    chart_data = filtered_data.groupby(["Kategori", "Jenis"])["Nominal"].sum().unstack(fill_value=0)
    st.bar_chart(chart_data)
else:
    st.info("Tidak ada data untuk ditampilkan. Coba ubah filter di samping.")

# Tabel Data
st.subheader("Data Transaksi")
st.dataframe(
    filtered_data.sort_values("Tanggal", ascending=False),
    use_container_width=True
)
