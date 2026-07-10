# components/grid_renderer.py

GRID = [
    [0,0,0,1,0,0,0,1,0],
    [0,1,0,1,0,1,0,1,0],
    [0,1,0,0,0,1,0,0,0],
    [0,0,0,1,0,0,0,1,0],
    [1,1,0,1,0,1,0,0,0],
    [0,0,0,0,0,1,1,1,0],
    [0,1,1,1,0,0,0,0,0],
    [0,0,0,1,0,1,0,1,0],
    [0,0,0,0,0,0,0,0,0]
]

START = (0, 0)
GOAL = (8, 8)


def create_grid_html(grid, start, goal, path=None):

    if path is None:
        path = []

    # Gaya CSS global ditambahkan untuk memastikan layout fleksibel dan responsif
    # Menggunakan warna latar belakang gelap elegan (#0F172A) dengan aksen warna cerah
    html = """
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        .grid-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin: 10px auto;
            width: 100%;
            overflow-x: auto;
        }
        .grid-matrix {
            display: grid;
            grid-template-columns: repeat(9, 40px);
            gap: 5px;
            padding: 15px;
            background: #1E293B;
            border-radius: 16px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.4);
            width: fit-content;
        }
        .grid-cell {
            width: 40px;
            height: 40px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            border: 1px solid #334155;
            transition: background-color 0.2s ease;
        }
        .legend-container {
            display: flex;
            justify-content: center;
            gap: 20px;
            flex-wrap: wrap;
            margin-top: 15px;
            font-size: 13px;
            font-weight: 600;
            color: #E2E8F0;
            font-family: system-ui, -apple-system, sans-serif;
            text-align: center;
            width: 100%;
        }
    </style>
    <div class="grid-container">
        <div class="grid-matrix">
    """

    for r in range(len(grid)):
        for c in range(len(grid[0])):

            # Default: Jalan atau area kosong (Abu-abu gelap elegan)
            color = "#334155"
            icon = ""

            # 1. Rintangan Macet (Merah Marun Cerah / Muted Red)
            if grid[r][c] == 1:
                color = "#991B1B"
                icon = "🛑"

            # 2. Rute Pergerakan Kurir (Biru Neon Cerah)
            if (r, c) in path:
                color = "#2563EB"
                icon = "🚚"

            # 3. Posisi Gudang Asal / Start (Hijau Emerald Cerah)
            if (r, c) == start:
                color = "#059669"
                icon = "🏬"

            # 4. Posisi Konsumen / Goal (Kuning Oranye Cerah)
            if (r, c) == goal:
                color = "#D97706"
                icon = "📦"

            html += f"""
            <div class="grid-cell" style="background: {color};">
                {icon}
            </div>
            """

    # Bagian legenda bawah yang bersih dari tumpukan emoji berlebih
    html += """
        </div>
    </div>

    <div class="legend-container">
        <span>🏬 Gudang (Start)</span>
        <span>📦 Konsumen (Goal)</span>
        <span>🛑 Rintangan Macet</span>
        <span>🚚 Rute Kurir</span>
    </div>
    """

    return html