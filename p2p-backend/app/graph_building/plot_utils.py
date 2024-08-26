import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import io
from flask import send_file
from .util import calculate_percentile

matplotlib.use('Agg')  
plt.style.use("fivethirtyeight")

# Utility Function to Save Plot to BytesIO
def save_plot_to_bytesio(fig):
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plt.close(fig)
    return send_file(img, mimetype='image/png')

# General Plot Functions
def plot_participation_by_year(df):
    participation = df.groupby('Year')['Name'].count()
    fig, ax = plt.subplots()
    participation.plot(kind='bar', ax=ax, color='skyblue')
    ax.set_title('Overall Participation by Year')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Participants')
    ax.legend(['Participants'], loc='best')
    ax.grid(True)
    return save_plot_to_bytesio(fig)

def plot_average_time_by_year(df):
    avg_time = df.groupby('Year')['Time (min)'].mean()
    overall_avg_time = df['Time (min)'].mean()
    fig, ax = plt.subplots()
    avg_time.plot(ax=ax, color='orange')
    ax.axhline(y=overall_avg_time, color='red', linestyle='--', label=f'Overall Average: {overall_avg_time:.2f} min')
    ax.set_title('Average Time by Year')
    ax.set_xlabel('Year')
    ax.set_ylabel('Average Time (min)')
    ax.legend(loc='best')
    ax.grid(True)
    return save_plot_to_bytesio(fig)

def plot_participation_by_age_group(df):
    bins = [0, 18, 30, 40, 50, 60, 70, 80]
    labels = ['<18', '18-29', '30-39', '40-49', '50-59', '60-69', '70+']
    df['AgeGroup'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
    fig, ax = plt.subplots()
    df['AgeGroup'].value_counts(sort=False).plot(kind='bar', ax=ax, color='green')
    ax.set_title('Participation by Age Group')
    ax.set_xlabel('Age Group')
    ax.set_ylabel('Number of Participants')
    ax.legend(['Participants'], loc='best')
    ax.grid(True)
    return save_plot_to_bytesio(fig)

def plot_participation_by_region(df):
    top_regions = df['Region'].value_counts().head(10)
    fig, ax = plt.subplots()
    top_regions.plot(kind='bar', ax=ax, color='purple')
    ax.set_title('Top 10 Regions by Participation')
    ax.set_xlabel('Region')
    ax.set_ylabel('Number of Participants')
    ax.legend(['Participants'], loc='best')
    ax.grid(True)
    return save_plot_to_bytesio(fig)

def plot_time_percentiles_by_year(df):
    percentiles = df['Time (min)'].quantile([0.25, 0.5, 0.75])
    fig, ax = plt.subplots()
    percentiles.plot(kind='bar', ax=ax, color='blue')
    ax.set_title('Time Percentiles')
    ax.set_xlabel('Percentile')
    ax.set_ylabel('Time (min)')
    ax.legend(['Time (min)'], loc='best')
    ax.grid(True)
    return save_plot_to_bytesio(fig)

def plot_gender_distribution_by_year(df):
    df = df[df['Gender'].isin(['M', 'F'])]
    gender_distribution = df.groupby('Year')['Gender'].value_counts().unstack().fillna(0)
    fig, ax = plt.subplots()
    gender_distribution.plot(kind='bar', stacked=True, ax=ax, color=['#1f77b4', '#ff7f0e'])
    ax.set_title('Gender Distribution by Year')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Participants')
    ax.legend(['Male', 'Female'], loc='best')
    ax.grid(True)
    return save_plot_to_bytesio(fig)

def plot_top_10_fastest_swimmers(df):
    top_10_fastest = df.nsmallest(10, 'Time (min)')
    fig, ax = plt.subplots()
    top_10_fastest.plot(kind='bar', x='Name', y='Time (min)', ax=ax, color='red')
    ax.set_title('Top 10 Fastest Swimmers')
    ax.set_xlabel('Swimmer')
    ax.set_ylabel('Time (min)')
    ax.legend(['Time (min)'], loc='best')
    ax.grid(True)
    return save_plot_to_bytesio(fig)

def plot_average_time_by_age_group_and_year(df):
    bins = [0, 18, 30, 40, 50, 60, 70, 80]
    labels = ['<18', '18-29', '30-39', '40-49', '50-59', '60-69', '70+']
    df['AgeGroup'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
    avg_time_age_group = df.groupby(['Year', 'AgeGroup'])['Time (min)'].mean().unstack()
    fig, ax = plt.subplots(figsize=(10, 6))
    avg_time_age_group.plot(ax=ax)
    ax.set_title('Average Time by Age Group and Year')
    ax.set_xlabel('Year')
    ax.set_ylabel('Average Time (min)')
    ax.legend(loc='best')
    ax.grid(True)
    return save_plot_to_bytesio(fig)

def plot_age_vs_time_distribution(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(df['Age'], df['Time (min)'], alpha=0.5, color='brown')
    ax.set_title('Age vs. Time Distribution')
    ax.set_xlabel('Age')
    ax.set_ylabel('Time (min)')
    ax.legend(['Time (min)'], loc='best')
    ax.grid(True)
    return save_plot_to_bytesio(fig)

def plot_median_time_by_year(df):
    median_time = df.groupby('Year')['Time (min)'].median()
    overall_median_time = df['Time (min)'].median()
    fig, ax = plt.subplots()
    median_time.plot(ax=ax, color='darkgreen')
    ax.axhline(y=overall_median_time, color='green', linestyle='--', label=f'Overall Median: {overall_median_time:.2f} min')
    ax.set_title('Median Time by Year')
    ax.set_xlabel('Year')
    ax.set_ylabel('Median Time (min)')
    ax.legend(loc='best')
    ax.grid(True)
    return save_plot_to_bytesio(fig)

# User-Specific Plot Functions
def plot_user_time_by_year(df, name):
    person_data = df[df['Name'] == name]
    if person_data.empty:
        return {"error": f"No data found for {name}"}, 404

    fig, ax = plt.subplots()
    person_data.plot(kind='line', x='Year', y='Time (min)', marker='o', color='navy', ax=ax)
    ax.set_title(f"{name}'s Time Over the Years")
    ax.set_xlabel('Year')
    ax.set_ylabel('Time (min)')
    ax.legend([f"{name}'s Time"], loc='best')
    ax.grid(True)
    return save_plot_to_bytesio(fig)

def plot_user_time_percentile_by_year(df, name):
    person_data = df[df['Name'] == name]
    if person_data.empty:
        return {"error": f"No data found for {name}"}, 404

    person_gender = person_data['Gender'].iloc[0]
    percentiles_all = []
    percentiles_gender = []

    for year in person_data['Year'].unique():
        yearly_data = df[df['Year'] == year]
        yearly_data_gender = yearly_data[yearly_data['Gender'] == person_gender]
        time = person_data[person_data['Year'] == year]['Time (min)'].values[0]
        percentiles_all.append((year, calculate_percentile(yearly_data['Time (min)'], time)))
        percentiles_gender.append((year, calculate_percentile(yearly_data_gender['Time (min)'], time)))

    years, percentiles_all = zip(*percentiles_all)
    _, percentiles_gender = zip(*percentiles_gender)

    fig, ax = plt.subplots()
    ax.plot(years, percentiles_all, marker='o', label='Overall Percentile', color='blue')
    ax.plot(years, percentiles_gender, marker='x', label=f"{person_gender} Percentile", color='purple')
    ax.set_title(f"{name}'s Percentile Over the Years")
    ax.set_xlabel('Year')
    ax.set_ylabel('Percentile')
    ax.set_ylim(0, 100)
    ax.legend(loc='best')
    ax.grid(True)
    return save_plot_to_bytesio(fig)

# Swimmer Analysis Functions (Non-Plot)
def find_user_position_in_year(df, name, year):
    swimmer_data = df[(df['Name'] == name) & (df['Year'] == year)]
    if swimmer_data.empty:
        return {"error": f"No data found for {name} in {year}"}, 404

    best_time = swimmer_data['Time (min)'].min()
    overall_rank = (df[df['Year'] == year]['Time (min)'] < best_time).sum() + 1
    return {
        "name": name,
        "year": year,
        "position": overall_rank,
        "total_participants": len(df[df['Year'] == year])
    }
