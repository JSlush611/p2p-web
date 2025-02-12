from app.graph_building.util import customize_layout
from plotly import graph_objs as go
from flask import jsonify

# General Plot Functions
def plot_participation_by_year(df):
    participation = df.groupby("Year")["Name"].count()
    trace = go.Bar(
        x=participation.index.tolist(),
        y=participation.tolist(),
        name="Participants",
        marker=dict(color="skyblue"),
    )
    layout = customize_layout(
        "Overall Participation by Year", "Year", "Number of Participants"
    )
    fig = go.Figure(data=[trace], layout=layout)
    tabular_data = participation.reset_index().to_dict(orient="records")
    return jsonify({"graph": fig.to_json(), "table": tabular_data})


def plot_average_time_by_year(df):
    avg_time = df.groupby("Year")["Time (min)"].mean()
    overall_avg_time = df["Time (min)"].mean()
    trace1 = go.Scatter(
        x=avg_time.index.tolist(),
        y=avg_time.tolist(),
        mode="lines+markers",
        name="Average Time",
        line=dict(color="orange"),
    )
    trace2 = go.Scatter(
        x=avg_time.index.tolist(),
        y=[overall_avg_time] * len(avg_time),
        mode="lines",
        name=f"Overall Average: {overall_avg_time:.2f} min",
        line=dict(color="red", dash="dash"),
    )
    layout = customize_layout("Average Time by Year", "Year", "Average Time (min)")
    fig = go.Figure(data=[trace1, trace2], layout=layout)
    tabular_data = avg_time.reset_index().to_dict(orient="records")
    return jsonify({"graph": fig.to_json(), "table": tabular_data})


def plot_participation_by_age_group(df):
    age_group_counts = df["AgeGroup"].value_counts(sort=False)
    trace = go.Bar(
        x=age_group_counts.index.tolist(),
        y=age_group_counts.tolist(),
        name="Participants",
        marker=dict(color="green"),
    )
    layout = customize_layout(
        "Participation by Age Group", "Age Group", "Number of Participants"
    )
    fig = go.Figure(data=[trace], layout=layout)
    tabular_data = age_group_counts.reset_index().to_dict(orient="records")
    return jsonify({"graph": fig.to_json(), "table": tabular_data})


def plot_participation_by_region(df):
    top_regions = df["Region"].value_counts().head(10)
    trace = go.Bar(
        x=top_regions.index.tolist(),
        y=top_regions.tolist(),
        name="Participants",
        marker=dict(color="purple"),
    )
    layout = customize_layout(
        "Top 10 Regions by Participation", "Region", "Number of Participants"
    )
    fig = go.Figure(data=[trace], layout=layout)
    tabular_data = top_regions.reset_index().to_dict(orient="records")
    return jsonify({"graph": fig.to_json(), "table": tabular_data})


def plot_time_percentiles_by_year(df):
    percentiles = df["Time (min)"].quantile([0.25, 0.5, 0.75])
    trace = go.Bar(
        x=["25th Percentile", "50th Percentile", "75th Percentile"],
        y=percentiles.tolist(),
        name="Time (min)",
        marker=dict(color="blue"),
    )
    layout = customize_layout("Time Percentiles", "Percentile", "Time (min)")
    fig = go.Figure(data=[trace], layout=layout)
    tabular_data = [
        {"Percentile": f"{int(p*100)}th Percentile", "Time (min)": time}
        for p, time in percentiles.items()
    ]
    return jsonify({"graph": fig.to_json(), "table": tabular_data})


def plot_gender_distribution_by_year(df):
    df = df[df["Gender"].isin(["M", "F"])]
    gender_distribution = (
        df.groupby("Year")["Gender"].value_counts().unstack().fillna(0)
    )
    trace1 = go.Bar(
        x=gender_distribution.index.tolist(),
        y=gender_distribution["M"].tolist(),
        name="Male",
        marker=dict(color="#1f77b4"),
    )
    trace2 = go.Bar(
        x=gender_distribution.index.tolist(),
        y=gender_distribution["F"].tolist(),
        name="Female",
        marker=dict(color="#ff7f0e"),
    )
    layout = customize_layout(
        "Gender Distribution by Year", "Year", "Number of Participants", barmode="stack"
    )
    fig = go.Figure(data=[trace1, trace2], layout=layout)
    tabular_data = gender_distribution.reset_index().to_dict(orient="records")
    return jsonify({"graph": fig.to_json(), "table": tabular_data})


def plot_top_10_fastest_swimmers(df):
    top_10_fastest = df.nsmallest(10, "Time (min)")
    trace = go.Bar(
        x=top_10_fastest["Name"].tolist(),
        y=top_10_fastest["Time (min)"].tolist(),
        name="Time (min)",
        marker=dict(color="red"),
    )
    layout = customize_layout("Top 10 Fastest Swimmers", "Swimmer", "Time (min)")
    fig = go.Figure(data=[trace], layout=layout)
    tabular_data = top_10_fastest[["Name", "Time (min)"]].to_dict(orient="records")
    return jsonify({"graph": fig.to_json(), "table": tabular_data})


def plot_average_time_by_age_group_and_year(df):
    avg_time_age_group = df.groupby(["Year", "AgeGroup"])["Time (min)"].mean().unstack()
    traces = []
    for age_group in avg_time_age_group.columns:
        trace = go.Scatter(
            x=avg_time_age_group.index.tolist(),  # Years
            y=avg_time_age_group[
                age_group
            ].tolist(),  # Average times for this age group
            mode="lines+markers",
            name=f"{age_group}",  # Name the trace by the age group
        )
        traces.append(trace)
    layout = customize_layout(
        "Average Time by Age Group and Year", "Year", "Average Time (min)"
    )
    fig = go.Figure(data=traces, layout=layout)
    tabular_data = avg_time_age_group.reset_index().to_dict(orient="records")
    return jsonify(
        {
            "graph": fig.to_json(),
            # "table": tabular_data,
        }
    )


def plot_age_vs_time_distribution(df):
    trace = go.Scatter(
        x=df["Age"].tolist(),
        y=df["Time (min)"].tolist(),
        mode="markers",
        marker=dict(color="brown", opacity=0.5),
        name="Time (min)",
    )
    layout = customize_layout("Age vs. Time Distribution", "Age", "Time (min)")
    fig = go.Figure(data=[trace], layout=layout)
    tabular_data = df[["Age", "Time (min)"]].to_dict(orient="records")
    return jsonify({"graph": fig.to_json(), "table": tabular_data})


def plot_median_time_by_year(df):
    median_time = df.groupby("Year")["Time (min)"].median()
    overall_median_time = df["Time (min)"].median()
    trace1 = go.Scatter(
        x=median_time.index.tolist(),
        y=median_time.tolist(),
        mode="lines+markers",
        name="Median Time",
        line=dict(color="darkgreen"),
    )
    trace2 = go.Scatter(
        x=median_time.index.tolist(),
        y=[overall_median_time] * len(median_time),
        mode="lines",
        name=f"Overall Median: {overall_median_time:.2f} min",
        line=dict(color="green", dash="dash"),
    )
    layout = customize_layout("Median Time by Year", "Year", "Median Time (min)")
    fig = go.Figure(data=[trace1, trace2], layout=layout)
    tabular_data = median_time.reset_index().to_dict(orient="records")
    return jsonify({"graph": fig.to_json(), "table": tabular_data})