from app.graph_building.util import customize_layout, calculate_percentile
from plotly import graph_objs as go
from flask import jsonify

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