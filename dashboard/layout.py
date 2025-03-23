import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table

# Descrizione dei dati
descrizione_dati = {
    "Temperatura (°C)": "Misura la temperatura dell'aria in gradi Celsius. Valori elevati possono influenzare la crescita delle colture.",
    "Umidità (%)": "Indica la percentuale di umidità nell'aria. Un'umidità ottimale aiuta a mantenere il raccolto sano.",
    "Precipitazioni (mm)": "Quantità di pioggia caduta misurata in millimetri. Piogge abbondanti possono favorire o danneggiare le coltivazioni.",
    "Produzione (kg/ha)": "Quantità di raccolto per ettaro. Questo valore indica il rendimento agricolo.",
    "Efficienza (%)": "Percentuale di utilizzo ottimale delle risorse disponibili. Un'alta efficienza significa minori sprechi e maggiore produttività."
}

# Lista degli anni e nomi dei mesi
lista_anni = [str(y) for y in range(2018, 2031)]
mesi_italiani = {
    "1": "Gennaio", "2": "Febbraio", "3": "Marzo", "4": "Aprile",
    "5": "Maggio", "6": "Giugno", "7": "Luglio", "8": "Agosto",
    "9": "Settembre", "10": "Ottobre", "11": "Novembre", "12": "Dicembre"
}
opzioni_mesi = [{"label": v, "value": k} for k, v in mesi_italiani.items()]
opzioni_anni = [{"label": y, "value": y} for y in lista_anni]

# Layout principale
layout = dbc.Container(
    fluid=True,
    style={
        "backgroundColor": "#ecf4e7",
        "backgroundImage": "url('https://images.unsplash.com/photo-1596607146011-41079a6be6fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80')",
        "backgroundSize": "cover",
        "backgroundRepeat": "no-repeat",
        "backgroundPosition": "center",
        "minHeight": "100vh",
        "padding": "20px"
    },
    children=[
        # TITOLO CENTRALE
        dbc.Row(
            dbc.Col(
                [
                    html.H1("🌱 AZIENDA AGRICOLA ROSSI",
                            className="text-center mb-2",
                            style={"color": "#2c3e50", "fontWeight": "bold"}),
                    html.H3("Monitoraggio delle metriche ambientali e produttive",
                            className="text-center text-secondary mb-4")
                ],
                width=12
            )
        ),


        dbc.Row([
            # (colonna sinistra)
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H4("Menu", className="card-title text-center mb-3", style={"color": "#16a085"}),

                        # MENU
                        dbc.Nav(
                            [
                                dbc.NavLink("Indicatori ultimo mese", id="open-lastmonth-modal", style={"cursor": "pointer"}, n_clicks=0),
                                dbc.NavLink("KPI ultimo Anno", id="open-lastyear-kpi-modal", style={"cursor": "pointer"}, n_clicks=0),
                                dbc.NavLink("Analisi Periodo Migliore", id="open-analisi-modal", style={"cursor": "pointer"}, n_clicks=0),
                                dbc.NavLink("Previsioni Meteo", id="open-weather-modal", style={"cursor": "pointer"}, n_clicks=0),
                                dbc.NavLink("Dati Completi", id="open-data-modal", style={"cursor": "pointer"}, n_clicks=0),
                            ],
                            vertical=True,
                            pills=True
                        )
                    ]),
                    className="mb-4 shadow-sm",
                    style={"backgroundColor": "rgba(255,255,255,0.8)"}
                ),
                width=2
            ),

            # Contenuto principale (colonna destra)
            dbc.Col([
                dcc.Interval(id='interval-update', interval=5000, n_intervals=0),

                # Selezione variabile + descrizione
                dbc.Card(
                    dbc.CardBody([
                        html.Label("Seleziona la variabile da analizzare:", className="fw-bold text-center d-block"),
                        dcc.Dropdown(
                            id='grafico-dropdown',
                            options=[{'label': key, 'value': key} for key in descrizione_dati.keys()],
                            value='Temperatura (°C)',
                            clearable=False,
                            className="mb-2"
                        ),
                        html.P(id='descrizione-dati', className="text-center text-info mb-0", style={"fontWeight": "500"})
                    ]),
                    className="mb-4 shadow-sm",
                    style={"backgroundColor": "rgba(255,255,255,0.8)"}
                ),

                # Filtro e scelta tipo grafico
                dbc.Card(
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col(
                                [
                                    html.Label("Tipo di grafico:", className="fw-bold"),
                                    dcc.Dropdown(
                                        id='chart-type',
                                        options=[
                                            {'label': 'Linea', 'value': 'line'},
                                            {'label': 'Barre', 'value': 'bar'},
                                            {'label': 'Scatter', 'value': 'scatter'}
                                        ],
                                        value='line',
                                        clearable=False
                                    )
                                ],
                                width=3
                            ),
                            dbc.Col(
                                [
                                    html.Label("Inizio:", className="fw-bold"),
                                    html.Div([
                                        dcc.Dropdown(
                                            id='start-month-dropdown',
                                            options=opzioni_mesi,
                                            value=None,
                                            placeholder="Mese Inizio",
                                            clearable=True,
                                            style={"width": "120px", "display": "inline-block", "marginRight": "10px"}
                                        ),
                                        dcc.Dropdown(
                                            id='start-year-dropdown',
                                            options=opzioni_anni,
                                            value=None,
                                            placeholder="Anno Inizio",
                                            clearable=True,
                                            style={"width": "100px", "display": "inline-block"}
                                        )
                                    ])
                                ],
                                width=4
                            ),
                            dbc.Col(
                                [
                                    html.Label("Fine:", className="fw-bold"),
                                    html.Div([
                                        dcc.Dropdown(
                                            id='end-month-dropdown',
                                            options=opzioni_mesi,
                                            value=None,
                                            placeholder="Mese Fine",
                                            clearable=True,
                                            style={"width": "120px", "display": "inline-block", "marginRight": "10px"}
                                        ),
                                        dcc.Dropdown(
                                            id='end-year-dropdown',
                                            options=opzioni_anni,
                                            value=None,
                                            placeholder="Anno Fine",
                                            clearable=True,
                                            style={"width": "100px", "display": "inline-block"}
                                        )
                                    ])
                                ],
                                width=4
                            )
                        ])
                    ]),
                    className="mb-4 shadow-sm",
                    style={"backgroundColor": "rgba(255,255,255,0.8)"}
                ),

                # Grafico CENTRALE
                dbc.Card(
                    dbc.CardBody(
                        dcc.Graph(id='grafico-linea')
                    ),
                    className="mb-4 shadow-sm",
                    style={"backgroundColor": "rgba(255,255,255,0.8)"}
                ),

                # Slider per il numero di dati
                dbc.Card(
                    dbc.CardBody([
                        html.Label("Numero di dati da visualizzare:", className="fw-bold"),
                        dcc.Slider(
                            id='slider-righe',
                            min=10, max=100, step=10,
                            value=50,
                            marks={i: str(i) for i in range(10, 101, 20)}
                        )
                    ]),
                    className="mb-4 shadow-sm",
                    style={"backgroundColor": "rgba(255,255,255,0.8)"}
                ),

                # Modal per Indicatori Ultimo Mese
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("Indicatori Ultimo Mese")),
                        dbc.ModalBody(html.Div(id="lastmonth-modal-content")),
                        dbc.ModalFooter(
                            dbc.Button("Chiudi", id="close-lastmonth-modal", className="ms-auto", n_clicks=0)
                        )
                    ],
                    id="lastmonth-modal",
                    is_open=False,
                    centered=True,
                    size="lg"
                ),

                # Modal per Previsioni Meteo
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("Previsioni Meteo")),
                        dbc.ModalBody(html.Div(id="weather-modal-content")),
                        dbc.ModalFooter(
                            dbc.Button("Chiudi", id="close-weather-modal", className="ms-auto", n_clicks=0)
                        )
                    ],
                    id="weather-modal",
                    is_open=False,
                    centered=True,
                    size="lg"
                ),

                # Modal per Analisi
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("Analisi delle Condizioni Ottimali")),
                        dbc.ModalBody([
                            html.Div(id='analisi-condizioni', className="text-center mb-3"),
                            dcc.Graph(id='grafico-condizioni')
                        ]),
                        dbc.ModalFooter(
                            dbc.Button("Chiudi", id="close-analisi-modal", className="ms-auto", n_clicks=0)
                        )
                    ],
                    id="modal",
                    is_open=False,
                    centered=True,
                    size="lg"
                ),

                # Modal per Dati Completi
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("Dati Completi")),
                        dbc.ModalBody([
                            dbc.Row(
                                dbc.Col(
                                    [
                                        html.Label("Ordina per:", className="fw-bold"),
                                        dcc.Dropdown(
                                            id='order-dropdown',
                                            options=[
                                                {'label': 'Data', 'value': 'Data'},
                                                {'label': 'Temperatura (°C)', 'value': 'Temperatura (°C)'},
                                                {'label': 'Umidità (%)', 'value': 'Umidità (%)'},
                                                {'label': 'Precipitazioni (mm)', 'value': 'Precipitazioni (mm)'},
                                                {'label': 'Produzione (kg/ha)', 'value': 'Produzione (kg/ha)'},
                                                {'label': 'Efficienza (%)', 'value': 'Efficienza (%)'}
                                            ],
                                            value='Data',
                                            clearable=False
                                        )
                                    ],
                                    width=6,
                                    className="mx-auto mb-3"
                                )
                            ),
                            dash_table.DataTable(
                                id='data-table',
                                data=[],
                                columns=[],
                                sort_action='native',
                                style_table={'overflowX': 'auto'},
                                page_size=10
                            )
                        ]),
                        dbc.ModalFooter(
                            dbc.Button("Chiudi", id="close-data-modal", className="ms-auto", n_clicks=0)
                        )
                    ],
                    id="data-modal",
                    is_open=False,
                    centered=True,
                    size="lg"
                ),

                # Modal per KPI Ultimo Anno
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("KPI Ultimo Anno")),
                        dbc.ModalBody(html.Div(id="lastyear-kpi-modal-content")),
                        dbc.ModalFooter(
                            dbc.Button("Chiudi", id="close-lastyear-kpi-modal", className="ms-auto", n_clicks=0)
                        )
                    ],
                    id="lastyear-kpi-modal",
                    is_open=False,
                    centered=True,
                    size="lg"
                )

            ], width=10)
        ])
    ]
)
