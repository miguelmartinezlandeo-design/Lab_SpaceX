# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
spacex_df['Payload Mass (kg)'] = pd.to_numeric(spacex_df['Payload Mass (kg)'], errors='coerce').fillna(0)
spacex_df['class'] = spacex_df['class'].astype(int)
max_payload = int(spacex_df['Payload Mass (kg)'].max())
min_payload = int(spacex_df['Payload Mass (kg)'].min())

# Create a dash application
app = dash.Dash(__name__)

# Create a dash application layout
app.layout = html.Div(children=[
    html.H1(
        'SpaceX Launch Records Dashboard',
        style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}
    ),
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
        ],
        value='ALL',
        placeholder='Select a Launch Site',
        searchable=True
    ),
    html.Br(),
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    html.P('Payload range (Kg):'),
    dcc.RangeSlider(
        id='payload-slider',
        min=min_payload,
        max=max_payload,
        value=[min_payload, max_payload],
        step=max(1000, (max_payload - min_payload) // 10),
        allowCross=False,
        tooltip={'always_visible': True, 'placement': 'bottom'}
    ),
    html.Br(),
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])


@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        site_data = spacex_df.groupby('Launch Site', as_index=False).agg(successful_launches=('class', 'sum'))
        fig = px.pie(
            site_data,
            names='Launch Site',
            values='successful_launches',
            title='Lanzamientos exitosos totales por sitio'
        )
    else:
        site_data = spacex_df[spacex_df['Launch Site'] == selected_site]
        counts = site_data['class'].value_counts().rename(index={1: 'Satisfactorio', 0: 'Fracaso'}).reset_index()
        counts.columns = ['Outcome', 'count']
        fig = px.pie(
            counts,
            names='Outcome',
            values='count',
            title=f'Satisfactorio vs fracaso de lanzamientos para {selected_site}',
            color='Outcome',
            color_discrete_map={'Satisfactorio': '#2ca02c', 'Fracaso': '#d62728'}
        )
    return fig


@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'), Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_range):
    filtered_df = spacex_df if selected_site == 'ALL' else spacex_df[spacex_df['Launch Site'] == selected_site]
    min_value, max_value = payload_range
    filtered_df = filtered_df[(filtered_df['Payload Mass (kg)'] >= min_value) & (filtered_df['Payload Mass (kg)'] <= max_value)]

    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        hover_name='Launch Site',
        size='Flight Number',
        title='Masa de la carga útil vs resultado del lanzamiento',
        labels={'class': 'Resultado del lanzamiento (1 = Exito, 0 = Fracaso)', 'Payload Mass (kg)': 'Masa de la carga útil (kg)'}
    )
    fig.update_yaxes(tickvals=[0, 1], ticktext=['Fracaso', 'Exito'])
    return fig


# Run the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)

## PARA PODER VER EL DASH EN TERMINAL TIENES Q PONER
# (.venv) miguel@LAPTOP-FGN1E5V9:~/mi_entorno/Python/Modulo10$ python3.12 spacex-dash-app.py
