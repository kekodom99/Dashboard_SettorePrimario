import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime
from layout import layout, descrizione_dati

# Conversione da numero a nome mese
mesi_italiani = {
    1: "Gennaio", 2: "Febbraio", 3: "Marzo", 4: "Aprile",
    5: "Maggio", 6: "Giugno", 7: "Luglio", 8: "Agosto",
    9: "Settembre", 10: "Ottobre", 11: "Novembre", 12: "Dicembre"
}

def carica_dati():
    df = pd.read_csv("../data/dati_simulati.csv")
    df['Data e Ora'] = pd.to_datetime(df['Data e Ora'])
    df['Data'] = df['Data e Ora'].apply(lambda x: f"{mesi_italiani[x.month]} {x.year}")
    return df

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])
app.layout = layout

# 1) Scelta variabile
@app.callback(
    Output('descrizione-dati', 'children'),
    Input('grafico-dropdown', 'value')
)
def aggiorna_descrizione(variabile):
    return descrizione_dati.get(variabile, "Seleziona una variabile per visualizzarne la descrizione.")

# 2) Grafico centrale
@app.callback(
    Output('grafico-linea', 'figure'),
    [
        Input('grafico-dropdown', 'value'),
        Input('slider-righe', 'value'),
        Input('chart-type', 'value'),
        Input('start-month-dropdown', 'value'),
        Input('start-year-dropdown', 'value'),
        Input('end-month-dropdown', 'value'),
        Input('end-year-dropdown', 'value'),
        Input('interval-update', 'n_intervals')
    ]
)
def aggiorna_grafico(variabile, num_righe, chart_type,
                     start_month, start_year, end_month, end_year, _):
    df = carica_dati()
    df = df.sort_values(by='Data e Ora', ascending=True)
    if start_month and start_year and end_month and end_year:
        start_date = datetime(int(start_year), int(start_month), 1)
        end_date = datetime(int(end_year), int(end_month), 1)
        mask = (df['Data e Ora'] >= start_date) & (df['Data e Ora'] <= end_date)
        df = df.loc[mask]
    df_filtrato = df.tail(num_righe)
    if chart_type == 'bar':
        fig = px.bar(df_filtrato, x='Data', y=variabile, title=f"Andamento di {variabile}")
    elif chart_type == 'scatter':
        fig = px.scatter(df_filtrato, x='Data', y=variabile, title=f"Andamento di {variabile}")
    else:
        fig = px.line(df_filtrato, x='Data', y=variabile, title=f"Andamento di {variabile}")
    fig.update_layout(xaxis_title="Data (Mese e Anno)", yaxis_title=variabile)
    return fig

# 3) Ultimo Mese
@app.callback(
    Output("lastmonth-modal-content", "children"),
    Input('interval-update', 'n_intervals')
)
def aggiorna_lastmonth_modal(_):
    df = carica_dati()
    last_date = df["Data e Ora"].max()
    last_month = last_date.month
    last_year = last_date.year
    df_last = df[(df["Data e Ora"].dt.month == last_month) & (df["Data e Ora"].dt.year == last_year)]
    last_values = df_last.mean(numeric_only=True)
    df_prev = df[(df["Data e Ora"].dt.month == last_month) & (df["Data e Ora"].dt.year == (last_year - 1))]
    if not df_prev.empty:
        prev_values = df_prev.mean(numeric_only=True)
    else:
        prev_values = None
    df_same_month = df[df["Data e Ora"].dt.month == last_month]
    prod_mean = df_same_month["Produzione (kg/ha)"].mean()
    prod_std = df_same_month["Produzione (kg/ha)"].std()
    unit = {
        "Temperatura (°C)": "°C",
        "Umidità (%)": "%",
        "Precipitazioni (mm)": "mm",
        "Produzione (kg/ha)": "kg/ha",
        "Efficienza (%)": "%"
    }
    kpi_labels = {
        "Temperatura (°C)": "Temp (°C)",
        "Umidità (%)": "Umid. (%)",
        "Precipitazioni (mm)": "Pioggia (mm)",
        "Produzione (kg/ha)": "Prod. (kg/ha)",
        "Efficienza (%)": "Eff. (%)"
    }
    cards = []
    for col in kpi_labels.keys():
        current_val = round(last_values[col], 2)
        if prev_values is not None:
            prev_val = round(prev_values[col], 2)
            diff = current_val - prev_val
            if diff > 0:
                arrow = html.Span(
                    f"↑ +{round(diff, 2)} {unit[col]} rispetto allo scorso anno",
                    style={"color": "green", "fontWeight": "bold", "marginLeft": "5px"}
                )
            elif diff < 0:
                arrow = html.Span(
                    f"↓ -{abs(round(diff, 2))} {unit[col]} rispetto allo scorso anno",
                    style={"color": "red", "fontWeight": "bold", "marginLeft": "5px"}
                )
            else:
                arrow = html.Span(
                    "→ 0 rispetto allo scorso anno",
                    style={"color": "gray", "fontWeight": "bold", "marginLeft": "5px"}
                )
        else:
            arrow = html.Span("?", style={"color": "gray", "fontWeight": "bold", "marginLeft": "5px"})
        card_style = {"minWidth": "180px", "border": "none", "boxShadow": "0 2px 5px rgba(0,0,0,0.1)"}
        if col == "Produzione (kg/ha)":
            deviation = abs(current_val - prod_mean)
            if deviation <= prod_std:
                card_style["backgroundColor"] = "lightgreen"
            elif prod_std < deviation <= 2 * prod_std:
                card_style["backgroundColor"] = "orange"
            else:
                card_style["backgroundColor"] = "lightcoral"
        card = dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H4(kpi_labels[col], className="card-title text-center text-secondary",
                            style={"fontSize": "1rem", "whiteSpace": "nowrap"}),
                    arrow
                ], className="text-center mb-2"),
                html.P(f"{current_val}", className="card-text text-center text-primary mb-0",
                       style={"fontSize": "22px", "whiteSpace": "nowrap"})
            ]),
            className="m-2",
            style=card_style
        )
        cards.append(card)

    legenda_colori = html.Div([
        html.P("Legenda Produzione (kg/ha):", style={"fontWeight": "bold"}),
        html.Ul([
            html.Li("Verde: valore entro 1 dev. std dalla media storica del mese"),
            html.Li("Arancione: valore tra 1 e 2 dev. std dalla media storica del mese"),
            html.Li("Rosso: valore oltre 2 dev. std dalla media storica del mese")
        ], style={"fontSize": "14px"})
    ], style={"marginTop": "10px"})

    return html.Div([dbc.Row(cards, justify="center", className="mt-3"), legenda_colori])

@app.callback(
    Output("lastmonth-modal", "is_open"),
    [Input("open-lastmonth-modal", "n_clicks"),
     Input("close-lastmonth-modal", "n_clicks")],
    State("lastmonth-modal", "is_open")
)
def toggle_lastmonth_modal(open_clicks, close_clicks, is_open):
    if open_clicks or close_clicks:
        return not is_open
    return is_open

# 5) API Meteo real-time
def get_weather_forecast():
    url = "http://api.weatherapi.com/v1/forecast.json"
    params = {
        "key": "d61ca0082fa0495f83d234117251303",
        "q": "Castel Di Tora",
        "days": 3,
        "aqi": "no",
        "alerts": "no"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        forecast_days = data.get("forecast", {}).get("forecastday", [])
        cards = []

        for day in forecast_days:
            date_str = day.get("date", "")
            day_info = day.get("day", {})
            astro_info = day.get("astro", {})

            avgtemp_c = day_info.get("avgtemp_c", "N/A")
            avghumidity = day_info.get("avghumidity", "N/A")
            totalprecip_mm = day_info.get("totalprecip_mm", "N/A")

            sunrise = astro_info.get("sunrise", "")
            sunset = astro_info.get("sunset", "")

            condition = day_info.get("condition", {})
            condition_text = condition.get("text", "")
            icon_url = condition.get("icon", "")
            if icon_url.startswith("//"):
                icon_url = "https:" + icon_url

            card = dbc.Card(
                dbc.CardBody([
                    html.H6(date_str, className="card-title",
                            style={"fontSize": "0.9rem", "fontWeight": "bold"}),

                    html.Div([
                        html.Img(src=icon_url, style={"width": "32px", "margin": "5px"})
                    ], style={"textAlign": "center"}),

                    html.P(condition_text,
                           style={"fontSize": "0.8rem", "margin": "2px"}),

                    html.P(f"Temp: {avgtemp_c}°C",
                           style={"fontSize": "0.8rem", "margin": "2px"}),
                    html.P(f"Umidità: {avghumidity}%",
                           style={"fontSize": "0.8rem", "margin": "2px"}),
                    html.P(f"Precipitazioni: {totalprecip_mm} mm",
                           style={"fontSize": "0.8rem", "margin": "2px"}),

                    html.P(f"Alba: {sunrise}  |  Tramonto: {sunset}",
                           style={"fontSize": "0.8rem", "margin": "2px"})
                ]),
                className="m-2",
                style={"minWidth": "160px", "textAlign": "center"}
            )
            cards.append(card)

        return dbc.Row(cards, justify="center", className="mt-3")
    else:
        return html.Div("Impossibile ottenere le previsioni meteo.")

@app.callback(
    Output("weather-modal-content", "children"),
    Input("weather-modal", "is_open")
)
def update_weather_modal(is_open):
    if is_open:
        return get_weather_forecast()
    return ""

@app.callback(
    Output("weather-modal", "is_open"),
    [Input("open-weather-modal", "n_clicks"),
     Input("close-weather-modal", "n_clicks")],
    State("weather-modal", "is_open")
)
def toggle_weather_modal(open_clicks, close_clicks, is_open):
    if open_clicks or close_clicks:
        return not is_open
    return is_open

# 6) Analisi periodo migliore
@app.callback(
    [Output('grafico-condizioni', 'figure'),
     Output('analisi-condizioni', 'children')],
    Input('interval-update', 'n_intervals')
)
def analisi_condizioni(_):
    df = carica_dati()
    df = df.sort_values(by='Data e Ora', ascending=True)
    migliore_periodo = df.loc[df['Produzione (kg/ha)'].idxmax()]
    cond_migliori = df.groupby('Temperatura (°C)')['Produzione (kg/ha)'].mean().idxmax()
    fig = px.scatter(df, x='Temperatura (°C)', y='Produzione (kg/ha)',
                     title='Relazione tra Temperatura e Produzione',
                     color='Temperatura (°C)')
    testo = (
        f"Il periodo con la produzione migliore è {migliore_periodo['Data']} "
        f"con {migliore_periodo['Produzione (kg/ha)']} kg/ha. "
        f"Le condizioni ottimali si verificano con una temperatura di circa {cond_migliori}°C."
    )
    return fig, testo

@app.callback(
    Output("modal", "is_open"),
    [Input("open-analisi-modal", "n_clicks"),
     Input("close-analisi-modal", "n_clicks")],
    State("modal", "is_open")
)
def toggle_modal(open_clicks, close_clicks, is_open):
    if open_clicks or close_clicks:
        return not is_open
    return is_open

# 7) Visualizzazione Tabella Dati Completi
@app.callback(
    [Output('data-table', 'data'),
     Output('data-table', 'columns')],
    [Input('interval-update', 'n_intervals'),
     Input('order-dropdown', 'value')]
)
def update_data_table(_, order_column):
    df = carica_dati()
    df = df.sort_values(by='Data e Ora', ascending=True)
    display_cols = ["Data", "Temperatura (°C)", "Umidità (%)",
                    "Precipitazioni (mm)", "Produzione (kg/ha)", "Efficienza (%)"]
    if order_column == "Data":
        df = df.sort_values(by="Data e Ora", ascending=True)
    elif order_column in df.columns:
        df = df.sort_values(by=order_column, ascending=True)
    data = df[display_cols].to_dict('records')
    columns = [{"name": col, "id": col} for col in display_cols]
    return data, columns

@app.callback(
    Output("data-modal", "is_open"),
    [Input("open-data-modal", "n_clicks"),
     Input("close-data-modal", "n_clicks")],
    State("data-modal", "is_open")
)
def toggle_data_modal(open_clicks, close_clicks, is_open):
    if open_clicks or close_clicks:
        return not is_open
    return is_open

# 8) KPI Ultimo Anno
@app.callback(
    Output("lastyear-kpi-modal-content", "children"),
    Input('interval-update', 'n_intervals')
)
def aggiorna_lastyear_kpi_modal(_):
    df = carica_dati()
    df['year'] = df['Data e Ora'].dt.year
    df['month'] = df['Data e Ora'].dt.month

    # Stagioni + emoji
    cond_2024_inverno = ((df['year'] == 2024) & (df['month'].isin([1, 2]))) | ((df['year'] == 2023) & (df['month'] == 12))
    cond_2023_inverno = ((df['year'] == 2023) & (df['month'].isin([1, 2]))) | ((df['year'] == 2022) & (df['month'] == 12))

    cond_2024_primavera = (df['year'] == 2024) & (df['month'].isin([3, 4, 5]))
    cond_2023_primavera = (df['year'] == 2023) & (df['month'].isin([3, 4, 5]))

    cond_2024_estate = (df['year'] == 2024) & (df['month'].isin([6, 7, 8]))
    cond_2023_estate = (df['year'] == 2023) & (df['month'].isin([6, 7, 8]))

    cond_2024_autunno = (df['year'] == 2024) & (df['month'].isin([9, 10, 11]))
    cond_2023_autunno = (df['year'] == 2023) & (df['month'].isin([9, 10, 11]))

    stagioni = {
        "Inverno": (cond_2024_inverno, cond_2023_inverno, "❄️", [12, 1, 2]),
        "Primavera": (cond_2024_primavera, cond_2023_primavera, "🌸", [3, 4, 5]),
        "Estate": (cond_2024_estate, cond_2023_estate, "☀️", [6, 7, 8]),
        "Autunno": (cond_2024_autunno, cond_2023_autunno, "🍂", [9, 10, 11])
    }

    # Nuovi indicatori
    indicatori = ["Produzione (kg/ha)", "Temperatura (°C)", "Precipitazioni (mm)", "Efficienza (%)"]

    season_cards = []
    style_card = {
        "minWidth": "100px",
        "border": "none",
        "boxShadow": "0 2px 5px rgba(0,0,0,0.1)"
    }

    for stagione, (cond_2024, cond_2023, emoji_stagione, months_stagione) in stagioni.items():
        card_elements = []
        cond_media_storica = df['month'].isin(months_stagione)

        for ind in indicatori:
            media_2024 = df.loc[cond_2024, ind].mean()
            media_2023 = df.loc[cond_2023, ind].mean()
            media_storica = df.loc[cond_media_storica, ind].mean()

            # Confronto vs anno precedente
            if pd.notna(media_2024) and pd.notna(media_2023):
                diff_anno_prec = media_2024 - media_2023
                if diff_anno_prec > 0:
                    arrow_anno = html.Span(
                        f"↑ +{round(diff_anno_prec, 2)} vs 2023",
                        style={"color": "green", "fontWeight": "bold", "marginLeft": "5px", "fontSize": "0.65rem"}
                    )
                elif diff_anno_prec < 0:
                    arrow_anno = html.Span(
                        f"↓ -{abs(round(diff_anno_prec, 2))} vs 2023",
                        style={"color": "red", "fontWeight": "bold", "marginLeft": "5px", "fontSize": "0.65rem"}
                    )
                else:
                    arrow_anno = html.Span(
                        "→ 0 vs 2023",
                        style={"color": "gray", "fontWeight": "bold", "marginLeft": "5px", "fontSize": "0.65rem"}
                    )
            else:
                arrow_anno = html.Span("N/A", style={"color": "gray", "fontWeight": "bold", "marginLeft": "5px", "fontSize": "0.65rem"})

            # Confronto vs media storica
            if pd.notna(media_2024) and pd.notna(media_storica):
                diff_storica = media_2024 - media_storica
                if diff_storica > 0:
                    arrow_storica = html.Span(
                        f"↑ +{round(diff_storica, 2)} vs media",
                        style={"color": "green", "fontWeight": "bold", "marginLeft": "5px", "fontSize": "0.65rem"}
                    )
                elif diff_storica < 0:
                    arrow_storica = html.Span(
                        f"↓ -{abs(round(diff_storica, 2))} vs media",
                        style={"color": "red", "fontWeight": "bold", "marginLeft": "5px", "fontSize": "0.65rem"}
                    )
                else:
                    arrow_storica = html.Span(
                        "→ 0 vs media",
                        style={"color": "gray", "fontWeight": "bold", "marginLeft": "5px", "fontSize": "0.65rem"}
                    )
            else:
                arrow_storica = html.Span("N/A", style={"color": "gray", "fontWeight": "bold", "marginLeft": "5px", "fontSize": "0.65rem"})

            # Valore 2024
            if pd.notna(media_2024):
                valore = f"{round(media_2024, 2)}"
            else:
                valore = "N/A"

            card_elements.append(
                dbc.Card(
                    dbc.CardBody([
                        html.H6(ind, className="card-title", style={"fontSize": "0.65rem", "textAlign": "center"}),
                        html.P(valore, className="card-text text-center", style={"fontSize": "0.8rem"}),
                        html.Div(arrow_anno, style={"textAlign": "center"}),
                        html.Div(arrow_storica, style={"textAlign": "center"})
                    ]),
                    className="m-1",
                    style=style_card
                )
            )

        season_card = dbc.Card(
            [
                dbc.CardHeader(
                    html.H5(f"{emoji_stagione} {stagione}", className="text-center",
                            style={"color": "#16a085", "fontSize": "0.8rem"})
                ),
                dbc.CardBody(
                    dbc.Row(card_elements, justify="center", className="gx-1 gy-1")
                )
            ],
            className="m-1",
            style={"border": "1px solid #e3e3e3", "boxShadow": "0 2px 5px rgba(0,0,0,0.1)"}
        )
        season_cards.append(season_card)

    # Layout delle stagioni
    if len(season_cards) == 4:
        layout_stagioni = html.Div([
            dbc.Row([
                dbc.Col(season_cards[0], width=6),
                dbc.Col(season_cards[1], width=6)
            ], className="mb-1"),
            dbc.Row([
                dbc.Col(season_cards[2], width=6),
                dbc.Col(season_cards[3], width=6)
            ])
        ])
    else:
        layout_stagioni = html.Div(season_cards)

    return layout_stagioni

@app.callback(
    Output("lastyear-kpi-modal", "is_open"),
    [Input("open-lastyear-kpi-modal", "n_clicks"),
     Input("close-lastyear-kpi-modal", "n_clicks")],
    State("lastyear-kpi-modal", "is_open")
)
def toggle_lastyear_kpi_modal(open_clicks, close_clicks, is_open):
    if open_clicks or close_clicks:
        return not is_open
    return is_open

if __name__ == '__main__':
    app.run_server(debug=True)
