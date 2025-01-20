import plotly.graph_objs as go
from flask import jsonify
from .util import calculate_percentile
import pandas as pd


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


# User-Specific Plot Functions
def plot_user_time_by_year(df, name):
    person_data = df[df["Name"] == name]
    if person_data.empty:
        return jsonify({"error": f"No data found for {name}"}), 404

    trace = go.Scatter(
        x=person_data["Year"].tolist(),
        y=person_data["Time (min)"].tolist(),
        mode="lines+markers",
        name=f"{name}'s Time",
        line=dict(color="navy"),
    )
    layout = customize_layout(f"{name}'s Time Over the Years", "Year", "Time (min)")
    fig = go.Figure(data=[trace], layout=layout)
    tabular_data = person_data[["Year", "Time (min)"]].to_dict(orient="records")
    return jsonify({"graph": fig.to_json(), "table": tabular_data})


def plot_user_time_percentile_by_year(df, name):
    person_data = df[df["Name"] == name]
    if person_data.empty:
        return jsonify({"error": f"No data found for {name}"}), 404

    person_gender = person_data["Gender"].iloc[0]
    percentiles_all = []
    percentiles_gender = []

    for year in person_data["Year"].unique():
        yearly_data = df[df["Year"] == year]
        yearly_data_gender = yearly_data[yearly_data["Gender"] == person_gender]
        time = person_data[person_data["Year"] == year]["Time (min)"].values[0]
        percentiles_all.append(
            (year, calculate_percentile(yearly_data["Time (min)"], time))
        )
        percentiles_gender.append(
            (year, calculate_percentile(yearly_data_gender["Time (min)"], time))
        )

    years, percentiles_all = zip(*percentiles_all)
    _, percentiles_gender = zip(*percentiles_gender)

    trace1 = go.Scatter(
        x=years,
        y=percentiles_all,
        mode="lines+markers",
        name="Overall Percentile",
        line=dict(color="blue"),
    )
    trace2 = go.Scatter(
        x=years,
        y=percentiles_gender,
        mode="lines+markers",
        name=f"{person_gender} Percentile",
        line=dict(color="purple", dash="dash"),
    )
    layout = customize_layout(
        f"{name}'s Percentile Over the Years", "Year", "Percentile"
    )
    fig = go.Figure(data=[trace1, trace2], layout=layout)
    tabular_data = pd.DataFrame(
        {
            "Year": years,
            "Overall Percentile": percentiles_all,
            f"{person_gender} Percentile": percentiles_gender,
        }
    ).to_dict(orient="records")
    return jsonify({"graph": fig.to_json(), "table": tabular_data})


def plot_average_time_by_gender_age_group_and_year(
    df, gender, age_group, name, overlay_avg_time=False, overlay_user_time=False
):
    filtered_df = df[(df["Gender"] == gender) & (df["AgeGroup"] == age_group)]
    avg_time = filtered_df.groupby("Year")["Time (min)"].mean()

    trace1 = go.Scatter(
        x=avg_time.index.tolist(),
        y=avg_time.tolist(),
        mode="lines+markers",
        name=f"Average Time ({gender}, {age_group})",
        line=dict(color="blue"),
    )
    traces = [trace1]

    if overlay_avg_time:
        overall_avg_time = df.groupby("Year")["Time (min)"].mean()
        trace2 = go.Scatter(
            x=overall_avg_time.index.tolist(),
            y=overall_avg_time.tolist(),
            mode="lines",
            name="Overall Average Time",
            line=dict(color="red", dash="dash"),
        )
        traces.append(trace2)

    if overlay_user_time and name:
        user_data = df[df["Name"] == name]
        if not user_data.empty:
            user_time_by_year = user_data.groupby("Year")["Time (min)"].mean()
            trace3 = go.Scatter(
                x=user_time_by_year.index.tolist(),
                y=user_time_by_year.tolist(),
                mode="lines+markers",
                name=f"{name}'s Time",
                line=dict(color="green"),
            )
            traces.append(trace3)

    layout = customize_layout(
        f"Average Time by Year with Overlays ({gender}, {age_group})",
        "Year",
        "Time (min)",
    )
    fig = go.Figure(data=traces, layout=layout)
    tabular_data = avg_time.reset_index().to_dict(orient="records")
    return jsonify({"graph": fig.to_json(), "table": tabular_data})


# Swimmer Analysis Functions (Non-Plot)
def find_user_position_in_year(df, name, year):
    swimmer_data = df[(df["Name"] == name) & (df["Year"] == year)]
    if swimmer_data.empty:
        return {"error": f"No data found for {name} in {year}"}, 404

    best_time = swimmer_data["Time (min)"].min()
    overall_rank = int((df[df["Year"] == year]["Time (min)"] < best_time).sum() + 1)

    age_group = str(swimmer_data["AgeGroup"].iloc[0])
    gender = swimmer_data["Gender"].iloc[0]
    total_participants_in_age_group_and_gender = int(
        len(
            df[
                (df["Year"] == year)
                & (df["AgeGroup"] == age_group)
                & (df["Gender"] == gender)
            ]
        )
    )

    return {
        "name": name,
        "year": int(year),
        "position": overall_rank,
        "total_participants": int(len(df[df["Year"] == year])),
        "age_group": age_group,
        "total_participants_in_age_group": total_participants_in_age_group_and_gender,
    }
