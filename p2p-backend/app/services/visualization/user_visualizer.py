from plotly import graph_objs as go
from flask import jsonify
from app.services.visualization.general_visualizer import Layout


class UserVisualizer:
    @staticmethod
    def plot_user_time_by_year(person_data):
        if person_data is None:
            return None
        name = person_data["Name"].iloc[0]
        trace = go.Scatter(
            x=person_data["Year"].tolist(),
            y=person_data["Time (min)"].tolist(),
            mode="lines+markers",
            name=f"{name}'s Time",
            line=dict(color="navy"),
        )
        layout = Layout.customize_layout(f"{name}'s Time Over the Years", "Year", "Time (min)")
        fig = go.Figure(data=[trace], layout=layout)
        tabular_data = person_data[["Year", "Time (min)"]].to_dict(orient="records")
        return jsonify({"graph": fig.to_json(), "table": tabular_data})

    @staticmethod
    def plot_user_time_percentile_by_year(data):
        if data is None:
            return None
        person_data, person_gender, percentiles_all, percentiles_gender = data
        name = person_data["Name"].iloc[0]
        years, percentiles_all_values = zip(*percentiles_all)
        _, percentiles_gender_values = zip(*percentiles_gender)

        trace1 = go.Scatter(
            x=years,
            y=percentiles_all_values,
            mode="lines+markers",
            name="Overall Percentile",
            line=dict(color="blue"),
        )
        trace2 = go.Scatter(
            x=years,
            y=percentiles_gender_values,
            mode="lines+markers",
            name=f"{person_gender} Percentile",
            line=dict(color="purple", dash="dash"),
        )
        layout = Layout.customize_layout(f"{name}'s Percentile Over the Years", "Year", "Percentile")
        fig = go.Figure(data=[trace1, trace2], layout=layout)
        tabular_data = {
            "Year": [int(y) for y in years],
            "Overall Percentile": [float(p) for p in percentiles_all_values],
            f"{person_gender} Percentile": [float(p) for p in percentiles_gender_values],
        }
        return jsonify({"graph": fig.to_json(), "table": tabular_data})

    @staticmethod
    def plot_average_time_by_gender_age_group_and_year(data, gender, age_group, name=None, show_overall_avg=False, show_user_time=False):
        if data is None:
            return None
        avg_time, overall_avg_time, user_data = data

        traces = [
            go.Scatter(
                x=avg_time.index.tolist(),
                y=avg_time.tolist(),
                mode="lines+markers",
                name=f"Average Time ({gender}, {age_group})",
                line=dict(color="blue"),
            )
        ]

        if show_overall_avg and overall_avg_time is not None:
            traces.append(
                go.Scatter(
                    x=overall_avg_time.index.tolist(),
                    y=overall_avg_time.tolist(),
                    mode="lines",
                    name="Overall Average Time",
                    line=dict(color="red", dash="dash"),
                )
            )

        if show_user_time and user_data is not None:
            user_time_by_year = user_data.groupby("Year")["Time (min)"].mean()
            traces.append(
                go.Scatter(
                    x=user_time_by_year.index.tolist(),
                    y=user_time_by_year.tolist(),
                    mode="lines+markers",
                    name=f"{name}'s Time",
                    line=dict(color="green"),
                )
            )

        layout = Layout.customize_layout(
            f"Average Time by Year with Overlays ({gender}, {age_group})",
            "Year",
            "Time (min)",
        )
        fig = go.Figure(data=traces, layout=layout)
        tabular_data = avg_time.reset_index().to_dict(orient="records")
        return jsonify({"graph": fig.to_json(), "table": tabular_data})
