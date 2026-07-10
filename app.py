import streamlit as st
import pandas as pd
import time
import copy
from algorithms.bfs import bfs
from algorithms.astar import astar
import streamlit.components.v1 as components
from probability.weather import simulate_weather
from ml.battery_predictor import predict_energy

from components.grid_renderer import (
    GRID,
    START,
    GOAL,
    create_grid_html
)

from components.tictactoe import render_game


# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Intelligent Agent Navigation & Strategy System",
    page_icon="🤖",
    layout="wide"
)


# =====================================
# SESSION STATE
# =====================================

if "mission_started" not in st.session_state:
    st.session_state.mission_started = False

if "mission_completed" not in st.session_state:
    st.session_state.mission_completed = False


# =====================================
# SIDEBAR
# =====================================

st.sidebar.title("Intelligent Agent AI")

menu = st.sidebar.radio(
    "Navigasi Menu",
    [
        "Dashboard Utama",
        "Dokumentasi State Space",
        "Analisis Alpha-Beta Pruning"
    ]
)


# =====================================
# STATE SPACE PAGE (Sub-CPMK 3.1.1)
# =====================================

if menu == "Dokumentasi State Space":

    st.title("Dokumentasi Ruang Keadaan (Sub-CPMK 3.1.1)")

    st.markdown("""
### 1. Initial State (Keadaan Awal)
Agen Cerdas atau kurir logistik berada tepat pada titik koordinat awal yaitu **Gudang (Start)**.

### 2. Actions (Aksi Pergerakan)
Agen dapat bergerak memilih satu dari empat arah mata angin yang valid di dalam lingkungan grid:
- **Move Up** (Berpindah satu baris ke atas)
- **Move Down** (Berpindah satu baris ke bawah)
- **Move Left** (Berpindah satu kolom ke kiri)
- **Move Right** (Berpindah satu kolom ke kanan)

### 3. Transition Model (Model Transisi)
Agen berpindah dari posisi koordinat saat ini $(x, y)$ ke sel tetangga terdekat $(x \pm 1, y)$ atau $(x, y \pm 1)$ pada matriks berukuran $9\\times9$. Syarat utama transisi adalah sel tujuan tidak boleh berupa area rintangan macet (Obstacles).

### 4. Goal Test (Uji Titik Tujuan)
Evaluasi logika untuk memastikan apakah misi pengantaran selesai. Kondisi bernilai benar jika titik koordinat posisi terkini agen sama dengan koordinat lokasi **Konsumen (Goal)**.

### 5. Path Cost (Biaya Jalur)
Setiap satu langkah perpindahan antar sel memiliki nilai bobot atau biaya sebesar 1. Total biaya perjalanan dihitung dari akumulasi jumlah langkah keseluruhan yang ditempuh agen dari Gudang menuju titik Konsumen.
""")

    st.stop()


# =====================================
# ALPHA BETA PAGE (Sub-CPMK 6.2.1)
# =====================================

if menu == "Analisis Alpha-Beta Pruning":

    st.title("Analisis Alpha-Beta Pruning (Sub-CPMK 6.2.1)")

    st.success("""
### Bukti Capaian Evaluasi Pohon Keputusan (Sub-CPMK 6.2.1)
Dalam implementasi mesin kecerdasan buatan berbasis algoritma Minimax pada game Tic-Tac-Toe ini, pemangkasan komputasi (alpha-beta pruning) terjadi pada cabang vertikal yang tidak lagi prospektif untuk dieksplorasi. Kondisi ini dipicu ketika nilai evaluasi batas bawah (alpha) yang dimiliki oleh pergerakan manusia sebagai Maximizer terdeteksi sudah lebih besar atau sama dengan nilai batas atas (beta) yang dipegang oleh Agen Bot sebagai Minimizer, atau dituliskan secara matematis dengan rumus alpha >= beta. 

Sebagai contoh nyata di dalam game, saat pemain manusia mengambil langkah strategis di area sudut grid yang mengunci potensi kemenangan ganda pada giliran berikutnya, fungsi rekursif pada backend sistem akan langsung membaca lonjakan nilai alpha lawan. Ketika sistem masuk untuk mengecek sisa ubin kosong di bawah cabang anak vertikal berikutnya, perulangan komputasi akan diputus (break) secara instan. Algoritma memotong sisa sub-pohon yang merepresentasikan opsi langkah blunder milik Agen Bot karena hasilnya dipastikan tidak akan mengubah keputusan pergerakan optimal yang diambil oleh komputer. Langkah ini menghemat penggunaan memori pencarian status (state space) secara signifikan tanpa menurunkan tingkat kecerdasan bot.
""")

    st.stop()


# =====================================
# DASHBOARD
# =====================================

st.title("Smart Agent Navigation & Strategy System")
st.caption(
    "Aplikasi Web Optimasi Rute Pengantaran Kurir dan Sistem Strategi Kompetitif Support"
)


# =====================================
# WEATHER SELECTOR & PROBABILITY (P7 & P13)
# =====================================

selected_weather = st.selectbox(
    "Pilih Kondisi Cuaca Saat Ini",
    [
        "Cerah (Sunny)",
        "Berawan (Cloudy)",
        "Hujan (Rainy)",
        "Badai (Storm)"
    ]
)

# Menyelaraskan teks seleksi dengan parameter fungsi backend weather
weather_mapping = {
    "Cerah (Sunny)": "Sunny",
    "Berawan (Cloudy)": "Cloudy",
    "Hujan (Rainy)": "Rainy",
    "Badai (Storm)": "Storm"
}
backend_weather_name = weather_mapping[selected_weather]

weather = simulate_weather(backend_weather_name)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Dampak Cuaca",
        weather["weather"]
    )

with col2:
    st.metric(
        "Probabilitas Jalur Macet",
        f"{int(weather['blockage_probability'] * 100)}%"
    )

with col3:
    status = (
        "Selesai"
        if st.session_state.mission_completed
        else "Siap Jalan"
    )
    st.metric(
        "Status Pengantaran",
        status
    )

st.info(
    f"Rekomendasi Aturan Keputusan Bayes: {weather['recommendation']}"
)


# =====================================
# DYNAMIC GRID BASED ON WEATHER LOGIC (9x9)
# =====================================
DYNAMIC_GRID = copy.deepcopy(GRID)

# Jika probabilitas kemacetan tinggi akibat cuaca buruk, sistem memicu titik macet tambahan di area tengah
if weather['blockage_probability'] >= 0.8:
    if DYNAMIC_GRID[4][4] == 0:
        DYNAMIC_GRID[4][4] = 1 
    if DYNAMIC_GRID[4][5] == 0:
        DYNAMIC_GRID[4][5] = 1
    if DYNAMIC_GRID[5][4] == 0:
        DYNAMIC_GRID[5][4] = 1


# =====================================
# RUN ALGORITHMS WITH DYNAMIC GRID
# =====================================

bfs_result = bfs(DYNAMIC_GRID, START, GOAL)
astar_result = astar(DYNAMIC_GRID, START, GOAL)

weather_penalty = 0
if backend_weather_name == "Rainy":
    weather_penalty = 10
elif backend_weather_name == "Storm":
    weather_penalty = 25


# =====================================
# NAVIGATION MAP
# =====================================

st.subheader("Simulasi Peta Grid (9x9)")

map_placeholder = st.empty()

# Parameter height diturunkan ke 520 agar pas dan tidak memicu potongan margin bawah iframe
if not st.session_state.mission_started:
    grid_html = create_grid_html(DYNAMIC_GRID, START, GOAL, [])
    with map_placeholder.container():
        components.html(grid_html, height=520, scrolling=False)
else:
    grid_html = create_grid_html(DYNAMIC_GRID, START, GOAL, astar_result["path"])
    with map_placeholder.container():
        components.html(grid_html, height=520, scrolling=False)


# =====================================
# START BUTTON
# =====================================

if not st.session_state.mission_started:

    if st.button("Mulai Navigasi Kurir Cerdas", use_container_width=True):

        current_path = []

        for step in astar_result["path"]:
            current_path.append(step)
            html = create_grid_html(DYNAMIC_GRID, START, GOAL, current_path)

            with map_placeholder.container():
                components.html(html, height=520, scrolling=False)

            time.sleep(0.15)

        st.session_state.mission_started = True
        st.session_state.mission_completed = True
        st.rerun()


# =====================================
# RESULTS AFTER MISSION START
# =====================================

if st.session_state.mission_started:

    # =====================================
    # ALGORITHM COMPARISON (Sub-CPMK 6.1.1)
    # =====================================

    st.subheader("Tabel Perbandingan Efisiensi Algoritma")

    comparison = pd.DataFrame({
        "Algoritma Pencarian": ["BFS (Blind Search)", "A* (Heuristic Search)"],
        "Panjang Rute Jalur": [
            len(bfs_result["path"]),
            len(astar_result["path"])
        ],
        "Jumlah Node yang Dieksplorasi": [
            bfs_result["nodes_explored"],
            astar_result["nodes_explored"]
        ]
    })

    st.dataframe(comparison, use_container_width=True)


    # =====================================
    # AI ANALYSIS
    # =====================================

    st.subheader("Analisis Efisiensi Navigasi")

    if astar_result["nodes_explored"] < bfs_result["nodes_explored"]:
        st.success(
            f"Algoritma A* Search terbukti lebih efisien dibandingkan dengan BFS. "
            f"Metode BFS mengeksplorasi sebanyak {bfs_result['nodes_explored']} node, "
            f"sedangkan A* hanya membutuhkan eksplorasi sebanyak {astar_result['nodes_explored']} node. "
            f"Hasil ini memvalidasi bahwa fungsi heuristik Manhattan Distance mampu mengarahkan pencarian langsung "
            f"ke lokasi target tanpa perlu memeriksa seluruh ruang keadaan secara menyeluruh pada peta 9x9 ini."
        )
    else:
        st.info(
            "Pada konfigurasi peta ini, kedua algoritma memeriksa jumlah titik yang setara karena penempatan sebaran titik rintangan."
        )


    # =====================================
    # MACHINE LEARNING ENERGY PREDICTION (P9, P11, P12)
    # =====================================

    route_length = len(astar_result["path"])
    energy = predict_energy(route_length)
    energy = max(0, energy - weather_penalty)
    
    st.subheader("Prediksi Sisa Energi Baterai (Model Regresi Linier)")

    col_m1, col_m2 = st.columns(2)

    with col_m1:
        st.metric(
            "Panjang Rute Hasil Kalkulasi A*",
            f"{route_length} Satuan Langkah"
        )

    with col_m2:
        st.metric(
            "Prediksi Sisa Baterai Kurir",
            f"{energy}%"
        )


    # =====================================
    # RISK ASSESSMENT
    # =====================================

    st.subheader("Penilaian Tingkat Risiko Operasional")

    if backend_weather_name == "Sunny":
        st.success("Tingkat Risiko Rendah - Kondisi perjalanan kurir sangat optimal.")
    elif backend_weather_name == "Cloudy":
        st.info("Tingkat Risiko Normal - Parameter standar pengantaran terpenuhi.")
    elif backend_weather_name == "Rainy":
        st.warning("Tingkat Risiko Sedang - Potensi keterlambatan tinggi akibat titik macet tambahan.")
    else:
        st.error("Tingkat Risiko Tinggi - Cuaca buruk ekstrem. Disarankan untuk memprioritaskan jalur alternatif eksternal.")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Jumlah Total Blokade Jalan",
            sum(row.count(1) for row in DYNAMIC_GRID)
        )

    with c2:
        st.metric(
            "Total Langkah Rute Final",
            len(astar_result["path"])
        )

    with c3:
        st.metric(
            "Konsumen Terjangkau",
            "Ya, Terantar"
        )


    # =====================================
    # SUCCESS
    # =====================================

    st.success(
        "Misi Pengantaran Berhasil - Armada Kurir Cerdas Telah Tiba di Lokasi Konsumen."
    )


    # =====================================
    # MINI-GAME TIC TAC TOE (Sub-CPMK 6.2.1)
    # =====================================

    st.divider()
    st.subheader("Simulator Keputusan Strategis (Tic-Tac-Toe Minimax Bot)")
    render_game()


    # =====================================
    # PATH DETAILS
    # =====================================

    with st.expander("Lihat Detail Koordinat Jalur Komputasi A*"):
        st.write(astar_result["path"])

    with st.expander("Lihat Detail Koordinat Jalur Komputasi BFS"):
        st.write(bfs_result["path"])