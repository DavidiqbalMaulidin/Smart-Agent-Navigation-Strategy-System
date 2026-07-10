import numpy as np
from sklearn.linear_model import LinearRegression

# =========================================================
# DATA TRAINING Sederhana (Representasi Konsumsi Energi Agen)
# =========================================================
# X: Panjang Rute (Langkah), y: Sisa Baterai Agen (%)
X = np.array([[5], [10], [15], [20], [25], [30], [35], [40], [50], [81]])
y = np.array([95,  90,   85,   80,   75,   70,   65,   60,   50,   20])

# Menginisialisasi dan melatih model Linear Regression sekali di tingkat modul
# (Proses training tidak berulang-ulang setiap kali fungsi dipanggil)
_model_baterai = LinearRegression()
_model_baterai.fit(X, y)


def predict_energy(route_length):
    """
    Fungsi untuk memprediksi sisa baterai/energi agen cerdas 
    berdasarkan panjang rute kalkulasi A* menggunakan Scikit-Learn.
    """
    # Melakukan prediksi berdasarkan model regresi linear yang sudah terlatih
    prediction = _model_baterai.predict([[route_length]])
    
    # Memastikan nilai output berada di rentang 0% - 100% dan membulatkannya
    sisa_energi = round(float(prediction[0]), 2)
    return max(0.0, min(100.0, sisa_energi))