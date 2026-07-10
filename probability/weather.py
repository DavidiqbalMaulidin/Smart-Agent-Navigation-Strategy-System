# probability/weather.py

def simulate_weather(weather):
    """
    Menghitung rekomendasi keputusan rute kurir berdasarkan Aturan Bayes.
    Mengevaluasi Posterior Probability: P(Macet | Cuaca)
    """
    # 1. Prior Probability: Probabilitas dasar rute utama mengalami macet (30%)
    p_macet = 0.3
    p_lancar = 0.7

    # 2. Likelihood: Peluang munculnya cuaca tertentu berdasarkan kondisi jalan P(Cuaca | Kondisi)
    if weather == "Sunny":
        p_cuaca_jika_macet = 0.2    # Peluang cerah saat jalanan macet
        p_cuaca_jika_lancar = 0.8   # Peluang cerah saat jalanan lancar
        recommendation = "Pertahankan rute utama. Hambatan di jalan sangat minim."

    elif weather == "Cloudy":
        p_cuaca_jika_macet = 0.4
        p_cuaca_jika_lancar = 0.6
        recommendation = "Kondisi jalan stabil. Rute utama aman untuk dilewati armada."

    elif weather == "Rainy":
        p_cuaca_jika_macet = 0.8    # Peluang hujan saat jalanan macet parah
        p_cuaca_jika_lancar = 0.2   # Peluang hujan saat jalanan lancar
        recommendation = "Gunakan rute alternatif. Probabilitas kemacetan tinggi akibat hujan."

    elif weather == "Storm":
        p_cuaca_jika_macet = 0.95   # Peluang badai saat jalanan macet total
        p_cuaca_jika_lancar = 0.05  # Peluang badai saat jalanan lancar
        recommendation = "Risiko operasional kritis. Wajib hindari rute utama dan gunakan jalur alternatif."
        
    else:
        # Nilai fallback jika ada input yang tidak sesuai
        p_cuaca_jika_macet = 0.2
        p_cuaca_jika_lancar = 0.8
        recommendation = "Kondisi jalan normal."

    # 3. Total Probability / Evidence: P(Cuaca)
    # P(Cuaca) = P(Cuaca|Macet) * P(Macet) + P(Cuaca|Lancar) * P(Lancar)
    p_cuaca = (p_cuaca_jika_macet * p_macet) + (p_cuaca_jika_lancar * p_lancar)

    # 4. Teorema Bayes: Menghitung Posterior Probability P(Macet | Cuaca)
    p_macet_jika_cuaca = (p_cuaca_jika_macet * p_macet) / p_cuaca

    return {
        "weather": weather,
        "blockage_probability": round(p_macet_jika_cuaca, 2),
        "recommendation": recommendation
    }