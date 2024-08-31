from flask import Blueprint, request
from app.services.data_service import df
from app.graph_building.plot_utils import (
    plot_participation_by_year,
    plot_average_time_by_year,
    plot_participation_by_age_group,
    plot_participation_by_region,
    plot_time_percentiles_by_year,
    plot_gender_distribution_by_year,
    plot_median_time_by_year,
    plot_top_10_fastest_swimmers,
    plot_user_time_by_year,
    plot_user_time_percentile_by_year,
    plot_average_time_by_age_group_and_year,
    plot_age_vs_time_distribution,
    find_user_position_in_year,
    plot_average_time_by_gender_age_group_and_year
)

api_bp = Blueprint('api', __name__)

@api_bp.route('/test', methods=['GET'])
def test_api():
    return {
        "message": "Hello, this is a test!",
        "status": "success"
    }

# General Plot Routes
@api_bp.route('/participation-by-year', methods=['GET'])
def get_participation_over_years():
    return plot_participation_by_year(df)

@api_bp.route('/average-time-by-year', methods=['GET'])
def get_average_time_over_years():
    return plot_average_time_by_year(df)

@api_bp.route('/participation-by-age-group', methods=['GET'])
def get_participation_by_age_group():
    return plot_participation_by_age_group(df)

@api_bp.route('/participation-by-region', methods=['GET'])
def get_regional_participation():
    return plot_participation_by_region(df)

@api_bp.route('/time-percentiles-by-year', methods=['GET'])
def get_time_percentiles():
    return plot_time_percentiles_by_year(df)

@api_bp.route('/gender-distribution-by-year', methods=['GET'])
def get_gender_distribution():
    return plot_gender_distribution_by_year(df)

@api_bp.route('/median-time-by-year', methods=['GET'])
def get_median_over_years():
    return plot_median_time_by_year(df)

@api_bp.route('/top-10-fastest-swimmers', methods=['GET'])
def get_top_10_fastest_swimmers():
    return plot_top_10_fastest_swimmers(df)

@api_bp.route('/age-vs-time-distribution', methods=['GET'])
def get_age_vs_time_distribution():
    return plot_age_vs_time_distribution(df)

@api_bp.route('/average-time-by-age-group-and-year', methods=['GET'])
def get_average_time_by_age_group_over_years():
    return plot_average_time_by_age_group_and_year(df)

# User Specific Routes (Plots)
@api_bp.route('/user-time-by-year', methods=['GET'])
def get_user_time_over_years():
    name = request.args.get('name').lower()
    if not name:
        return {"error": "Name parameter is required"}, 400
    return plot_user_time_by_year(df, name)  

@api_bp.route('/user-percentile-by-year', methods=['GET'])
def get_user_percentile_over_years():
    name = request.args.get('name').lower()
    if not name:
        return {"error": "Name, gender parameters is required"}, 400
    return plot_user_time_percentile_by_year(df, name) 

@api_bp.route('/user-average-time-gender-age-group-and-year', methods=['GET'])
def get_average_time_by_gender_age_group_and_year():
    gender = request.args.get('gender')
    age_group = request.args.get('age_group')
    name = request.args.get('name').lower()
    overlay_avg_time = request.args.get('overlay', 'false').lower() == 'true'
    overlay_user_time = request.args.get('overlay_user_time', 'false').lower() == 'true'  

    if not gender or not age_group:
        return {"error": "Gender and Age Group parameters are required"}, 400

    return plot_average_time_by_gender_age_group_and_year(df, gender, age_group, name, overlay_avg_time, overlay_user_time)

# User Specific Routes (Stats)
@api_bp.route('/user-position-in-year', methods=['GET'])
def get_user_position():
    name = request.args.get('name').lower()
    year = request.args.get('year')
    if not name or not year:
        return {"error": "Name and year parameters are required"}, 400
    return find_user_position_in_year(df, name, int(year))


