# Dashboard_SettorePrimario

**Dashboard interattiva per il monitoraggio delle performance ambientali e produttive nel settore primario.**

## 📌 Descrizione del progetto

Il progetto è composto da due parti principali:

1. **Simulatore di dati (utils/simulatore.py)**: genera dati ambientali realistici (temperatura, umidità, precipitazioni) e dati di performance agricola (produzione, efficienza) per 100 mesi, basandosi su range mensili basati su dati climatici storici reali.

2. **Dashboard interattiva (dashboard/dashboard.py)**: visualizza graficamente i dati prodotti dal simulatore con funzionalità interattive, come:
   - Selezione della variabile e tipo di grafico
   - Filtraggio temporale per periodo
   - Indicatori del mese corrente e confronto con lo stesso mese dell'anno precedente
   - Analisi delle condizioni ottimali di produzione
   - Previsioni meteo in tempo reale
   - KPI stagionali e confronto con media storica
   - Tabella completa ordinabile

## 📁 Struttura delle cartelle

```
Dashboard_SettorePrimario/
│
├── dashboard/
│   ├── dashboard.py
│   ├── layout.py
│
├── utils/
│   └── simulatore.py
│
├── data/
│   └── dati_simulati.csv
│
├── requirements.txt
└── README.md
```

1. Clona il repository:
   ```bash
   git clone [https://github.com/tuo-utente/Dashboard_SettorePrimario.git](https://github.com/kekodom99/pw-Dashboard_SettorePrimario)
   cd Dashboard_SettorePrimario
   ```

2. Crea un ambiente virtuale e attivalo:
   ```bash
   python -m venv venv
   source venv/bin/activate 
   ```

3. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```

4. Genera il dataset simulato:
   ```bash
   python utils/simulatore.py
   ```

5. Avvia la dashboard:
   ```bash
   python dashboard/dashboard.py
   ```


## 📊 Funzionalità chiave

- Grafici interattivi per tutte le variabili ambientali e produttive
- Analisi KPI stagionali
- Previsioni meteo aggiornate
- Tabelle ordinabili complete
- Analisi delle condizioni ottimali di produzione

## 📌 Requisiti minimi

- Python 3.8+
- Connessione Internet (per la sezione previsioni meteo)
