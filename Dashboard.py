import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# Load dataset
day_df = pd.read_csv('day_cleaned.csv')

# Konversi kolom tanggal ke tipe datetime
day_df["date"] = pd.to_datetime(day_df["date"])

# Filter tanggal dari dataset
min_date = day_df["date"].min()
max_date = day_df["date"].max()

# Sidebar untuk filter
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://thumbs.dreamstime.com/z/bike-sharing-thin-line-icon-bicycle-pointers-logo-rental-service-modern-vector-illustration-195163820.jpg")
    
    # Pastikan date_input mengembalikan tuple berisi 2 nilai
    date_selection = st.date_input(
        label="Rentang Waktu",
        min_value=min_date.date(),
        max_value=max_date.date(),
        value=(min_date.date(), max_date.date()),  
        key="date_range"
    )

    # Jika hanya 1 nilai dipilih, set start_date = end_date
    if isinstance(date_selection, tuple) and len(date_selection) == 2:
        start_date, end_date = date_selection
    else:
        start_date = end_date = date_selection

# Konversi start_date & end_date ke datetime64
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter berdasarkan tanggal (menggunakan normalize untuk dibandingkan dengan Timestamp)
main_df = day_df[(day_df["date"].dt.normalize() >= start_date) & 
                 (day_df["date"].dt.normalize() <= end_date)]

# Menampilkan total penyewaan
total_rentals = main_df["count"].sum()
st.sidebar.write(f"### Total Penyewaan Sepeda: {total_rentals}")

 # Menambahkan fitur pemilihan satu hari
st.markdown("### 🔍 Lihat Penyewaan di Hari Tertentu")
selected_day = st.date_input("Pilih Tanggal", min_date.date(), min_value=min_date.date(), max_value=max_date.date())

# Konversi selected_day ke datetime64
selected_day = pd.to_datetime(selected_day)

# Filter data berdasarkan tanggal yang dipilih
selected_day_df = day_df[day_df["date"].dt.normalize() == selected_day]

# Menampilkan jumlah penyewaan di hari yang dipilih
if not selected_day_df.empty:
     rental_count = selected_day_df["count"].values[0]
     st.write(f"🚲 **Jumlah Penyewaan pada {selected_day.strftime('%d %B %Y')}:** {rental_count} sepeda")
else:
     st.warning("⚠ Tidak ada data untuk tanggal ini.")

# Menampilkan data yang sudah difilter
st.dataframe(main_df)

# Judul Dashboard
st.header('Bike Sharing Dashboard 🚲')
st.subheader('Tren Harian Penyewaan Sepeda')

# Sidebar untuk memilih visualisasi
st.sidebar.title("Dashboard Penyewaan Sepeda")
option = st.sidebar.selectbox("Pilih Visualisasi:", [
    "Tren Penyewaan Sepeda", 
    "Distribusi Penyewaan Berdasarkan Hari", 
    "Pengaruh Cuaca terhadap Penyewaan", 
    "Analisis Hubungan dan Kategori Penyewaan"
])

st.title(option)

# 1. Tren Penyewaan Sepeda Sepanjang Waktu
if option == "Tren Penyewaan Sepeda":
    if not main_df.empty:
        fig, ax = plt.subplots(figsize=(10, 5))
        main_df.set_index("date")["count"].plot(ax=ax, color='b', alpha=0.7)
        ax.set_title("Tren Penyewaan Sepeda")
        ax.set_ylabel("Jumlah Penyewaan")
        ax.set_xlabel("Tanggal")
        st.pyplot(fig)

        st.subheader("📊 Tren Penyewaan Sepeda per Bulan (Perbandingan 2011 & 2012)")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(data=main_df, x="month", y="count", hue="year", marker="o", ax=ax)
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", 
                            "Jul", "Agu", "Sep", "Okt", "Nov", "Des"])
        ax.set_title("Tren Penyewaan Sepeda per Bulan")
        ax.set_xlabel("Bulan")
        ax.set_ylabel("Jumlah Penyewaan Sepeda")
        ax.legend(title="Tahun", labels=["2011", "2012"])
        st.pyplot(fig)
    else:
        st.warning("Tidak ada data untuk rentang waktu yang dipilih.")

# 2. Distribusi Penyewaan Sepeda Berdasarkan Hari dalam Seminggu
elif option == "Distribusi Penyewaan Berdasarkan Hari":
    if not main_df.empty:
        st.subheader("Distribusi Penyewaan Berdasarkan Hari dalam Seminggu")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.boxplot(x="weekday", y="count", hue="workingday", data=main_df, ax=ax, palette="coolwarm")
        ax.set_title("Distribusi Penyewaan Sepeda Berdasarkan Hari")
        ax.set_xlabel("Hari")
        ax.set_ylabel("Jumlah Penyewaan")
        st.pyplot(fig)
   
        st.markdown("### 📈 Tren Penyewaan Sepeda per Hari")
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(data=main_df, x="weekday", y="count", hue="workingday", marker="o", ax=ax, palette="tab10")
        ax.set_title("Tren Penyewaan Sepeda Berdasarkan Hari")
        ax.set_xlabel("Hari dalam Seminggu")
        ax.set_ylabel("Jumlah Penyewaan Sepeda")
        ax.legend(title="Hari Kerja", labels=["Akhir Pekan / Libur", "Hari Kerja"])

        # Pastikan label sumbu x sesuai
        ax.set_xticks(range(7))
        ax.set_xticklabels(["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"])

        ax.grid()
        st.pyplot(fig)

    else:
        st.warning("⚠ Tidak ada data untuk rentang waktu yang dipilih.")


# 3. Pengaruh Cuaca terhadap Penyewaan
elif option == "Pengaruh Cuaca terhadap Penyewaan":
    if not main_df.empty:
        st.subheader("☁️ Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda")

        # BOXPLOT - Distribusi Penyewaan Berdasarkan Cuaca
        st.markdown("### 📊 Distribusi Penyewaan Berdasarkan Cuaca")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.boxplot(x="weather_condition", y="count", data=main_df, hue="weather_condition", ax=ax, palette="Set2", legend=False)
        ax.set_title("Distribusi Penyewaan Sepeda Berdasarkan Cuaca")
        ax.set_xlabel("Kondisi Cuaca")
        ax.set_ylabel("Jumlah Penyewaan")

        # Pastikan jumlah ticks sesuai sebelum mengganti label
        ax.set_xticks(range(4))  
        ax.set_xticklabels(["Cerah", "Berawan", "Hujan Ringan", "Hujan Deras"])

        st.pyplot(fig)

        # BARPLOT - Rata-rata Penyewaan Berdasarkan Cuaca
        st.markdown("### 📊 Rata-rata Penyewaan Sepeda per Kondisi Cuaca")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(data=main_df, x="weather_condition", y="count", hue="weather_condition", palette="viridis", ax=ax, legend=False)
        ax.set_title("Pengaruh Cuaca terhadap Jumlah Penyewaan Sepeda")
        ax.set_xlabel("Kondisi Cuaca")
        ax.set_ylabel("Rata-rata Penyewaan Sepeda")

        # Pastikan jumlah ticks sesuai sebelum mengganti label
        ax.set_xticks(range(4))
        ax.set_xticklabels(["Cerah", "Berawan", "Hujan Ringan", "Hujan Deras"])

        st.pyplot(fig)

    else:
        st.warning("⚠ Tidak ada data untuk rentang waktu yang dipilih.")

# 4. Analisis Hubungan Faktor dan Kategori Penyewaan
elif option == "Analisis Hubungan dan Kategori Penyewaan":
    if not main_df.empty:
        st.subheader("📌 Korelasi Faktor dan Kategori Penyewaan Sepeda")

        # HEATMAP KORELASI
        st.markdown("### 🔥 Hubungan Antar Faktor yang Mempengaruhi Penyewaan")
        columns_to_drop = ["date", "season", "year", "month", "holiday", 
                           "weekday", "workingday", "weather_condition", "year_month"]
        main_df_numeric = main_df.drop(columns=columns_to_drop, errors="ignore")

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(main_df_numeric.corr(), annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
        ax.set_title("Heatmap Korelasi Variabel terhadap Jumlah Penyewaan")
        st.pyplot(fig)

        # KATEGORI PENYEWAAN
        st.markdown("### 📊 Klasifikasi Hari Berdasarkan Tingkat Penyewaan")

        # ✅ Gunakan `.loc` untuk menghindari SettingWithCopyWarning
        main_df.loc[:, "rental_category"] = pd.cut(
            main_df["count"], bins=3, labels=["Low", "Medium", "High"]
        )

        # COUNT PLOT - Distribusi Kategori Penyewaan
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.countplot(data=main_df, x="rental_category", palette="pastel", ax=ax)
        ax.set_title("Kategori Penyewaan Sepeda Berdasarkan Binning")
        ax.set_xlabel("Kategori Penyewaan")
        ax.set_ylabel("Jumlah Hari")
        
        st.pyplot(fig)

    else:
        st.warning("⚠ Tidak ada data untuk rentang waktu yang dipilih.")

st.sidebar.write("Sumber Data: https://www.kaggle.com/code/ramanchandra/bike-sharing-data-analysis")
