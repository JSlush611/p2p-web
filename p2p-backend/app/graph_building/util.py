from plotly import graph_objs as go

def calculate_percentile(series, value):
    rank = series.rank(pct=True).loc[series == value]
    if rank.empty:
        return None
    else:
        return rank.values[0] * 100

def customize_layout(title, xaxis_title, yaxis_title, barmode=None):
    layout = go.Layout(
        title=title,
        xaxis=dict(title=xaxis_title, title_font=dict(size=14)),
        yaxis=dict(title=yaxis_title, title_font=dict(size=14)),
        barmode=barmode,
        legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2),
        hovermode="closest",
        margin=dict(l=50, r=50, t=50, b=50),
        font=dict(family="Arial, sans-serif", size=12, color="#7f7f7f"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        template="plotly_white",
        dragmode="pan",
        modebar=dict(
            orientation="v",
            bgcolor="rgba(0,0,0,0)",
            color="#7f7f7f",
            activecolor="#FF5733",
        ),
    )
    return layout