import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# Dizionari con i range (min, max) per ciascun mese

umidita_ranges = {
    1: (76, 83),  # Gennaio
    2: (73, 80),
    3: (67, 74),
    4: (70, 75),
    5: (70, 82),
    6: (69, 76),
    7: (60, 68),
    8: (64, 72),
    9: (73, 77),
    10: (76, 83),
    11: (81, 84),
    12: (78, 83)
}

temperature_ranges = {
    1: (2.7, 6.7),  # Gennaio
    2: (4.0, 8.1),
    3: (6.9, 9.8),
    4: (9.6, 13.8),
    5: (11.8, 16.9),
    6: (18.0, 22.2),
    7: (19.5, 24.5),
    8: (21.1, 24.5),
    9: (16.3, 20.1),
    10: (11.5, 16.6),
    11: (8.0, 11.4),
    12: (4.4, 7.8)
}

precipitations_ranges = {
    1: (30.2, 136.2),  # Gennaio
    2: (52.2, 116.2),
    3: (55.2, 138.0),
    4: (61.0, 101.8),
    5: (46.4, 147.6),
    6: (16.4, 102.6),
    7: (13.6, 46.0),
    8: (8.2, 75.2),
    9: (53.0, 151.2),
    10: (32.8, 163.2),
    11: (79.6, 204.4),
    12: (47.6, 199.8)
}


def genera_dati_ultimi_100_mesi():

    # Punto di partenza: mese corrente
    data_corrente = datetime.now()

    dati = []

    for i in range(100):
        # Calcolo la data del mese
        data_mese = (data_corrente - relativedelta(months=i)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        # Ricaviamo il numero del mese
        mese_num = data_mese.month

        # Range specifici per Umidità, Temperatura e Precipitazioni
        umid_min, umid_max = umidita_ranges[mese_num]
        temp_min, temp_max = temperature_ranges[mese_num]
        prec_min, prec_max = precipitations_ranges[mese_num]

        # Generazione valori random
        umidita = round(np.random.uniform(umid_min, umid_max), 2)
        temperatura = round(np.random.uniform(temp_min, temp_max), 2)
        precipitazioni = round(np.random.uniform(prec_min, prec_max), 2)
        produzione = round(np.random.uniform(500, 2000), 2)
        efficienza = round(np.random.uniform(70, 100), 2)

        # Append della riga ai dati
        dati.append([
            data_mese,
            temperatura,
            umidita,
            precipitazioni,
            produzione,
            efficienza
        ])

    # DataFrame con le stesse colonne originali
    df = pd.DataFrame(dati, columns=[
        "Data e Ora",
        "Temperatura (°C)",
        "Umidità (%)",
        "Precipitazioni (mm)",
        "Produzione (kg/ha)",
        "Efficienza (%)"
    ])

    return df


def salva_dati_csv(nome_file="data/dati_simulati.csv"):
    df = genera_dati_ultimi_100_mesi()
    df.to_csv(nome_file, index=False)
    print(f"Dati salvati in {nome_file}")


# Eseguiamo lo script solo se viene lanciato direttamente
if __name__ == "__main__":
    salva_dati_csv()
