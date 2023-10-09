from dash import Dash, dash_table, dcc, html,Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.tools as tls
import plotly.graph_objs as go
from backend.granulometria import granulometria
#from backend.cartaplasticidad import *

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H1("Tabla de granulometria"),
    dash_table.DataTable(
        id='tabla_granulometria',
        columns=[
            {'name':'Malla','id':'Malla','editable':False},
            {'name':'Abertura','id':'Abertura','editable': False},
            {'name':'Retenido','id':'Retenido','editable': True},
            {'name':'Retenido_acum','id':'Retenido_acum','editable':False},
            {'name':'Pasa','id':'Pasa','editable':False},
            {'name':'Por_pasa','id':'Por_Pasa','editable':False},
        ],
        data=granulometria.to_dict('records')

    ),
    dcc.Graph(id='granulometria-plot')
])


@callback(
    Output('tabla_granulometria','data'),
    [Input('tabla_granulometria','data'),
     Input('tabla_granulometria','columns')]
)

def update_grabulometria_table(rows,colums):
    granulometria = pd.DataFrame(rows)
    granulometria["Retenido"]=granulometria["Retenido"].astype("int")
    granulometria["Retenido_acum"]=granulometria["Retenido"].cumsum()
    granulometria["Pasa"] = granulometria["Retenido"].sum()-granulometria["Retenido_acum"]
    granulometria["Por_pasa"]= round(granulometria["Pasa"]*100/granulometria["Retenido"].sum(),2)

    granulometria["Retenido"]=granulometria["Retenido"].astype(str)
    granulometria["Retenido_acum"]=granulometria["Retenido_acum"].astype(str)
    granulometria["Pasa"] = granulometria["Pasa"].astype(str)
    granulometria["Por_pasa"]=granulometria["Por_Pasa"].astype(str)

    return granulometria.to_dict('records')


@app.callback(
    Output('granulometria-plot','figure'),
    [Input('tabla_granulometria','data')]
)
def update_granulometria_plot(rows):
    granulometria = pd.DataFrame(rows)
    
    trace = go.scatter(
        x=granulometria['Abertura'][0:11],
        y=granulometria['Por_pasa'][0:11],
        mode='lines',
        line=dict(color='black',width=2),
        name='Curva Granulometrica'
    )

    layout = go.Layout(
        title = 'Curva Granulometrica',
        xaxis = dict(
            title = 'Tamiz (mm)',
            type = 'log',
            autorange = True,
        ),
        yaxis = dict(
            title = 'Prcentaje Pasa Acumulado %',
            range = [0,100],
        )
    )

    return{'data':[trace],'layout': layout}
    
if __name__ == "__main__":
    app.run_server(debug=True)
