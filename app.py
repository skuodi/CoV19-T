import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output

app = dash.Dash('__main__')
server = app.server
df = pd.read_csv('data/african.csv',index_col=1,parse_dates=True)
#fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')

fig = go.Figure(go.Scattergeo())
fig.update_geos(
    #projection_type="orthographic",
    resolution=50,scope="africa",
    showcoastlines=True, coastlinecolor="RebeccaPurple",
    showland=True, landcolor="LightGreen",
    showocean=True, oceancolor="LightBlue",
    showlakes=True, lakecolor="Blue",
    showcountries=True,
    showrivers=True, rivercolor="Blue"
)
fig.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})

def get_options(list_stocks):
    dict_list = []
    for i in list_stocks:
        dict_list.append({'label': i, 'value': i})

    return dict_list

app.layout = html.Div(children=[
                      html.Div(className='row',  # Define the row element
                               children=[
                                    html.Div(className='four columns div-user-controls',children=[
                                    html.H1('COVID19 TRACKER'),
                                    html.H2('''A Visualisation of Covid 19 cases in Africa'''),
                                    html.P('''Pick one or more countries from the dropdown below to view and compare.'''),
                                    html.Div(className='div-for-dropdown',
                                      children=[
                                          dcc.Dropdown(id='stockselector',
                                                       options=get_options(df['location'].unique()),
                                                       multi=True,
                                                       value=[df['location'].sort_values()[0]],
                                                       style={'backgroundColor': '#1E1E1E'},
                                                       className='stockselector')
                                                ],
                                      style={'color': '#1E1E1E'}),
                                    html.Div(className='div-for-dropdown',
                                      children=[
                                            dcc.Graph(figure=fig) # Define the right element
                                                ],
                                      style={'color': '#1E1E1E'}),

                                    ])
                                    ,  # Define the left element

                                    html.Div(className='eight columns div-for-charts bg-grey',
                                    children=[
                                        #dcc.Graph(figure=fig) # Define the right element
                                        dcc.Graph(id='timeseries',
                                            config={'displayModeBar': False},
                                            animate=True,
                                            figure=px.line(df,
                                                 x='date',
                                                 y='new_cases',
                                                 color='location',
                                                 template='plotly_dark').update_layout(
                                                   {'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                                    'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
                                                                        )

                                    ])
                                    ])
                                    ])

@app.callback(Output('timeseries', 'figure'),
              [Input('stockselector', 'value')])
def update_timeseries(selected_dropdown_value):
    ''' Draw traces of the feature 'value' based one the currently selected stocks '''
    # STEP 1
    trace = []  
    df_sub = df
    # STEP 2
    # Draw and append traces for each stock
    for stock in selected_dropdown_value:   
        trace.append(go.Scatter(x=df_sub[df_sub['location'] == stock].index,
                                 y=df_sub[df_sub['location'] == stock]['new_cases'],
                                 mode='lines',
                                 opacity=0.7,
                                 name=stock,
                                 textposition='bottom center'))  
    # STEP 3
    traces = [trace]
    data = [val for sublist in traces for val in sublist]
    # Define Figure
    # STEP 4
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'b': 15},
                  hovermode='x',
                  autosize=True,
                  title={'text': 'New Cases Per Day', 'font': {'color': 'white'}, 'x': 0.5},
                  xaxis={'range': [df_sub.index.min(), df_sub.index.max()]},
              ),

              }

    return figure

                                
if __name__ == '__main__':
    app.run_server(debug=True)
