import streamlit as st
import json
import matplotlib.pyplot as plt
import os

# ---------------------------
# Judul & Deskripsi
# ---------------------------
st.title("🎯 Sistem Pendukung Keputusan - Rekomendasi Karier (CBR)")
st.write("""
👋 Halo sobat!  
Selamat datang di **Sistem Pendukung Keputusan Karier** 💼  
Yuk, cari tahu rekomendasi karier yang paling cocok buat kamu berdasarkan minat, keahlian, dan kepribadianmu.  
""")
# ---------------------------
# Input Pengguna
# ---------------------------
st.subheader("🧩 Isi Data Diri Kamu")

nama = st.text_input("Nama (opsional):", placeholder="Contoh: Wulan")
minat = st.selectbox("Pilih minat utama kamu:", ["-", "Teknologi", "Bisnis", "Desain", "Kesehatan", "Pendidikan"])
keahlian = st.selectbox("Pilih keahlian utama kamu:", ["-", "Analisis Data", "Komunikasi", "Kreativitas", "Pemrograman", "Kepemimpinan"])
kepribadian = st.selectbox("Pilih tipe kepribadian kamu:", ["-", "Introvert", "Ekstrovert", "Ambivert"])

# ---------------------------
# Tombol Proses
# ---------------------------
if st.button("🔍 Cari Rekomendasi Karier"):
    # Validasi input
    if "-" in [minat, keahlian, kepribadian]:
        st.warning("⚠️ Silakan lengkapi semua pilihan terlebih dahulu sebelum mencari rekomendasi.")
        st.stop()

    # ---------------------------
    # Kasus Lama (Basis Kasus)
    # ---------------------------
    kasus_lama = [
        {"minat": "Teknologi", "keahlian": "Pemrograman", "kepribadian": "Introvert", "karier": "Software Engineer"},
        {"minat": "Bisnis", "keahlian": "Kepemimpinan", "kepribadian": "Ekstrovert", "karier": "Manajer Pemasaran"},
        {"minat": "Desain", "keahlian": "Kreativitas", "kepribadian": "Ambivert", "karier": "UI/UX Designer"},
        {"minat": "Kesehatan", "keahlian": "Komunikasi", "kepribadian": "Ekstrovert", "karier": "Perawat"},
        {"minat": "Pendidikan", "keahlian": "Komunikasi", "kepribadian": "Ambivert", "karier": "Guru BK"},
        {"minat": "Teknologi", "keahlian": "Analisis Data", "kepribadian": "Introvert", "karier": "Data Analyst"},
    ]

    # ---------------------------
    # Fungsi Hitung Kemiripan
    # ---------------------------
    def hitung_kemiripan(kasus, minat, keahlian, kepribadian):
        score = 0
        if kasus["minat"] == minat:
            score += 1
        if kasus["keahlian"] == keahlian:
            score += 1
        if kasus["kepribadian"] == kepribadian:
            score += 1
        return (score / 3) * 100  # hasil dalam persen

    # Hitung kemiripan semua kasus
    skor_list = []
    for kasus in kasus_lama:
        skor = hitung_kemiripan(kasus, minat, keahlian, kepribadian)
        skor_list.append({"karier": kasus["karier"], "skor": skor})

    # Urutkan berdasarkan skor tertinggi
    skor_list.sort(key=lambda x: x["skor"], reverse=True)
    top_case = skor_list[0]

    # ---------------------------
    # Tampilkan hasil rekomendasi
    # ---------------------------
    st.success(f"💼 **Rekomendasi Karier:** {top_case['karier']}")
    st.write(f"Tingkat kemiripan dengan basis kasus: **{top_case['skor']:.2f}%**")

    # Visualisasi top 3 kemiripan
    top3 = skor_list[:3]
    labels = [c["karier"] for c in top3]
    scores = [c["skor"] for c in top3]

    fig, ax = plt.subplots()
    ax.barh(labels, scores, color="skyblue")
    ax.set_xlabel("Persentase Kemiripan (%)")
    ax.set_xlim(0, 100)
    ax.set_title("Top 3 Rekomendasi Karier Serupa")
    st.pyplot(fig)

    # ---------------------------
    # Simpan data pengguna (anonim)
    # ---------------------------
    new_case = {
        "nama": nama if nama else "Anonim",
        "minat": minat,
        "keahlian": keahlian,
        "kepribadian": kepribadian,
        "karier_rekomendasi": top_case["karier"]
    }

    # Pastikan folder data ada
    os.makedirs("data", exist_ok=True)
    data_path = "data/hasil_pengguna.json"

    try:
        with open(data_path, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(new_case)

    with open(data_path, "w") as f:
        json.dump(data, f, indent=4)

    st.info("✅ Data kamu telah disimpan secara anonim untuk keperluan analisis.")

# ---------------------------
# Footer
# ---------------------------
st.markdown("---")
st.caption("© 2025 - Sistem CBR Karier | Dibuat dengan ❤️ menggunakan Streamlit")