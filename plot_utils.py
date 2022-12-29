# -- import modules
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import plotly.express as px
from adtk.data import validate_series


def plot_gender(x, digits=1, title=""):
    """ Return gender figure pourcent of a serie of value (x)"""

    # -- Check input
    err_msg = ValueError(f"`x` must be a {pd.Series.__module__}")
    assert isinstance(x, pd.Series), msg

    # -- Compute gender percent
    gender = (
        x
        .value_counts(normalize=True)
        .mul(100)
        .round(digits)
    )

    # -- Plot scatter figure
    fig = px.scatter(x=[1, 1.2, 1.3], y=[0, 0, 0], color_discrete_sequence=['#fff'])
    # -- Hide xy axes
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_traces(textposition='top center')
    fig.update_layout(height=375, width=500,
                      plot_bgcolor='#fff', paper_bgcolor='#fff',
                      margin=dict(b=0, r=50, l=50, t=110),
                      title={'text': title,
                             'y': 0.8, 'x': 0.5,
                             'xanchor': 'center', 'yanchor': 'top'},
                      font=dict(size=9, color='#666')
                      )

    # -- Add Man image
    fig.add_layout_image(
        dict(
            source="https://i.imgur.com/3Cab96Z.jpg",
            xref="paper", yref="paper",
            x=0.4, y=0.38,
            sizex=0.6, sizey=0.635,
            xanchor="right", yanchor="bottom", sizing="contain"
        )
    )

    # -- Add Women image
    fig.add_layout_image(
        dict(
            source="https://i.imgur.com/c6QKoDy.jpg",
            xref="paper", yref="paper",
            x=0.7, y=0.38,
            sizex=0.6, sizey=0.65,
            xanchor="right", yanchor="bottom", sizing="contain",
        )
    )

    # -- Add % and names
    fig.add_annotation(
        dict(
            x=0.37, y=0.3, ax=0, ay=0,
            xref="paper", yref="paper",
            text="<b>{}%</b>".format(gender.values[1]),
            font=dict(color='black', size=22, family="sans serif")
        )
    )

    fig.add_annotation(
        dict(
            x=0.66, y=0.3, ax=0, ay=0,
            xref="paper", yref="paper",
            text="<b>{}%</b>".format(gender.values[0]),
            font=dict(color='black', size=22, family="sans serif")
        )
    )

    # -- Return plotly figure
    return fig


def get_barpolar_fig(df, col, tickevery=2, **kwargs):
    """ Return bar polar figure according to selected column """
    # -- Perform groupby on given time period column
    df_gb = (
        df
        .groupby(by=col, as_index=False)
        .agg({'Num_Acc': 'count'})
        .rename(columns={'Num_Acc': 'n_accident'})
        .astype({col: str})
    )
    # -- Build bar polar figure
    fig = px.bar_polar(
        df_gb,
        r='n_accident',
        theta=col,
        hover_data={"n_accident": True, col: True},
        color="n_accident",
        color_continuous_scale='algae',
        template='ggplot2',
        barnorm='fraction',
        **kwargs
    )

    fig.add_annotation(text="<b>Safe</b>",
                       x=0.5,
                       y=0.5,
                       font=dict(size=18),
                       showarrow=False)

    # -- Update layout
    fig.update_layout(
        coloraxis=dict(
            colorbar=dict(
                title=dict(
                    font=dict(size=14),
                    text='<b>Number of accident</b>',
                    side='right'
                )
            )
        ),
        polar=dict(
            hole=0.18,
            angularaxis=dict(
                categoryarray=df_gb[col].unique(),
                tickmode="array",
                tickvals=df_gb[col].unique().tolist()[::tickevery],
                ticktext=df_gb[col].unique().tolist()[::tickevery]
            ),
            radialaxis=dict(
                showticklabels=False,
                ticks='',
                linewidth=0
            )
        )
    )

    # -- Return figure
    return fig


def plot_anomalies(ts, anomalies):
    """ Return a line plot of time series with highlighted anomalic values"""
    # -- Validate timeseries
    ts = validate_series(ts)
    # -- Inititate graph object list
    data = []
    # -- Add data (line)
    data.append(go.Scatter(x=ts.index,
                           y=ts,
                           name=ts.name,
                           mode='lines',
                           line=dict(color='#4d6f08',
                                     width=1)))
    # -- Add anomaly markers
    data.append(go.Scatter(x=ts[anomalies].index,
                           y=ts[anomalies],
                           name='Anomalies',
                           mode='markers',
                           marker=dict(color='rgba(254, 79, 79, 0.3)',
                                       size=7.5,
                                       line=dict(color='red',
                                                 width=1.1))))
    # -- Build layout
    layout = dict(template='ggplot2',
                  height=300,
                  width=950,
                  margin=dict(t=10, l=10, r=10, b=10),
                  xaxis=dict(type='date'),
                  legend=dict(orientation="v",
                              yanchor="top",
                              y=.95,
                              xanchor="right",
                              x=.97))
    # -- Create figure
    fig = go.Figure(data=data, layout=layout)

    # -- Return fugure
    return fig


def plot_ts_components(df, col, trend, seasonal, rolling, template='plotly_dark'):
    """ Plot several components of a time series (moving average, trend, ...) """
    # -- Inititate graph object list
    data = []
    # -- Add Seasonal trace (as xaxis)
    data.append(go.Scatter(x=df.index,
                           y=[0] * len(df),
                           xaxis='x',
                           yaxis='y',
                           mode='lines',
                           showlegend=False,
                           line=dict(color='black',
                                     width=1)))
    data.append(go.Scatter(x=df.index,
                           y=df[seasonal],
                           name='Seasonal decomposition (365 days)',
                           xaxis='x',
                           yaxis='y',
                           mode='lines',
                           line=dict(color='#bc9768',
                                     width=1)))
    # -- Add raw accident number trace
    data.append(go.Scatter(x=df.index,
                           y=df[col],
                           name='Number of accident',
                           xaxis='x2',
                           yaxis='y2',
                           mode='lines',
                           line=dict(color='#4cdbb5',
                                     width=0.5)))
    # -- Add moving average trace
    data.append(go.Scatter(x=df.index,
                           y=df[rolling],
                           name='Moving average ({} days)'.format(rolling.split('_')[-1]),
                           xaxis='x2',
                           yaxis='y2',
                           mode='lines',
                           line=dict(color='#db00db',
                                     width=1.4)))
    # -- Add trend trace
    data.append(go.Scatter(x=df.index,
                           y=df[trend],
                           name='Trend',
                           xaxis='x2',
                           yaxis='y2',
                           mode='lines',
                           line=dict(color='red',
                                     width=2.2,
                                     dash='dash')))
    # -- Build layout
    layout = dict(template=template,
                  margin=dict(t=10, l=0, r=30, b=15),
                  yaxis2=dict(color='gray',
                              linecolor='gray',
                              showgrid=False,
                              mirror=True),
                  xaxis2=dict(type='date',
                              overlaying='x',
                              matches='x',
                              visible=False),
                  yaxis=dict(visible=False),
                  xaxis=dict(type='date',
                             automargin=True,
                             color='gray',
                             linecolor='gray',
                             showgrid=False,
                             mirror=True,
                             rangeslider=dict(visible=True,
                                              bordercolor='gray')),
                  legend=dict(orientation="h",
                              yanchor="top",
                              y=1.1,
                              xanchor="center",
                              x=0.5,
                              font=dict(size=13)))
    # -- Build figure
    fig = go.Figure(data=data, layout=layout)
    # -- Add annotation on  xaxis
    fig.add_annotation(dict(xref='paper',
                            yref='paper',
                            text='<b>Seasonal patterns</b>',
                            showarrow=False,
                            x=0.5,
                            y=-0.338,
                            font=dict(size=16,
                                      family='Courier New, monospace',
                                      color='#bc9768'),
                            align='center'))
    # -- Return main figure
    return fig


def plot_dist_box(data, group_labels, colors, bin_size=40, template='ggplot2'):
    """ Build a combinaiton of dist, kde and box plot in a same figure """
    # -- Build boxplots
    boxplots = [
        go.Box(x=x,
               boxmean=True,
               line=dict(width=1, color='black'),
               fillcolor=c,
               orientation='h',
               opacity=.8,
               showlegend=False) for x, c in zip(data, colors)
    ]

    # -- Build distplot figure as widget
    distplots = ff.create_distplot(
        hist_data=data,
        group_labels=group_labels,
        bin_size=bin_size,
        colors=colors,
        curve_type='kde',
        show_rug=False,
    )

    # -- Create and organize subplots
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        row_heights=[0.25, 0.7],
        vertical_spacing=0
    )

    # -- Add traces one-by-one
    for trace in boxplots:
        fig.append_trace(trace, row=1, col=1)
    for trace in distplots['data']:
        fig.append_trace(trace, row=2, col=1)

    # -- Updating layout
    fig.update_layout(
        template=template,
        barmode='overlay',
        margin=dict(l=0, r=20, t=15, b=5),
        height=500,
        yaxis=dict(showticklabels=False, ticks=''),
        xaxis2=dict(ticks="inside"),
        legend=dict(
            orientation='h',
            yanchor="top",
            y=1.08,
            xanchor="center",
            x=0.5,
            font=dict(size=15)
        )
    )
    # -- Return figure
    return fig
