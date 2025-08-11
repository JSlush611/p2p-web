from flask import Blueprint, request, jsonify
from app.services.data.data_loader import load_data
from app.services.analysis.general_analysis import GeneralAnalysis
from app.services.analysis.user_analysis import UserAnalysis
from app.services.visualization.general_visualizer import GeneralVisualizer
from app.services.visualization.user_visualizer import UserVisualizer

api_bp = Blueprint("api", __name__)


def load_dataset_from_request():
    dataset_type = request.args.get("dataset", "competitive")
    return load_data(competitive=(dataset_type == "competitive"))


# General Plot Routes
@api_bp.route("/participation-by-year", methods=["GET"])
def get_participation_over_years():
    df = load_dataset_from_request()
    participation_data = GeneralAnalysis.get_participation_by_year(df)
    return GeneralVisualizer.plot_participation_by_year(participation_data)


@api_bp.route("/average-time-by-year", methods=["GET"])
def get_average_time_over_years():
    df = load_dataset_from_request()
    avg_time, overall_avg_time = GeneralAnalysis.get_average_time_by_year(df)
    return GeneralVisualizer.plot_average_time_by_year(avg_time, overall_avg_time)


@api_bp.route("/participation-by-age-group", methods=["GET"])
def get_participation_by_age_group():
    df = load_dataset_from_request()
    age_group_counts = GeneralAnalysis.get_participation_by_age_group(df)
    return GeneralVisualizer.plot_participation_by_age_group(age_group_counts)


@api_bp.route("/participation-by-region", methods=["GET"])
def get_regional_participation():
    df = load_dataset_from_request()
    top_regions = GeneralAnalysis.get_participation_by_region(df)
    return GeneralVisualizer.plot_participation_by_region(top_regions)


@api_bp.route("/time-percentiles-by-year", methods=["GET"])
def get_time_percentiles():
    df = load_dataset_from_request()
    percentiles = GeneralAnalysis.get_time_percentiles(df)
    return GeneralVisualizer.plot_time_percentiles(percentiles)


@api_bp.route("/gender-distribution-by-year", methods=["GET"])
def get_gender_distribution():
    df = load_dataset_from_request()
    gender_distribution = GeneralAnalysis.get_gender_distribution_by_year(df)
    return GeneralVisualizer.plot_gender_distribution_by_year(gender_distribution)


@api_bp.route("/median-time-by-year", methods=["GET"])
def get_median_over_years():
    df = load_dataset_from_request()
    median_time, overall_median_time = GeneralAnalysis.get_median_time_by_year(df)
    return GeneralVisualizer.plot_median_time_by_year(median_time, overall_median_time)


@api_bp.route("/top-10-fastest-swimmers", methods=["GET"])
def get_top_10_fastest_swimmers():
    df = load_dataset_from_request()
    top_10_fastest = GeneralAnalysis.get_top_10_fastest_swimmers(df)
    return GeneralVisualizer.plot_top_10_fastest_swimmers(top_10_fastest)


@api_bp.route("/average-time-by-age-group-and-year", methods=["GET"])
def get_average_time_by_age_group_over_years():
    df = load_dataset_from_request()
    avg_time_age_group = GeneralAnalysis.get_average_time_by_age_group_and_year(df)
    return GeneralVisualizer.plot_average_time_by_age_group_and_year(avg_time_age_group)


# User Specific Routes (Plots)
@api_bp.route("/user-time-by-year", methods=["GET"])
def get_user_time_over_years():
    df = load_dataset_from_request()
    name = request.args.get("name", "").lower()
    if not name:
        return {"error": "Name parameter is required"}, 400

    person_data, error = UserAnalysis.get_user_time_by_year(df, name)
    if error:
        return jsonify(error), 404

    return UserVisualizer.plot_user_time_by_year(person_data)


@api_bp.route("/user-percentile-by-year", methods=["GET"])
def get_user_percentile_over_years():
    df = load_dataset_from_request()
    name = request.args.get("name", "").lower()
    if not name:
        return {"error": "Name parameter is required"}, 400

    data, error = UserAnalysis.get_user_time_percentile_by_year(df, name)
    if error:
        return jsonify(error), 404

    return UserVisualizer.plot_user_time_percentile_by_year(data)


@api_bp.route("/user-average-time-gender-age-group-and-year", methods=["GET"])
def get_average_time_by_gender_age_group_and_year():
    df = load_dataset_from_request()
    gender = request.args.get("gender")
    age_group = request.args.get("age_group")
    name = request.args.get("name", "").lower()
    show_overall_avg = request.args.get("overlay", "false").lower() == "true"
    show_user_time = request.args.get("overlay_user_time", "false").lower() == "true"

    if not gender or not age_group:
        return {"error": "Gender and Age Group parameters are required"}, 400

    data, error = UserAnalysis.get_average_time_by_gender_age_group_and_year(df, gender, age_group, name)
    if error:
        return jsonify(error), 404

    return UserVisualizer.plot_average_time_by_gender_age_group_and_year(data, gender, age_group, name, show_overall_avg, show_user_time)


# User Specific Routes (Stats)
@api_bp.route("/user-position-in-year", methods=["GET"])
def get_user_position():
    df = load_dataset_from_request()
    name = request.args.get("name", "").lower()
    year = request.args.get("year")
    if not name or not year:
        return {"error": "Name and year parameters are required"}, 400

    position_data, error = UserAnalysis.find_user_position_in_year(df, name, int(year))
    if error:
        return jsonify({"error": True, "message": error}), 404

    return jsonify(position_data)
