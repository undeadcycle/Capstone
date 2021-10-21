import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

app = dash.Dash(__name__)

app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                html.Br(),
                                dcc.Dropdown(id='site_dropdown',
                                            options=[{'label':'All Sites','value':'ALL'},
                                                    {'label':'CCAFS LC-40','value':'CCAFS LC-40'},
                                                    {'label':'VAFB SLC-4E','value':'VAFB SLC-4E'},
                                                    {'label':'KSC LC-39A','value':'KSC LC-39A'},
                                                    {'label':'CCAFS SLC-40','value':'CCAFS SLC-40'}],
                                            value='ALL',
                                            placeholder='Select a launch site here',
                                            searchable=True),
                                html.Br(),

                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,
                                                max=10000,
                                                step=1000,
                                                marks={0:'0',100:'100'},
                                                value=[min_payload,max_payload]),

                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
                Input(component_id='site_dropdown', component_property='value'))
def get_pie_chart (site_dropdown):
    filtered_df = spacex_df
    if site_dropdown == 'ALL':
        fig = px.pie(spacex_df,
                    values='class',
                    names='Launch Site',
                    title='Total Success Launches')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == site_dropdown]
        filtered_df = filtered_df.groupby(['Launch Site','class']).size().reset_index(name='class count')
        fig=px.pie(filtered_df,
                    values='class count',
                    names='class',
                    title="Total Success Launches for site")
        return fig

@app.callback(Output(component_id='success-payload-scatter-chart',component_property='figure'),
                [Input(component_id='site_dropdown',component_property='value'),
                Input(component_id='payload-slider',component_property='value')])

def scatter (site_dropdown,payload):
    low,high=payload
    mask=(spacex_df['Payload Mass (kg)']>low)&(spacex_df['Payload Mass (kg)']<high)
    filtered_df = spacex_df[mask]
    if site_dropdown == 'ALL':
        fig = px.scatter(spacex_df, x='Payload Mass (kg)', y='class',
                            color='Booster Version Category',
                            title='Payload vs. Outcome for All Sites')
        return fig
    else:
        filtered_df1 = filtered_df[filtered_df['Launch Site']==site_dropdown]
        fig = px.scatter (filtered_df1, x='Payload Mass (kg)', y='class',
                            color='Booster Version Category',
                            title='Payload and Booster Versions for site')
        return fig

if __name__ == '__main__':
    app.run_server()
