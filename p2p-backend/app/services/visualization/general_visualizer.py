from plotly import graph_objs as go
from flask import jsonify


class Layout:
    @staticmethod
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


class GeneralVisualizer:
    @staticmethod
    def plot_participation_by_year(participation_data):
        trace = go.Bar(
            x=participation_data.index.tolist(),
            y=participation_data.tolist(),
            name="Participants",
            marker=dict(color="skyblue"),
        )
        layout = Layout.customize_layout("Overall Participation by Year", "Year", "Number of Participants")
        fig = go.Figure(data=[trace], layout=layout)
        tabular_data = participation_data.reset_index().to_dict(orient="records")
        return jsonify({"graph": fig.to_json(), "table": tabular_data})

    @staticmethod
    def plot_average_time_by_year(avg_time, overall_avg_time):
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
        layout = Layout.customize_layout("Average Time by Year", "Year", "Average Time (min)")
        fig = go.Figure(data=[trace1, trace2], layout=layout)
        tabular_data = avg_time.reset_index().to_dict(orient="records")
        return jsonify({"graph": fig.to_json(), "table": tabular_data})

    @staticmethod
    def plot_participation_by_age_group(age_group_counts):
        trace = go.Bar(
            x=age_group_counts.index.tolist(),
            y=age_group_counts.tolist(),
            name="Participants",
            marker=dict(color="green"),
        )
        layout = Layout.customize_layout("Participation by Age Group", "Age Group", "Number of Participants")
        fig = go.Figure(data=[trace], layout=layout)
        tabular_data = age_group_counts.reset_index().to_dict(orient="records")
        return jsonify({"graph": fig.to_json(), "table": tabular_data})

    @staticmethod
    def plot_participation_by_region(top_regions):
        trace = go.Bar(
            x=top_regions.index.tolist(),
            y=top_regions.tolist(),
            name="Participants",
            marker=dict(color="purple"),
        )
        layout = Layout.customize_layout("Top 10 Regions by Participation", "Region", "Number of Participants")
        fig = go.Figure(data=[trace], layout=layout)
        tabular_data = top_regions.reset_index().to_dict(orient="records")
        return jsonify({"graph": fig.to_json(), "table": tabular_data})

    @staticmethod
    def plot_time_percentiles(percentiles):
        trace = go.Bar(
            x=["25th Percentile", "50th Percentile", "75th Percentile"],
            y=percentiles.tolist(),
            name="Time (min)",
            marker=dict(color="blue"),
        )
        layout = Layout.customize_layout("Time Percentiles", "Percentile", "Time (min)")
        fig = go.Figure(data=[trace], layout=layout)
        tabular_data = [{"Percentile": f"{int(p*100)}th Percentile", "Time (min)": time} for p, time in percentiles.items()]
        return jsonify({"graph": fig.to_json(), "table": tabular_data})

    @staticmethod
    def plot_gender_distribution_by_year(gender_distribution):
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
        layout = Layout.customize_layout("Gender Distribution by Year", "Year", "Number of Participants", barmode="stack")
        fig = go.Figure(data=[trace1, trace2], layout=layout)
        tabular_data = gender_distribution.reset_index().to_dict(orient="records")
        return jsonify({"graph": fig.to_json(), "table": tabular_data})

    @staticmethod
    def plot_top_10_fastest_swimmers(top_10_fastest):
        trace = go.Bar(
            x=top_10_fastest["Name"].tolist(),
            y=top_10_fastest["Time (min)"].tolist(),
            name="Time (min)",
            marker=dict(color="red"),
        )
        layout = Layout.customize_layout("Top 10 Fastest Swimmers", "Swimmer", "Time (min)")
        fig = go.Figure(data=[trace], layout=layout)
        tabular_data = top_10_fastest[["Name", "Time (min)"]].to_dict(orient="records")
        return jsonify({"graph": fig.to_json(), "table": tabular_data})

    @staticmethod
    def plot_average_time_by_age_group_and_year(avg_time_age_group):
        traces = []
        for age_group in avg_time_age_group.columns:
            trace = go.Scatter(
                x=avg_time_age_group.index.tolist(),
                y=avg_time_age_group[age_group].tolist(),
                mode="lines+markers",
                name=f"{age_group}",
            )
            traces.append(trace)
        layout = Layout.customize_layout("Average Time by Age Group and Year", "Year", "Average Time (min)")
        fig = go.Figure(data=traces, layout=layout)
        tabular_data = avg_time_age_group.reset_index().to_dict(orient="records")
        return jsonify({"graph": fig.to_json()})

    @staticmethod
    def plot_age_vs_time_distribution(age_time_data):
        trace = go.Scatter(
            x=age_time_data["Age"].tolist(),
            y=age_time_data["Time (min)"].tolist(),
            mode="markers",
            marker=dict(color="brown", opacity=0.5),
            name="Time (min)",
        )
        layout = Layout.customize_layout("Age vs. Time Distribution", "Age", "Time (min)")
        fig = go.Figure(data=[trace], layout=layout)
        tabular_data = age_time_data.to_dict(orient="records")
        return jsonify({"graph": fig.to_json(), "table": tabular_data})

    @staticmethod
    def plot_median_time_by_year(median_time, overall_median_time):
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
        layout = Layout.customize_layout("Median Time by Year", "Year", "Median Time (min)")
        fig = go.Figure(data=[trace1, trace2], layout=layout)
        tabular_data = median_time.reset_index().to_dict(orient="records")
        return jsonify({"graph": fig.to_json(), "table": tabular_data})
