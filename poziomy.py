# importing necessery modules
import glob
from datetime import date, timedelta
from dash import dcc, html, Input, Output, dash
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

# creating path to data files
folder_path = '/home/piotrmichna/meteo'
file_type = '/*csv'
files = glob.glob(folder_path + file_type)

# creating data variables
today_date = date.today()
today = today_date.strftime('%d/%m/%Y')
yesterday_date = today_date - timedelta(days=1)
yesterday = yesterday_date.strftime('%d/%m')

# Creating an empty list for the file system
files_lst = []

# Appending to the empty list two newest file from the data folder
for each in files:
    files_lst.append(each)

latest_file = files_lst[-1]
second_file = files_lst[-2]

todays_data = pd.read_csv(latest_file, names=["Data - godzina", "Stacja - Rzeka", "Poziom wody w cm"],
                          on_bad_lines='skip').dropna(axis=0, how='any')
yesterday_data = data_1 = pd.read_csv(second_file, names=["Data - godzina", "Stacja - Rzeka", "Poziom wody w cm"],
                                      on_bad_lines='skip').dropna(axis=0, how='any')
two_days_data = pd.concat([todays_data, yesterday_data])

drop_down_lst = todays_data['Stacja - Rzeka'].sort_values().unique()

app = dash.Dash(__name__,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}])

app.layout = dbc.Container([

    dbc.Row([
        dbc.Col([
            html.Br(),
            html.B('Wybierz stację pomiaru', style={'textAlign': 'center', 'color': '#000709'}),
        ], width=12)], justify="center"),

    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id="dropdown",
                options=drop_down_lst,
                clearable=False,
                placeholder="Wybierz stację pomiaru",
                value='San - Lesko',
                style={'margin': 'auto', 'width': '100%', 'align-items': 'center', 'justify-content': 'center'}
            )], width=12)], justify="center"),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id="graph")], width=12)], justify="center"),

    dbc.Row([
        dbc.Col(
            [html.Br(),
             dcc.Markdown('''
    ** Kontakt:**\n
    info@naszerzeki.pl \n       

    ** Dane do wykresu: **\n
    https://danepubliczne.imgw.pl/''')], width=10)], style={"height": "200%"}, justify="center")

])


@app.callback(
    Output("graph", "figure"),
    Input("dropdown", "value"))
def update_line_chart(station):
    df = two_days_data.sort_values(by='Data - godzina')
    mask = df["Stacja - Rzeka"] == station
    df['Data - godzina'] = pd.to_datetime(df['Data - godzina']).dt.strftime('%d.%m - %H:%M')
    fig = px.line(df[mask], x='Data - godzina', y="Poziom wody w cm", markers=True,
                  title='{} {} - {}.'.format(station, yesterday, today))
    fig.update_xaxes(type='category', tickangle=90)
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey')
    fig.update_layout(title=dict(x=0.5), margin=dict(l=5, r=5, t=100, b=20))
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })

    return fig


app.run_server(debug=True)